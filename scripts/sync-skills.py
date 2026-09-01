#!/usr/bin/env python3
"""Install the canonical ai-kit skills into the two shared user roots.

The adapter scripts are deliberately only compatibility entry points.  This
module owns enumeration, link classification, preflight, ownership evidence,
prepared transactions, recovery, and baseline-preserving rollback.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable


EXIT_OK = 0
EXIT_FAILURE = 1
EXIT_USAGE = 2
SCHEMA_VERSION = 1
SKILL_NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
TRANSACTION_PHASE = "prepared"
ACTION_PROGRESS_PENDING = "pending"
ACTION_PROGRESS_REPLACEMENT_AUTHORIZED = "replacement-authorized"


class SyncError(Exception):
    """A user-actionable runtime or safety failure."""


class PlanConflict(SyncError):
    """A complete preflight found one or more unsafe states."""

    def __init__(self, conflicts: Iterable[str]):
        self.conflicts = list(conflicts)
        super().__init__("; ".join(self.conflicts))


def _pairs_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def path_text(path: Path) -> str:
    return os.path.abspath(os.fspath(path))


def strip_windows_namespace_prefix(value: str) -> str:
    if value.startswith("\\\\?\\UNC\\"):
        return "\\\\" + value[8:]
    if value.startswith("\\\\?\\") or value.startswith("\\??\\"):
        return value[4:]
    return value


def normalized_path(path: str | Path) -> str:
    raw = strip_windows_namespace_prefix(os.fspath(path))
    resolved = strip_windows_namespace_prefix(os.path.realpath(raw))
    return os.path.normcase(os.path.normpath(resolved))


def paths_equal(left: str | Path, right: str | Path) -> bool:
    return normalized_path(left) == normalized_path(right)


def entry_exists(path: Path) -> bool:
    """Return true for normal, dangling, and Windows reparse entries."""
    try:
        os.lstat(path)
        return True
    except OSError:
        if os.name == "nt":
            try:
                return bool(path.is_junction())
            except (AttributeError, OSError):
                return False
        return False


def is_junction(path: Path) -> bool:
    if os.name != "nt":
        return False
    try:
        return bool(path.is_junction())
    except (AttributeError, OSError):
        return False


def is_link(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
    except OSError:
        pass
    return is_junction(path)


def link_kind(path: Path) -> str:
    if is_junction(path):
        return "junction"
    if path.is_symlink():
        return "symlink"
    raise SyncError(f"not a link or junction: {path}")


def raw_link_target(path: Path) -> str:
    try:
        return os.fsdecode(os.readlink(path))
    except OSError:
        try:
            return os.fsdecode(path.readlink())
        except (AttributeError, OSError) as exc:
            raise SyncError(f"cannot read link target: {path}: {exc}") from exc


def resolved_link_target(path: Path, raw_target: str | None = None) -> str:
    raw = raw_target if raw_target is not None else raw_link_target(path)
    target = Path(raw)
    if not os.path.isabs(raw):
        target = path.parent / target
    return normalized_path(target)


def entry_state(path: Path) -> dict[str, Any]:
    """Describe an entry without traversing a link target."""
    if not entry_exists(path):
        return {"state": "absent"}
    if is_link(path):
        raw = raw_link_target(path)
        return {
            "state": "link",
            "kind": link_kind(path),
            "raw_target": raw,
            "resolved_target": resolved_link_target(path, raw),
        }
    try:
        mode = os.lstat(path).st_mode
    except OSError as exc:
        raise SyncError(f"cannot inspect {path}: {exc}") from exc
    if stat.S_ISDIR(mode):
        return {"state": "directory"}
    if stat.S_ISREG(mode):
        return {"state": "file"}
    return {"state": "other"}


def states_equal(left: dict[str, Any], right: dict[str, Any]) -> bool:
    if left.get("state") != right.get("state"):
        return False
    if left.get("state") == "link":
        if left.get("kind") != right.get("kind"):
            return False
        if left.get("kind") == "junction":
            return paths_equal(left.get("raw_target"), right.get("raw_target")) and paths_equal(
                left.get("resolved_target"), right.get("resolved_target")
            )
        return left.get("raw_target") == right.get("raw_target") and left.get("resolved_target") == right.get(
            "resolved_target"
        )
    return True


def link_state(kind: str, raw_target: str, resolved_target: str) -> dict[str, Any]:
    return {
        "state": "link",
        "kind": kind,
        "raw_target": raw_target,
        "resolved_target": resolved_target,
    }


def validate_name(name: Any, context: str) -> str:
    if not isinstance(name, str) or not SKILL_NAME_RE.fullmatch(name):
        raise SyncError(f"{context}: invalid skill name")
    return name


def validate_state(state: Any, context: str, *, allow_directory: bool = False) -> dict[str, Any]:
    if not isinstance(state, dict) or not isinstance(state.get("state"), str):
        raise SyncError(f"{context}: invalid state object")
    kind = state["state"]
    if kind == "absent":
        if set(state) != {"state"}:
            raise SyncError(f"{context}: absent state has unexpected fields")
        return {"state": "absent"}
    if kind == "directory" and allow_directory:
        if set(state) != {"state"}:
            raise SyncError(f"{context}: directory state has unexpected fields")
        return {"state": "directory"}
    if kind != "link":
        raise SyncError(f"{context}: unsupported state {kind!r}")
    expected = {"state", "kind", "raw_target", "resolved_target"}
    if set(state) != expected:
        raise SyncError(f"{context}: link state fields are invalid")
    if not isinstance(state["kind"], str) or state["kind"] not in {"symlink", "junction"}:
        raise SyncError(f"{context}: unsupported link kind")
    for field in ("raw_target", "resolved_target"):
        if not isinstance(state[field], str) or not state[field] or "\x00" in state[field]:
            raise SyncError(f"{context}: invalid {field}")
    return copy.deepcopy(state)


def validate_baseline(baseline: Any, context: str) -> dict[str, Any]:
    return validate_state(baseline, context)


def validate_record(record: Any, *, root: Path, name: str, repo_root: str, context: str) -> dict[str, Any]:
    if not isinstance(record, dict) or set(record) != {"managed_target", "managed_kind", "baseline"}:
        raise SyncError(f"{context}: invalid ownership record fields")
    target = record["managed_target"]
    if not isinstance(target, str) or not os.path.isabs(target) or "\x00" in target:
        raise SyncError(f"{context}: managed_target must be absolute")
    expected = Path(repo_root) / "skills" / name
    historical_shape = Path(target).name == name and Path(target).parent.name == "skills"
    if not paths_equal(target, expected) and not historical_shape:
        raise SyncError(f"{context}: managed_target is outside the canonical skill path")
    kind = record["managed_kind"]
    if not isinstance(kind, str) or kind not in {"symlink", "junction"}:
        raise SyncError(f"{context}: invalid managed_kind")
    baseline = validate_baseline(record["baseline"], f"{context}.baseline")
    if baseline["state"] == "link":
        baseline_target = os.path.realpath(os.path.join(os.fspath(root), baseline["raw_target"]))
        if not paths_equal(baseline_target, baseline["resolved_target"]):
            raise SyncError(f"{context}.baseline: raw and resolved targets disagree")
    return {
        "managed_target": target,
        "managed_kind": kind,
        "baseline": baseline,
    }


def validate_transaction(transaction: Any, *, roots: list[Path], repo_root: str) -> dict[str, Any]:
    if not isinstance(transaction, dict):
        raise SyncError("manifest transaction is not an object")
    required = {"operation", "phase", "repo_root", "root_actions", "actions", "records_after"}
    if set(transaction) != required:
        raise SyncError("manifest transaction has invalid fields")
    if not isinstance(transaction["operation"], str) or transaction["operation"] not in {"apply", "prune", "uninstall"}:
        raise SyncError("manifest transaction has invalid operation")
    if transaction["phase"] != TRANSACTION_PHASE:
        raise SyncError("manifest transaction has invalid phase")
    tx_repo_root = transaction["repo_root"]
    if not isinstance(tx_repo_root, str) or not os.path.isabs(tx_repo_root):
        raise SyncError("manifest transaction repo_root is invalid")
    root_names = {path_text(root) for root in roots}
    if not isinstance(transaction["root_actions"], list) or not isinstance(transaction["actions"], list):
        raise SyncError("manifest transaction actions are not arrays")
    for index, root_action in enumerate(transaction["root_actions"]):
        if not isinstance(root_action, dict) or set(root_action) != {"root", "before", "after"}:
            raise SyncError(f"transaction root action {index} is invalid")
        if not isinstance(root_action["root"], str) or root_action["root"] not in root_names:
            raise SyncError(f"transaction root action {index} has an unknown root")
        validate_state(root_action["before"], f"transaction root action {index}.before", allow_directory=True)
        validate_state(root_action["after"], f"transaction root action {index}.after", allow_directory=True)
    records_after = transaction["records_after"]
    if not isinstance(records_after, dict) or set(records_after) != root_names:
        raise SyncError("transaction records_after roots are invalid")
    normalized_records: dict[str, dict[str, Any]] = {}
    for root in roots:
        key = path_text(root)
        records = records_after[key]
        if not isinstance(records, dict):
            raise SyncError(f"transaction records_after {key} is invalid")
        normalized_records[key] = {}
        for name, record in records.items():
            validate_name(name, f"transaction records_after {key}")
            normalized_records[key][name] = validate_record(
                record, root=root, name=name, repo_root=tx_repo_root, context=f"transaction record {key}/{name}"
            )
    normalized_actions: list[dict[str, Any]] = []
    for index, action in enumerate(transaction["actions"]):
        legacy_fields = {"root", "name", "action", "before", "after", "baseline"}
        current_fields = legacy_fields | {"progress"}
        if not isinstance(action, dict) or (set(action) != legacy_fields and set(action) != current_fields):
            raise SyncError(f"transaction action {index} is invalid")
        if not isinstance(action["root"], str) or action["root"] not in root_names:
            raise SyncError(f"transaction action {index} has an unknown root")
        name = validate_name(action["name"], f"transaction action {index}")
        if not isinstance(action["action"], str) or action["action"] not in {"create", "adopt", "leave", "retarget", "remove", "restore"}:
            raise SyncError(f"transaction action {index} has an invalid operation")
        validate_state(action["before"], f"transaction action {index}.before")
        validate_state(action["after"], f"transaction action {index}.after")
        validate_baseline(action["baseline"], f"transaction action {index}.baseline")
        progress = action.get("progress", ACTION_PROGRESS_PENDING)
        if progress not in {ACTION_PROGRESS_PENDING, ACTION_PROGRESS_REPLACEMENT_AUTHORIZED}:
            raise SyncError(f"transaction action {index} has invalid progress")
        if progress == ACTION_PROGRESS_REPLACEMENT_AUTHORIZED and action["action"] not in {"retarget", "restore"}:
            raise SyncError(f"transaction action {index} has invalid replacement progress")
        normalized_action = copy.deepcopy(action)
        normalized_action["progress"] = progress
        normalized_actions.append(normalized_action)
    return {
        "operation": transaction["operation"],
        "phase": transaction["phase"],
        "repo_root": tx_repo_root,
        "root_actions": copy.deepcopy(transaction["root_actions"]),
        "actions": normalized_actions,
        "records_after": normalized_records,
    }


def validate_manifest(data: Any, *, manifest_path: Path, roots: list[Path]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise SyncError(f"manifest is not an object: {manifest_path}")
    required = {"schema_version", "repo_root", "roots", "transaction"}
    if set(data) != required:
        raise SyncError(f"manifest has invalid top-level fields: {manifest_path}")
    if data["schema_version"] != SCHEMA_VERSION:
        raise SyncError(f"unsupported manifest schema: {manifest_path}")
    repo_root = data["repo_root"]
    if not isinstance(repo_root, str) or not os.path.isabs(repo_root) or "\x00" in repo_root:
        raise SyncError(f"manifest repo_root is invalid: {manifest_path}")
    root_names = {path_text(root) for root in roots}
    if not isinstance(data["roots"], dict) or set(data["roots"]) != root_names:
        raise SyncError(f"manifest roots do not match the managed roots: {manifest_path}")
    normalized_roots: dict[str, dict[str, Any]] = {}
    for root in roots:
        key = path_text(root)
        records = data["roots"][key]
        if not isinstance(records, dict):
            raise SyncError(f"manifest root records are invalid: {key}")
        normalized_roots[key] = {}
        for name, record in records.items():
            validate_name(name, f"manifest record {key}")
            normalized_roots[key][name] = validate_record(
                record, root=root, name=name, repo_root=repo_root, context=f"manifest record {key}/{name}"
            )
    transaction = data["transaction"]
    normalized_transaction = None
    if transaction is not None:
        normalized_transaction = validate_transaction(transaction, roots=roots, repo_root=repo_root)
    return {
        "schema_version": SCHEMA_VERSION,
        "repo_root": repo_root,
        "roots": normalized_roots,
        "transaction": normalized_transaction,
    }


def read_manifest(path: Path, roots: list[Path]) -> dict[str, Any] | None:
    if not entry_exists(path):
        return None
    if is_link(path) or not path.is_file():
        raise SyncError(f"manifest is not a regular file: {path}")
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw, object_pairs_hook=_pairs_without_duplicates)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise SyncError(f"cannot parse manifest {path}: {exc}") from exc
    return validate_manifest(data, manifest_path=path, roots=roots)


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, indent=2, sort_keys=True) + "\n"
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temporary)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_path, path)
        if os.name != "nt":
            try:
                directory_fd = os.open(path.parent, os.O_DIRECTORY)
                try:
                    os.fsync(directory_fd)
                finally:
                    os.close(directory_fd)
            except OSError:
                pass
    except Exception:
        try:
            temp_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise


def copy_records(records: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return copy.deepcopy(records)


def json_manifest(repo_root: str, roots: dict[str, dict[str, Any]], transaction: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "repo_root": repo_root,
        "roots": copy_records(roots),
        "transaction": copy.deepcopy(transaction),
    }


def create_link(path: Path, target: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        result = subprocess.run(
            ["cmd.exe", "/d", "/c", "mklink", "/J", str(path), str(target)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            raise SyncError(f"cannot create junction {path}: {detail}")
    else:
        try:
            path.symlink_to(target, target_is_directory=True)
        except OSError as exc:
            raise SyncError(f"cannot create symlink {path}: {exc}") from exc


def remove_link(path: Path) -> None:
    if not is_link(path):
        raise SyncError(f"refusing to remove non-link entry: {path}")
    try:
        if is_junction(path):
            path.rmdir()
        else:
            path.unlink()
    except OSError as exc:
        raise SyncError(f"cannot remove link {path}: {exc}") from exc


class SyncEngine:
    def __init__(self, repo_root: Path, home: Path, preserve_specs: Iterable[str] = ()) -> None:
        self.repo_root = repo_root.resolve(strict=False)
        self.home = home.resolve(strict=False)
        self.skills_source = self.repo_root / "skills"
        self.roots = [self.home / ".claude" / "skills", self.home / ".agents" / "skills"]
        self.manifest_path = self.home / ".claude" / "ownership" / "ai-kit-skill-sync.json"
        self.preserve_specs = list(preserve_specs)
        self.preserved: dict[str, set[str]] = {}
        self.skills: dict[str, Path] = {}
        self.manifest: dict[str, Any] | None = None
        self.actions_done = 0

    def root_key(self, root: Path) -> str:
        return path_text(root)

    def validate_home(self) -> None:
        if not entry_exists(self.home) or not self.home.is_dir() or is_link(self.home):
            raise SyncError(f"home must be an existing real directory: {self.home}")

    def enumerate_skills(self) -> None:
        if not entry_exists(self.skills_source) or is_link(self.skills_source) or not self.skills_source.is_dir():
            raise SyncError(f"canonical skills directory is not a real directory: {self.skills_source}")
        errors: list[str] = []
        skills: dict[str, Path] = {}
        try:
            entries = sorted(os.scandir(self.skills_source), key=lambda item: item.name)
        except OSError as exc:
            raise SyncError(f"cannot enumerate canonical skills: {exc}") from exc
        for entry in entries:
            child = Path(entry.path)
            try:
                is_directory = entry.is_dir(follow_symlinks=False)
                if not is_directory and is_link(child):
                    is_directory = child.is_dir()
            except OSError:
                is_directory = False
            if not is_directory:
                continue
            name = entry.name
            if not SKILL_NAME_RE.fullmatch(name):
                errors.append(f"invalid canonical skill directory name: {name}")
                continue
            skill_file = child / "SKILL.md"
            try:
                valid_file = skill_file.is_file() and not skill_file.is_symlink() and os.access(skill_file, os.R_OK)
            except OSError:
                valid_file = False
            if not valid_file:
                errors.append(f"canonical skill envelope missing readable file: {skill_file}")
                continue
            # Keep the canonical entry path (including a directory link) in
            # ownership state.  Target comparisons normalize through it, while
            # preserving the one source path for future checkout moves.
            skills[name] = child
        if errors:
            raise SyncError("; ".join(errors))
        if not skills:
            raise SyncError(f"canonical skills directory is empty: {self.skills_source}")
        self.skills = dict(sorted(skills.items()))

    def inspect_roots(self, *, require_real_directory: bool = False) -> list[str]:
        conflicts: list[str] = []
        for root in self.roots:
            state = entry_state(root)
            if state["state"] == "link":
                conflicts.append(f"root-layout-conflict: managed root is a link/junction: {root}")
            elif state["state"] not in {"absent", "directory"}:
                conflicts.append(f"root-layout-conflict: managed root is not a directory: {root}")
            elif require_real_directory and state["state"] == "absent":
                conflicts.append(f"missing managed root: {root}")
        return conflicts

    def load(self) -> None:
        self.validate_home()
        self.enumerate_skills()
        self.parse_preserve_specs()
        self.manifest = read_manifest(self.manifest_path, self.roots)

    def parse_preserve_specs(self) -> None:
        aliases = {"claude": self.roots[0], "agents": self.roots[1]}
        preserved = {self.root_key(root): set() for root in self.roots}
        for raw_spec in self.preserve_specs:
            if not isinstance(raw_spec, str) or raw_spec.count("/") != 1:
                raise SyncError(
                    f"--preserve value {raw_spec!r} must use the form <claude|agents>/<skill-name>"
                )
            alias, name = raw_spec.split("/", 1)
            if alias not in aliases:
                raise SyncError(f"--preserve root {alias!r} is invalid; use 'claude' or 'agents'")
            validate_name(name, f"--preserve {raw_spec}")
            if name not in self.skills:
                raise SyncError(f"--preserve {raw_spec} does not name a canonical skill")
            preserved[self.root_key(aliases[alias])].add(name)
        self.preserved = preserved

    def preserved_names(self, root: Path) -> set[str]:
        return self.preserved.get(self.root_key(root), set())

    def preserved_count(self) -> int:
        return sum(len(names) for names in self.preserved.values())

    def check_preserved_entries(self, root: Path, records: dict[str, Any], conflicts: list[str]) -> None:
        for name in sorted(self.preserved_names(root)):
            path = self.live_path(root, name)
            live = entry_state(path)
            if name in records:
                conflicts.append(f"preserved-entry-owned: {path} is already recorded in the ownership manifest")
            if live["state"] == "absent":
                conflicts.append(f"preserved-entry-missing: {path} does not exist")
            elif live["state"] not in {"directory", "link"}:
                conflicts.append(f"preserved-entry-invalid: {path} is a real {live['state']}")
            else:
                skill_file = path / "SKILL.md"
                try:
                    valid_envelope = skill_file.is_file() and os.access(skill_file, os.R_OK)
                except OSError:
                    valid_envelope = False
                if not valid_envelope:
                    conflicts.append(f"preserved-entry-invalid: {path} lacks a readable SKILL.md")

    def desired_state(self, target: Path) -> dict[str, Any]:
        kind = "junction" if os.name == "nt" else "symlink"
        raw = str(target)
        return link_state(kind, raw, normalized_path(target))

    def records_for(self) -> dict[str, dict[str, Any]]:
        assert self.manifest is not None
        return self.manifest["roots"]

    def live_path(self, root: Path, name: str) -> Path:
        return root / name

    def check_unowned_extra_links(self, root: Path, records: dict[str, Any], conflicts: list[str]) -> None:
        if not entry_exists(root) or entry_state(root)["state"] != "directory":
            return
        try:
            entries = sorted(os.scandir(root), key=lambda item: item.name)
        except OSError as exc:
            conflicts.append(f"cannot enumerate managed root {root}: {exc}")
            return
        canonical_root = normalized_path(self.skills_source)
        for entry in entries:
            name = entry.name
            if name in self.skills or name in records:
                continue
            path = Path(entry.path)
            state = entry_state(path)
            if state["state"] == "link" and state["resolved_target"].startswith(canonical_root + os.sep):
                conflicts.append(f"unowned-ai-kit-entry: {path} resolves into the canonical skills tree")

    def apply_plan(self, *, force: bool) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[str]]:
        root_conflicts = self.inspect_roots()
        if root_conflicts:
            raise PlanConflict(root_conflicts)
        old_roots: dict[str, dict[str, Any]] = (
            copy_records(self.records_for()) if self.manifest is not None else {self.root_key(root): {} for root in self.roots}
        )
        final_roots = copy_records(old_roots)
        actions: list[dict[str, Any]] = []
        conflicts: list[str] = []
        root_actions: list[dict[str, Any]] = []
        for root in self.roots:
            key = self.root_key(root)
            root_before = entry_state(root)
            root_actions.append({"root": key, "before": root_before, "after": {"state": "directory"}})
            records = old_roots[key]
            preserved = self.preserved_names(root)
            self.check_preserved_entries(root, records, conflicts)
            self.check_unowned_extra_links(root, records, conflicts)
            for name, target in self.skills.items():
                if name in preserved:
                    continue
                path = self.live_path(root, name)
                live = entry_state(path)
                old_record = records.get(name)
                desired = self.desired_state(target)
                if old_record is not None:
                    if live["state"] != "link":
                        conflicts.append(f"ownership-mismatch: {path} is not the recorded link/junction")
                        continue
                    if live["kind"] != old_record["managed_kind"]:
                        conflicts.append(f"ownership-mismatch: {path} link kind differs from manifest")
                        continue
                    if not paths_equal(live["resolved_target"], old_record["managed_target"]):
                        conflicts.append(f"ownership-mismatch: {path} target differs from manifest")
                        continue
                    baseline = old_record["baseline"]
                    if paths_equal(old_record["managed_target"], target):
                        after = live
                        action_name = "leave"
                    elif not force:
                        conflicts.append(f"stale: {path} points to {live['resolved_target']}; use --force")
                        continue
                    else:
                        after = desired
                        action_name = "retarget"
                    final_roots[key][name] = {
                        "managed_target": str(target),
                        "managed_kind": after["kind"],
                        "baseline": copy.deepcopy(baseline),
                    }
                else:
                    baseline = copy.deepcopy(live)
                    if live["state"] == "absent":
                        after = desired
                        action_name = "create"
                    elif live["state"] == "link" and paths_equal(live["resolved_target"], target):
                        after = live
                        action_name = "adopt"
                    elif live["state"] == "link":
                        conflicts.append(f"unowned-link-conflict: {path} points to {live['resolved_target']}")
                        continue
                    else:
                        conflicts.append(f"unowned-entry-conflict: {path} is a real {live['state']}")
                        continue
                    final_roots[key][name] = {
                        "managed_target": str(target),
                        "managed_kind": after["kind"],
                        "baseline": baseline,
                    }
                actions.append({
                    "root": key,
                    "name": name,
                    "action": action_name,
                    "before": copy.deepcopy(live),
                    "after": copy.deepcopy(after),
                    "baseline": copy.deepcopy(baseline),
                    "progress": ACTION_PROGRESS_PENDING,
                })
        if conflicts:
            raise PlanConflict(conflicts)
        repo_root = path_text(self.repo_root)
        transaction = {
            "operation": "apply",
            "phase": TRANSACTION_PHASE,
            "repo_root": repo_root,
            "root_actions": root_actions,
            "actions": actions,
            "records_after": final_roots,
        }
        return transaction, root_actions, actions, []

    def restore_action(
        self, root: Path, name: str, record: dict[str, Any], *, action_context: str
    ) -> tuple[dict[str, Any], str]:
        path = self.live_path(root, name)
        live = entry_state(path)
        if live["state"] != "link":
            raise PlanConflict([f"ownership-mismatch: {path} is not the recorded link/junction"])
        if live["kind"] != record["managed_kind"] or not paths_equal(live["resolved_target"], record["managed_target"]):
            raise PlanConflict([f"ownership-mismatch: {path} changed since it was managed"])
        baseline = record["baseline"]
        if baseline["state"] == "absent":
            return {"state": "absent"}, "remove"
        if states_equal(live, baseline):
            return live, "leave"
        if baseline["kind"] == "junction" and os.name != "nt":
            raise PlanConflict([f"{action_context}: cannot restore a Windows junction on this host: {path}"])
        return copy.deepcopy(baseline), "restore"

    def uninstall_plan(self, *, only_orphans: bool = False) -> dict[str, Any]:
        root_conflicts = self.inspect_roots(require_real_directory=True)
        if root_conflicts:
            raise PlanConflict(root_conflicts)
        if self.manifest is None:
            return {
                "operation": "uninstall",
                "phase": TRANSACTION_PHASE,
                "repo_root": path_text(self.repo_root),
                "root_actions": [],
                "actions": [],
                "records_after": {self.root_key(root): {} for root in self.roots},
            }
        old_roots = self.records_for()
        final_roots = copy_records(old_roots)
        actions: list[dict[str, Any]] = []
        conflicts: list[str] = []
        for root in self.roots:
            key = self.root_key(root)
            self.check_unowned_extra_links(root, old_roots[key], conflicts)
            for name in sorted(old_roots[key]):
                is_orphan = name not in self.skills
                if only_orphans and not is_orphan:
                    continue
                record = old_roots[key][name]
                try:
                    after, action_name = self.restore_action(root, name, record, action_context=f"{key}/{name}")
                except PlanConflict as exc:
                    conflicts.extend(exc.conflicts)
                    continue
                actions.append({
                    "root": key,
                    "name": name,
                    "action": action_name,
                    "before": entry_state(self.live_path(root, name)),
                    "after": copy.deepcopy(after),
                    "baseline": copy.deepcopy(record["baseline"]),
                    "progress": ACTION_PROGRESS_PENDING,
                })
                del final_roots[key][name]
        if conflicts:
            raise PlanConflict(conflicts)
        return {
            "operation": "prune" if only_orphans else "uninstall",
            "phase": TRANSACTION_PHASE,
            "repo_root": path_text(self.repo_root),
            "root_actions": [],
            "actions": actions,
            "records_after": final_roots,
        }

    def check(self) -> None:
        conflicts = self.inspect_roots(require_real_directory=True)
        if conflicts:
            raise PlanConflict(conflicts)
        if self.manifest is None:
            raise SyncError(f"incomplete: ownership manifest is absent: {self.manifest_path}")
        if self.manifest["transaction"] is not None:
            raise SyncError("incomplete: prepared transaction exists; rerun apply/uninstall to recover it")
        if not paths_equal(self.manifest["repo_root"], self.repo_root):
            raise SyncError("incomplete: manifest repo_root does not match the current checkout")
        conflicts = []
        expected_names = set(self.skills)
        for root in self.roots:
            key = self.root_key(root)
            records = self.records_for()[key]
            preserved = self.preserved_names(root)
            self.check_preserved_entries(root, records, conflicts)
            missing = sorted(expected_names - preserved - set(records))
            extra = sorted(set(records) - expected_names)
            conflicts.extend(f"incomplete: {key}/{name} has no ownership record" for name in missing)
            conflicts.extend(f"orphan-record: {key}/{name} remains in the ownership manifest" for name in extra)
            self.check_unowned_extra_links(root, records, conflicts)
            for name, target in self.skills.items():
                if name in preserved:
                    continue
                record = records.get(name)
                if record is None:
                    continue
                live = entry_state(self.live_path(root, name))
                if live["state"] != "link":
                    conflicts.append(f"incomplete: {key}/{name} is not a link/junction")
                    continue
                if live["kind"] != record["managed_kind"]:
                    conflicts.append(f"incomplete: {key}/{name} link kind differs from manifest")
                    continue
                if not paths_equal(live["resolved_target"], target):
                    conflicts.append(f"incomplete: {key}/{name} does not resolve to the current canonical skill")
                if not paths_equal(record["managed_target"], target):
                    conflicts.append(f"incomplete: {key}/{name} managed_target is stale")
        if conflicts:
            raise PlanConflict(conflicts)
        preserved_count = self.preserved_count()
        if preserved_count:
            managed_count = sum(len(records) for records in self.records_for().values())
            print(
                f"OK — qualified population policy satisfied for {len(self.skills)} canonical names "
                f"({managed_count} managed links; {preserved_count} explicitly preserved external skills)."
            )
        else:
            print(f"OK — {len(self.skills)} canonical skills resolve from both managed roots ({len(self.skills) * 2} links total).")

    def print_plan(self, transaction: dict[str, Any], *, label: str) -> None:
        print("ai-kit common skill sync")
        print(f"  repo        : {self.repo_root}")
        print(f"  home        : {self.home}")
        print(f"  mode        : {label}")
        root_actions = transaction.get("root_actions", [])
        actions = transaction.get("actions", [])
        for root in self.roots:
            for name in sorted(self.preserved_names(root)):
                print(f"  preserve  {self.root_key(root)}/{name} (explicitly preserved; not managed)")
        for root_action in root_actions:
            if root_action["before"] != root_action["after"]:
                print(f"  would-create root {root_action['root']}")
        counts: dict[str, int] = {}
        for action in actions:
            counts[action["action"]] = counts.get(action["action"], 0) + 1
            if action["before"] == action["after"]:
                print(f"  {action['action']:<9} {action['root']}/{action['name']} (current)")
            else:
                print(f"  {action['action']:<9} {action['root']}/{action['name']}")
        if self.preserved_count():
            counts["preserved"] = self.preserved_count()
        count_text = ", ".join(f"{key}={counts[key]}" for key in sorted(counts)) or "no actions"
        print(f"Plan: {count_text}")

    def invoke_hook(self, root: Path, name: str) -> None:
        hook = os.environ.get("AI_KIT_SYNC_ACTION_HOOK")
        if not hook:
            return
        command = [hook, str(root), name]
        if Path(hook).suffix.lower() == ".py":
            command.insert(0, sys.executable)
        try:
            subprocess.run(command, check=True)
        except (OSError, subprocess.CalledProcessError) as exc:
            raise SyncError(f"test action hook failed for {root}/{name}: {exc}") from exc

    def maybe_fail(self, point: str) -> None:
        value = os.environ.get(point)
        if value:
            raise SyncError(f"injected interruption at {point}")

    def persist_transaction_progress(self, transaction: dict[str, Any]) -> None:
        prepared = json_manifest(transaction["repo_root"], transaction["records_after"], transaction)
        atomic_write_json(self.manifest_path, prepared)
        self.manifest = prepared

    def execute_action(self, transaction: dict[str, Any], action: dict[str, Any]) -> None:
        root = Path(action["root"])
        name = action["name"]
        path = root / name
        self.invoke_hook(root, name)
        observed = entry_state(path)
        before = action["before"]
        after = action["after"]
        operation = action["action"]
        if states_equal(observed, after):
            return
        if operation in {"retarget", "restore"}:
            progress = action.get("progress", ACTION_PROGRESS_PENDING)
            if progress == ACTION_PROGRESS_PENDING:
                if not states_equal(observed, before):
                    raise PlanConflict([f"action-time-conflict: {path} is neither the recorded before nor planned after state"])
                action["progress"] = ACTION_PROGRESS_REPLACEMENT_AUTHORIZED
                self.persist_transaction_progress(transaction)
                self.maybe_fail("AI_KIT_SYNC_FAIL_AFTER_REPLACEMENT_PREPARE")
                observed = entry_state(path)
            if states_equal(observed, before):
                if observed["state"] != "link":
                    raise PlanConflict([f"action-time-conflict: {path} changed before replacement"])
                remove_link(path)
                self.maybe_fail("AI_KIT_SYNC_FAIL_AFTER_REPLACEMENT_UNLINK")
                observed = entry_state(path)
            if observed["state"] != "absent":
                raise PlanConflict([f"action-time-conflict: {path} is not the recorded replacement transition"])
        elif not states_equal(observed, before):
            raise PlanConflict([f"action-time-conflict: {path} is neither the recorded before nor planned after state"])
        if operation in {"adopt", "leave"}:
            return
        if operation == "remove":
            if entry_state(path)["state"] != "link":
                raise PlanConflict([f"action-time-conflict: {path} changed before removal"])
            remove_link(path)
            if after["state"] == "absent":
                return
        elif operation not in {"create", "retarget", "restore"}:
            raise SyncError(f"unsupported transaction action: {operation}")
        if after["state"] == "link":
            target = Path(after["raw_target"])
            create_link(path, target)
        elif after["state"] == "absent":
            if entry_exists(path):
                raise PlanConflict([f"action-time-conflict: expected {path} to be absent after removal"])
        else:
            raise SyncError(f"unsupported planned post-state for {path}")
        actual = entry_state(path)
        if not states_equal(actual, after):
            raise PlanConflict([f"action-time-conflict: {path} did not reach the planned post-state"])

    def execute_transaction(self, transaction: dict[str, Any]) -> None:
        for root_action in transaction["root_actions"]:
            root = Path(root_action["root"])
            observed = entry_state(root)
            before = root_action["before"]
            after = root_action["after"]
            if states_equal(observed, after):
                continue
            if not states_equal(observed, before):
                raise PlanConflict([f"action-time-conflict: managed root changed: {root}"])
            if after["state"] == "directory":
                root.mkdir(parents=True, exist_ok=True)
            if entry_state(root)["state"] != "directory":
                raise PlanConflict([f"action-time-conflict: managed root is not a real directory: {root}"])
        for action in transaction["actions"]:
            self.execute_action(transaction, action)
            self.actions_done += 1
            fail_after = os.environ.get("AI_KIT_SYNC_FAIL_AFTER_ACTION")
            if fail_after and self.actions_done >= int(fail_after):
                raise SyncError("injected interruption after action")

    def finalize_transaction(self, transaction: dict[str, Any]) -> None:
        self.maybe_fail("AI_KIT_SYNC_FAIL_BEFORE_FINALIZE")
        final = json_manifest(transaction["repo_root"], transaction["records_after"], None)
        atomic_write_json(self.manifest_path, final)

    def recover_transaction(self) -> None:
        if self.manifest is None or self.manifest["transaction"] is None:
            return
        transaction = self.manifest["transaction"]
        print("Recovering prepared transaction before continuing.")
        self.execute_transaction(transaction)
        self.finalize_transaction(transaction)
        self.manifest = read_manifest(self.manifest_path, self.roots)

    def run_apply(self, *, dry_run: bool, force: bool) -> int:
        if self.manifest is not None and self.manifest["transaction"] is not None:
            if dry_run:
                raise SyncError("incomplete: prepared transaction exists; dry-run cannot recover it")
            self.recover_transaction()
        transaction, _, _, _ = self.apply_plan(force=force)
        if dry_run:
            self.print_plan(transaction, label="DRY RUN (no filesystem or manifest changes)")
            return EXIT_OK
        current = self.manifest
        if current is not None and current["transaction"] is None:
            candidate = json_manifest(transaction["repo_root"], transaction["records_after"], None)
            if candidate == current and all(a["before"] == a["after"] for a in transaction["actions"]):
                print(f"OK — {len(self.skills)} canonical skills already current; no changes made.")
                return EXIT_OK
        prepared = json_manifest(transaction["repo_root"], transaction["records_after"], transaction)
        atomic_write_json(self.manifest_path, prepared)
        self.maybe_fail("AI_KIT_SYNC_FAIL_AFTER_PREPARE")
        self.execute_transaction(transaction)
        self.finalize_transaction(transaction)
        if self.preserved_count():
            print(f"OK — applied {len(self.skills)} canonical names with {self.preserved_count()} explicitly preserved external skills.")
        else:
            print(f"OK — applied {len(self.skills)} canonical skills to both managed roots.")
        return EXIT_OK

    def run_uninstall(self, *, dry_run: bool) -> int:
        if self.manifest is not None and self.manifest["transaction"] is not None:
            if dry_run:
                raise SyncError("incomplete: prepared transaction exists; dry-run cannot recover it")
            self.recover_transaction()
        transaction = self.uninstall_plan()
        if dry_run:
            self.print_plan(transaction, label="DRY RUN UNINSTALL (no filesystem or manifest changes)")
            return EXIT_OK
        if not transaction["actions"] and self.manifest is None:
            print("OK — no ai-kit ownership manifest exists; nothing to uninstall.")
            return EXIT_OK
        prepared = json_manifest(transaction["repo_root"], transaction["records_after"], transaction)
        atomic_write_json(self.manifest_path, prepared)
        self.maybe_fail("AI_KIT_SYNC_FAIL_AFTER_PREPARE")
        self.execute_transaction(transaction)
        self.finalize_transaction(transaction)
        print("OK — restored each managed entry to its first-managed baseline.")
        return EXIT_OK

    def run_prune(self, *, dry_run: bool, force: bool) -> int:
        if self.manifest is not None and self.manifest["transaction"] is not None:
            if dry_run:
                raise SyncError("incomplete: prepared transaction exists; dry-run cannot recover it")
            self.recover_transaction()
        if self.manifest is None:
            print("OK — no ai-kit ownership manifest exists; no orphans found.")
            return EXIT_OK
        transaction = self.uninstall_plan(only_orphans=True)
        if not transaction["actions"]:
            print("OK — no manifest-owned orphaned entries found.")
            return EXIT_OK
        if not force:
            self.print_plan(transaction, label="REPORT ONLY (use --prune --force to restore baselines)")
            return EXIT_OK
        if dry_run:
            self.print_plan(transaction, label="DRY RUN PRUNE (no filesystem or manifest changes)")
            return EXIT_OK
        prepared = json_manifest(transaction["repo_root"], transaction["records_after"], transaction)
        atomic_write_json(self.manifest_path, prepared)
        self.maybe_fail("AI_KIT_SYNC_FAIL_AFTER_PREPARE")
        self.execute_transaction(transaction)
        self.finalize_transaction(transaction)
        print("OK — restored and released manifest-owned orphaned entries.")
        return EXIT_OK


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Synchronize canonical ai-kit skills into ~/.claude/skills and ~/.agents/skills."
    )
    result.add_argument("--dry-run", action="store_true", help="print the complete plan without changing state")
    result.add_argument("--check", action="store_true", help="read-only completeness and ownership check")
    result.add_argument("--uninstall", action="store_true", help="restore immutable first-managed baselines")
    result.add_argument("--force", action="store_true", help="allow only manifest-proven stale relinking")
    result.add_argument("--prune", action="store_true", help="report or restore manifest-owned orphans")
    result.add_argument(
        "--preserve",
        action="append",
        default=[],
        metavar="ROOT/SKILL",
        help="leave an existing canonical-name entry unmanaged (repeat; ROOT is claude or agents)",
    )
    result.add_argument("--home", type=Path, default=Path.home(), help="user-home fixture root")
    return result


def validate_args(args: argparse.Namespace, parser_obj: argparse.ArgumentParser) -> None:
    if args.dry_run and args.check:
        parser_obj.error("--dry-run and --check cannot be combined")
    if args.check and (args.force or args.prune or args.uninstall):
        parser_obj.error("--check cannot be combined with --force, --prune, or --uninstall")
    if args.uninstall and (args.force or args.prune):
        parser_obj.error("--uninstall cannot be combined with --force or --prune")
    if args.preserve and (args.uninstall or args.prune):
        parser_obj.error("--preserve can only be used with apply, --dry-run, or --check")


def main(argv: list[str] | None = None) -> int:
    argument_parser = parser()
    args = argument_parser.parse_args(argv)
    validate_args(args, argument_parser)
    try:
        repo_root = Path(__file__).resolve().parents[1]
        engine = SyncEngine(repo_root, args.home, args.preserve)
        engine.load()
        if args.check:
            if engine.manifest is not None and engine.manifest["transaction"] is not None:
                raise SyncError("incomplete: prepared transaction exists; rerun apply/uninstall to recover it")
            engine.check()
            return EXIT_OK
        if args.uninstall:
            return engine.run_uninstall(dry_run=args.dry_run)
        if args.prune:
            return engine.run_prune(dry_run=args.dry_run, force=args.force)
        return engine.run_apply(dry_run=args.dry_run, force=args.force)
    except PlanConflict as exc:
        print("CONFLICT — no filesystem or manifest changes were made:", file=sys.stderr)
        for conflict in exc.conflicts:
            print(f"  - {conflict}", file=sys.stderr)
        return EXIT_FAILURE
    except SyncError as exc:
        print(f"ERROR — {exc}", file=sys.stderr)
        return EXIT_FAILURE
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"ERROR — {exc}", file=sys.stderr)
        return EXIT_FAILURE


if __name__ == "__main__":
    raise SystemExit(main())
