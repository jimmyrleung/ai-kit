#!/usr/bin/env python3
"""Build a generated, interactive HTML view of a spec folder.

The markdown files stay the source of truth; the page is a disposable build
output written to ``<spec>/.views/view.html``. Model-written illustrations
("exhibits") live as JSON in ``<spec>/.views/exhibits/``. Each one is stamped
with the hash of the sections it illustrates (and of the code it shows), so a
later build can tell which ones went stale and only those need redrawing.

Standard library only. Code excerpts and diffs read the repository given with
``--repo``; git diffs also need ``git`` on PATH.

    render_view.py plan  SPEC_DIR|DOC [--all]
    render_view.py build SPEC_DIR|DOC [--repo DIR]... [--out FILE]
    render_view.py check SPEC_DIR|DOC [--out FILE]

Given a doc instead of a folder, the view covers the doc's folder and opens on
that doc. A doc with a ``## Walkthrough — <date> (round N)`` section renders
its latest round as a decision round: premise cards, one card per item, and
answers that leave the page through Respond.
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


EXIT_OK = 0
EXIT_STALE = 1
EXIT_USAGE = 2
MANIFEST_VERSION = 1
SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"
VIEW_DIR = ".views"
EXHIBIT_TYPES = (
    "claims", "flow", "tree", "states", "graph", "sequence", "walk", "timeline", "code", "diff", "decisions", "decision",
)
CODE_EXHIBITS = ("code", "diff")
DOC_ORDER = ("user_story.md", "requirements.md", "techspec.md", "tasks.md")
DOC_LABELS = {
    "user_story.md": "User story",
    "requirements.md": "Requirements",
    "techspec.md": "Techspec",
    "tasks.md": "Tasks",
    "qa.md": "QA",
}
PRUNED_DIRS = {
    ".git", "node_modules", "bin", "obj", "dist", "build", ".next", "coverage",
    ".venv", "venv", "__pycache__", ".idea", ".vs", "packages", VIEW_DIR,
}
CODE_EXTENSIONS = (
    "tsx", "ts", "jsx", "js", "mjs", "cjs", "py", "cs", "csproj", "json", "md", "sql",
    "yaml", "yml", "tf", "tfvars", "css", "scss", "html", "sh", "ps1", "go", "rs",
    "java", "kt", "rb", "php", "xml", "config", "props", "toml", "ini", "mdc",
)
MAX_EXCERPT_LINES = 60

FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d{1,9}[.)])(\s+|$)(.*)$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
HR_RE = re.compile(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$")
QUOTE_RE = re.compile(r"^\s{0,3}>\s?(.*)$")
ID_RE = re.compile(r"(?<![\w/.#\-])([A-Z][A-Z0-9]{0,3}(?:-[A-Z]{1,3})?-?\d{1,3}[a-z]?)(?![\w\-])")
ID_FULL_RE = re.compile(r"^[A-Z][A-Z0-9]{0,3}(?:-[A-Z]{1,3})?-?\d{1,3}[a-z]?$")
PATH_RE = re.compile(
    r"^(?P<path>(?:[a-z][\w-]*:)?(?:[\w.@-]+/)*[\w.@-]+\.(?:" + "|".join(CODE_EXTENSIONS) + r"))"
    r"(?::(?P<line>\d+)(?:-\d+)?)?$"
)
IMPL_HEADING_RE = re.compile(
    r"^(?P<lead>\d+[a-z]?\.\s*)?(?P<subject>.+?)\s+[—–-]{1,2}\s+"
    r"(?P<action>Create|Modify|Delete|Remove|Rename)\b(?P<rest>.*)$"
)
TEXT_DIAGRAM_RE = re.compile(r"[├└┬┴┼│─►▶→]|-->|─>")
BEFORE_AFTER_RE = re.compile(r"^\s*(?://|#|--)\s*(before|after)\b", re.I)
GIT_REF_RE = re.compile(r"^(?!-)[\w./^~@{}-]{1,80}$")
HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$")
STATUS_HEADERS = {"status", "disposition", "decision", "result", "outcome"}
ROUND_RE = re.compile(r"^Walkthrough\s+[—–-]{1,2}\s+(\d{4}-\d{2}-\d{2})\s+\(round\s+(\d+)\)", re.I)
ROUND_LINE_RE = re.compile(r"^##\s+Walkthrough\s+[—–-]{1,2}\s+\d{4}-\d{2}-\d{2}\s+\(round\s+\d+\)", re.I | re.M)
PREMISE_RE = re.compile(r"^\s*\*\*\s*([A-Z][A-Z0-9]{0,3}-?\d{1,3}[a-z]?)\s*[—–:-]+\s*(.+?)\s*\*\*\s*(.*)$", re.S)
PREMISE_STATUS_RE = re.compile(r"\s+→\s+\*\*(?:Confirmed|Corrected)\*\*.*$", re.S)
ITEM_ANSWER_HEADERS = ("disposition", "decision", "status", "outcome", "result", "answer")
ITEM_SOURCE_HEADERS = ("source", "sources", "from", "origin")
OPEN_ANSWERS = {"", "open", "pending", "tbd", "todo", "undecided", "—", "–", "-"}
STEP_RE = re.compile(r"^(S\d{1,2})\s+[—–-]{1,2}\s+(.+)$")
TOUR_LINE_RE = re.compile(r"^##\s+Change set\s*$", re.I | re.M)
WORKING_TREE = "working tree"
STATUS_CLASSES = (
    ("ok", ("complete", "completed", "done", "keep", "kept", "accepted", "passed", "pass",
            "applied", "approved", "fresh", "yes", "go")),
    ("info", ("in progress", "running", "started", "partial")),
    ("warn", ("blocked", "fail", "failed", "remove", "removed", "change", "changed",
              "stale", "no-go", "rejected", "deferred")),
    ("neutral", ("not started", "pending", "queued", "open", "todo", "planned", "n/a")),
)

LANG_FAMILIES = {
    "c": {"ts", "tsx", "typescript", "js", "jsx", "javascript", "mjs", "cjs", "json", "jsonc", "cs",
          "csharp", "java", "kt", "kotlin", "go", "rs", "rust", "c", "cpp", "h", "swift", "css",
          "scss", "dart", "php"},
    "hash": {"py", "python", "sh", "bash", "shell", "zsh", "yaml", "yml", "toml", "ps1",
             "powershell", "rb", "ruby", "tf", "hcl", "dockerfile", "ini", "conf"},
    "sql": {"sql", "psql", "plpgsql", "tsql"},
}
TOKEN_RES = {
    "c": re.compile(
        r"(?P<com>//[^\n]*|/\*.*?\*/)"
        r"|(?P<str>`(?:\\.|[^`\\])*`|\"(?:\\.|[^\"\\\n])*\"|'(?:\\.|[^'\\\n])*')"
        r"|(?P<num>\b\d[\w.]*)"
        r"|(?P<word>[A-Za-z_$][\w$]*)",
        re.S,
    ),
    "hash": re.compile(
        r"(?P<com>#[^\n]*)"
        r"|(?P<str>\"\"\".*?\"\"\"|'''.*?'''|\"(?:\\.|[^\"\\\n])*\"|'(?:\\.|[^'\\\n])*')"
        r"|(?P<num>\b\d[\w.]*)"
        r"|(?P<word>[A-Za-z_][\w-]*)",
        re.S,
    ),
    "sql": re.compile(
        r"(?P<com>--[^\n]*|/\*.*?\*/)"
        r"|(?P<str>'(?:''|[^'])*')"
        r"|(?P<num>\b\d[\d.]*)"
        r"|(?P<word>[A-Za-z_][\w$]*)",
        re.S,
    ),
}
KEYWORDS = frozenset(
    """abstract as async await break case catch class const continue debugger default delete do
    else enum export extends false finally for from function get if implements import in instanceof
    interface let new null of private protected public readonly return set static super switch this
    throw true try type typeof undefined var void while with yield namespace using bool string int
    long double decimal base override virtual sealed partial record struct out ref params def elif
    lambda None True False pass raise is not and or global nonlocal fn mut pub impl match func
    package go defer select chan map range nil keyof satisfies declare module""".split()
)
SQL_KEYWORDS = frozenset(
    """select from where and or not insert into values update set delete create table alter drop
    index on join left right inner outer full group by order having limit offset as case when then
    else end begin commit rollback returning with union all distinct null is in exists primary key
    references foreign default constraint unique check cascade function returns language declare
    if loop for while do grant to text uuid timestamptz integer bigint boolean varchar""".split()
)


class ViewError(Exception):
    """A user-actionable failure."""


@dataclass
class Heading:
    level: int
    text: str
    anchor: str
    line: int
    end: int = 0
    hash: str = ""


@dataclass
class RoundItem:
    """A premise or an item of a walkthrough round. The hash leaves out the answer, so recording one
    does not make the item's drawings stale."""

    ident: str
    kind: str  # "premise" or "item"
    hash: str
    text: str
    title: str = ""
    fields: list[tuple[str, str]] = field(default_factory=list)
    source: str = ""
    answer: str = ""
    status: str = "open"  # item: open, decided, deferred; premise: open, confirmed, corrected
    recorded: list[list[dict[str, Any]]] = field(default_factory=list)


@dataclass
class Round:
    number: int
    date: str
    anchor: str
    premises: list[RoundItem] = field(default_factory=list)
    items: list[RoundItem] = field(default_factory=list)
    table: dict[str, Any] | None = None
    premise_list: dict[str, Any] | None = None
    premise_heading: dict[str, Any] | None = None
    premise_anchor: str = ""
    dispositions_heading: dict[str, Any] | None = None

    def find(self, ident: str) -> RoundItem | None:
        return next((item for item in self.premises + self.items if item.ident == ident), None)


@dataclass
class ChangedFile:
    path: str  # relative to the repository root, with forward slashes
    status: str  # A, M, D, T, or "new" for an untracked file
    added: int
    deleted: int


@dataclass
class ChangeRow:
    """One repository of a tour's change set, compared from the merge base of `base` to `head`."""

    prefix: str
    path: Path
    base: str
    head: str
    top: Path | None = None
    merge_base: str = ""
    files: list[ChangedFile] = field(default_factory=list)
    fingerprint: str = ""
    problem: str = ""

    @property
    def working(self) -> bool:
        return self.head.lower() in ("", WORKING_TREE, "working-tree", "worktree")

    @property
    def name(self) -> str:
        return self.prefix or (self.top or self.path).name


@dataclass
class Tour:
    rows: list[ChangeRow] = field(default_factory=list)
    steps: list[tuple[str, str, str]] = field(default_factory=list)  # (id, heading anchor, title)
    table: dict[str, Any] | None = None


@dataclass
class Doc:
    path: Path
    file: str
    id: str
    label: str
    text: str
    sha: str
    title: str = ""
    headings: list[Heading] = field(default_factory=list)
    blocks: list[dict[str, Any]] = field(default_factory=list)
    main: bool = False
    round: Round | None = None
    tour: Tour | None = None

    def heading(self, anchor: str) -> Heading | None:
        return next((h for h in self.headings if h.anchor == anchor), None)


@dataclass
class Exhibit:
    path: Path
    data: dict[str, Any]
    doc: Doc | None = None
    anchor: str = ""
    item: str = ""
    status: str = "fresh"
    problems: list[str] = field(default_factory=list)
    code: dict[str, Any] | None = None

    @property
    def id(self) -> str:
        return str(self.data.get("id") or self.path.stem)

    @property
    def kind(self) -> str:
        return str(self.data.get("type") or "")


# ---------------------------------------------------------------- helpers


