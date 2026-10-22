#!/usr/bin/env python3
"""Build a generated, interactive HTML view of a spec folder.

The markdown files stay the source of truth; the page is a disposable build
output written to ``<spec>/.views/view.html``. Model-written illustrations
("exhibits") live as JSON in ``<spec>/.views/exhibits/``. Each one is stamped
with the hash of the sections it illustrates (and of the code it shows), so a
later build can tell which ones went stale and only those need redrawing.

Standard library only. Code excerpts and diffs read the repository given with
``--repo``; git diffs also need ``git`` on PATH.

    render_view.py plan  SPEC_DIR [--all]
    render_view.py build SPEC_DIR [--repo DIR]... [--out FILE]
    render_view.py check SPEC_DIR [--out FILE]
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
EXHIBIT_TYPES = ("claims", "flow", "tree", "states", "graph", "sequence", "walk", "code", "diff", "decisions")
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
    r"^(?P<path>(?:[\w.@-]+/)*[\w.@-]+\.(?:" + "|".join(CODE_EXTENSIONS) + r"))"
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

    def anchor_hashes(self) -> dict[str, str]:
        hashes = {h.anchor: h.hash for h in self.headings}
        hashes["*"] = self.sha
        return hashes

    def heading(self, anchor: str) -> Heading | None:
        return next((h for h in self.headings if h.anchor == anchor), None)


@dataclass
class Exhibit:
    path: Path
    data: dict[str, Any]
    doc: Doc | None = None
    anchor: str = ""
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


def discover_docs(spec_dir: Path) -> list[Doc]:
    files = [name for name in DOC_ORDER if (spec_dir / name).is_file()]
    files += sorted(path.name for path in spec_dir.glob("task_*.md") if path.is_file())
    if (spec_dir / "qa.md").is_file():
        files.append("qa.md")
    if not files:
        files = sorted(path.name for path in spec_dir.glob("*.md") if path.is_file())
    if not files:
        raise ViewError(f"no markdown docs found in {spec_dir}")
    docs = []
    used_ids: set[str] = set()
    for file in files:
        path = spec_dir / file
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n").expandtabs(4)
        doc_id = doc_id_for(file)
        while doc_id in used_ids:
            doc_id += "-x"
        used_ids.add(doc_id)
        doc = Doc(path=path, file=file, id=doc_id, label=doc_label_for(file), text=text, sha=short_hash(text))
        lines = text.split("\n")
        doc.headings = scan_headings(lines)
        doc.blocks = parse_blocks(lines)
        h1 = next((h for h in doc.headings if h.level == 1), None)
        doc.title = plain(h1.text) if h1 else doc.label
        docs.append(doc)
    return docs


def main_doc(docs: list[Doc]) -> Doc:
    return next((doc for doc in docs if doc.file == "techspec.md"), docs[0])


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
        exhibit.doc = by_file.get(str(data.get("doc") or default.file))
        exhibit.anchor = str(data.get("anchor") or "top")
        if exhibit.kind not in EXHIBIT_TYPES:
            exhibit.status = "invalid"
            exhibit.problems.append(f"type must be one of {', '.join(EXHIBIT_TYPES)}")
        elif exhibit.doc is None:
            exhibit.status = "orphan"
            exhibit.problems.append(f"doc {data.get('doc')!r} is not in this spec folder")
        elif exhibit.anchor != "top" and exhibit.doc.heading(exhibit.anchor) is None:
            exhibit.status = "orphan"
            exhibit.problems.append(f"anchor {exhibit.anchor!r} is not a heading in {exhibit.doc.file}")
        exhibits.append(exhibit)
    return exhibits


def exhibit_sources(exhibit: Exhibit) -> list[str]:
    sources = exhibit.data.get("sources")
    if isinstance(sources, list) and sources:
        return [str(source) for source in sources]
    return ["*"] if exhibit.anchor == "top" else [exhibit.anchor]


def evaluate_exhibit(exhibit: Exhibit, repo: Repo, *, stamp_new: bool) -> None:
    """Compare an exhibit's stamp with its sources (and its code); stamp new ones."""
    if exhibit.status in {"invalid", "orphan"} or exhibit.doc is None:
        return
    current = exhibit.doc.anchor_hashes()
    sources = exhibit_sources(exhibit)
    missing = [source for source in sources if source not in current]
    if missing:
        exhibit.status = "orphan"
        exhibit.problems.append(f"sources not found in {exhibit.doc.file}: {', '.join(missing)}")
        return
    hashes = {source: current[source] for source in sources}
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
                candidates.insert(0, target + ref[len(prefix):])
                break
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
    base = check_ref(spec.get("base") or "HEAD", "base")
    head = check_ref(spec["head"], "head") if spec.get("head") else None
    context = max(0, min(int(spec.get("context", 3)), 12))
    args = ["diff", "--no-color", "--no-ext-diff", f"-U{context}", base] + ([head] if head else []) + ["--", resolved.name]
    diff_text = run_git(resolved.parent, *args)
    if not diff_text.strip():
        raise ViewError(f"git diff {base} {head or '(working tree)'} shows no change in {reference}")
    return {"mode": "git", "path": resolved, "reference": reference, "diff": diff_text, "lang": lang,
            "base": base, "head": head or "working tree", "window": parse_range(spec.get("lines")),
            "hash": short_hash(diff_text)}


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
            if exhibit.doc is doc and exhibit.status not in {"invalid", "orphan"}:
                by_anchor.setdefault(exhibit.anchor, []).append(exhibit)
        headings = iter(doc.headings)
        out: list[str] = []
        stack: list[int] = []
        intro: list[str] = []
        notes: list[str] = []
        seen_section = False
        for block in doc.blocks:
            if block["t"] == "heading":
                heading = next(headings, None) or Heading(block["level"], block["text"], slugify(block["text"]), 0)
                if block["level"] == 1 and not seen_section:
                    continue
                seen_section = True
                out.append(self.heading(block, heading, stack, counts))
                out.extend(self.exhibit(exhibit) for exhibit in by_anchor.get(heading.anchor, []))
                continue
            rendered = self.block(block)
            if not seen_section:
                (notes if block["t"] == "quote" else intro).append(rendered)
            else:
                out.append(rendered)
        while stack:
            stack.pop()
            out.append("</div></section>")
        self.counts[doc.id] = counts
        top = "".join(self.exhibit(exhibit) for exhibit in by_anchor.get("top", []))
        notes_html = (
            f'<div class="doc-notes"><div class="label">Notes at the top of this doc</div>{"".join(notes)}</div>'
            if notes else ""
        )
        intro_html = f'<div class="doc-intro">{"".join(intro)}</div>' if intro else ""
        article = (
            f'<article class="doc" id="{doc.id}" data-doc="{doc.id}" hidden>{self.doc_head(doc, counts)}'
            f'{notes_html}{intro_html}{top}{"".join(out)}</article>'
        )
        return article, self.outline(doc, by_anchor)

    def heading(self, block: dict[str, Any], heading: Heading, stack: list[int], counts: dict[str, int]) -> str:
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
        return (
            "".join(closing)
            + f'<section class="sec lvl{level}" data-anchor="{esc(heading.anchor)}" data-title="{title}">'
            f'<div class="sec-head"><h{level} id="{esc(element_id)}" class="anchored">{text_html}</h{level}>'
            f'<div class="sec-tools">'
            f'<button type="button" class="tool" data-action="comment" aria-label="Comment on {title}">Comment</button>'
            f'<button type="button" class="tool" data-action="collapse" aria-expanded="true" aria-label="Collapse {title}">'
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
            heading = exhibit.doc.heading(source) if exhibit.doc and source != "*" else None
            labels.append("whole doc" if source == "*" else "§ " + plain(heading.text if heading else source))
        return ", ".join(labels)

    def exhibit(self, exhibit: Exhibit) -> str:
        data = exhibit.data
        kind = exhibit.kind
        try:
            body = getattr(self, f"exhibit_{kind}")(exhibit, data.get("data") or {})
        except (ViewError, KeyError, TypeError, ValueError) as exc:
            self.lint.setdefault("illustrations", set()).add(f"{exhibit.id}: {exc}")
            body = f'<p class="ex-error">This illustration could not be drawn: {esc(str(exc))}</p>'
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
    return Repo([Path(root) for root in roots], collect_aliases(docs))


def describe_exhibits(exhibits: list[Exhibit]) -> None:
    print(f"\nExhibits ({VIEW_DIR}/exhibits):")
    if not exhibits:
        print("  none")
    for exhibit in exhibits:
        location = f"{exhibit.doc.file if exhibit.doc else exhibit.data.get('doc')}#{exhibit.anchor}"
        problems = f"  ({'; '.join(exhibit.problems)})" if exhibit.problems else ""
        print(f"  {exhibit.id:<28} {exhibit.kind:<9} {location:<44} {exhibit.status}{problems}")


def command_plan(args: argparse.Namespace) -> int:
    spec_dir = Path(args.spec).expanduser().resolve()
    docs = discover_docs(spec_dir)
    repo = repo_for(spec_dir, docs, None, persist=False)
    exhibits = load_exhibits(spec_dir, docs)
    for exhibit in exhibits:
        evaluate_exhibit(exhibit, repo, stamp_new=False)
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
    describe_exhibits(exhibits)
    return EXIT_OK


def command_build(args: argparse.Namespace) -> int:
    spec_dir = Path(args.spec).expanduser().resolve()
    docs = discover_docs(spec_dir)
    view_dir = ensure_view_dir(spec_dir)
    repo = repo_for(spec_dir, docs, args.repo, persist=True)
    exhibits = load_exhibits(spec_dir, docs)
    for exhibit in exhibits:
        evaluate_exhibit(exhibit, repo, stamp_new=True)
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
    spec_dir = Path(args.spec).expanduser().resolve()
    view = Path(args.out).expanduser().resolve() if args.out else spec_dir / VIEW_DIR / "view.html"
    manifest = read_manifest(view)
    docs = discover_docs(spec_dir)
    built = {entry["file"]: entry["sha"] for entry in manifest.get("docs", [])}
    current = {doc.file: doc.sha for doc in docs}
    changed = sorted(file for file in current if file in built and built[file] != current[file])
    added = sorted(set(current) - set(built))
    removed = sorted(set(built) - set(current))
    repo = repo_for(spec_dir, docs, None, persist=False)
    exhibits = load_exhibits(spec_dir, docs)
    for exhibit in exhibits:
        evaluate_exhibit(exhibit, repo, stamp_new=False)
    stale = [exhibit for exhibit in exhibits if exhibit.status in {"stale", "orphan", "invalid", "unstamped"}]
    print(f"View built {manifest.get('builtAt')} for {spec_dir.as_posix()}")
    for label, files in (("changed", changed), ("new", added), ("removed", removed)):
        if files:
            print(f"Docs {label} since the build: {', '.join(files)}")
    for exhibit in stale:
        print(f"Exhibit {exhibit.id}: {exhibit.status}" + (f" ({'; '.join(exhibit.problems)})" if exhibit.problems else ""))
    if changed or added or removed or stale:
        print("Stale: rebuild (and redraw the exhibits listed above).")
        return EXIT_STALE
    print("Fresh: the view matches its sources.")
    return EXIT_OK


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Build a generated HTML view of a spec folder.")
    commands = root.add_subparsers(dest="command", required=True)

    plan = commands.add_parser("plan", help="List docs, section anchors and hashes, and exhibit status.")
    plan.add_argument("spec", help="spec folder, for example specs/<slug>")
    plan.add_argument("--all", action="store_true", help="list sections of every doc, not only the main doc")
    plan.set_defaults(handler=command_plan)

    build = commands.add_parser("build", help="Stamp new exhibits and write .views/view.html.")
    build.add_argument("spec", help="spec folder, for example specs/<slug>")
    build.add_argument("--repo", action="append", help="code root for code links, excerpts and diffs (repeatable; remembered)")
    build.add_argument("--out", help="output file (default: SPEC/.views/view.html)")
    build.add_argument("--max-report", type=int, default=15, help="report lines per lint kind (default 15)")
    build.set_defaults(handler=command_build)

    check = commands.add_parser("check", help="Exit 1 when the view or an exhibit is stale.")
    check.add_argument("spec", help="spec folder, for example specs/<slug>")
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