def short_hash(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()[:12]


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def plain(text: str) -> str:
    """Markdown inline text to plain text, for labels and definitions."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`+([^`]*)`+", r"\1", text)
    text = re.sub(r"(\*\*|__|~~)(.+?)\1", r"\2", text)
    text = text.replace("\\|", "|").replace("\\", "")
    return re.sub(r"\s+", " ", text).strip()


def shorten(text: str, limit: int = 150) -> str:
    """Plain text cut at a word boundary, for one-line summaries."""
    text = plain(text)
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:—– ") + "…"


def blocks_text(blocks: list[dict[str, Any]]) -> str:
    """The raw markdown text of parsed blocks, for searching."""
    parts: list[str] = []
    for block in blocks:
        if block["t"] in ("para", "code", "heading"):
            parts.append(block["text"])
        elif block["t"] == "quote":
            parts.append(blocks_text(block["blocks"]))
        elif block["t"] == "list":
            parts.extend(blocks_text(item) for item in block["items"])
        elif block["t"] == "table":
            parts.extend(" | ".join(row) for row in [block["header"], *block["rows"]])
    return "\n".join(parts)


def slugify(text: str) -> str:
    """GitHub-style heading anchor, so links written in the markdown resolve."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def doc_id_for(file: str) -> str:
    stem = Path(file).stem.lower()
    return re.sub(r"[^a-z0-9]+", "-", stem).strip("-") or "doc"


def doc_label_for(file: str) -> str:
    if file in DOC_LABELS:
        return DOC_LABELS[file]
    match = re.match(r"task_(\d+)\.md$", file)
    if match:
        return f"Task {match.group(1)}"
    match = re.match(r"tour[_-](\d{4}-\d{2}-\d{2})\.md$", file)
    if match:
        return f"Tour {match.group(1)}"
    return Path(file).stem.replace("_", " ").replace("-", " ").capitalize()


def status_class(value: str) -> str | None:
    lowered = plain(value).lower()
    if not lowered or len(lowered) > 28:
        return None
    for css_class, words in STATUS_CLASSES:
        if any(lowered == word or lowered.startswith(word + " ") for word in words):
            return css_class
    return None


def read_asset(name: str) -> str:
    path = ASSETS_DIR / name
    if not path.is_file():
        raise ViewError(f"missing asset: {path}")
    return path.read_text(encoding="utf-8")


def parse_range(value: Any, total: int | None = None) -> tuple[int, int] | None:
    if value in (None, ""):
        return None
    match = re.fullmatch(r"\s*(\d+)\s*(?:[-–]\s*(\d+))?\s*", str(value))
    if not match:
        raise ViewError(f"lines must look like 40 or 40-72, not {value!r}")
    start = int(match.group(1))
    end = int(match.group(2) or start)
    if end < start:
        start, end = end, start
    if total is not None:
        start = max(1, min(start, total))
        end = max(start, min(end, total))
    return start, end


def parse_line_set(value: Any) -> set[int]:
    numbers: set[int] = set()
    items = value if isinstance(value, list) else str(value or "").split(",")
    for item in items:
        bounds = parse_range(item) if str(item).strip() else None
        if bounds:
            numbers.update(range(bounds[0], bounds[1] + 1))
    return numbers


# ---------------------------------------------------------------- markdown blocks


def scan_headings(lines: list[str]) -> list[Heading]:
    headings: list[Heading] = []
    fence: str | None = None
    seen: dict[str, int] = {}
    for index, line in enumerate(lines):
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(2)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not fence_match.group(3).strip():
                fence = None
            continue
        if fence is not None:
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        anchor = slugify(match.group(2))
        if anchor in seen:
            seen[anchor] += 1
            anchor = f"{anchor}-{seen[anchor]}"
        else:
            seen[anchor] = 0
        headings.append(Heading(len(match.group(1)), match.group(2), anchor, index))
    for position, heading in enumerate(headings):
        heading.end = len(lines)
        for later in headings[position + 1:]:
            if later.level <= heading.level:
                heading.end = later.line
                break
        heading.hash = short_hash("\n".join(lines[heading.line:heading.end]))
    return headings


def split_row(line: str) -> list[str]:
    row = line.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|") and not row.endswith("\\|"):
        row = row[:-1]
    return [cell.strip().replace("\\|", "|") for cell in re.split(r"(?<!\\)\|", row)]


def table_aligns(separator: str) -> list[str]:
    aligns = []
    for cell in split_row(separator):
        cell = cell.strip()
        if cell.startswith(":") and cell.endswith(":"):
            aligns.append("center")
        elif cell.endswith(":"):
            aligns.append("right")
        else:
            aligns.append("")
    return aligns


def starts_block(lines: list[str], index: int) -> bool:
    line = lines[index]
    if FENCE_RE.match(line) or HEADING_RE.match(line) or QUOTE_RE.match(line) or HR_RE.match(line):
        return True
    list_match = LIST_RE.match(line)
    if list_match and indent_of(line) <= 3 and list_match.group(4).strip():
        marker = list_match.group(2)
        if not marker[0].isdigit() or marker[:-1] == "1":
            return True
    return "|" in line and index + 1 < len(lines) and bool(TABLE_SEP_RE.match(lines[index + 1]))


def parse_blocks(lines: list[str]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    index = 0
    total = len(lines)
    while index < total:
        line = lines[index]
        if not line.strip():
            index += 1
            continue

        fence_match = FENCE_RE.match(line)
        if fence_match and len(fence_match.group(1)) <= 3:
            indent = len(fence_match.group(1))
            marker = fence_match.group(2)
            info = fence_match.group(3).strip()
            body = []
            index += 1
            while index < total:
                closing = FENCE_RE.match(lines[index])
                if (
                    closing
                    and closing.group(2)[0] == marker[0]
                    and len(closing.group(2)) >= len(marker)
                    and not closing.group(3).strip()
                ):
                    index += 1
                    break
                body_line = lines[index]
                body.append(body_line[min(indent, indent_of(body_line)):])
                index += 1
            blocks.append({"t": "code", "lang": info.split()[0] if info else "", "text": "\n".join(body)})
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            blocks.append({"t": "heading", "level": len(heading_match.group(1)), "text": heading_match.group(2)})
            index += 1
            continue

        if HR_RE.match(line):
            blocks.append({"t": "hr"})
            index += 1
            continue

        if QUOTE_RE.match(line):
            body = []
            while index < total and lines[index].strip():
                quote_match = QUOTE_RE.match(lines[index])
                if quote_match:
                    body.append(quote_match.group(1))
                elif body and body[-1].strip() and not starts_block(lines, index):
                    body.append(lines[index].strip())
                else:
                    break
                index += 1
            blocks.append({"t": "quote", "blocks": parse_blocks(body)})
            continue

        if "|" in line and index + 1 < total and TABLE_SEP_RE.match(lines[index + 1]) and "-" in lines[index + 1]:
            header = split_row(line)
            aligns = table_aligns(lines[index + 1])
            rows = []
            index += 2
            while index < total and lines[index].strip() and "|" in lines[index]:
                rows.append(split_row(lines[index]))
                index += 1
            blocks.append({"t": "table", "header": header, "aligns": aligns, "rows": rows})
            continue

        list_match = LIST_RE.match(line)
        if list_match and indent_of(line) <= 3:
            block, index = parse_list(lines, index)
            blocks.append(block)
            continue

        paragraph = [line.strip()]
        index += 1
        while index < total and lines[index].strip() and not starts_block(lines, index):
            paragraph.append(lines[index].strip())
            index += 1
        blocks.append({"t": "para", "text": "\n".join(paragraph)})
    return blocks


def parse_list(lines: list[str], index: int) -> tuple[dict[str, Any], int]:
    first = LIST_RE.match(lines[index])
    assert first is not None
    ordered = first.group(2)[0].isdigit()
    start = int(first.group(2)[:-1]) if ordered else 1
    items: list[list[dict[str, Any]]] = []
    total = len(lines)
    content_indent = 0
    while index < total:
        match = LIST_RE.match(lines[index])
        if not match or match.group(2)[0].isdigit() != ordered:
            break
        if items and indent_of(lines[index]) >= content_indent:
            break
        spacing = len(match.group(3)) if match.group(3) else 1
        if spacing > 4:
            spacing = 1
        content_indent = indent_of(lines[index]) + len(match.group(2)) + spacing
        body = [match.group(4)]
        index += 1
        while index < total:
            line = lines[index]
            if not line.strip():
                ahead = index
                while ahead < total and not lines[ahead].strip():
                    ahead += 1
                if ahead < total and indent_of(lines[ahead]) >= content_indent:
                    body.extend([""] * (ahead - index))
                    index = ahead
                    continue
                break
            if indent_of(line) >= content_indent:
                body.append(line[content_indent:])
                index += 1
                continue
            if LIST_RE.match(line):
                break
            if body[-1].strip() and not starts_block(lines, index) and "|" not in line:
                body.append(line.strip())
                index += 1
                continue
            break
        items.append(parse_blocks(body))
        ahead = index
        while ahead < total and not lines[ahead].strip():
            ahead += 1
        sibling = LIST_RE.match(lines[ahead]) if ahead < total else None
        if sibling and sibling.group(2)[0].isdigit() == ordered and indent_of(lines[ahead]) < content_indent:
            index = ahead
            continue
        break
    return {"t": "list", "ordered": ordered, "start": start, "items": items}, index


# ---------------------------------------------------------------- loading


def resolve_target(value: str) -> tuple[Path, str | None]:
    """A spec folder, or a doc in it: (folder, doc file name or None)."""
    path = Path(value).expanduser().resolve()
    if path.is_file():
        if path.suffix.lower() != ".md":
            raise ViewError(f"{path} is not a markdown doc")
        return path.parent, path.name
    if not path.is_dir():
        raise ViewError(f"{path} does not exist")
    return path, None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").expandtabs(4)


def discover_docs(spec_dir: Path, focus: str | None = None) -> list[Doc]:
    files = [name for name in DOC_ORDER if (spec_dir / name).is_file()]
    files += sorted(path.name for path in spec_dir.glob("task_*.md") if path.is_file())
    if (spec_dir / "qa.md").is_file():
        files.append("qa.md")
    if not files:
        files = sorted(path.name for path in spec_dir.glob("*.md") if path.is_file())
    else:
        # Walkthrough files (decision rounds) and implementation tours belong with the spec they serve.
        files += sorted(
            path.name for path in spec_dir.glob("*.md")
            if path.is_file() and path.name not in files and is_round_or_tour(read_text(path))
        )
    if focus and focus not in files:
        files.append(focus)
    if not files:
        raise ViewError(f"no markdown docs found in {spec_dir}")
    docs = []
    used_ids: set[str] = set()
    for file in files:
        path = spec_dir / file
        text = read_text(path)
        doc_id = doc_id_for(file)
        while doc_id in used_ids:
            doc_id += "-x"
        used_ids.add(doc_id)
        doc = Doc(path=path, file=file, id=doc_id, label=doc_label_for(file), text=text, sha=short_hash(text),
                  main=file == focus)
        lines = text.split("\n")
        doc.headings = scan_headings(lines)
        doc.blocks = parse_blocks(lines)
        h1 = next((h for h in doc.headings if h.level == 1), None)
        doc.title = plain(h1.text) if h1 else doc.label
        doc.round = parse_round(doc)
        doc.tour = parse_tour(doc)
        docs.append(doc)
    return docs


def is_round_or_tour(text: str) -> bool:
    return bool(ROUND_LINE_RE.search(text) or (TOUR_LINE_RE.search(text) and re.search(r"^##\s+S\d", text, re.M)))


def main_doc(docs: list[Doc]) -> Doc:
    return next((doc for doc in docs if doc.main), None) or next((doc for doc in docs if doc.file == "techspec.md"), docs[0])


# ---------------------------------------------------------------- walkthrough rounds


def answer_status(answer: str) -> str:
    text = plain(answer).lower().strip(" *_.")
    if text in OPEN_ANSWERS or text.startswith("open"):
        return "open"
    if text.startswith("defer"):
        return "deferred"
    return "decided"


def premise_from(item: list[dict[str, Any]]) -> RoundItem | None:
    if not item or item[0]["t"] != "para":
        return None
    first = PREMISE_STATUS_RE.sub("", item[0]["text"])
    match = PREMISE_RE.match(first)
    if match:
        ident, title, text = match.group(1), match.group(2).rstrip(" ."), match.group(3)
    else:
        ident = leading_id(first)
        if not ident:
            return None
        title = ""
        text = re.sub(r"^\s*(?:\*\*)?" + re.escape(ident) + r"(?:\*\*)?\s*(?::|—|–|\s-\s)\s*", "", first)
    marks = item[0]["text"] + "\n" + blocks_text(item[1:])
    status = "corrected" if "**Corrected**" in marks else "confirmed" if "**Confirmed**" in marks else "open"
    return RoundItem(ident, "premise", short_hash(first), text.strip(), title=title, status=status,
                     recorded=[item[1:]] if item[1:] else [])


def is_item_table(block: dict[str, Any]) -> bool:
    return len(block["header"]) >= 2 and any(row and definition_id(row[0]) for row in block["rows"])


def items_from(block: dict[str, Any]) -> list[RoundItem]:
    header = [plain(cell).lower() for cell in block["header"]]
    answer_col = next((i for i in range(len(header) - 1, 0, -1) if header[i] in ITEM_ANSWER_HEADERS), None)
    source_col = next((i for i, name in enumerate(header) if i and name in ITEM_SOURCE_HEADERS), None)
    items = []
    for row in block["rows"]:
        ident = definition_id(row[0]) if row else None
        if not ident:
            continue
        cells = row + [""] * (len(header) - len(row))
        fields = [
            (block["header"][i], cells[i]) for i in range(1, len(header))
            if i not in (answer_col, source_col) and plain(cells[i])
        ]
        text = max(fields, key=lambda pair: len(plain(pair[1])))[1] if fields else ""
        answer = cells[answer_col] if answer_col is not None else ""
        hashed = "\x1f".join(cell for i, cell in enumerate(cells) if i != answer_col)
        items.append(RoundItem(
            ident, "item", short_hash(hashed), text, fields=fields,
            source=cells[source_col] if source_col is not None else "", answer=answer, status=answer_status(answer),
        ))
    return items


def parse_round(doc: Doc) -> Round | None:
    """The latest walkthrough round of a doc: its premises, its item table and recorded dispositions."""
    rounds = [h for h in doc.headings if h.level == 2 and ROUND_RE.match(plain(h.text))]
    if not rounds:
        return None
    active = rounds[-1]
    match = ROUND_RE.match(plain(active.text))
    assert match is not None
    current = Round(int(match.group(2)), match.group(1), active.anchor)
    headings = iter(doc.headings)
    inside = False
    sub = ""
    entries: dict[str, list[list[dict[str, Any]]]] = {}
    for block in doc.blocks:
        if block["t"] == "heading":
            heading = next(headings, None)
            if block["level"] <= 2:
                inside = heading is active
                sub = ""
            elif inside and block["level"] == 3:
                sub = plain(block["text"]).lower()
                if sub.startswith("premises") and current.premise_heading is None and heading:
                    current.premise_heading = block
                    current.premise_anchor = heading.anchor
                elif sub.startswith("dispositions") and current.dispositions_heading is None:
                    current.dispositions_heading = block
            continue
        if not inside:
            continue
        if block["t"] == "list" and sub.startswith("premises") and current.premise_list is None:
            current.premise_list = block
            current.premises = [premise for premise in map(premise_from, block["items"]) if premise]
        elif block["t"] == "table" and current.table is None and not sub.startswith("premises") and is_item_table(block):
            current.table = block
            current.items = items_from(block)
        elif block["t"] == "list" and sub.startswith("dispositions"):
            for item in block["items"]:
                ident = leading_id(item[0]["text"]) if item and item[0]["t"] == "para" else None
                if ident:
                    entries.setdefault(ident, []).append(item)
    by_id = {item.ident: item for item in current.items}
    for ident, recorded in entries.items():
        # Sub-decisions (D40a) without a row of their own show in their parent's card.
        target = by_id.get(ident) or by_id.get(re.sub(r"[a-z]+$", "", ident))
        if target:
            target.recorded.extend(recorded)
    return current if current.items or current.premises else None


# ---------------------------------------------------------------- implementation tours


def parse_tour(doc: Doc) -> Tour | None:
    """A tour doc: a `## Change set` table (prefix, repo, base, head) and `## S<n> — <layer>` steps."""
    tour = Tour()
    for heading in doc.headings:
        match = STEP_RE.match(plain(heading.text)) if heading.level == 2 else None
        if match:
            tour.steps.append((match.group(1), heading.anchor, match.group(2)))
    headings = iter(doc.headings)
    inside = False
    for block in doc.blocks:
        if block["t"] == "heading":
            next(headings, None)
            if block["level"] <= 2:
                inside = plain(block["text"]).lower() == "change set"
            continue
        if not inside or block["t"] != "table" or tour.table is not None:
            continue
        header = [plain(cell).lower() for cell in block["header"]]
        path_col = next((header.index(name) for name in ("repo", "path", "repository") if name in header), None)
        if "base" not in header or path_col is None:
            continue
        tour.table = block
        prefix_col = header.index("prefix") if "prefix" in header else None
        head_col = header.index("head") if "head" in header else None
        for row in block["rows"]:
            cells = row + [""] * (len(header) - len(row))
            raw = cells[path_col].strip().strip("`").strip()
            if not raw:
                continue
            path = Path(os.path.expanduser(raw.replace("\\", "/"))).resolve()
            tour.rows.append(ChangeRow(
                prefix=plain(cells[prefix_col]) if prefix_col is not None else "",
                path=path,
                base=plain(cells[header.index("base")]),
                head=plain(cells[head_col]) if head_col is not None else WORKING_TREE,
            ))
    return tour if tour.rows and tour.steps else None


def count_lines(path: Path) -> int:
    try:
        data = path.read_bytes()
    except OSError:
        return 0
    if b"\0" in data[:8000]:
        return 0
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def load_change(row: ChangeRow, seen: dict[str, str]) -> None:
    """Fill a change-set row from git: merge base, changed and untracked files, and a fingerprint."""
    if not row.path.exists():
        row.problem = f"{row.path.as_posix()} does not exist"
        return
    top = git_top(row.path if row.path.is_dir() else row.path.parent)
    if top is None:
        row.problem = f"{row.path.as_posix()} is not in a git repository"
        return
    key = os.path.normcase(str(top))
    if key in seen:
        row.problem = f"same repository as {seen[key]}"
        return
    seen[key] = row.name
    row.top = top
    try:
        base = check_ref(row.base or "HEAD", "base")
        head = None if row.working else check_ref(row.head, "head")
        row.merge_base = run_git(top, "merge-base", base, head or "HEAD").strip()
        target = [row.merge_base] + ([head] if head else [])
        statuses: dict[str, str] = {}
        parts = run_git(top, "diff", "--name-status", "--no-renames", "-z", *target).split("\0")
        for status, name in zip(parts[0::2], parts[1::2]):
            statuses[name] = status[:1]
        numstat = run_git(top, "diff", "--numstat", "--no-renames", "-z", *target)
        for entry in numstat.split("\0"):
            fields = entry.split("\t")
            if len(fields) != 3:
                continue
            added, deleted, name = fields
            row.files.append(ChangedFile(name, statuses.get(name, "M"),
                                         int(added) if added.isdigit() else 0, int(deleted) if deleted.isdigit() else 0))
        fingerprint = [run_git(top, "diff", *target)]
        if head is None:
            for name in run_git(top, "ls-files", "--others", "--exclude-standard", "-z").split("\0"):
                if name:
                    row.files.append(ChangedFile(name, "new", count_lines(top / name), 0))
                    try:
                        fingerprint.append(name + ":" + hashlib.sha256((top / name).read_bytes()).hexdigest())
                    except OSError:
                        fingerprint.append(name)
        row.files.sort(key=lambda changed: changed.path)
        row.fingerprint = short_hash("\n".join(fingerprint))
    except ViewError as exc:
        row.problem = str(exc)


def load_config(spec_dir: Path) -> dict[str, Any]:
    path = spec_dir / VIEW_DIR / "config.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ViewError(f"{path}: invalid JSON: {exc}") from exc


def save_config(spec_dir: Path, config: dict[str, Any]) -> None:
    view_dir = ensure_view_dir(spec_dir)
    (view_dir / "config.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")


def ensure_view_dir(spec_dir: Path) -> Path:
    view_dir = spec_dir / VIEW_DIR
    (view_dir / "exhibits").mkdir(parents=True, exist_ok=True)
    ignore = view_dir / ".gitignore"
    if not ignore.exists():
        ignore.write_text("# Generated views are build output; never commit them.\n*\n", encoding="utf-8")
    return view_dir


def load_exhibits(spec_dir: Path, docs: list[Doc]) -> list[Exhibit]:
    exhibit_dir = spec_dir / VIEW_DIR / "exhibits"
    if not exhibit_dir.is_dir():
        return []
    by_file = {doc.file: doc for doc in docs}
    default = main_doc(docs)
    exhibits = []
    for path in sorted(exhibit_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("an exhibit must be a JSON object")
        except (ValueError, json.JSONDecodeError) as exc:
            exhibit = Exhibit(path=path, data={}, status="invalid")
            exhibit.problems.append(str(exc))
            exhibits.append(exhibit)
            continue
        exhibit = Exhibit(path=path, data=data)
        exhibit.item = str(data.get("item") or "").strip()
        if exhibit.item and not data.get("doc"):
            # An item exhibit belongs to the round that lists the item, the main doc's first.
            exhibit.doc = next(
                (doc for doc in [default, *docs] if doc.round and doc.round.find(exhibit.item)),
                next((doc for doc in [default, *docs] if doc.round), None),
            )
        else:
            exhibit.doc = by_file.get(str(data.get("doc") or default.file))
        exhibit.anchor = "" if exhibit.item else str(data.get("anchor") or "top")
        if exhibit.kind not in EXHIBIT_TYPES:
            exhibit.status = "invalid"
            exhibit.problems.append(f"type must be one of {', '.join(EXHIBIT_TYPES)}")
        elif exhibit.kind == "decision" and not exhibit.item:
            exhibit.status = "invalid"
            exhibit.problems.append("a decision exhibit needs item (the round item it answers, such as D4)")
        elif exhibit.kind == "decision" and decision_problem(data.get("data") or {}):
            exhibit.status = "invalid"
            exhibit.problems.append(decision_problem(data.get("data") or {}))
        elif exhibit.doc is None:
            exhibit.status = "orphan"
            exhibit.problems.append(
                f"doc {data.get('doc')!r} is not in this spec folder" if data.get("doc")
                else "no doc in this folder has a walkthrough round"
            )
        elif exhibit.item and (exhibit.doc.round is None or exhibit.doc.round.find(exhibit.item) is None):
            exhibit.status = "orphan"
            exhibit.problems.append(f"item {exhibit.item!r} is not in the latest round of {exhibit.doc.file}")
        elif not exhibit.item and exhibit.anchor != "top" and exhibit.doc.heading(exhibit.anchor) is None:
            exhibit.status = "orphan"
            exhibit.problems.append(f"anchor {exhibit.anchor!r} is not a heading in {exhibit.doc.file}")
        exhibits.append(exhibit)
    return exhibits


def decision_problem(data: dict[str, Any]) -> str:
    options = data.get("options") or []
    if not isinstance(options, list):
        return "options must be a list"
    suggested = sum(1 for option in options if isinstance(option, dict) and option.get("suggested"))
    if options and suggested != 1:
        return f"exactly one option needs \"suggested\": true (found {suggested})"
    return ""


def exhibit_sources(exhibit: Exhibit) -> list[str]:
    sources = exhibit.data.get("sources")
    if isinstance(sources, list) and sources:
        return [str(source) for source in sources]
    if exhibit.item:
        return [exhibit.item]
    return ["*"] if exhibit.anchor == "top" else [exhibit.anchor]


def source_hash(source: str, doc: Doc, by_file: dict[str, Doc]) -> str | None:
    """The current hash of one exhibit source: `*`, an anchor, a round item, or `file.md#anchor`."""
    if source == "*":
        return doc.sha
    if "#" in source or source.lower().endswith(".md"):
        file, _, anchor = source.partition("#")
        target = by_file.get(Path(file).name) if file else doc
        if target is None:
            return None
        if not anchor:
            return target.sha
        heading = target.heading(anchor)
        return heading.hash if heading else None
    heading = doc.heading(source)
    if heading:
        return heading.hash
    item = doc.round.find(source) if doc.round else None
    return item.hash if item else None


def evaluate_exhibit(exhibit: Exhibit, repo: Repo, by_file: dict[str, Doc], *, stamp_new: bool) -> None:
    """Compare an exhibit's stamp with its sources (and its code); stamp new ones."""
    if exhibit.status in {"invalid", "orphan"} or exhibit.doc is None:
        return
    sources = exhibit_sources(exhibit)
    current = {source: source_hash(source, exhibit.doc, by_file) for source in sources}
    missing = [source for source, value in current.items() if value is None]
    if missing:
        exhibit.status = "orphan"
        exhibit.problems.append(f"sources not found from {exhibit.doc.file}: {', '.join(missing)}")
        return
    hashes: dict[str, str] = {source: value for source, value in current.items() if value is not None}
    if exhibit.kind in CODE_EXHIBITS:
        try:
            exhibit.code = load_code(exhibit.data, repo)
        except ViewError as exc:
            exhibit.status = "invalid"
            exhibit.problems.append(str(exc))
            return
        hashes["code"] = exhibit.code["hash"]
    stamp = exhibit.data.get("stamp")
    if not isinstance(stamp, dict) or not stamp:
        if stamp_new:
            exhibit.data["stamp"] = hashes
            exhibit.path.write_text(json.dumps(exhibit.data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            exhibit.status = "stamped"
        else:
            exhibit.status = "unstamped"
        return
    changed = [key for key, value in hashes.items() if stamp.get(key) != value]
    if changed:
        exhibit.status = "stale"
        named = ["the code it shows" if key == "code" else key for key in changed]
        exhibit.problems.append("changed since drawn: " + ", ".join(named))


# ---------------------------------------------------------------- repository links


class Repo:
    def __init__(self, roots: list[Path], aliases: list[tuple[str, str]]):
        self.roots = [root for root in roots if root.is_dir()]
        self.aliases = sorted(aliases, key=lambda pair: -len(pair[0]))
        self._files: list[str] | None = None
        self._by_name: dict[str, list[str]] = {}
        self.cache: dict[str, Path | None] = {}
        self.change_rows: list[ChangeRow] = []

    def change_row(self, path: Path) -> ChangeRow | None:
        """The tour change-set row whose repository holds path."""
        target = os.path.normcase(os.path.abspath(path))
        for row in self.change_rows:
            top = os.path.normcase(os.path.abspath(row.top)) if row.top else ""
            if top and target.startswith(top + os.sep):
                return row
        return None

    def _index(self) -> list[str]:
        if self._files is None:
            self._files = []
            for root in self.roots:
                for current, dirs, files in os.walk(root):
                    dirs[:] = [name for name in dirs if name not in PRUNED_DIRS and not name.startswith(".")]
                    for name in files:
                        absolute = Path(current, name).as_posix()
                        self._files.append(absolute)
                        self._by_name.setdefault(name, []).append(absolute)
        return self._files

    def resolve(self, ref: str) -> Path | None:
        if ref in self.cache:
            return self.cache[ref]
        found = self._resolve(ref) if self.roots else None
        self.cache[ref] = found
        return found

    def _resolve(self, ref: str) -> Path | None:
        candidates = [ref]
        for prefix, target in self.aliases:
            if ref.startswith(prefix):
                candidates[:0] = [target + ref[len(prefix):], ref[len(prefix):]]
                break
        else:
            bare = re.sub(r"^[a-z][\w-]*:", "", ref)
            if bare != ref:
                candidates.insert(0, bare)
        for candidate in candidates:
            for root in self.roots:
                path = root / candidate
                if path.is_file():
                    return path
        files = self._index()
        if "/" not in ref:
            hits = self._by_name.get(ref, [])
            return Path(hits[0]) if len(hits) == 1 else None
        for candidate in candidates:
            suffix = "/" + candidate.lstrip("/")
            hits = [path for path in files if path.endswith(suffix)]
            if len(hits) == 1:
                return Path(hits[0])
        return None


def collect_aliases(docs: list[Doc]) -> list[tuple[str, str]]:
    aliases: list[tuple[str, str]] = []

    def visit(blocks: list[dict[str, Any]]) -> None:
        for block in blocks:
            if block["t"] == "table":
                header = [plain(cell).lower() for cell in block["header"]]
                if len(header) >= 2 and header[0] == "prefix" and header[1] == "path":
                    for row in block["rows"]:
                        if len(row) >= 2 and plain(row[0]) and plain(row[1]):
                            aliases.append((plain(row[0]), plain(row[1])))
            elif block["t"] == "quote":
                visit(block["blocks"])
            elif block["t"] == "list":
                for item in block["items"]:
                    visit(item)

    for doc in docs:
        visit(doc.blocks)
    return aliases


# ---------------------------------------------------------------- code, git and diffs


def lang_family(lang: str) -> str | None:
    lang = (lang or "").lower()
    return next((family for family, names in LANG_FAMILIES.items() if lang in names), None)


def highlight_lines(text: str, lang: str) -> list[str]:
    """Escape and colour code, returned one HTML string per source line."""
    family = lang_family(lang)
    if family is None:
        return [esc(line) for line in text.split("\n")]
    keywords = SQL_KEYWORDS if family == "sql" else KEYWORDS
    lines: list[list[str]] = [[]]

    def emit(kind: str | None, chunk: str) -> None:
        for number, piece in enumerate(chunk.split("\n")):
            if number:
                lines.append([])
            if piece:
                lines[-1].append(f'<span class="tk-{kind}">{esc(piece)}</span>' if kind else esc(piece))

    position = 0
    for match in TOKEN_RES[family].finditer(text):
        if match.start() > position:
            emit(None, text[position:match.start()])
        kind: str | None = match.lastgroup
        token = match.group()
        if kind == "word":
            word = token.lower() if family == "sql" else token
            if word in keywords:
                kind = "kw"
            elif text[match.end():match.end() + 1] == "(":
                kind = "fn"
            elif family == "c" and token[:1].isupper():
                kind = "ty"
            else:
                kind = None
        emit(kind, token)
        position = match.end()
    emit(None, text[position:])
    return ["".join(parts) for parts in lines]


def git_top(path: Path) -> Path | None:
    for parent in [path, *path.parents]:
        if (parent / ".git").exists():
            return parent
    return None


def run_git(cwd: Path, *args: str) -> str:
    git = shutil.which("git")
    if not git:
        raise ViewError("git is not on PATH")
    result = subprocess.run(
        [git, "-C", str(cwd), *args], capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if result.returncode != 0:
        raise ViewError(f"git {' '.join(args[:3])} failed: {result.stderr.strip()[:200]}")
    return result.stdout


def check_ref(ref: Any, name: str) -> str:
    ref = str(ref).strip()
    if not GIT_REF_RE.match(ref):
        raise ViewError(f"{name} {ref!r} is not a plain git ref")
    return ref


def head_label(path: Path) -> str:
    if git_top(path) is None:
        return "working tree"
    try:
        return "working tree at " + run_git(path.parent, "rev-parse", "--short", "HEAD").strip()
    except ViewError:
        return "working tree"


def load_code(data: dict[str, Any], repo: Repo) -> dict[str, Any]:
    """The code a code/diff exhibit shows, plus a hash used to notice when it changes."""
    spec = data.get("data") or {}
    if data.get("type") == "diff" and isinstance(spec.get("before"), str) and isinstance(spec.get("after"), str):
        before, after = spec["before"], spec["after"]
        return {"mode": "text", "before": before, "after": after, "lang": str(spec.get("lang") or ""),
                "hash": short_hash(before + "\x00" + after)}
    reference = str(spec.get("path") or "").strip()
    if not reference:
        raise ViewError("needs data.path (or data.before and data.after for a diff)")
    if not repo.roots:
        raise ViewError("needs --repo so the code can be read")
    resolved = repo.resolve(reference)
    if resolved is None:
        raise ViewError(f"path {reference!r} not found under the repo roots")
    lang = str(spec.get("lang") or resolved.suffix.lstrip("."))
    if data.get("type") == "code":
        ref = check_ref(spec["ref"], "ref") if spec.get("ref") else None
        if ref:
            text = run_git(resolved.parent, "show", f"{ref}:./{resolved.name}")
        else:
            text = resolved.read_text(encoding="utf-8", errors="replace")
        lines = text.replace("\r\n", "\n").split("\n")
        bounds = parse_range(spec.get("lines"), len(lines)) or (1, min(len(lines), 40))
        start, end = bounds[0], min(bounds[1], bounds[0] + MAX_EXCERPT_LINES - 1)
        excerpt = "\n".join(lines[start - 1:end])
        return {"mode": "code", "path": resolved, "reference": reference, "start": start, "end": end,
                "text": excerpt, "lang": lang, "at": ref or head_label(resolved), "hash": short_hash(excerpt)}
    if git_top(resolved) is None:
        raise ViewError(f"{reference} is not in a git repository")
    row = repo.change_row(resolved)
    if spec.get("base"):
        base = check_ref(spec["base"], "base")
        head = check_ref(spec["head"], "head") if spec.get("head") else None
        base_label = base
    elif row:
        # In a tour, a diff defaults to the change set: merge base → head (or the working tree).
        base, head = row.merge_base, None if row.working else row.head
        base_label = f"{row.base} (merge base {row.merge_base[:7]})"
    else:
        base, head, base_label = "HEAD", None, "HEAD"
    context = max(0, min(int(spec.get("context", 3)), 12))
    if head is None and not is_tracked(resolved):
        lines = resolved.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").split("\n")
        if lines and lines[-1] == "":
            lines.pop()
        diff_text = f"@@ -0,0 +1,{len(lines)} @@\n" + "\n".join("+" + line for line in lines)
        base_label = "untracked (new file)"
    else:
        args = ["diff", "--no-color", "--no-ext-diff", f"-U{context}", base] + ([head] if head else []) + ["--", resolved.name]
        diff_text = run_git(resolved.parent, *args)
    if not diff_text.strip():
        raise ViewError(f"git diff {base_label} {head or '(working tree)'} shows no change in {reference}")
    return {"mode": "git", "path": resolved, "reference": reference, "diff": diff_text, "lang": lang,
            "base": base_label, "head": head or WORKING_TREE, "window": parse_range(spec.get("lines")),
            "hash": short_hash(diff_text)}


def is_tracked(path: Path) -> bool:
    try:
        run_git(path.parent, "ls-files", "--error-unmatch", "--", path.name)
        return True
    except ViewError:
        return False


def parse_unified(diff_text: str) -> list[dict[str, Any]]:
    hunks: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for line in diff_text.split("\n"):
        match = HUNK_RE.match(line)
        if match:
            current = {"old": int(match.group(1)), "new": int(match.group(3)), "section": match.group(5).strip(), "lines": []}
            hunks.append(current)
        elif current is not None and line[:1] in ("+", "-", " ") and not line.startswith(("+++", "---")):
            current["lines"].append((line[0], line[1:]))
    return hunks


def git_diff_rows(diff_text: str, lang: str, window: tuple[int, int] | None) -> list[tuple[str, int | None, int | None, str]]:
    rows: list[tuple[str, int | None, int | None, str]] = []
    for hunk in parse_unified(diff_text):
        old, new = hunk["old"], hunk["new"]
        hunk_rows = []
        for sign, content in hunk["lines"]:
            line_html = highlight_lines(content, lang)[0] if content else ""
            if sign == " ":
                hunk_rows.append((" ", old, new, line_html))
                old += 1
                new += 1
            elif sign == "-":
                hunk_rows.append(("-", old, None, line_html))
                old += 1
            else:
                hunk_rows.append(("+", None, new, line_html))
                new += 1
        if window:
            kept = []
            position = hunk["new"]
            for row in hunk_rows:
                at = row[2] if row[2] is not None else position
                if window[0] <= at <= window[1]:
                    kept.append(row)
                if row[2] is not None:
                    position = row[2] + 1
            hunk_rows = kept
        if not hunk_rows:
            continue
        numbers = [row[2] for row in hunk_rows if row[2] is not None] or [hunk["new"]]
        label = f"@@ lines {min(numbers)}–{max(numbers)}" + (f" · {hunk['section']}" if hunk["section"] else "")
        rows.append(("@", None, None, esc(label)))
        rows.extend(hunk_rows)
    return rows


def text_diff_rows(before: str, after: str, lang: str) -> list[tuple[str, int | None, int | None, str]]:
    before_lines, after_lines = before.split("\n"), after.split("\n")
    before_html, after_html = highlight_lines(before, lang), highlight_lines(after, lang)
    rows: list[tuple[str, int | None, int | None, str]] = []
    matcher = difflib.SequenceMatcher(None, before_lines, after_lines, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            rows.extend((" ", i1 + k + 1, j1 + k + 1, after_html[j1 + k]) for k in range(i2 - i1))
            continue
        rows.extend(("-", k + 1, None, before_html[k]) for k in range(i1, i2))
        rows.extend(("+", None, k + 1, after_html[k]) for k in range(j1, j2))
    return rows


def split_before_after(text: str) -> tuple[str, str] | None:
    """A fenced block holding `// before` then `// after` sections, as two texts."""
    lines = text.split("\n")
    marks = [(index, match.group(1).lower()) for index, line in enumerate(lines) if (match := BEFORE_AFTER_RE.match(line))]
    if len(marks) != 2 or marks[0][1] != "before" or marks[1][1] != "after":
        return None
    before_at, after_at = marks[0][0], marks[1][0]
    preamble = lines[:before_at]
    before = lines[before_at + 1:after_at]
    while before and not before[-1].strip():
        before.pop()
    after = lines[after_at + 1:]
    return "\n".join(preamble + before), "\n".join(preamble + after)


# ---------------------------------------------------------------- diagrams


def text_width(text: str, size: float = 13.0) -> float:
    total = 0.0
    for char in text:
        if char in "ilIjt.,:;'|!()[] ":
            total += 0.33
        elif char.isupper() or char in "mwMW@%":
            total += 0.7
        else:
            total += 0.56
    return total * size


def border_point(cx: float, cy: float, half_w: float, half_h: float, dx: float, dy: float) -> tuple[float, float]:
    tx = half_w / abs(dx) if dx else math.inf
    ty = half_h / abs(dy) if dy else math.inf
    t = min(tx, ty)
    return cx + dx * t, cy + dy * t


def grid_positions(ids: list[str], grid: Any) -> tuple[dict[str, tuple[int, int]], int, int]:
    positions: dict[str, tuple[int, int]] = {}
    used_rows = 0
    if isinstance(grid, list):
        used_rows = len(grid)
        for row_index, row in enumerate(grid):
            if not isinstance(row, list):
                continue
            for col_index, cell in enumerate(row):
                if cell is not None and str(cell) in ids and str(cell) not in positions:
                    positions[str(cell)] = (row_index, col_index)
    missing = [ident for ident in ids if ident not in positions]
    for number, ident in enumerate(missing):
        positions[ident] = (used_rows + number // 3, number % 3)
    rows = max((row for row, _ in positions.values()), default=0) + 1
    cols = max((col for _, col in positions.values()), default=0) + 1
    return positions, rows, cols


def svg_open(kind: str, uid: str, width: float, height: float, label: str) -> str:
    heads = "".join(
        f'<marker id="{uid}-head{suffix}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" '
        f'markerHeight="8" orient="auto-start-reverse"><path class="dg-head{css}" d="M0 0 L10 5 L0 10 z"/></marker>'
        for suffix, css in (("", ""), ("-new", " new"), ("-del", " del"))
    )
    return (
        f'<div class="dg-wrap"><svg class="dg dg-{kind}" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-label="{esc(label)}"><defs>{heads}</defs>'
    )


def label_right(x: float, text: str, anchor: str = "middle") -> float:
    width = text_width(text, 12) + 10
    return {"middle": x + width / 2, "start": x - 4 + width, "end": x + 4}[anchor]


def label_box(x: float, y: float, text: str, *, anchor: str = "middle", css: str = "elabel") -> str:
    width = text_width(text, 12) + 10
    left = {"middle": x - width / 2, "start": x - 4, "end": x - width + 4}[anchor]
    return (
        f'<g class="{css}"><rect x="{left:.1f}" y="{y - 10:.1f}" width="{width:.1f}" height="18" rx="4"/>'
        f'<text x="{x:.1f}" y="{y + 3:.1f}" text-anchor="{anchor}">{esc(text)}</text></g>'
    )


# ---------------------------------------------------------------- id index


def definition_id(text: str) -> str | None:
    candidate = plain(text).strip(" :.*")
    return candidate if ID_FULL_RE.match(candidate) else None


def item_element_id(doc: Doc, ident: str) -> str:
    return f"{doc.id}__item-{slugify(ident)}"


def item_label(item: RoundItem) -> str:
    if item.kind == "premise":
        label = f"{item.ident} · {plain(item.title)} — {plain(item.text)}" if item.title else f"{item.ident} · {plain(item.text)}"
    else:
        label = f"{item.ident} · " + " · ".join(f"{plain(name)}: {plain(cell)}" for name, cell in item.fields)
        if plain(item.answer):
            label += f" · Disposition: {plain(item.answer)}"
    return label[:320]


def leading_id(text: str) -> str | None:
    match = re.match(r"^\s*(?:\*\*)?([A-Z][A-Z0-9]{0,3}(?:-[A-Z]{1,3})?-?\d{1,3}[a-z]?)(?:\*\*)?\s*(?::|—|–|\s-\s)", text)
    return match.group(1) if match else None


class Index:
    """IDs defined in the spec set (table first cells, list items, headings)."""

    def __init__(self, docs: list[Doc]):
        self.defs: dict[str, dict[str, str]] = {}
        self.assigned: set[str] = set()
        self.task_docs = {}
        for doc in docs:
            match = re.match(r"task_(\d+)\.md$", doc.file)
            if match:
                self.task_docs[f"T{int(match.group(1))}"] = doc
        for doc in docs:
            self._visit(doc, doc.blocks)
        for task_id, doc in self.task_docs.items():
            self.defs.setdefault(task_id, {"t": doc.id, "l": doc.title, "d": doc.file})
        for doc in docs:
            # A round's IDs point at its cards, not at an earlier round's row of the same item.
            for item in (doc.round.premises + doc.round.items) if doc.round else []:
                entry = self.defs.get(item.ident)
                if entry is None or entry["d"] == doc.file:
                    self.defs[item.ident] = {"t": item_element_id(doc, item.ident), "l": item_label(item), "d": doc.file}
                    self.assigned.add(item.ident)
            # A tour's step IDs point at the step headings, not at the roadmap rows.
            for ident, anchor, title in doc.tour.steps if doc.tour else []:
                entry = self.defs.get(ident)
                if entry is None or entry["d"] == doc.file:
                    self.defs[ident] = {"t": f"{doc.id}__{anchor}", "l": f"{ident} — {plain(title)}", "d": doc.file}
                    self.assigned.add(ident)

    def _add(self, ident: str, doc: Doc, label: str, anchor: str) -> None:
        if ident not in self.defs:
            self.defs[ident] = {"t": f"{doc.id}__{anchor}", "l": label[:320], "d": doc.file}

    def _visit(self, doc: Doc, blocks: list[dict[str, Any]]) -> None:
        heading_anchors = iter(doc.headings)
        for block in blocks:
            kind = block["t"]
            if kind == "heading":
                heading = next(heading_anchors, None)
                ident = leading_id(block["text"] + " :") or definition_id(block["text"].split(" ")[0])
                if ident and heading:
                    self._add(ident, doc, plain(block["text"]), heading.anchor)
            elif kind == "table":
                self._table(doc, block)
            elif kind == "list":
                self._list(doc, block)
            elif kind == "quote":
                self._nested(doc, block["blocks"])

    def _table(self, doc: Doc, block: dict[str, Any]) -> None:
        header = [plain(cell) for cell in block["header"]]
        for row in block["rows"]:
            ident = definition_id(row[0]) if row else None
            if ident:
                parts = [
                    f"{header[i]}: {plain(cell)}" if i < len(header) and header[i] else plain(cell)
                    for i, cell in enumerate(row[1:], start=1)
                    if plain(cell)
                ]
                self._add(ident, doc, f"{ident} · " + " · ".join(parts), "id-" + slugify(ident))

    def _list(self, doc: Doc, block: dict[str, Any]) -> None:
        for item in block["items"]:
            if item and item[0]["t"] == "para":
                ident = leading_id(item[0]["text"])
                if ident:
                    self._add(ident, doc, plain(item[0]["text"]), "id-" + slugify(ident))
            self._nested(doc, item)

    def _nested(self, doc: Doc, blocks: list[dict[str, Any]]) -> None:
        for block in blocks:
            if block["t"] == "list":
                self._list(doc, block)
            elif block["t"] == "table":
                self._table(doc, block)

    def claim(self, ident: str, doc: Doc) -> str | None:
        """Return the element id for the first definition of ident in doc, once."""
        entry = self.defs.get(ident)
        if not entry or entry["d"] != doc.file or ident in self.assigned:
            return None
        target = entry["t"].split("__", 1)
        if len(target) != 2 or not target[1].startswith("id-"):
            return None
        self.assigned.add(ident)
        return entry["t"]


# ---------------------------------------------------------------- rendering


class Renderer:
    def __init__(self, spec_dir: Path, docs: list[Doc], exhibits: list[Exhibit], repo: Repo):
        self.spec_dir = spec_dir
        self.docs = docs
        self.by_file = {doc.file: doc for doc in docs}
        self.exhibits = exhibits
        self.repo = repo
        self.index = Index(docs)
        self.lint: dict[str, set[str]] = {"unresolved paths": set(), "unresolved links": set(), "unresolved refs": set()}
        self.counts: dict[str, dict[str, int]] = {}
        self.doc: Doc = docs[0]
        self.lint_paths = True
        self.step: str | None = None  # the tour step being rendered
        self.cites: dict[str, set[str]] = {}  # file (normalized absolute path) -> tour steps that cite it
        self.tour_stats: dict[str, dict[str, int]] = {}

    def cite(self, path: Path) -> None:
        if self.step:
            self.cites.setdefault(os.path.normcase(os.path.abspath(path)), set()).add(self.step)

    # ---- inline

    def inline(self, text: str, *, ids: bool = True) -> str:
        slots: list[str] = []

        def keep(fragment: str) -> str:
            slots.append(fragment)
            return f"\x00{len(slots) - 1}\x00"

        def code_span(match: re.Match[str]) -> str:
            code = match.group(2)
            if len(code) > 2 and code[0] == " " and code[-1] == " " and code.strip():
                code = code[1:-1]
            return keep(self.code_span(code))

        text = re.sub(r"(`+)(.+?)(?<!`)\1(?!`)", code_span, text, flags=re.S)
        text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|~<>])", lambda m: keep(esc(m.group(1))), text)

        def link(match: re.Match[str]) -> str:
            label = match.group(2)
            target = re.sub(r"\s+\"[^\"]*\"$", "", match.group(3)).strip().strip("<>")
            href, external = self.link_target(target)
            if match.group(1) == "!":
                return keep(f'<img src="{esc(href)}" alt="{esc(plain(label))}" loading="lazy">')
            attrs = ' target="_blank" rel="noopener"' if external else ""
            return keep(f'<a href="{esc(href)}"{attrs}>{self.emphasis(label, ids=False)}</a>')

        text = re.sub(r"(!?)\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^()\s]*(?:\([^()\s]*\))?[^()\s]*(?:\s+\"[^\"]*\")?)\)", link, text)
        text = re.sub(
            r"<(https?://[^>\s]+)>",
            lambda m: keep(f'<a href="{esc(m.group(1))}" target="_blank" rel="noopener">{esc(m.group(1))}</a>'),
            text,
        )
        text = re.sub(
            r"(?<![\"'=\w/])(https?://[^\s<>()\]\x00]+[^\s<>()\].,;:!?'\"\x00])",
            lambda m: keep(f'<a href="{esc(m.group(1))}" target="_blank" rel="noopener">{esc(m.group(1))}</a>'),
            text,
        )
        rendered = self.emphasis(text, ids=ids)
        while "\x00" in rendered:
            rendered = re.sub(r"\x00(\d+)\x00", lambda m: slots[int(m.group(1))], rendered)
        return rendered

    def emphasis(self, text: str, *, ids: bool) -> str:
        text = html.escape(text, quote=False)
        text = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<![\w_])__(?=\S)(.+?)(?<=\S)__(?![\w_])", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<![\w*])\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?![\w*])", r"<em>\1</em>", text)
        text = re.sub(r"(?<![\w_])_(?=[^\s_])(.+?)(?<=[^\s_])_(?![\w_])", r"<em>\1</em>", text)
        text = re.sub(r"~~(?=\S)(.+?)(?<=\S)~~", r"<del>\1</del>", text)
        if ids:
            text = ID_RE.sub(lambda m: self.id_anchor(m.group(1)), text)
        return text

    def id_anchor(self, ident: str) -> str:
        entry = self.index.defs.get(ident)
        if not entry:
            return esc(ident)
        return f'<a class="idref" href="#{esc(entry["t"])}" data-id="{esc(ident)}">{esc(ident)}</a>'

    def editor_link(self, path: Path, line: int | str, inner: str) -> str:
        href = "vscode://file/" + path.as_posix() + f":{line}"
        title = f"Open in VS Code: {path.as_posix()}"
        return f'<a class="code-ref" href="{esc(href)}" title="{esc(title)}">{inner}</a>'

    def code_span(self, code: str) -> str:
        inner = f"<code>{esc(code)}</code>"
        match = PATH_RE.match(code.strip())
        if not match or not self.repo.roots:
            return inner
        resolved = self.repo.resolve(match.group("path"))
        if resolved is None:
            if "/" in match.group("path") and self.lint_paths:
                self.lint["unresolved paths"].add(f"{self.doc.file}: {match.group('path')}")
            return inner
        self.cite(resolved)
        return self.editor_link(resolved, match.group("line") or "1", inner)

    def link_target(self, target: str) -> tuple[str, bool]:
        if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
            return target, True
        if target.startswith("#"):
            anchor = target[1:]
            if not anchor:
                return f"#{self.doc.id}", False
            if self.doc.heading(anchor) is None:
                self.lint["unresolved links"].add(f"{self.doc.file}: {target}")
            return f"#{self.doc.id}__{anchor}", False
        path_part, _, anchor = target.partition("#")
        resolved = (self.doc.path.parent / path_part).resolve()
        for doc in self.docs:
            if doc.path.resolve() == resolved:
                if anchor and doc.heading(anchor) is None:
                    self.lint["unresolved links"].add(f"{self.doc.file}: {target}")
                return (f"#{doc.id}__{anchor}" if anchor else f"#{doc.id}"), False
        if not resolved.exists():
            self.lint["unresolved links"].add(f"{self.doc.file}: {target}")
        relative = os.path.relpath(resolved, self.spec_dir / VIEW_DIR).replace(os.sep, "/")
        return relative + (f"#{anchor}" if anchor else ""), False

    # ---- blocks

    def blocks(self, blocks: list[dict[str, Any]], *, tight: bool = False) -> str:
        return "".join(self.block(block, tight=tight) for block in blocks)

    def block(self, block: dict[str, Any], *, tight: bool = False) -> str:
        kind = block["t"]
        if kind == "para":
            body = self.inline(block["text"])
            return body if tight else f"<p>{body}</p>"
        if kind == "code":
            return self.code_block(block)
        if kind == "quote":
            return f"<blockquote>{self.blocks(block['blocks'])}</blockquote>"
        if kind == "hr":
            return "<hr>"
        if kind == "list":
            return self.list_block(block)
        if kind == "table":
            return self.table(block)
        if kind == "heading":
            return f"<h{block['level']}>{self.inline(block['text'])}</h{block['level']}>"
        return ""

    def list_block(self, block: dict[str, Any]) -> str:
        tag = "ol" if block["ordered"] else "ul"
        start = f' start="{block["start"]}"' if block["ordered"] and block["start"] != 1 else ""
        items = []
        for item in block["items"]:
            ident = leading_id(item[0]["text"]) if item and item[0]["t"] == "para" else None
            element_id = self.index.claim(ident, self.doc) if ident else None
            attr = f' id="{esc(element_id)}"' if element_id else ""
            tight = len(item) == 1 and item[0]["t"] == "para"
            items.append(f"<li{attr}>{self.blocks(item, tight=tight)}</li>")
        return f"<{tag}{start}>{''.join(items)}</{tag}>"

    def code_block(self, block: dict[str, Any]) -> str:
        lang = block["lang"]
        text = block["text"]
        is_diagram = (not lang or lang in {"text", "txt", "plain"}) and bool(TEXT_DIAGRAM_RE.search(text))
        if is_diagram:
            return (
                '<figure class="codeblock diagram"><figcaption><span class="cap">text diagram</span></figcaption>'
                f"<pre><code>{esc(text)}</code></pre></figure>"
            )
        split = split_before_after(text) if lang_family(lang) else None
        if split:
            rows = text_diff_rows(split[0], split[1], lang)
            return self.diff_figure(rows, f"{esc(lang)} · before → after, from the spec")
        return self.code_figure(highlight_lines(text, lang), f'<span class="cap">{esc(lang or "text")}</span>')

    def code_figure(self, lines_html: list[str], caption: str, *, start: int = 1,
                    highlight: set[int] | None = None, pins: dict[int, list[str]] | None = None) -> str:
        highlight = highlight or set()
        pins = pins or {}
        rows = []
        for offset, line_html in enumerate(lines_html):
            number = start + offset
            css = "cl hl" if number in highlight else "cl"
            rows.append(f'<span class="{css}"><span class="ln" aria-hidden="true">{number}</span>'
                        f'<span class="lc">{line_html or " "}</span></span>')
            rows.extend(pins.get(number, []))
        return (
            f'<figure class="codeblock"><figcaption>{caption}</figcaption>'
            f'<pre class="code"><code>{"".join(rows)}</code></pre></figure>'
        )

    def diff_figure(self, rows: list[tuple[str, int | None, int | None, str]], caption: str) -> str:
        adds = sum(1 for row in rows if row[0] == "+")
        dels = sum(1 for row in rows if row[0] == "-")
        body = []
        for sign, old, new, line_html in rows:
            if sign == "@":
                body.append(f'<span class="dl hunk"><span class="lc">{line_html}</span></span>')
                continue
            css = {"+": "add", "-": "del", " ": "ctx"}[sign]
            body.append(
                f'<span class="dl {css}"><span class="ln" aria-hidden="true">{old or ""}</span>'
                f'<span class="ln" aria-hidden="true">{new or ""}</span>'
                f'<span class="sg">{"" if sign == " " else sign}</span><span class="lc">{line_html or " "}</span></span>'
            )
        return (
            f'<figure class="codeblock diffblock"><figcaption><span class="cap">{caption}</span>'
            f'<span class="diffstat"><span class="add">+{adds}</span><span class="del">−{dels}</span></span></figcaption>'
            f'<pre class="diff"><code>{"".join(body)}</code></pre></figure>'
        )

    def table(self, block: dict[str, Any]) -> str:
        header = block["header"]
        lowered = [plain(cell).lower() for cell in header]
        if "weight" in lowered and "score" in lowered:
            confidence = self.confidence(block, lowered)
            if confidence:
                return confidence
        status_columns = {i for i, name in enumerate(lowered) if name in STATUS_HEADERS}
        aligns = block["aligns"]
        head_cells = "".join(
            f'<th scope="col"{self.align(aligns, i)}>{self.inline(cell)}</th>' for i, cell in enumerate(header)
        )
        rows = []
        for row in block["rows"]:
            ident = definition_id(row[0]) if row else None
            element_id = self.index.claim(ident, self.doc) if ident else None
            attr = f' id="{esc(element_id)}"' if element_id else ""
            cells = []
            for i, cell in enumerate(row):
                content = self.inline(cell)
                if i in status_columns:
                    css = status_class(cell)
                    if css:
                        content = f'<span class="chip {css}">{content}</span>'
                cells.append(f"<td{self.align(aligns, i)}>{content}</td>")
            rows.append(f"<tr{attr}>{''.join(cells)}</tr>")
        return (
            f'<div class="tbl"><table><thead><tr>{head_cells}</tr></thead>'
            f"<tbody>{''.join(rows)}</tbody></table></div>"
        )

    @staticmethod
    def align(aligns: list[str], index: int) -> str:
        return f' style="text-align:{aligns[index]}"' if index < len(aligns) and aligns[index] else ""

    def confidence(self, block: dict[str, Any], lowered: list[str]) -> str:
        weight_col = lowered.index("weight")
        score_col = lowered.index("score")
        evidence_col = next((i for i, name in enumerate(lowered) if name in {"evidence", "notes", "why"}), None)
        rows = []
        total = ""
        for row in block["rows"]:
            if len(row) <= max(weight_col, score_col):
                continue
            weight = re.search(r"(\d+(?:\.\d+)?)", plain(row[weight_col]))
            score = re.search(r"(\d+(?:\.\d+)?)", plain(row[score_col]))
            if plain(row[0]).lower().startswith("total"):
                total = plain(row[score_col])
                continue
            if not weight or not score:
                continue
            weight_value = float(weight.group(1))
            percent = max(0.0, min(100.0, 100.0 * float(score.group(1)) / weight_value)) if weight_value else 0.0
            evidence = ""
            if evidence_col is not None and evidence_col < len(row) and plain(row[evidence_col]):
                evidence = f'<div class="conf-evidence">{self.inline(row[evidence_col])}</div>'
            rows.append(
                f'<div class="conf-row"><div class="conf-label">{self.inline(row[0])}'
                f' <span class="muted">· {esc(plain(row[weight_col]))}</span></div>'
                f'<div class="conf-score">{score.group(1)} / {weight.group(1)}</div>'
                f'<div class="conf-bar" role="img" aria-label="{percent:.0f}% of the weight">'
                f'<span style="width:{percent:.0f}%"></span></div>{evidence}</div>'
            )
        if not rows:
            return ""
        total_html = f'<div class="conf-total">Total <strong>{esc(total)}</strong></div>' if total else ""
        return f'<div class="confidence">{total_html}{"".join(rows)}</div>'

    # ---- documents

    def render_doc(self, doc: Doc) -> tuple[str, str]:
        self.doc = doc
        counts = {"create": 0, "modify": 0, "delete": 0}
        by_anchor: dict[str, list[Exhibit]] = {}
        for exhibit in self.exhibits:
            if exhibit.doc is doc and exhibit.status not in {"invalid", "orphan"} and not exhibit.item:
                by_anchor.setdefault(exhibit.anchor, []).append(exhibit)
        headings = iter(doc.headings)
        out: list[str] = []
        stack: list[int] = []
        intro: list[str] = []
        notes: list[str] = []
        seen_section = False
        current = doc.round
        tour = doc.tour
        steps = tour.steps if tour else []
        step_nav = {
            anchor: (ident, steps[i - 1][1] if i else None, steps[i + 1][1] if i + 1 < len(steps) else None)
            for i, (ident, anchor, _) in enumerate(steps)
        }
        coverage_slot = "\x00coverage\x00"
        self.step = None
        for block in doc.blocks:
            if block["t"] == "heading":
                heading = next(headings, None) or Heading(block["level"], block["text"], slugify(block["text"]), 0)
                if block["level"] == 1 and not seen_section:
                    continue
                if current and block is current.premise_heading:
                    continue  # its list is drawn as Round 0 at the top of the round
                seen_section = True
                if block["level"] <= 2:
                    nav = step_nav.get(heading.anchor)
                    self.step = nav[0] if nav else None
                collapsed = bool(current) and block is current.dispositions_heading
                step = step_nav.get(heading.anchor) if block["level"] == 2 else None
                out.append(self.heading(block, heading, stack, counts, collapsed=collapsed, step=step))
                out.extend(self.exhibit(exhibit) for exhibit in by_anchor.get(heading.anchor, []))
                continue
            if current and block is current.premise_list:
                if current.table is None:
                    out.append(self.round_panel(doc, current))
                continue
            if current and block is current.table:
                out.append(self.round_panel(doc, current))
                continue
            if tour and block is tour.table:
                out.append(self.block(block) + coverage_slot)
                continue
            rendered = self.block(block)
            if not seen_section:
                (notes if block["t"] == "quote" else intro).append(rendered)
            else:
                out.append(rendered)
        while stack:
            stack.pop()
            out.append("</div></section>")
        self.step = None
        self.counts[doc.id] = counts
        body = "".join(out)
        if tour:
            # Rendered last: it marks every changed file with the steps that cited it.
            body = body.replace(coverage_slot, self.coverage(doc, tour))
        top = "".join(self.exhibit(exhibit) for exhibit in by_anchor.get("top", []))
        notes_html = (
            f'<div class="doc-notes"><div class="label">Notes at the top of this doc</div>{"".join(notes)}</div>'
            if notes else ""
        )
        intro_html = f'<div class="doc-intro">{"".join(intro)}</div>' if intro else ""
        article = (
            f'<article class="doc" id="{doc.id}" data-doc="{doc.id}" hidden>{self.doc_head(doc, counts)}'
            f'{notes_html}{intro_html}{top}{body}</article>'
        )
        return article, self.outline(doc, by_anchor)

    def heading(self, block: dict[str, Any], heading: Heading, stack: list[int], counts: dict[str, int],
                *, collapsed: bool = False, step: tuple[str, str | None, str | None] | None = None) -> str:
        level = block["level"]
        element_id = f"{self.doc.id}__{heading.anchor}"
        text_html = self.heading_text(block["text"], counts)
        if level > 3:
            return f'<h{level} id="{esc(element_id)}" class="anchored">{text_html}</h{level}>'
        closing = []
        while stack and stack[-1] >= level:
            stack.pop()
            closing.append("</div></section>")
        stack.append(level)
        title = esc(plain(block["text"]))
        step_attr = step_tools = ""
        if step:
            ident, before, after = step
            step_attr = f' data-step="{esc(ident)}"'
            links = [
                f'<a class="tool" href="#{esc(self.doc.id)}__{esc(target)}" aria-label="{label} step">{arrow}</a>'
                for target, label, arrow in ((before, "Previous", "←"), (after, "Next", "→")) if target
            ]
            step_tools = (
                "".join(links)
                + f'<button type="button" class="tool" data-action="reviewed" aria-pressed="false">Reviewed</button>'
            )
        return (
            "".join(closing)
            + f'<section class="sec lvl{level}{" collapsed" if collapsed else ""}" data-anchor="{esc(heading.anchor)}" data-title="{title}"{step_attr}>'
            f'<div class="sec-head"><h{level} id="{esc(element_id)}" class="anchored">{text_html}</h{level}>'
            f'<div class="sec-tools">{step_tools}'
            f'<button type="button" class="tool" data-action="comment" aria-label="Comment on {title}">Comment</button>'
            f'<button type="button" class="tool" data-action="collapse" aria-expanded="{"false" if collapsed else "true"}" aria-label="Collapse {title}">'
            f'<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 6 L8 10 L12 6"></path></svg></button>'
            f"</div></div><div class=\"sec-body\">"
        )

    def heading_text(self, text: str, counts: dict[str, int]) -> str:
        match = IMPL_HEADING_RE.match(text)
        if not match:
            return self.inline(text)
        action = match.group("action").lower()
        key = {"create": "create", "modify": "modify"}.get(action, "delete")
        counts[key] += 1
        mark = {"create": "+", "modify": "~", "delete": "−"}[key]
        lead = esc(match.group("lead") or "")
        rest = self.inline(match.group("rest")) if match.group("rest").strip() else ""
        self.lint_paths = key != "create"
        subject = self.inline(match.group("subject"))
        self.lint_paths = True
        return (
            f'<span class="impl"><span class="mark {key}" aria-label="{esc(match.group("action"))}">{mark}</span>'
            f'{lead}{subject}<span class="impl-action">{esc(match.group("action"))}{rest}</span></span>'
        )

    def doc_head(self, doc: Doc, counts: dict[str, int]) -> str:
        chips = []
        mode = re.search(r"Mode:\s*\*\*([^*]+)\*\*", doc.text)
        approach = re.search(r"Design approach:\s*\*\*([^*]+)\*\*", doc.text)
        if mode:
            chips.append(esc(mode.group(1).strip()))
        if approach:
            chips.append(esc(approach.group(1).strip()))
        total = self.confidence_total(doc)
        if total:
            chips.append(f"Confidence {esc(total)}")
        files = counts["create"] + counts["modify"] + counts["delete"]
        if files:
            parts = [f"+{counts['create']} create"] if counts["create"] else []
            parts += [f"~{counts['modify']} modify"] if counts["modify"] else []
            parts += [f"−{counts['delete']} delete"] if counts["delete"] else []
            chips.append(f"Implementation map · {files} entries · " + " · ".join(parts))
        progress = re.search(r"\*\*Overall Progress\*\*:\s*([^\n]+)", doc.text)
        if progress:
            chips.append(esc(plain(progress.group(1))))
        if doc.round:
            chips.insert(0, f"Walkthrough · round {doc.round.number} · {esc(doc.round.date)}")
        stats = self.tour_stats.get(doc.id)
        if doc.tour and stats:
            chips[:0] = [
                f"Tour · {len(doc.tour.steps)} steps",
                f"{stats['repos']} repos · {stats['files']} files · +{stats['added']} −{stats['deleted']}",
                f"{stats['cited']} of {stats['files']} files cited",
                f'<span data-reviewed-count>0</span>&nbsp;of {len(doc.tour.steps)} steps reviewed',
            ]
        exhibits = sum(1 for exhibit in self.exhibits if exhibit.doc is doc and exhibit.status not in {"invalid", "orphan"})
        if exhibits:
            chips.append(f'<span class="tag">Illustrations</span> {exhibits}')
        chip_html = "".join(f'<span class="chip">{chip}</span>' for chip in chips)
        return (
            f'<header class="doc-head"><div class="kicker">{esc(doc.file)}</div>'
            f"<h1>{esc(doc.title)}</h1>"
            f'<div class="chips">{chip_html}</div></header>'
        )

    @staticmethod
    def confidence_total(doc: Doc) -> str:
        for line in doc.text.split("\n"):
            if re.match(r"^\|\s*\**total\**\s*\|", line, re.I):
                percents = re.findall(r"(\d{1,3}(?:\.\d+)?)\s*%", line)
                if percents:
                    return percents[-1] + "%"
        return ""

    def outline(self, doc: Doc, by_anchor: dict[str, list[Exhibit]]) -> str:
        items = []
        for heading in doc.headings:
            if heading.level not in (2, 3):
                continue
            marks = ""
            exhibits = by_anchor.get(heading.anchor, [])
            if exhibits:
                stale = any(exhibit.status == "stale" for exhibit in exhibits)
                marks = f'<span class="dot{" stale" if stale else ""}" title="{"Stale illustration" if stale else "Illustration"}"></span>'
            items.append(
                f'<li class="lvl{heading.level}"><a href="#{doc.id}__{esc(heading.anchor)}">'
                f"{esc(plain(heading.text))}{marks}</a></li>"
            )
        return f'<ol class="outline" data-doc="{doc.id}" hidden>{"".join(items)}</ol>'

    # ---- exhibits

    def refs(self, refs: Any) -> str:
        if not isinstance(refs, list) or not refs:
            return ""
        chips = []
        for ref in refs:
            ref = str(ref)
            if ref in self.index.defs:
                chips.append(self.id_anchor(ref))
                continue
            if ref.startswith("#") or re.match(r"^[\w./-]+\.md(#|$)", ref):
                href, _ = self.link_target(ref)
                path_part, _, anchor = ref.partition("#")
                doc = self.by_file.get(Path(path_part).name) if path_part else self.doc
                heading = doc.heading(anchor) if doc and anchor else None
                if heading:
                    label = "§ " + plain(heading.text)
                elif doc and not anchor:
                    label = doc.label
                else:
                    label = ref
                    self.lint["unresolved refs"].add(f"{self.doc.file}: {ref}")
                chips.append(f'<a href="{esc(href)}">{esc(label)}</a>')
                continue
            self.lint["unresolved refs"].add(f"{self.doc.file}: {ref}")
            chips.append(f"<span>{esc(ref)}</span>")
        return f'<span class="refs">{"".join(chips)}</span>'

    def source_label(self, exhibit: Exhibit) -> str:
        labels = []
        for source in exhibit_sources(exhibit):
            if source == "*":
                labels.append("whole doc")
                continue
            file, hash_sign, anchor = source.partition("#")
            if hash_sign or source.lower().endswith(".md"):
                target = self.by_file.get(Path(file).name) if file else exhibit.doc
                heading = target.heading(anchor) if target and anchor else None
                name = Path(file).name if file else (exhibit.doc.file if exhibit.doc else "")
                labels.append(name + (f" § {plain(heading.text)}" if heading else f"#{anchor}" if anchor else ""))
                continue
            heading = exhibit.doc.heading(source) if exhibit.doc else None
            labels.append("§ " + plain(heading.text) if heading else source)
        return ", ".join(labels)

    def exhibit(self, exhibit: Exhibit) -> str:
        data = exhibit.data
        kind = exhibit.kind
        try:
            body = getattr(self, f"exhibit_{kind}")(exhibit, data.get("data") or {})
        except (ViewError, KeyError, TypeError, ValueError) as exc:
            self.lint.setdefault("illustrations", set()).add(f"{exhibit.id}: {exc}")
            body = f'<p class="ex-error">This illustration could not be drawn: {esc(str(exc))}</p>'
        if exhibit.code and exhibit.code.get("path"):
            self.cite(exhibit.code["path"])
        stamp = data.get("stamp") or {}
        stamp_text = " · ".join(sorted({str(value)[:6] for key, value in stamp.items() if key != "code"})) if isinstance(stamp, dict) else ""
        status = ""
        if exhibit.status == "stale":
            status = f'<span class="chip warn">Stale: {esc("; ".join(exhibit.problems) or "a source changed")}</span>'
        title = f'<div class="ex-title">{self.inline(str(data["title"]))}</div>' if data.get("title") else ""
        caption = f'<p class="ex-caption">{self.inline(str(data["caption"]))}</p>' if data.get("caption") else ""
        return (
            f'<figure class="exhibit ex-{kind}{" is-stale" if exhibit.status == "stale" else ""}" data-exhibit="{esc(exhibit.id)}">'
            f'<div class="ex-head"><span class="tag">Illustration</span>'
            f'<span class="ex-meta">model-drawn · from {esc(self.source_label(exhibit))}{" · " + esc(stamp_text) if stamp_text else ""}</span>'
            f"{status}</div>{title}{body}{caption}</figure>"
        )

    def exhibit_claims(self, exhibit: Exhibit, data: dict[str, Any]) -> str:
        items = []
        for number, item in enumerate(data.get("items") or [], start=1):
            items.append(
                f'<li><span class="n">{number}</span><span class="t">{self.inline(str(item.get("text", "")))}</span>'
                f'{self.refs(item.get("refs"))}</li>'
            )
        return f'<ol class="claims">{"".join(items)}</ol>'

    def exhibit_flow(self, exhibit: Exhibit, data: dict[str, Any]) -> str:
        steps = []
        for step in data.get("steps") or []:
            kind = str(step.get("kind") or "step")
            detail = f'<span class="detail">{self.inline(str(step["detail"]))}</span>' if step.get("detail") else ""
            exit_html = (
                f'<div class="exit"><span class="exit-arrow" aria-hidden="true">↳</span>{self.inline(str(step["exit"]))}</div>'
                if step.get("exit") else ""
            )
            steps.append(
                f'<li class="step k-{esc(kind)}"><div class="box"><b>{self.inline(str(step.get("label", "")))}</b>'
                f'{detail}{self.refs(step.get("refs"))}</div>{exit_html}</li>'
            )
        return f'<ol class="flow">{"".join(steps)}</ol>'

    def exhibit_tree(self, exhibit: Exhibit, data: dict[str, Any]) -> str:
        def nodes(items: Any) -> str:
            if not isinstance(items, list) or not items:
                return ""
            parts = []
            for node in items:
                mark = str(node.get("mark") or "same")
                detail = f'<span class="detail">{self.inline(str(node["detail"]))}</span>' if node.get("detail") else ""
                parts.append(
                    f'<li><div class="node m-{esc(mark)}"><span class="mark-chip">{esc(mark)}</span>'
                    f'<b>{self.inline(str(node.get("label", "")))}</b>{detail}{self.refs(node.get("refs"))}</div>'
                    f'{nodes(node.get("children"))}</li>'
                )
            return f"<ul>{''.join(parts)}</ul>"

        return f'<div class="tree">{nodes(data.get("nodes"))}</div>'

    def exhibit_walk(self, exhibit: Exhibit, data: dict[str, Any]) -> str:
        steps = []
        for number, step in enumerate(data.get("steps") or [], start=1):
            wrong = bool(step.get("wrong"))
            when = esc(str(step.get("when") or number))
            steps.append(
                f'<li class="{"wrong" if wrong else ""}"><span class="when">{when}'
                f'{" · wrong outcome" if wrong else ""}</span><span>{self.inline(str(step.get("text", "")))}</span></li>'
            )
        outcome = f'<p class="walk-outcome">{self.inline(str(data["outcome"]))}</p>' if data.get("outcome") else ""
        return f'<ol class="walk">{"".join(steps)}</ol>{outcome}'

    def exhibit_timeline(self, exhibit: Exhibit, data: dict[str, Any]) -> str:
        points = []
        for point in data.get("points") or []:
            tone = re.sub(r"[^\w-]", "", str(point.get("tone") or ""))
            css = f' class="tone-{tone}"' if tone else ""
            detail = f'<span class="detail">{self.inline(str(point["detail"]))}</span>' if point.get("detail") else ""
            points.append(
                f'<li{css}><span class="t-dot" aria-hidden="true"></span>'
                f'<span class="when">{esc(str(point.get("at", "")))}</span><b>{self.inline(str(point.get("label", "")))}</b>'
                f'{detail}{self.refs(point.get("refs"))}</li>'
            )
        return f'<ol class="timeline">{"".join(points)}</ol>'

    def exhibit_decision(self, exhibit: Exhibit, data: dict[str, Any]) -> str:
        raise ViewError("a decision exhibit answers an item of the round's table, not a premise")

    def exhibit_decisions(self, exhibit: Exhibit, data: dict[str, Any]) -> str:
        fieldsets = []
        for number, item in enumerate(data.get("items") or [], start=1):
            item_id = str(item.get("id") or number)
            name = f"dec-{exhibit.id}-{item_id}"
            options = []
            for option in item.get("options") or []:
                suggested = bool(option.get("suggested"))
                note = f'<span class="note">{self.inline(str(option["note"]))}</span>' if option.get("note") else ""
                tag = '<span class="chip info">suggested</span>' if suggested else ""
                options.append(
                    f'<label class="opt"><input type="radio" name="{esc(name)}" value="{esc(str(option.get("value", "")))}"'
                    f'{" checked" if suggested else ""} data-label="{esc(plain(str(option.get("label", ""))))}"'
                    f'{" data-suggested" if suggested else ""}>'
                    f'<span><span class="opt-label">{self.inline(str(option.get("label", "")))}{tag}</span>{note}</span></label>'
                )
            confidence = f'<span class="muted">Recommendation confidence {esc(str(item["confidence"]))}%</span>' if item.get("confidence") else ""
            fieldsets.append(
                f'<fieldset class="decision" data-decision="{esc(name)}" data-item="{esc(item_id)}" '
                f'data-question="{esc(plain(str(item.get("question", ""))))}">'
                f'<legend>{esc(item_id)} · {self.inline(str(item.get("question", "")))}</legend>'
                f'{"".join(options)}<div class="decision-foot">{confidence}{self.refs(item.get("refs"))}</div></fieldset>'
            )
        return f'<div class="decisions">{"".join(fieldsets)}</div>'

    # ---- walkthrough rounds

    def round_panel(self, doc: Doc, current: Round) -> str:
        by_item: dict[str, list[Exhibit]] = {}
        for exhibit in self.exhibits:
            if exhibit.doc is doc and exhibit.item and exhibit.status not in {"invalid", "orphan"}:
                by_item.setdefault(exhibit.item, []).append(exhibit)
        premises = {premise.ident: premise for premise in current.premises}
        cards: list[str] = []
        tags: dict[str, int] = {}
        counts = {"open": 0, "decided": 0, "deferred": 0, "needs": 0}
        any_suggested = False
        for item in current.items:
            card, info = self.item_card(doc, item, by_item.get(item.ident, []), premises)
            cards.append(card)
            counts[item.status] += 1
            counts["needs"] += 1 if info["needs"] else 0
            any_suggested = any_suggested or info["suggested"]
            for tag in info["tags"]:
                tags[tag] = tags.get(tag, 0) + 1

        to_confirm = sum(1 for premise in current.premises if premise.status == "open")
        chips = [("", f"{len(current.items)} items")]
        if counts["needs"]:
            chips.append(("warn", f"{counts['needs']} need you"))
        chips += [("", f"{counts[key]} {key}") for key in ("open", "decided", "deferred") if counts[key]]
        if current.premises:
            chips.append(("", f"{len(current.premises)} premises" + (f", {to_confirm} to confirm" if to_confirm else "")))
        chip_html = "".join(f'<span class="chip {css}">{esc(text)}</span>' for css, text in chips)
        head = (
            f'<div class="round-head"><div class="kicker">Walkthrough · round {current.number} · {esc(current.date)}</div>'
            f'<div class="chips">{chip_html}</div></div>'
        )

        premise_html = ""
        if current.premises:
            section_id = f' id="{esc(doc.id)}__{esc(current.premise_anchor)}"' if current.premise_anchor else ""
            premise_html = (
                f'<section class="round-premises anchored"{section_id}><div class="round-label">Round 0 · Premises</div>'
                '<p class="muted">Confirm these first. Each decision links to the premises it uses.</p>'
                '<div class="premise-grid">'
                + "".join(self.premise_card(doc, premise, by_item.get(premise.ident, [])) for premise in current.premises)
                + "</div></section>"
            )

        filters = [("all", "All", len(current.items)), ("needs", "Need you", counts["needs"]),
                   ("open", "Open", counts["open"]), ("decided", "Decided", counts["decided"]),
                   ("deferred", "Deferred", counts["deferred"])]
        filters += [(f"tag:{tag}", tag.replace("-", " ").capitalize(), count) for tag, count in sorted(tags.items())]
        buttons = "".join(
            f'<button type="button" class="btn" data-filter="{esc(key)}" aria-pressed="{"true" if key == "all" else "false"}">'
            f'{esc(label)} <span class="n">{count}</span></button>'
            for key, label, count in filters if count or key == "all"
        )
        bulk = (
            '<div class="bulk-row"><button type="button" class="btn" data-action="bulk-accept" disabled>'
            'Accept suggested for <span data-bulk-count>0</span> shown</button></div>'
            if any_suggested else ""
        )
        items_html = (
            '<section class="round-items"><div class="round-label">Decisions</div>'
            f'<div class="filters" role="group" aria-label="Filter the items">{buttons}</div>{bulk}'
            f'<div class="cards">{"".join(cards)}</div>'
            '<button type="button" class="btn more" data-action="show-more" hidden>Show more</button></section>'
        )
        return (
            f'<div class="round" data-label="{esc(doc.title)}, round {current.number}">'
            f'<div class="round-main">{head}{premise_html}{items_html}</div>{self.round_side(doc, by_item)}</div>'
        )

    def round_side(self, doc: Doc, by_item: dict[str, list[Exhibit]]) -> str:
        used = [doc]
        for exhibits in by_item.values():
            for exhibit in exhibits:
                for source in exhibit_sources(exhibit):
                    file = source.partition("#")[0]
                    other = self.by_file.get(Path(file).name) if file.lower().endswith(".md") else None
                    if other and other not in used:
                        used.append(other)
        rows = [f"<dt>{esc(item.file)}</dt><dd>{esc(item.sha[:7])}</dd>" for item in used]
        for root in self.repo.roots:
            head = git_head(root)
            if head:
                rows.append(f"<dt>{esc(root.name)} (repo)</dt><dd>{esc(head[:7])}</dd>")
        return (
            '<aside class="round-side" aria-label="Respond to this round">'
            '<section class="panel"><h3>Respond</h3><p class="muted small">Your answers go back to the source as '
            'markdown. Paste them into the session; the walkthrough skill records them.</p>'
            '<pre class="live" data-live></pre>'
            '<div class="row-btns"><button type="button" class="btn" data-action="next-open"><span data-open-count>0</span> to answer</button>'
            '<button type="button" class="btn primary" data-action="copy-live">Copy response</button></div>'
            '<p class="muted small" data-copied-live hidden>Copied</p>'
            '<button type="button" class="linkish" data-action="clear-answers">Clear my answers</button></section>'
            f'<section class="panel"><h3>Built from</h3><dl class="built">{"".join(rows)}</dl>'
            '<p class="muted small">Rebuild after any source change; edits made on this page are lost on rebuild.</p></section>'
            "</aside>"
        )

    def premise_card(self, doc: Doc, premise: RoundItem, exhibits: list[Exhibit]) -> str:
        chip = {
            "open": '<span class="chip neutral">Not confirmed</span>',
            "confirmed": '<span class="chip ok">Confirmed</span>',
            "corrected": '<span class="chip warn">Corrected</span>',
        }[premise.status]
        title = f'<span class="p-title">{self.inline(premise.title)}</span>' if premise.title else ""
        drawn = "".join(self.exhibit(exhibit) for exhibit in exhibits)
        recorded = "".join(f'<div class="p-recorded">{self.blocks(blocks)}</div>' for blocks in premise.recorded)
        actions = ""
        if premise.status == "open":
            actions = (
                '<button type="button" class="btn" data-action="premise" data-value="correct" aria-pressed="false">Needs correction</button>'
                '<button type="button" class="btn" data-action="premise" data-value="confirm" aria-pressed="false">Confirm</button>'
            )
        name = plain(premise.title) or shorten(premise.text, 60)
        return (
            f'<article class="premise" id="{esc(item_element_id(doc, premise.ident))}" data-ckey="{esc(doc.id)}#item:{esc(premise.ident)}" '
            f'data-item="{esc(premise.ident)}" data-status="{premise.status}" data-ctitle="{esc(premise.ident)} · {esc(name)}">'
            f'<div class="p-head"><span class="pid">{esc(premise.ident)}</span>{title}{chip}</div>'
            f'<p class="p-text">{self.inline(premise.text)}</p>{drawn}{recorded}'
            '<div class="p-foot"><button type="button" class="tool" data-action="comment">Comment</button>'
            f'<div class="p-actions">{actions}</div></div><div class="comment-slot"></div></article>'
        )

    def item_card(self, doc: Doc, item: RoundItem, exhibits: list[Exhibit],
                  premises: dict[str, RoundItem]) -> tuple[str, dict[str, Any]]:
        decision = next((exhibit for exhibit in exhibits if exhibit.kind == "decision"), None)
        data = (decision.data.get("data") or {}) if decision else {}
        others = [exhibit for exhibit in exhibits if exhibit is not decision]
        is_open = item.status == "open"
        needs = bool(data.get("needs")) and is_open
        tags = [slug for slug in (re.sub(r"[^\w]+", "-", str(tag).lower()).strip("-") for tag in data.get("tags") or []) if slug]
        uses = [str(ident) for ident in data.get("uses") or []]
        options = [option for option in data.get("options") or [] if isinstance(option, dict)]
        suggested = next((option for option in options if option.get("suggested")), None)
        headline = plain(str(data["headline"])) if data.get("headline") else shorten(item.text)

        state = []
        if is_open:
            state.append('<span class="chip warn">Needs you</span>' if needs else '<span class="chip neutral">Open</span>')
            if suggested:
                state.append(f'<span class="c-suggest">Suggested: {esc(plain(str(suggested.get("label", ""))))}</span>')
        else:
            css = "info" if item.status == "deferred" else "ok"
            state.append(f'<span class="chip {css}">{esc(shorten(item.answer, 48))}</span>')
        state.append('<span class="chip info" data-answer-chip hidden></span>')
        tag_html = "".join(f'<span class="tag">{esc(tag.replace("-", " "))}</span>' for tag in tags)

        meta = [f"<span>Source {self.inline(item.source)}</span>"] if plain(item.source) else []
        if decision:
            stamp = decision.data.get("stamp") or {}
            stamp_text = " · ".join(sorted({str(value)[:6] for value in stamp.values()})) if isinstance(stamp, dict) else ""
            meta.append(f'<span class="muted">Headline, options and walk: model-drawn{" · " + esc(stamp_text) if stamp_text else ""}</span>')
            if decision.status == "stale":
                meta.append(f'<span class="chip warn">Stale: {esc("; ".join(decision.problems) or "the row changed")}</span>')
        fields = "".join(
            f'<div class="c-field"><div class="label">{self.inline(name)}</div><div>{self.inline(cell)}</div></div>'
            for name, cell in item.fields
        )
        uses_html = ""
        if uses:
            links = []
            for ident in uses:
                premise = premises.get(ident)
                if premise:
                    name = plain(premise.title) or shorten(premise.text, 40)
                    links.append(f'<a href="#{esc(item_element_id(doc, ident))}">{esc(ident)} · {esc(name)}</a>')
                else:
                    self.lint["unresolved refs"].add(f"{doc.file}: {item.ident} uses {ident}, not a premise of this round")
                    links.append(f"<span>{esc(ident)}</span>")
            uses_html = (
                f'<div class="c-uses"><span class="muted">Uses</span><span class="refs">{"".join(links)}</span>'
                '<span class="chip warn" data-premise-flag hidden>Rests on a premise marked for correction</span></div>'
            )
        walk_html = ""
        if decision and isinstance(data.get("walk"), dict):
            walk_html = (
                f'<div class="c-block"><div class="label">Failure walk · illustration</div>'
                f'{self.exhibit_walk(decision, data["walk"])}</div>'
            )
        drawn = "".join(self.exhibit(exhibit) for exhibit in others)
        recorded = ""
        if not is_open or item.recorded:
            answer = f'<p class="c-answer-cell">{self.inline(item.answer)}</p>' if plain(item.answer) else ""
            entries = "".join(f'<div class="c-entry">{self.blocks(blocks)}</div>' for blocks in item.recorded)
            recorded = f'<div class="c-recorded"><div class="label">Recorded</div>{answer}{entries}</div>'
        form = ""
        if is_open and options:
            name = f"rd-{doc.id}-{slugify(item.ident)}"
            choices = []
            for option in options:
                is_suggested = bool(option.get("suggested"))
                note = f'<span class="note">{self.inline(str(option["note"]))}</span>' if option.get("note") else ""
                marker = '<span class="chip info">suggested</span>' if is_suggested else ""
                choices.append(
                    f'<label class="opt"><input type="radio" name="{esc(name)}" value="{esc(str(option.get("value", "")))}" '
                    f'data-label="{esc(plain(str(option.get("label", ""))))}"{" data-suggested" if is_suggested else ""}>'
                    f'<span><span class="opt-label">{self.inline(str(option.get("label", "")))}{marker}</span>{note}</span></label>'
                )
            confidence = (
                f'<span class="muted">Recommendation confidence {esc(str(data["confidence"]))}%</span>'
                if data.get("confidence") else ""
            )
            form = (
                f'<fieldset class="rdecision"><legend class="label">Your decision</legend>{"".join(choices)}'
                f'<div class="decision-foot">{confidence}</div></fieldset>'
            )
        elif is_open:
            form = '<p class="muted small">No options are drawn for this item yet. Answer it with a comment.</p>'
        card = (
            f'<details class="card" id="{esc(item_element_id(doc, item.ident))}" data-ckey="{esc(doc.id)}#item:{esc(item.ident)}" '
            f'data-item="{esc(item.ident)}" data-status="{item.status}" data-needs="{"1" if needs else ""}" '
            f'data-tags="{esc(" ".join(tags))}" data-uses="{esc(" ".join(uses))}" '
            f'data-ctitle="{esc(item.ident)} · {esc(shorten(headline, 90))}" data-recorded="{esc(shorten(item.answer, 80))}"'
            f'{" open" if needs else ""}>'
            f'<summary><span class="cid">{esc(item.ident)}</span><span class="c-headline">{esc(headline)}</span>'
            f'<span class="c-state">{tag_html}{"".join(state)}</span></summary>'
            f'<div class="c-body"><div class="c-meta">{"".join(meta)}</div>{fields}{uses_html}{walk_html}{drawn}{recorded}{form}'
            f'<div class="c-foot"><button type="button" class="tool" data-action="comment">Comment on {esc(item.ident)}</button></div>'
            '<div class="comment-slot"></div></div></details>'
        )
        return card, {"needs": needs, "tags": tags, "suggested": bool(suggested) and is_open}

    # ---- implementation tours

    def coverage(self, doc: Doc, tour: Tour) -> str:
        """Every changed file of the change set, by repository and folder, with the steps that cite it."""
        order = {ident: index for index, (ident, _, _) in enumerate(tour.steps)}
        anchors = {ident: anchor for ident, anchor, _ in tour.steps}
        statuses = {"A": ("A", "added"), "M": ("M", "modified"), "D": ("D", "deleted"),
                    "T": ("T", "type changed"), "new": ("N", "new, untracked")}
        totals = {"repos": 0, "files": 0, "added": 0, "deleted": 0, "cited": 0}
        repos = []
        for row in tour.rows:
            if row.problem or row.top is None:
                repos.append(f'<p class="ex-error">{esc(row.name)}: {esc(row.problem or "not loaded")}</p>')
                continue
            totals["repos"] += 1
            folders: dict[str, list[str]] = {}
            folder_stats: dict[str, list[int]] = {}
            for changed in row.files:
                absolute = row.top / changed.path
                steps = sorted(self.cites.get(os.path.normcase(os.path.abspath(absolute)), set()),
                               key=lambda ident: order.get(ident, len(order)))
                folder, _, name = changed.path.rpartition("/")
                folder = folder or "."
                short, label = statuses.get(changed.status, (changed.status, changed.status))
                inner = f"<code>{esc(name)}</code>"
                link = self.editor_link(absolute, 1, inner) if changed.status != "D" and absolute.is_file() else inner
                step_links = "".join(f'<a href="#{esc(doc.id)}__{esc(anchors[ident])}">{esc(ident)}</a>' for ident in steps)
                folders.setdefault(folder, []).append(
                    f'<tr data-cited="{"1" if steps else ""}"><td><span class="st st-{esc(short)}" title="{esc(label)}">{esc(short)}</span></td>'
                    f'<td>{link}</td><td class="num add">+{changed.added}</td><td class="num del">−{changed.deleted}</td>'
                    f'<td><span class="refs">{step_links}</span></td></tr>'
                )
                stats = folder_stats.setdefault(folder, [0, 0, 0, 0])
                stats[0] += 1
                stats[1] += changed.added
                stats[2] += changed.deleted
                stats[3] += 0 if steps else 1
                totals["cited"] += 1 if steps else 0
            files = sum(stats[0] for stats in folder_stats.values())
            added = sum(stats[1] for stats in folder_stats.values())
            deleted = sum(stats[2] for stats in folder_stats.values())
            totals["files"] += files
            totals["added"] += added
            totals["deleted"] += deleted
            groups = "".join(
                f'<details class="cov-dir" data-uncited="{stats[3]}"><summary><code>{esc(folder)}/</code>'
                f'<span class="muted">{stats[0]} files · +{stats[1]} −{stats[2]}'
                f'{f" · {stats[3]} not in a step" if stats[3] else ""}</span></summary>'
                f'<div class="tbl"><table class="cov"><tbody>{"".join(folders[folder])}</tbody></table></div></details>'
                for folder, stats in sorted(folder_stats.items())
            )
            head = row.head if not row.working else WORKING_TREE
            repos.append(
                f'<div class="cov-repo"><div class="cov-head"><b>{esc(row.prefix or row.top.name)}</b> <code>{esc(row.top.name)}</code>'
                f'<span class="muted">{esc(row.base)} → {esc(head)} · merge base {esc(row.merge_base[:7])} · '
                f'{files} files · +{added} −{deleted}</span></div>{groups}</div>'
            )
        self.tour_stats[doc.id] = totals
        uncited = totals["files"] - totals["cited"]
        filters = (
            f'<button type="button" class="btn" data-cov-filter="all" aria-pressed="true">All files <span class="n">{totals["files"]}</span></button>'
            f'<button type="button" class="btn" data-cov-filter="uncited" aria-pressed="false">Not in any step <span class="n">{uncited}</span></button>'
        )
        return (
            '<div class="coverage" data-coverage><div class="label">Every changed file, from git</div>'
            f'<div class="filters">{filters}</div>{"".join(repos)}</div>'
        )

    # ---- code exhibits

    def exhibit_code(self, exhibit: Exhibit, data: dict[str, Any]) -> str:
        code = exhibit.code
        if not code:
            raise ViewError("the code could not be read (check --repo and the path)")
        pins: dict[int, list[str]] = {}
        for pin in data.get("pins") or []:
            line = int(pin.get("line", 0))
            tone = str(pin.get("tone") or "info")
            title = f"<b>{esc(str(pin['title']))}</b>" if pin.get("title") else ""
            text = self.inline(str(pin.get("text", "")))
            pins.setdefault(line, []).append(f'<span class="pin tone-{esc(tone)}">{title}{text}</span>')
        where = self.editor_link(code["path"], code["start"], f"<code>{esc(code['reference'])}</code>")
        caption = f'<span class="cap">{where} · lines {code["start"]}–{code["end"]} · {esc(code["at"])}</span>'
        return self.code_figure(
            highlight_lines(code["text"], code["lang"]), caption,
            start=code["start"], highlight=parse_line_set(data.get("highlight")), pins=pins,
        )

    def exhibit_diff(self, exhibit: Exhibit, data: dict[str, Any]) -> str:
        code = exhibit.code
        if not code:
            raise ViewError("the diff could not be read (check --repo, the path and the refs)")
        if code["mode"] == "text":
            label = esc(str(data.get("label") or "proposed change"))
            return self.diff_figure(text_diff_rows(code["before"], code["after"], code["lang"]), label)
        rows = git_diff_rows(code["diff"], code["lang"], code["window"])
        if not rows:
            raise ViewError("no diff lines fall inside data.lines")
        where = self.editor_link(code["path"], 1, f"<code>{esc(code['reference'])}</code>")
        return self.diff_figure(rows, f"{where} · {esc(code['base'])} → {esc(code['head'])}")

    # ---- diagrams

    @staticmethod
    def text_list(items: list[str]) -> str:
        if not items:
            return ""
        listed = "".join(f"<li>{item}</li>" for item in items)
        return f'<details class="dg-text"><summary>As text</summary><ul>{listed}</ul></details>'

    def exhibit_states(self, exhibit: Exhibit, data: dict[str, Any]) -> str:
        uid = "dg-" + re.sub(r"[^\w-]", "-", exhibit.id)
        states = [state for state in data.get("states") or [] if state.get("id")]
        ids = [str(state["id"]) for state in states]
        labels = {str(state["id"]): str(state.get("label") or state["id"]) for state in states}
        positions, rows, cols = grid_positions(ids, data.get("grid"))
        node_w = max((text_width(labels[ident], 14) for ident in ids), default=60) + 40
        node_h, gap_x, gap_y, left, top = 40, 128, 78, 78, 24
        width = left + cols * node_w + (cols - 1) * gap_x + 30
        height = top + rows * node_h + (rows - 1) * gap_y + 24
        centers = {
            ident: (left + col * (node_w + gap_x) + node_w / 2, top + row * (node_h + gap_y) + node_h / 2)
            for ident, (row, col) in positions.items()
        }
        transitions = [t for t in data.get("transitions") or [] if str(t.get("from")) in centers and str(t.get("to")) in centers]
        pairs = {(str(t["from"]), str(t["to"])) for t in transitions}
        edges, edge_labels, text_items = [], [], []
        for transition in transitions:
            source, target = str(transition["from"]), str(transition["to"])
            label = str(transition.get("label") or transition.get("event") or "")
            text_items.append(f"<b>{esc(source)}</b> → <b>{esc(target)}</b>{': ' + esc(label) if label else ''}")
            if source == target:
                continue
            (ax, ay), (bx, by) = centers[source], centers[target]
            dx, dy = bx - ax, by - ay
            length = math.hypot(dx, dy) or 1.0
            nx, ny = -dy / length, dx / length
            offset = 7.0 if (target, source) in pairs else 0.0
            sx, sy = border_point(ax + nx * offset, ay + ny * offset, node_w / 2, node_h / 2, dx, dy)
            ex, ey = border_point(bx + nx * offset, by + ny * offset, node_w / 2, node_h / 2, -dx, -dy)
            edges.append(
                f'<g class="edge" data-from="{esc(source)}" data-to="{esc(target)}">'
                f'<path d="M{sx:.1f} {sy:.1f} L{ex:.1f} {ey:.1f}" marker-end="url(#{uid}-head)"/></g>'
            )
            if label:
                mid_x, mid_y = (sx + ex) / 2, (sy + ey) / 2
                if abs(dy) > abs(dx):
                    side = 1 if nx > 0 or (nx == 0 and offset == 0) else -1
                    anchor = "start" if side > 0 else "end"
                    label_x, label_y = mid_x + side * 10, mid_y
                else:
                    anchor, label_x, label_y = "middle", mid_x + nx * 13, mid_y + ny * 13
                edge_labels.append(label_box(label_x, label_y, label, anchor=anchor))
                width = max(width, label_right(label_x, label, anchor) + 12)
        nodes = []
        for state in states:
            ident = str(state["id"])
            cx, cy = centers[ident]
            x, y = cx - node_w / 2, cy - node_h / 2
            inner = (
                f'<rect class="inner" x="{x + 4:.1f}" y="{y + 4:.1f}" width="{node_w - 8:.1f}" height="{node_h - 8:.1f}" rx="7"/>'
                if state.get("final") else ""
            )
            nodes.append(
                f'<g class="node{" final" if state.get("final") else ""}" data-node="{esc(ident)}" tabindex="0">'
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{node_w:.1f}" height="{node_h:.1f}" rx="10"/>{inner}'
                f'<text class="sname" x="{cx:.1f}" y="{cy + 5:.1f}" text-anchor="middle">{esc(labels[ident])}</text></g>'
            )
        start = str(data.get("initial") or (ids[0] if ids else ""))
        initial = ""
        if start in centers:
            ix, iy = centers[start]
            edge_x = ix - node_w / 2
            initial = (
                f'<circle class="init" cx="{edge_x - 42:.1f}" cy="{iy:.1f}" r="6"/>'
                f'<g class="edge"><path d="M{edge_x - 34:.1f} {iy:.1f} L{edge_x - 2:.1f} {iy:.1f}" marker-end="url(#{uid}-head)"/></g>'
            )
        svg = (
            svg_open("states", uid, width, height, f"State diagram: {', '.join(labels[i] for i in ids)}")
            + "".join(edges) + initial + "".join(nodes) + "".join(edge_labels) + "</svg></div>"
        )
        details = "".join(
            f"<dt>{esc(labels[str(state['id'])])}</dt><dd>{self.inline(str(state['detail']))}</dd>"
            for state in states if state.get("detail")
        )
        notes = f'<dl class="dg-notes">{details}</dl>' if details else ""
        return svg + notes + self.text_list(text_items)

    def exhibit_graph(self, exhibit: Exhibit, data: dict[str, Any]) -> str:
        uid = "dg-" + re.sub(r"[^\w-]", "-", exhibit.id)
        nodes = [node for node in data.get("nodes") or [] if node.get("id")]
        ids = [str(node["id"]) for node in nodes]
        info = {str(node["id"]): node for node in nodes}
        positions, rows, cols = grid_positions(ids, data.get("grid"))
        has_sub = any(node.get("sub") for node in nodes)
        node_h = 50 if has_sub else 34
        col_w = [120.0] * cols
        for ident, (_, col) in positions.items():
            node = info[ident]
            need = max(text_width(str(node.get("label") or ident), 13.5) * 1.08, text_width(str(node.get("sub") or ""), 12)) + 30
            col_w[col] = max(col_w[col], need)
        gap_x, gap_y, pad = 52, 58, 18
        col_left = []
        cursor = float(pad)
        for column_width in col_w:
            col_left.append(cursor)
            cursor += column_width + gap_x
        width = cursor - gap_x + pad
        height = pad * 2 + rows * node_h + (rows - 1) * gap_y
        centers = {ident: (col_left[col] + col_w[col] / 2, pad + row * (node_h + gap_y) + node_h / 2)
                   for ident, (row, col) in positions.items()}
        edges, edge_labels, text_items = [], [], []
        for edge in data.get("edges") or []:
            source, target = str(edge.get("from")), str(edge.get("to"))
            if source not in centers or target not in centers or source == target:
                continue
            label = str(edge.get("label") or "")
            text_items.append(f"<b>{esc(source)}</b> → <b>{esc(target)}</b>{': ' + esc(label) if label else ''}")
            (ax, ay), (bx, by) = centers[source], centers[target]
            (row_a, col_a), (row_b, col_b) = positions[source], positions[target]
            if row_b > row_a:
                sy, ey = ay + node_h / 2, by - node_h / 2
                mid = sy + gap_y / 2
                if abs(ax - bx) > 0.5:
                    path = f"M{ax:.1f} {sy:.1f} L{ax:.1f} {mid:.1f} L{bx:.1f} {mid:.1f} L{bx:.1f} {ey - 1:.1f}"
                else:
                    path = f"M{ax:.1f} {sy:.1f} L{bx:.1f} {ey - 1:.1f}"
                label_at = (bx + 8, (mid + ey) / 2 + 4, "start")
            else:
                sx, sy = border_point(ax, ay, col_w[col_a] / 2, node_h / 2, bx - ax, by - ay)
                ex, ey = border_point(bx, by, col_w[col_b] / 2, node_h / 2, ax - bx, ay - by)
                path = f"M{sx:.1f} {sy:.1f} L{ex:.1f} {ey:.1f}"
                label_at = ((sx + ex) / 2, (sy + ey) / 2 - 10, "middle")
            dashed = " dashed" if edge.get("dashed") else ""
            edges.append(
                f'<g class="edge{dashed}" data-from="{esc(source)}" data-to="{esc(target)}">'
                f'<path d="{path}" marker-end="url(#{uid}-head)"/></g>'
            )
            if label:
                edge_labels.append(label_box(label_at[0], label_at[1], label, anchor=label_at[2]))
                width = max(width, label_right(label_at[0], label, label_at[2]) + 12)
        boxes, marks_used = [], []
        for ident in ids:
            node = info[ident]
            row, col = positions[ident]
            cx, cy = centers[ident]
            mark = str(node.get("mark") or "same")
            if mark not in marks_used:
                marks_used.append(mark)
            label = esc(str(node.get("label") or ident))
            sub = str(node.get("sub") or "")
            if sub:
                text = (f'<text class="nlabel" x="{cx:.1f}" y="{cy - 3:.1f}" text-anchor="middle">{label}</text>'
                        f'<text class="sub" x="{cx:.1f}" y="{cy + 14:.1f}" text-anchor="middle">{esc(sub)}</text>')
            else:
                text = f'<text class="nlabel" x="{cx:.1f}" y="{cy + 5:.1f}" text-anchor="middle">{label}</text>'
            boxes.append(
                f'<g class="node m-{esc(mark)}" data-node="{esc(ident)}" tabindex="0">'
                f'<rect x="{col_left[col]:.1f}" y="{cy - node_h / 2:.1f}" width="{col_w[col]:.1f}" height="{node_h}" rx="8"/>{text}</g>'
            )
        legend = "".join(f'<span class="lg m-{esc(mark)}"><i></i>{esc(mark)}</span>' for mark in marks_used if mark != "same")
        svg = (
            svg_open("graph", uid, width, height, "Diagram: " + ", ".join(str(info[i].get("label") or i) for i in ids))
            + "".join(edges) + "".join(boxes) + "".join(edge_labels) + "</svg></div>"
        )
        return svg + (f'<div class="dg-legend">{legend}</div>' if legend else "") + self.text_list(text_items)

    def exhibit_sequence(self, exhibit: Exhibit, data: dict[str, Any]) -> str:
        uid = "dg-" + re.sub(r"[^\w-]", "-", exhibit.id)
        parts = [part for part in data.get("participants") or [] if part.get("id")]
        ids = [str(part["id"]) for part in parts]
        labels = {str(part["id"]): str(part.get("label") or part["id"]) for part in parts}
        lane_w = max([150.0] + [text_width(labels[i], 13.5) + 40 for i in ids])
        pad = 14
        xs = {ident: pad + index * lane_w + lane_w / 2 for index, ident in enumerate(ids)}
        steps = data.get("steps") or []
        fail_w = max([text_width("↳ " + str(step["fail"]), 12.5) for step in steps if step.get("fail")] or [0])
        lanes_right = pad + len(ids) * lane_w
        width = lanes_right + (fail_w + 18 if fail_w else 0) + pad
        y = 68.0
        body, text_items = [], []
        for step in steps:
            fail = str(step.get("fail") or "")
            fail_svg = f'<text class="fail" x="{lanes_right + 10:.1f}" y="{y + 4:.1f}">↳ {esc(fail)}</text>' if fail else ""
            if step.get("divider") is not None:
                text = str(step["divider"])
                body.append(f'<g class="divider"><line x1="{pad}" y1="{y:.1f}" x2="{lanes_right:.1f}" y2="{y:.1f}"/></g>'
                            + label_box((pad + lanes_right) / 2, y, text, css="dlabel"))
                text_items.append(f"<i>{esc(text)}</i>")
                y += 32
                continue
            if step.get("note") is not None:
                text = str(step["note"])
                over = [str(item) for item in step.get("over") or [] if str(item) in xs] or ids[:1]
                left, right = min(xs[item] for item in over), max(xs[item] for item in over)
                box_w = max(text_width(text, 12.5) + 24, right - left + 80)
                cx = (left + right) / 2
                body.append(
                    f'<g class="note"><rect x="{cx - box_w / 2:.1f}" y="{y - 13:.1f}" width="{box_w:.1f}" height="26" rx="6"/>'
                    f'<text x="{cx:.1f}" y="{y + 4:.1f}" text-anchor="middle">{esc(text)}</text></g>' + fail_svg
                )
                text_items.append(f"note: {esc(text)}" + (f" — {esc(fail)}" if fail else ""))
                y += 38
                continue
            source, target = str(step.get("from")), str(step.get("to"))
            if source not in xs or target not in xs:
                continue
            text = str(step.get("text") or "")
            kind = str(step.get("kind") or "call")
            mark = str(step.get("mark") or "")
            css = "msg" + (f" {kind}" if kind != "call" else "") + (f" m-{mark}" if mark else "")
            head = {"new": "-new", "removed": "-del"}.get(mark, "")
            x1, x2 = xs[source], xs[target]
            if source == target:
                shape = (f'<path d="M{x1:.1f} {y - 6:.1f} h30 v16 h-28" marker-end="url(#{uid}-head{head})"/>'
                         f'<text x="{x1 + 36:.1f}" y="{y + 1:.1f}">{esc(text)}</text>')
                y_step = 50
            else:
                direction = 1 if x2 > x1 else -1
                if kind == "lost":
                    xe = x1 + (x2 - x1) * 0.82
                    shape = (f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{xe:.1f}" y2="{y:.1f}"/>'
                             f'<path class="x" d="M{xe - 6:.1f} {y - 6:.1f} l12 12 M{xe + 6:.1f} {y - 6:.1f} l-12 12"/>')
                else:
                    shape = (f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2 - direction * 2:.1f}" y2="{y:.1f}" '
                             f'marker-end="url(#{uid}-head{head})"/>')
                shape += f'<text x="{(x1 + x2) / 2:.1f}" y="{y - 7:.1f}" text-anchor="middle">{esc(text)}</text>'
                y_step = 42
            body.append(f'<g class="{css}">{shape}</g>' + fail_svg)
            arrow = {"reply": "⇠", "lost": "✕"}.get(kind, "→")
            text_items.append(f"{esc(labels[source])} {arrow} {esc(labels[target])}: {esc(text)}"
                              + (f" ({esc(mark)})" if mark else "") + (f" — {esc(fail)}" if fail else ""))
            y += y_step
        height = y + 6
        heads = "".join(
            f'<line class="life" x1="{xs[i]:.1f}" y1="34" x2="{xs[i]:.1f}" y2="{height - 4:.1f}"/>'
            f'<g class="actor"><rect x="{xs[i] - (lane_w - 26) / 2:.1f}" y="4" width="{lane_w - 26:.1f}" height="30" rx="8"/>'
            f'<text x="{xs[i]:.1f}" y="24" text-anchor="middle">{esc(labels[i])}</text></g>'
            for i in ids
        )
        svg = (svg_open("sequence", uid, width, height, "Sequence: " + ", ".join(labels[i] for i in ids))
               + heads + "".join(body) + "</svg></div>")
        return svg + self.text_list(text_items)


# ---------------------------------------------------------------- page


def git_head(path: Path) -> str:
    top = git_top(path)
    if top is None or not (top / ".git").is_dir():
        return ""
    head = top / ".git"
    try:
        ref = (head / "HEAD").read_text(encoding="utf-8").strip()
        if ref.startswith("ref: "):
            ref_path = head / ref[5:]
            return ref_path.read_text(encoding="utf-8").strip()[:9] if ref_path.is_file() else ""
        return ref[:9]
    except OSError:
        return ""


def build_page(spec_dir: Path, docs: list[Doc], exhibits: list[Exhibit], repo: Repo) -> tuple[str, Renderer]:
    renderer = Renderer(spec_dir, docs, exhibits, repo)
    articles = []
    outlines = []
    for doc in docs:
        article, outline = renderer.render_doc(doc)
        articles.append(article)
        outlines.append(outline)

    primary = main_doc(docs)
    built_at = dt.datetime.now().astimezone().replace(microsecond=0)
    nav_docs = []
    task_items = []
    for doc in docs:
        button = (
            f'<li><a class="doclink" href="#{doc.id}" data-doc="{doc.id}">'
            f'<span>{esc(doc.label)}</span><span class="muted">{esc(doc.file)}</span></a></li>'
        )
        (task_items if doc.file.startswith("task_") else nav_docs).append(button)
    if task_items:
        nav_docs.append(
            f'<li class="group"><details><summary>Task files <span class="muted">{len(task_items)}</span></summary>'
            f'<ul>{"".join(task_items)}</ul></details></li>'
        )

    report = []
    for kind, entries in renderer.lint.items():
        if entries:
            listed = "".join(f"<li>{esc(entry)}</li>" for entry in sorted(entries)[:60])
            more = f"<li>… {len(entries) - 60} more</li>" if len(entries) > 60 else ""
            report.append(f"<h3>{esc(kind.capitalize())} · {len(entries)}</h3><ul>{listed}{more}</ul>")
    exhibit_problems = [
        f"<li>{esc(exhibit.id)} ({esc(exhibit.status)}): {esc('; '.join(exhibit.problems))}</li>"
        for exhibit in exhibits if exhibit.problems
    ]
    if exhibit_problems:
        report.append(f"<h3>Illustrations · {len(exhibit_problems)}</h3><ul>{''.join(exhibit_problems)}</ul>")
    notes = sum(len(v) for v in renderer.lint.values()) + len(exhibit_problems)
    report_html = (
        f'<details class="report"><summary>Build report · {notes} notes</summary>{"".join(report)}</details>'
        if report else '<p class="muted small">Build report: no unresolved links, paths or refs.</p>'
    )

    manifest = {
        "version": MANIFEST_VERSION,
        "spec": spec_dir.name,
        "specDir": spec_dir.resolve().as_posix(),
        "viewKey": "render-view:" + short_hash(spec_dir.resolve().as_posix()),
        "builtAt": built_at.isoformat(),
        "git": git_head(spec_dir),
        "mainDoc": primary.id,
        "docs": [{"id": doc.id, "file": doc.file, "sha": doc.sha, "title": doc.title} for doc in docs],
        "exhibits": [
            {"id": exhibit.id, "doc": exhibit.doc.file if exhibit.doc else None, "anchor": exhibit.anchor,
             "status": exhibit.status, "stamp": exhibit.data.get("stamp")}
            for exhibit in exhibits
        ],
        "defs": renderer.index.defs,
        "tours": tour_fingerprints(docs),
    }
    manifest_json = json.dumps(manifest, ensure_ascii=False).replace("</", "<\\/")
    title = f"{spec_dir.name} · {primary.label} view"
    built_text = built_at.strftime("%Y-%m-%d %H:%M")
    git_text = f" · vault at {esc(manifest['git'])}" if manifest["git"] else ""
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="generator" content="ai-kit render-view">
<title>{esc(title)}</title>
<style>{read_asset("view.css")}</style>
</head>
<body>
<header class="topbar">
  <span class="badge">GENERATED VIEW · DO NOT EDIT</span>
  <span class="build">Built {esc(built_text)} from <b>{esc(spec_dir.name)}/</b> · {len(docs)} docs{git_text}</span>
  <span class="spacer"></span>
  <button type="button" class="btn" data-action="collapse-all">Collapse all</button>
  <button type="button" class="btn primary" data-action="respond">Respond <span class="count" data-count>0</span></button>
</header>
<div class="layout">
  <nav class="side" aria-label="Documents">
    <div class="panel"><div class="label">Documents</div><ul class="docs">{"".join(nav_docs)}</ul></div>
    <div class="panel outline-panel"><div class="label">Outline</div>{"".join(outlines)}</div>
    <div class="panel small">{report_html}<p class="muted">Rebuild after any source change; edits to this page are lost. Check freshness with <code>render_view.py check</code>.</p></div>
  </nav>
  <main id="main">{"".join(articles)}</main>
</div>
<div class="respond" id="respond" role="dialog" aria-modal="false" aria-labelledby="respond-title" hidden>
  <div class="respond-head"><h2 id="respond-title">Respond</h2><button type="button" class="btn" data-action="close-respond">Close</button></div>
  <p class="muted">Your decisions and comments, as markdown for the session. The owning skill writes them into the source docs; this page keeps nothing.</p>
  <textarea id="respond-text" readonly rows="16" aria-label="Response markdown"></textarea>
  <div class="respond-actions"><button type="button" class="btn primary" data-action="copy">Copy response</button><span class="muted" data-copied hidden>Copied</span></div>
</div>
<div class="popover" id="popover" role="tooltip" hidden></div>
<script type="application/json" id="view-manifest">{manifest_json}</script>
<script>{read_asset("view.js")}</script>
</body>
</html>
"""
    return page, renderer


# ---------------------------------------------------------------- commands


def repo_for(spec_dir: Path, docs: list[Doc], repo_args: list[str] | None, *, persist: bool) -> Repo:
    config = load_config(spec_dir)
    if repo_args:
        roots = [str(Path(root).expanduser().resolve()) for root in repo_args]
        if persist and roots != config.get("repo"):
            config["repo"] = roots
            save_config(spec_dir, config)
    else:
        roots = config.get("repo") or []
    missing = [root for root in roots if not Path(root).is_dir()]
    if missing:
        print(f"warning: repo roots not found: {', '.join(missing)}", file=sys.stderr)
    paths = [Path(root) for root in roots]
    aliases = collect_aliases(docs)
    # A tour's change set names its repositories, so they need no --repo.
    rows = [row for doc in docs if doc.tour for row in doc.tour.rows]
    seen: dict[str, str] = {}
    for row in rows:
        load_change(row, seen)
        if row.path.is_dir() and all(os.path.normcase(str(row.path)) != os.path.normcase(str(path)) for path in paths):
            paths.append(row.path)
        if row.prefix:
            aliases.append((row.prefix, row.path.as_posix().rstrip("/") + "/"))
    repo = Repo(paths, aliases)
    repo.change_rows = [row for row in rows if row.top]
    return repo


def load_view(target: str, repo_args: list[str] | None = None, *, persist: bool = False,
              stamp_new: bool = False) -> tuple[Path, list[Doc], Repo, list[Exhibit]]:
    spec_dir, focus = resolve_target(target)
    docs = discover_docs(spec_dir, focus)
    repo = repo_for(spec_dir, docs, repo_args, persist=persist)
    exhibits = load_exhibits(spec_dir, docs)
    by_file = {doc.file: doc for doc in docs}
    for exhibit in exhibits:
        evaluate_exhibit(exhibit, repo, by_file, stamp_new=stamp_new)
    return spec_dir, docs, repo, exhibits


def describe_exhibits(exhibits: list[Exhibit]) -> None:
    print(f"\nExhibits ({VIEW_DIR}/exhibits):")
    if not exhibits:
        print("  none")
    for exhibit in exhibits:
        file = exhibit.doc.file if exhibit.doc else exhibit.data.get("doc")
        location = f"{file} item {exhibit.item}" if exhibit.item else f"{file}#{exhibit.anchor}"
        problems = f"  ({'; '.join(exhibit.problems)})" if exhibit.problems else ""
        print(f"  {exhibit.id:<28} {exhibit.kind:<9} {location:<44} {exhibit.status}{problems}")


def describe_round(doc: Doc) -> None:
    current = doc.round
    assert current is not None
    counts: dict[str, int] = {}
    for item in current.items:
        counts[item.status] = counts.get(item.status, 0) + 1
    summary = ", ".join(f"{count} {status}" for status, count in sorted(counts.items()))
    print(f"\nRound {current.number} ({current.date}) of {doc.file}: {len(current.items)} items ({summary}), "
          f"{len(current.premises)} premises  (id, kind, status, hash, text; exhibits attach with \"item\")")
    for item in current.premises + current.items:
        text = f"{plain(item.title)}: {item.text}" if item.title else item.text
        print(f"  {item.ident:<7} {item.kind:<8} {item.status:<9} {item.hash}  {shorten(text, 90)}")


def describe_tour(doc: Doc, show_files: bool) -> None:
    tour = doc.tour
    assert tour is not None
    print(f"\nTour {doc.file}: {len(tour.steps)} steps  (exhibits anchor to a step heading)")
    for ident, anchor, title in tour.steps:
        print(f"  {ident:<4} {anchor:<56} {shorten(title, 60)}")
    for row in tour.rows:
        if row.problem or row.top is None:
            print(f"\n  {row.name}: {row.problem}")
            continue
        head = WORKING_TREE if row.working else row.head
        print(f"\n  {row.name} {row.top.as_posix()}  {row.base} → {head}, merge base {row.merge_base[:9]}: "
              f"{len(row.files)} files, +{sum(f.added for f in row.files)} −{sum(f.deleted for f in row.files)}")
        folders: dict[str, list[int]] = {}
        for changed in row.files:
            stats = folders.setdefault(changed.path.rpartition("/")[0] or ".", [0, 0, 0])
            stats[0] += 1
            stats[1] += changed.added
            stats[2] += changed.deleted
        for folder, (count, added, deleted) in sorted(folders.items()):
            print(f"    {folder + '/':<70} {count:>4} files  +{added} −{deleted}")
            if show_files:
                for changed in row.files:
                    if (changed.path.rpartition("/")[0] or ".") == folder:
                        print(f"      {changed.status:<4} {changed.path.rpartition('/')[2]:<60} +{changed.added} −{changed.deleted}")


def tour_fingerprints(docs: list[Doc]) -> dict[str, dict[str, str]]:
    return {
        doc.file: {row.name: row.fingerprint for row in doc.tour.rows if row.fingerprint}
        for doc in docs if doc.tour
    }


def command_plan(args: argparse.Namespace) -> int:
    spec_dir, docs, repo, exhibits = load_view(args.spec)
    primary = main_doc(docs)
    print(f"Spec: {spec_dir.as_posix()}  (main doc: {primary.file})")
    print("Repo roots: " + (", ".join(root.as_posix() for root in repo.roots) or "none (code and diff exhibits need build --repo)"))
    print("Docs:")
    for doc in docs:
        print(f"  {doc.file:<22} sha {doc.sha}  {doc.text.count(chr(10)) + 1:>5} lines  {len(doc.headings):>3} headings")
    for doc in docs if args.all else [primary]:
        print(f"\nSections of {doc.file}  (anchor, hash, lines; * marks a text diagram)")
        lines = doc.text.split("\n")
        for heading in doc.headings:
            if heading.level < 2 or heading.level > 4:
                continue
            body = "\n".join(lines[heading.line:heading.end])
            has_diagram = bool(re.search(r"```(?:text)?\s*\n[^`]*?(?:├|└|─►|─>|-->|→)", body))
            indent = "  " * (heading.level - 2)
            marker = " *" if has_diagram else ""
            print(f"  {indent}{heading.anchor:<{56 - len(indent)}} {heading.hash}  {heading.end - heading.line:>4}{marker}")
    for doc in sorted((doc for doc in docs if doc.round), key=lambda doc: doc is not primary):
        describe_round(doc)
    for doc in sorted((doc for doc in docs if doc.tour), key=lambda doc: doc is not primary):
        describe_tour(doc, args.all)
    describe_exhibits(exhibits)
    return EXIT_OK


def command_build(args: argparse.Namespace) -> int:
    spec_dir, docs, repo, exhibits = load_view(args.spec, args.repo, persist=True, stamp_new=True)
    view_dir = ensure_view_dir(spec_dir)
    page, renderer = build_page(spec_dir, docs, exhibits, repo)
    out = Path(args.out).expanduser().resolve() if args.out else view_dir / "view.html"
    out.write_text(page, encoding="utf-8")
    statuses: dict[str, int] = {}
    for exhibit in exhibits:
        statuses[exhibit.status] = statuses.get(exhibit.status, 0) + 1
    print(f"Wrote {out.as_posix()} ({len(page.encode('utf-8')) // 1024} KB, {len(docs)} docs, {len(renderer.index.defs)} linked IDs)")
    print("Exhibits: " + (", ".join(f"{count} {status}" for status, count in sorted(statuses.items())) or "none"))
    for exhibit in exhibits:
        if exhibit.problems:
            print(f"  {exhibit.id}: {exhibit.status}: {'; '.join(exhibit.problems)}")
    for kind, entries in renderer.lint.items():
        if entries:
            print(f"{kind.capitalize()}: {len(entries)}")
            for entry in sorted(entries)[:args.max_report]:
                print(f"  {entry}")
            if len(entries) > args.max_report:
                print(f"  ... {len(entries) - args.max_report} more (see the build report in the page)")
    if not repo.roots:
        print("Note: no --repo given, so code paths are not linked and code/diff exhibits cannot be drawn.")
    return EXIT_OK


def read_manifest(view: Path) -> dict[str, Any]:
    if not view.is_file():
        raise ViewError(f"no view at {view}; run build first")
    text = view.read_text(encoding="utf-8")
    match = re.search(r'<script type="application/json" id="view-manifest">(.*?)</script>', text, re.S)
    if not match:
        raise ViewError(f"{view}: no view manifest found")
    return json.loads(match.group(1).replace("<\\/", "</"))


def command_check(args: argparse.Namespace) -> int:
    spec_dir, docs, repo, exhibits = load_view(args.spec)
    view = Path(args.out).expanduser().resolve() if args.out else spec_dir / VIEW_DIR / "view.html"
    manifest = read_manifest(view)
    built = {entry["file"]: entry["sha"] for entry in manifest.get("docs", [])}
    current = {doc.file: doc.sha for doc in docs}
    changed = sorted(file for file in current if file in built and built[file] != current[file])
    added = sorted(set(current) - set(built))
    removed = sorted(set(built) - set(current))
    stale = [exhibit for exhibit in exhibits if exhibit.status in {"stale", "orphan", "invalid", "unstamped"}]
    built_tours = manifest.get("tours") or {}
    code_changed = [
        f"{file} {name}" for file, rows in tour_fingerprints(docs).items()
        for name, fingerprint in rows.items() if (built_tours.get(file) or {}).get(name) != fingerprint
    ]
    print(f"View built {manifest.get('builtAt')} for {spec_dir.as_posix()}")
    for label, files in (("changed", changed), ("new", added), ("removed", removed)):
        if files:
            print(f"Docs {label} since the build: {', '.join(files)}")
    for entry in code_changed:
        print(f"Code changed since the build (tour {entry}): re-read the steps that cite it")
    for exhibit in stale:
        print(f"Exhibit {exhibit.id}: {exhibit.status}" + (f" ({'; '.join(exhibit.problems)})" if exhibit.problems else ""))
    if changed or added or removed or stale or code_changed:
        print("Stale: rebuild (and redraw the exhibits listed above).")
        return EXIT_STALE
    print("Fresh: the view matches its sources.")
    return EXIT_OK


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Build a generated HTML view of a spec folder.")
    commands = root.add_subparsers(dest="command", required=True)

    plan = commands.add_parser("plan", help="List docs, section anchors and hashes, and exhibit status.")
    plan.add_argument("spec", help="spec folder (specs/<slug>), or a doc in it to open first")
    plan.add_argument("--all", action="store_true", help="list sections of every doc, not only the main doc")
    plan.set_defaults(handler=command_plan)

    build = commands.add_parser("build", help="Stamp new exhibits and write .views/view.html.")
    build.add_argument("spec", help="spec folder (specs/<slug>), or a doc in it to open first")
    build.add_argument("--repo", action="append", help="code root for code links, excerpts and diffs (repeatable; remembered)")
    build.add_argument("--out", help="output file (default: SPEC/.views/view.html)")
    build.add_argument("--max-report", type=int, default=15, help="report lines per lint kind (default 15)")
    build.set_defaults(handler=command_build)

    check = commands.add_parser("check", help="Exit 1 when the view or an exhibit is stale.")
    check.add_argument("spec", help="spec folder (specs/<slug>), or a doc in it")
    check.add_argument("--out", help="view file to check (default: SPEC/.views/view.html)")
    check.set_defaults(handler=command_check)
    return root


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    args = parser().parse_args(argv)
    try:
        return args.handler(args)
    except ViewError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
