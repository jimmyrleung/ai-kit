#!/usr/bin/env python3
"""Isolated fixture coverage for scripts/sync-skills.py.

Every mutating test uses a temporary home.  The repository checkout and the
normal user-home roots are never used as sync destinations here.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SYNC_PATH = REPO_ROOT / "scripts" / "sync-skills.py"
SPEC = importlib.util.spec_from_file_location("ai_kit_sync_skills", SYNC_PATH)
assert SPEC is not None and SPEC.loader is not None
SYNC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC)


def run_cli(home: Path, *args: str, env: dict[str, str] | None = None, script: Path = SYNC_PATH) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(script), *args, "--home", str(home)]
    process_env = os.environ.copy()
    if env:
        process_env.update(env)
    return subprocess.run(command, cwd=REPO_ROOT, env=process_env, text=True, capture_output=True)


def root_paths(home: Path) -> tuple[Path, Path]:
    return home / ".claude" / "skills", home / ".agents" / "skills"


def manifest_path(home: Path) -> Path:
    return home / ".claude" / "ownership" / "ai-kit-skill-sync.json"


def manifest_data(home: Path) -> dict:
    return json.loads(manifest_path(home).read_text(encoding="utf-8"))


def direct_children(path: Path) -> list[Path]:
    if not path.is_dir() or SYNC.is_link(path):
        return []
    return sorted(path.iterdir(), key=lambda child: child.name)


def filesystem_snapshot(root: Path) -> dict[str, tuple]:
    snapshot: dict[str, tuple] = {}

    def visit(path: Path, relative: Path) -> None:
        try:
            info = path.lstat()
        except FileNotFoundError:
            return
        key = "." if not relative.parts else relative.as_posix()
        if SYNC.is_link(path):
            snapshot[key] = ("link", os.readlink(path), info.st_mode, info.st_mtime_ns)
            return
        if stat.S_ISDIR(info.st_mode):
            snapshot[key] = ("dir", info.st_mode, info.st_mtime_ns)
            for child in sorted(path.iterdir(), key=lambda item: item.name):
                visit(child, relative / child.name)
            return
        snapshot[key] = ("file", path.read_bytes(), info.st_mode, info.st_mtime_ns)

    visit(root, Path())
    return snapshot


def make_directory_link(path: Path, target: Path, *, raw_target: str | None = None) -> None:
    """Create the platform's managed directory-link kind unless a raw target is required."""
    if os.name == "nt" and raw_target is None:
        SYNC.create_link(path, target)
    else:
        path.symlink_to(raw_target if raw_target is not None else target, target_is_directory=True)


def remove_directory_link(path: Path) -> None:
    SYNC.remove_link(path)


def copy_checkout(destination: Path) -> Path:
    checkout = destination / "checkout"
    destination.mkdir(parents=True, exist_ok=True)
    checkout.mkdir()
    shutil.copytree(REPO_ROOT / "skills", checkout / "skills", symlinks=True)
    return checkout


def load_engine(repo: Path, home: Path) -> object:
    engine = SYNC.SyncEngine(repo, home)
    engine.load()
    return engine


class SyncSkillsTests(unittest.TestCase):
    def test_clean_apply_and_completeness_check(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            applied = run_cli(home)
            self.assertEqual(applied.returncode, 0, applied.stderr)
            for root in root_paths(home):
                entries = direct_children(root)
                self.assertEqual(len(entries), 31)
                self.assertTrue(all(SYNC.is_link(entry) for entry in entries))
                for entry in entries:
                    self.assertEqual(SYNC.normalized_path(entry), SYNC.normalized_path(REPO_ROOT / "skills" / entry.name))
            data = manifest_data(home)
            self.assertEqual(data["schema_version"], 1)
            self.assertIsNone(data["transaction"])
            self.assertEqual([len(data["roots"][str(root.resolve())]) for root in root_paths(home)], [31, 31])
            checked = run_cli(home, "--check")
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertIn("62 links total", checked.stdout)

    def test_idempotent_apply_does_not_rewrite_manifest_or_links(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            self.assertEqual(run_cli(home).returncode, 0)
            before = filesystem_snapshot(home)
            second = run_cli(home)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("no changes made", second.stdout)
            self.assertEqual(filesystem_snapshot(home), before)

    def test_dry_run_is_globally_non_mutating(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            before = filesystem_snapshot(home)
            dry = run_cli(home, "--dry-run")
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertIn("create=62", dry.stdout)
            self.assertEqual(filesystem_snapshot(home), before)

            conflict_root = home / ".agents" / "skills"
            conflict_root.mkdir(parents=True)
            collision = conflict_root / "teach"
            collision.mkdir()
            (collision / "sentinel").write_text("keep", encoding="utf-8")
            before_conflict = filesystem_snapshot(home)
            conflict_dry = run_cli(home, "--dry-run")
            self.assertEqual(conflict_dry.returncode, 1)
            self.assertIn("unowned-entry-conflict", conflict_dry.stderr)
            self.assertEqual(filesystem_snapshot(home), before_conflict)

    def test_explicit_per_root_preserve_policy_leaves_external_entries_unmanaged(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            agents_root = home / ".agents" / "skills"
            agents_root.mkdir(parents=True)
            preserved = {
                "find-skills": "external find-skills",
                "teach": "external teach",
            }
            for name, contents in preserved.items():
                entry = agents_root / name
                entry.mkdir()
                (entry / "SKILL.md").write_text(
                    f"---\nname: {name}\ndescription: {contents}\n---\n",
                    encoding="utf-8",
                )
            preserve_args = (
                "--preserve",
                "agents/find-skills",
                "--preserve",
                "agents/teach",
            )

            before_dry_run = filesystem_snapshot(home)
            dry_run = run_cli(home, "--dry-run", *preserve_args)
            self.assertEqual(dry_run.returncode, 0, dry_run.stderr)
            self.assertIn("create=60", dry_run.stdout)
            self.assertIn("preserved=2", dry_run.stdout)
            self.assertEqual(filesystem_snapshot(home), before_dry_run)

            applied = run_cli(home, *preserve_args)
            self.assertEqual(applied.returncode, 0, applied.stderr)
            claude_root, agents_root = root_paths(home)
            self.assertEqual(len(direct_children(claude_root)), 31)
            self.assertEqual(len(direct_children(agents_root)), 31)
            self.assertTrue(all(SYNC.is_link(entry) for entry in direct_children(claude_root)))
            agent_links = [entry for entry in direct_children(agents_root) if SYNC.is_link(entry)]
            self.assertEqual(len(agent_links), 29)
            self.assertTrue(set(preserved).isdisjoint({entry.name for entry in agent_links}))
            self.assertTrue(
                all(
                    SYNC.normalized_path(entry) == SYNC.normalized_path(REPO_ROOT / "skills" / entry.name)
                    for entry in agent_links
                )
            )
            for name, contents in preserved.items():
                entry = agents_root / name
                self.assertTrue(entry.is_dir())
                self.assertFalse(SYNC.is_link(entry))
                self.assertIn(contents, (entry / "SKILL.md").read_text(encoding="utf-8"))

            data = manifest_data(home)
            self.assertEqual(
                [len(data["roots"][str(root.resolve())]) for root in root_paths(home)],
                [31, 29],
            )
            checked = run_cli(home, "--check", *preserve_args)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertIn("60 managed links", checked.stdout)
            self.assertIn("2 explicitly preserved external skills", checked.stdout)

            before_unqualified_check = filesystem_snapshot(home)
            unqualified = run_cli(home, "--check")
            self.assertEqual(unqualified.returncode, 1)
            self.assertIn("has no ownership record", unqualified.stderr)
            self.assertEqual(filesystem_snapshot(home), before_unqualified_check)

            uninstalled = run_cli(home, "--uninstall")
            self.assertEqual(uninstalled.returncode, 0, uninstalled.stderr)
            self.assertEqual(direct_children(claude_root), [])
            self.assertEqual(sorted(entry.name for entry in direct_children(agents_root)), sorted(preserved))
            for name, contents in preserved.items():
                self.assertIn(contents, (agents_root / name / "SKILL.md").read_text(encoding="utf-8"))

    def test_preserve_policy_rejects_an_empty_skill_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            agents_root = home / ".agents" / "skills"
            agents_root.mkdir(parents=True)
            (agents_root / "teach").mkdir()
            before = filesystem_snapshot(home)
            result = run_cli(home, "--dry-run", "--preserve", "agents/teach")
            self.assertEqual(result.returncode, 1)
            self.assertIn("lacks a readable SKILL.md", result.stderr)
            self.assertEqual(filesystem_snapshot(home), before)

    def test_preserve_policy_requires_existing_canonical_name_entry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            agents_root = home / ".agents" / "skills"
            agents_root.mkdir(parents=True)
            (agents_root / "find-skills").mkdir()
            before = filesystem_snapshot(home)
            result = run_cli(home, "--dry-run", "--preserve", "agents/teach")
            self.assertEqual(result.returncode, 1)
            self.assertIn("preserved-entry-missing", result.stderr)
            self.assertEqual(filesystem_snapshot(home), before)

    def test_preserve_policy_cannot_hide_an_owned_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            self.assertEqual(run_cli(home).returncode, 0)
            before = filesystem_snapshot(home)
            result = run_cli(home, "--preserve", "agents/teach")
            self.assertEqual(result.returncode, 1)
            self.assertIn("preserved-entry-owned", result.stderr)
            self.assertEqual(filesystem_snapshot(home), before)

    def test_check_reports_missing_and_stale_states_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            self.assertEqual(run_cli(home).returncode, 0)
            missing = home / ".claude" / "skills" / "teach"
            remove_directory_link(missing)
            before = filesystem_snapshot(home)
            checked = run_cli(home, "--check")
            self.assertEqual(checked.returncode, 1)
            self.assertIn("incomplete", checked.stderr)
            self.assertEqual(filesystem_snapshot(home), before)

    def test_invalid_cli_combinations_return_usage_exit_two(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            cases = [
                ("--dry-run", "--check"),
                ("--check", "--force"),
                ("--check", "--prune"),
                ("--check", "--uninstall"),
                ("--uninstall", "--force"),
                ("--uninstall", "--prune"),
                ("--uninstall", "--preserve", "agents/teach"),
                ("--not-a-flag",),
            ]
            for case in cases:
                with self.subTest(case=case):
                    result = run_cli(home, *case)
                    self.assertEqual(result.returncode, 2)
            self.assertFalse(home.exists() and any(home.iterdir()))

    def test_malformed_manifest_is_rejected_before_any_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            self.assertEqual(run_cli(home).returncode, 0)
            original = manifest_path(home).read_text(encoding="utf-8")
            variants = [
                "{\"schema_version\": 1,\"schema_version\": 1,\"repo_root\": \"/tmp/x\",\"roots\": {},\"transaction\": null}",
                json.dumps({"schema_version": 99, "repo_root": "/tmp/x", "roots": {}, "transaction": None}),
                json.dumps({"schema_version": 1, "repo_root": "/tmp/x", "roots": {}, "transaction": None, "unexpected": True}),
            ]
            for variant in variants:
                with self.subTest(variant=variant):
                    manifest_path(home).write_text(variant, encoding="utf-8")
                    before = filesystem_snapshot(home)
                    result = run_cli(home, "--check")
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("manifest", result.stderr.lower())
                    self.assertEqual(filesystem_snapshot(home), before)
                    manifest_path(home).write_text(original, encoding="utf-8")

    def test_source_envelope_validation_is_standard_library_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            checkout = copy_checkout(Path(temporary))
            missing = checkout / "skills" / "teach" / "SKILL.md"
            missing.unlink()
            home = Path(temporary) / "home"
            home.mkdir()
            engine = SYNC.SyncEngine(checkout, home)
            with self.assertRaises(SYNC.SyncError) as raised:
                engine.load()
            self.assertIn("readable file", str(raised.exception))
            self.assertFalse((home / ".claude").exists())

    @unittest.skipUnless(os.name != "nt", "canonical directory-link coverage is exercised by the Windows matrix")
    def test_canonical_directory_links_are_enumerated_and_deployed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary).resolve()
            checkout = copy_checkout(base / "checkout-holder")
            external = base / "external" / "linked-skill"
            external.mkdir(parents=True)
            (external / "SKILL.md").write_text(
                "---\nname: linked-skill\ndescription: External canonical fixture\n---\n",
                encoding="utf-8",
            )
            os.symlink(external, checkout / "skills" / "linked-skill", target_is_directory=True)
            home = base / "home"
            home.mkdir()

            engine = load_engine(checkout, home)
            self.assertIn("linked-skill", engine.skills)
            self.assertEqual(engine.skills["linked-skill"], checkout / "skills" / "linked-skill")
            self.assertEqual(engine.run_apply(dry_run=False, force=False), 0)

            for root in root_paths(home):
                linked = root / "linked-skill"
                self.assertTrue(SYNC.is_link(linked))
                self.assertEqual(SYNC.normalized_path(linked), SYNC.normalized_path(checkout / "skills" / "linked-skill"))
            load_engine(checkout, home).check()

    @unittest.skipUnless(os.name != "nt", "raw relative symlink preservation is covered on POSIX")
    def test_relative_current_links_are_adopted_and_uninstall_preserves_raw_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            claude_root, agents_root = root_paths(home)
            claude_root.mkdir(parents=True)
            agents_root.mkdir(parents=True)
            target = REPO_ROOT / "skills" / "analyze-work"
            raw = os.path.relpath(target, claude_root.resolve())
            link = claude_root / "analyze-work"
            os.symlink(raw, link, target_is_directory=True)
            original_lstat = link.lstat()
            applied = run_cli(home)
            self.assertEqual(applied.returncode, 0, applied.stderr)
            record = manifest_data(home)["roots"][str(claude_root.resolve())]["analyze-work"]
            self.assertEqual(record["baseline"]["raw_target"], raw)
            self.assertEqual(link.lstat().st_ino, original_lstat.st_ino)
            uninstalled = run_cli(home, "--uninstall")
            self.assertEqual(uninstalled.returncode, 0, uninstalled.stderr)
            self.assertTrue(SYNC.is_link(link))
            self.assertEqual(os.readlink(link), raw)
            self.assertEqual(sorted(child.name for child in direct_children(claude_root)), ["analyze-work"])
            self.assertEqual(direct_children(agents_root), [])

    def test_cross_root_preflight_leaves_the_empty_root_untouched(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            agents_root = home / ".agents" / "skills"
            agents_root.mkdir(parents=True)
            collision = agents_root / "teach"
            collision.mkdir()
            sentinel = collision / "sentinel"
            sentinel.write_text("preserve", encoding="utf-8")
            before = filesystem_snapshot(home)
            result = run_cli(home)
            self.assertEqual(result.returncode, 1)
            self.assertFalse((home / ".claude").exists())
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve")
            self.assertEqual(filesystem_snapshot(home), before)

    def test_unowned_live_and_dangling_links_never_force(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            claude_root = home / ".claude" / "skills"
            claude_root.mkdir(parents=True)
            unrelated = Path(temporary) / "unrelated"
            unrelated.mkdir()
            collision = claude_root / "analyze-work"
            make_directory_link(collision, unrelated)
            before = filesystem_snapshot(home)
            result = run_cli(home, "--force")
            self.assertEqual(result.returncode, 1)
            self.assertIn("unowned-link-conflict", result.stderr)
            self.assertEqual(filesystem_snapshot(home), before)

            dangling = claude_root / "teach"
            dangling.symlink_to(Path(temporary) / "missing-target", target_is_directory=True)
            before_dangling = filesystem_snapshot(home)
            result_dangling = run_cli(home, "--force")
            self.assertEqual(result_dangling.returncode, 1)
            self.assertEqual(filesystem_snapshot(home), before_dangling)

    def test_checkout_move_retargets_only_proven_owned_links_and_rollback_restores_baselines(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            old = copy_checkout(temporary_root / "old-holder")
            new = copy_checkout(temporary_root / "new-holder")
            home = temporary_root / "home"
            home.mkdir()
            for root in root_paths(home):
                root.mkdir(parents=True)
                target = old / "skills" / "analyze-work"
                make_directory_link(root / "analyze-work", target)
            old_engine = load_engine(old, home)
            old_engine.run_apply(dry_run=False, force=False)
            old_target = SYNC.normalized_path(old / "skills" / "teach")
            moved_engine = load_engine(new, home)
            moved_engine.run_apply(dry_run=False, force=True)
            for root in root_paths(home):
                for name in sorted(path.name for path in direct_children(root)):
                    self.assertEqual(SYNC.normalized_path(root / name), SYNC.normalized_path(new / "skills" / name))
            self.assertEqual(SYNC.normalized_path(home / ".agents" / "skills" / "teach"), SYNC.normalized_path(new / "skills" / "teach"))
            self.assertNotEqual(old_target, SYNC.normalized_path(home / ".agents" / "skills" / "teach"))
            rollback = load_engine(new, home)
            rollback.run_uninstall(dry_run=False)
            for root in root_paths(home):
                self.assertTrue(SYNC.is_link(root / "analyze-work"))
                self.assertEqual(SYNC.normalized_path(root / "analyze-work"), SYNC.normalized_path(old / "skills" / "analyze-work"))
                self.assertEqual([child.name for child in direct_children(root)], ["analyze-work"])

    def test_owned_stale_state_is_report_only_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            holder = Path(temporary)
            old = copy_checkout(holder / "old-holder")
            new = copy_checkout(holder / "new-holder")
            home = holder / "home"
            home.mkdir()
            first = load_engine(old, home)
            first.run_apply(dry_run=False, force=False)
            before = filesystem_snapshot(home)
            stale = load_engine(new, home)
            with self.assertRaises(SYNC.PlanConflict):
                stale.run_apply(dry_run=False, force=False)
            self.assertEqual(filesystem_snapshot(home), before)
            stale = load_engine(new, home)
            stale.run_apply(dry_run=False, force=True)
            self.assertEqual(SYNC.normalized_path(home / ".claude" / "skills" / "teach"), SYNC.normalized_path(new / "skills" / "teach"))

    def test_manifest_live_target_mismatch_is_not_forceable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            self.assertEqual(run_cli(home).returncode, 0)
            link = home / ".claude" / "skills" / "teach"
            unrelated = Path(temporary) / "unrelated"
            unrelated.mkdir()
            remove_directory_link(link)
            make_directory_link(link, unrelated)
            before = filesystem_snapshot(home)
            result = run_cli(home, "--force")
            self.assertEqual(result.returncode, 1)
            self.assertIn("ownership-mismatch", result.stderr)
            self.assertEqual(filesystem_snapshot(home), before)

    def test_owned_orphan_prune_is_report_only_then_guarded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            holder = Path(temporary)
            checkout = copy_checkout(holder / "checkout-holder")
            home = holder / "home"
            home.mkdir()
            load_engine(checkout, home).run_apply(dry_run=False, force=False)
            removed = checkout / "skills" / "analyze-work"
            shutil.rmtree(removed)
            orphan = load_engine(checkout, home)
            before = filesystem_snapshot(home)
            orphan.run_prune(dry_run=False, force=False)
            self.assertEqual(filesystem_snapshot(home), before)
            orphan = load_engine(checkout, home)
            orphan.run_prune(dry_run=False, force=True)
            self.assertFalse((home / ".claude" / "skills" / "analyze-work").exists())
            self.assertNotIn("analyze-work", manifest_data(home)["roots"][str((home / ".claude" / "skills").resolve())])

    def test_unowned_dangling_neighbor_blocks_orphan_action(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            holder = Path(temporary)
            checkout = copy_checkout(holder / "checkout-holder")
            home = holder / "home"
            home.mkdir()
            load_engine(checkout, home).run_apply(dry_run=False, force=False)
            shutil.rmtree(checkout / "skills" / "analyze-work")
            neighbor = home / ".claude" / "skills" / "zombie"
            make_directory_link(neighbor, checkout / "skills" / "zombie")
            before = filesystem_snapshot(home)
            orphan = load_engine(checkout, home)
            with self.assertRaises(SYNC.PlanConflict):
                orphan.run_prune(dry_run=False, force=True)
            self.assertEqual(filesystem_snapshot(home), before)

    def test_managed_root_link_is_a_layout_conflict_and_is_not_traversed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            holder = Path(temporary)
            home = holder / "home"
            home.mkdir()
            legacy = holder / "legacy-root"
            legacy.mkdir()
            (legacy / "unrelated").write_text("unchanged", encoding="utf-8")
            managed_parent = home / ".claude"
            managed_parent.mkdir()
            make_directory_link(managed_parent / "skills", legacy)
            before = filesystem_snapshot(home)
            result = run_cli(home)
            self.assertEqual(result.returncode, 1)
            self.assertIn("root-layout-conflict", result.stderr)
            self.assertEqual(filesystem_snapshot(home), before)
            self.assertEqual((legacy / "unrelated").read_text(encoding="utf-8"), "unchanged")

    def test_action_time_race_leaves_prepared_transaction_without_false_records(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            holder = Path(temporary)
            home = holder / "home"
            home.mkdir()
            hook = holder / "race-hook.py"
            hook.write_text(
                "#!/usr/bin/env python3\n"
                "import pathlib, sys\n"
                "pathlib.Path(sys.argv[1], sys.argv[2]).mkdir()\n",
                encoding="utf-8",
            )
            hook.chmod(hook.stat().st_mode | stat.S_IXUSR)
            result = run_cli(home, env={"AI_KIT_SYNC_ACTION_HOOK": str(hook)})
            self.assertEqual(result.returncode, 1)
            self.assertIn("action-time-conflict", result.stderr)
            self.assertFalse(SYNC.is_link(home / ".claude" / "skills" / "analyze-work"))
            self.assertIsNotNone(manifest_data(home)["transaction"])

    def test_interrupted_link_action_recovers_exact_pre_and_post_states(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            interrupted = run_cli(home, env={"AI_KIT_SYNC_FAIL_AFTER_ACTION": "1"})
            self.assertEqual(interrupted.returncode, 1)
            self.assertIsNotNone(manifest_data(home)["transaction"])
            self.assertTrue(SYNC.is_link(home / ".claude" / "skills" / "analyze-work"))
            recovered = run_cli(home)
            self.assertEqual(recovered.returncode, 0, recovered.stderr)
            self.assertEqual(run_cli(home, "--check").returncode, 0)

    def test_interrupted_retarget_recovers_from_durable_replacement_transition(self) -> None:
        for failpoint in ("AI_KIT_SYNC_FAIL_AFTER_REPLACEMENT_PREPARE", "AI_KIT_SYNC_FAIL_AFTER_REPLACEMENT_UNLINK"):
            with self.subTest(failpoint=failpoint), tempfile.TemporaryDirectory() as temporary:
                holder = Path(temporary)
                old = copy_checkout(holder / "old-holder")
                new = copy_checkout(holder / "new-holder")
                home = holder / "home"
                home.mkdir()
                load_engine(old, home).run_apply(dry_run=False, force=False)

                interrupted = load_engine(new, home)
                with mock.patch.dict(os.environ, {failpoint: "1"}):
                    with self.assertRaises(SYNC.SyncError):
                        interrupted.run_apply(dry_run=False, force=True)
                prepared = manifest_data(home)["transaction"]
                self.assertIsNotNone(prepared)
                first = prepared["actions"][0]
                self.assertEqual(first["progress"], SYNC.ACTION_PROGRESS_REPLACEMENT_AUTHORIZED)
                if failpoint.endswith("UNLINK"):
                    self.assertEqual(SYNC.entry_state(home / ".claude" / "skills" / "analyze-work")["state"], "absent")

                recovered = load_engine(new, home)
                recovered.run_apply(dry_run=False, force=True)
                self.assertIsNone(manifest_data(home)["transaction"])
                for root in root_paths(home):
                    self.assertEqual(SYNC.normalized_path(root / "analyze-work"), SYNC.normalized_path(new / "skills" / "analyze-work"))

    def test_interrupted_restore_recovers_from_durable_replacement_transition(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            holder = Path(temporary)
            old = copy_checkout(holder / "old-holder")
            new = copy_checkout(holder / "new-holder")
            home = holder / "home"
            home.mkdir()
            for root in root_paths(home):
                root.mkdir(parents=True)
                make_directory_link(root / "analyze-work", old / "skills" / "analyze-work")
            load_engine(old, home).run_apply(dry_run=False, force=False)
            load_engine(new, home).run_apply(dry_run=False, force=True)

            interrupted = load_engine(new, home)
            with mock.patch.dict(os.environ, {"AI_KIT_SYNC_FAIL_AFTER_REPLACEMENT_UNLINK": "1"}):
                with self.assertRaises(SYNC.SyncError):
                    interrupted.run_uninstall(dry_run=False)
            prepared = manifest_data(home)["transaction"]
            self.assertIsNotNone(prepared)
            self.assertEqual(prepared["actions"][0]["progress"], SYNC.ACTION_PROGRESS_REPLACEMENT_AUTHORIZED)

            recovered = load_engine(new, home)
            recovered.run_uninstall(dry_run=False)
            self.assertIsNone(manifest_data(home)["transaction"])
            for root in root_paths(home):
                self.assertEqual([child.name for child in direct_children(root)], ["analyze-work"])
                self.assertEqual(SYNC.normalized_path(root / "analyze-work"), SYNC.normalized_path(old / "skills" / "analyze-work"))

    def test_replacement_recovery_rejects_an_unrecorded_third_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            holder = Path(temporary)
            old = copy_checkout(holder / "old-holder")
            new = copy_checkout(holder / "new-holder")
            home = holder / "home"
            home.mkdir()
            load_engine(old, home).run_apply(dry_run=False, force=False)

            interrupted = load_engine(new, home)
            with mock.patch.dict(os.environ, {"AI_KIT_SYNC_FAIL_AFTER_REPLACEMENT_UNLINK": "1"}):
                with self.assertRaises(SYNC.SyncError):
                    interrupted.run_apply(dry_run=False, force=True)
            collision = home / ".claude" / "skills" / "analyze-work"
            collision.mkdir()
            sentinel = collision / "sentinel"
            sentinel.write_text("third-party", encoding="utf-8")

            recovered = load_engine(new, home)
            with self.assertRaises(SYNC.PlanConflict) as raised:
                recovered.run_apply(dry_run=False, force=True)
            self.assertIn("not the recorded replacement transition", str(raised.exception))
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "third-party")
            self.assertIsNotNone(manifest_data(home)["transaction"])

    def test_interrupted_manifest_finalization_recovers_without_partial_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            interrupted = run_cli(home, env={"AI_KIT_SYNC_FAIL_BEFORE_FINALIZE": "1"})
            self.assertEqual(interrupted.returncode, 1)
            prepared = manifest_data(home)
            self.assertIsNotNone(prepared["transaction"])
            self.assertEqual(len(prepared["roots"][str((home / ".claude" / "skills").resolve())]), 31)
            recovered = run_cli(home)
            self.assertEqual(recovered.returncode, 0, recovered.stderr)
            finalized = manifest_data(home)
            self.assertIsNone(finalized["transaction"])

    def test_uninstall_preview_is_non_mutating_and_classifies_mixed_baselines(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            holder = Path(temporary)
            old = copy_checkout(holder / "old-holder")
            new = copy_checkout(holder / "new-holder")
            home = holder / "home"
            home.mkdir()
            for root in root_paths(home):
                root.mkdir(parents=True)
                target = old / "skills" / "analyze-work"
                make_directory_link(root / "analyze-work", target)
            load_engine(old, home).run_apply(dry_run=False, force=False)
            load_engine(new, home).run_apply(dry_run=False, force=True)
            before = filesystem_snapshot(home)
            preview = run_cli(home, "--dry-run", "--uninstall")
            self.assertEqual(preview.returncode, 0, preview.stderr)
            self.assertIn("remove", preview.stdout)
            self.assertIn("restore", preview.stdout)
            self.assertEqual(filesystem_snapshot(home), before)

    def test_uninstall_mismatch_is_global_preflight(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            self.assertEqual(run_cli(home).returncode, 0)
            link = home / ".agents" / "skills" / "analyze-work"
            other = Path(temporary) / "other"
            other.mkdir()
            remove_directory_link(link)
            make_directory_link(link, other)
            before = filesystem_snapshot(home)
            result = run_cli(home, "--uninstall")
            self.assertEqual(result.returncode, 1)
            self.assertIn("ownership-mismatch", result.stderr)
            self.assertEqual(filesystem_snapshot(home), before)

    def test_windows_junction_command_passes_each_argument_without_nested_quoting(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            holder = Path(temporary)
            path = holder / "managed root" / "analyze-work"
            target = holder / "canonical skills" / "analyze-work"
            completed = subprocess.CompletedProcess([], 0, "", "")
            with mock.patch.object(SYNC.os, "name", "nt"), mock.patch.object(
                SYNC.subprocess, "run", return_value=completed
            ) as run:
                SYNC.create_link(path, target)
            run.assert_called_once_with(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(path), str(target)],
                capture_output=True,
                text=True,
            )

    def test_windows_junction_state_ignores_namespace_prefix_representation(self) -> None:
        target = r"C:\canonical skills\analyze-work"
        namespaced = r"\\?\C:\canonical skills\analyze-work"
        actual = SYNC.link_state("junction", namespaced, namespaced)
        planned = SYNC.link_state("junction", target, target)
        self.assertEqual(SYNC.strip_windows_namespace_prefix(namespaced), target)
        self.assertEqual(
            SYNC.strip_windows_namespace_prefix(r"\\?\UNC\server\share\analyze-work"),
            r"\\server\share\analyze-work",
        )
        self.assertEqual(SYNC.strip_windows_namespace_prefix(r"\??\C:\canonical skills\analyze-work"), target)
        self.assertTrue(SYNC.states_equal(actual, planned))

    def test_resolved_link_target_uses_raw_target_when_the_target_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            holder = Path(temporary)
            link = holder / "managed" / "analyze-work"
            link.parent.mkdir()
            link.symlink_to(Path("..") / "missing" / "analyze-work", target_is_directory=True)
            expected = holder / "missing" / "analyze-work"
            self.assertFalse(expected.exists())
            self.assertEqual(SYNC.resolved_link_target(link), SYNC.normalized_path(expected))

    def test_python_action_hook_uses_the_active_interpreter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            hook = home / "race hook.py"
            root = home / ".claude" / "skills"
            engine = SYNC.SyncEngine(REPO_ROOT, home)
            with mock.patch.dict(os.environ, {"AI_KIT_SYNC_ACTION_HOOK": str(hook)}), mock.patch.object(
                SYNC.subprocess, "run"
            ) as run:
                engine.invoke_hook(root, "analyze-work")
            run.assert_called_once_with(
                [sys.executable, str(hook), str(root), "analyze-work"],
                check=True,
            )

    @unittest.skipUnless(os.name != "nt", "POSIX compatibility wrappers are exercised on POSIX runners")
    def test_compatibility_posix_wrappers_forward_and_reject_private_home_override(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            clean_env = {"CODEX_HOME": "", "CURSOR_HOME": ""}
            # An empty variable is still set in the shell, so remove it from the subprocess environment.
            for wrapper, variable in (
                (REPO_ROOT / "adapters" / "codex" / "sync.sh", "CODEX_HOME"),
                (REPO_ROOT / "adapters" / "cursor" / "sync.sh", "CURSOR_HOME"),
            ):
                env = os.environ.copy()
                env.pop(variable, None)
                result = subprocess.run(
                    ["bash", str(wrapper), "--dry-run", "--home", str(home)],
                    cwd=REPO_ROOT,
                    env=env,
                    text=True,
                    capture_output=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("create=62", result.stdout)
                env[variable] = str(holder := (home / ("private-" + variable.lower())))
                rejected = subprocess.run(
                    ["bash", str(wrapper), "--dry-run", "--home", str(home)],
                    cwd=REPO_ROOT,
                    env=env,
                    text=True,
                    capture_output=True,
                )
                self.assertEqual(rejected.returncode, 2)
                self.assertIn(variable, rejected.stderr)
            del clean_env

    def test_powershell_wrappers_are_translators_only_until_windows_matrix(self) -> None:
        for provider, legacy in (("codex", "CodexHome"), ("cursor", "CursorHome")):
            source = (REPO_ROOT / "adapters" / provider / "sync.ps1").read_text(encoding="utf-8")
            self.assertIn("-UserHome", source)
            self.assertIn("--dry-run", source)
            self.assertIn("--check", source)
            self.assertIn("--uninstall", source)
            self.assertIn("--force", source)
            self.assertIn("--prune", source)
            self.assertIn("Preserve", source)
            self.assertIn(legacy, source)
            self.assertNotIn("Get-ChildItem", source)
            self.assertNotIn("New-Item", source)
            self.assertNotIn("Remove-Item", source)

    @unittest.skipUnless(os.name == "nt", "junction lifecycle is exercised by the Windows CI matrix")
    def test_windows_junction_lifecycle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            applied = run_cli(home)
            self.assertEqual(applied.returncode, 0, applied.stderr)
            for root in root_paths(home):
                entries = direct_children(root)
                self.assertEqual(len(entries), 31)
                self.assertTrue(all(SYNC.is_junction(entry) for entry in entries))

            checked = run_cli(home, "--check")
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertIn("62 links total", checked.stdout)

            uninstalled = run_cli(home, "--uninstall")
            self.assertEqual(uninstalled.returncode, 0, uninstalled.stderr)
            for root in root_paths(home):
                self.assertEqual(direct_children(root), [])

            reapplied = run_cli(home)
            self.assertEqual(reapplied.returncode, 0, reapplied.stderr)
            self.assertTrue(all(SYNC.is_junction(entry) for root in root_paths(home) for entry in direct_children(root)))

    def test_whole_root_migration_fixture_stops_then_preserves_child_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            holder = Path(temporary)
            home = holder / "home"
            home.mkdir()
            old_root = holder / "old-root"
            old_root.mkdir()
            unrelated_target = holder / "unrelated-target"
            unrelated_target.mkdir()
            (unrelated_target / "payload").write_text("unchanged", encoding="utf-8")
            for name in ("analyze-work", "teach"):
                make_directory_link(old_root / name, REPO_ROOT / "skills" / name)
            make_directory_link(old_root / "unrelated", unrelated_target)
            old_inventory = {
                child.name: ("link" if SYNC.is_link(child) else "directory", SYNC.normalized_path(child))
                for child in direct_children(old_root)
            }
            managed_root = home / ".agents" / "skills"
            managed_root.parent.mkdir(parents=True)
            make_directory_link(managed_root, old_root)
            stopped = run_cli(home, "--dry-run")
            self.assertEqual(stopped.returncode, 1)
            self.assertIn("root-layout-conflict", stopped.stderr)
            self.assertEqual(
                {child.name: ("link" if SYNC.is_link(child) else "directory", SYNC.normalized_path(child)) for child in direct_children(old_root)},
                old_inventory,
            )

            remove_directory_link(managed_root)
            managed_root.mkdir()
            for child in direct_children(old_root):
                managed_child = managed_root / child.name
                if SYNC.is_link(child):
                    make_directory_link(managed_child, child.resolve(strict=False))
            applied = run_cli(home)
            self.assertEqual(applied.returncode, 0, applied.stderr)
            after_names = {child.name for child in direct_children(managed_root)}
            expected_names = set(old_inventory) | {child.name for child in direct_children(REPO_ROOT / "skills")}
            self.assertEqual(after_names, expected_names)
            for name, (_, target) in old_inventory.items():
                self.assertEqual(SYNC.normalized_path(managed_root / name), target)
            for name in expected_names - set(old_inventory):
                self.assertEqual(SYNC.normalized_path(managed_root / name), SYNC.normalized_path(REPO_ROOT / "skills" / name))
            self.assertEqual((unrelated_target / "payload").read_text(encoding="utf-8"), "unchanged")


class GitHubActionsTestResult(unittest.TextTestResult):
    """Expose individual unittest tracebacks through public check annotations."""

    def _emit_annotation(self, test: unittest.case.TestCase, err: tuple) -> None:
        title = str(test).replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        traceback = self._exc_info_to_string(err, test)
        message = traceback.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::error file=tests/test_sync_skills.py,title={title}::{message}", flush=True)

    def addError(self, test: unittest.case.TestCase, err: tuple) -> None:
        super().addError(test, err)
        self._emit_annotation(test, err)

    def addFailure(self, test: unittest.case.TestCase, err: tuple) -> None:
        super().addFailure(test, err)
        self._emit_annotation(test, err)


if __name__ == "__main__":
    runner = None
    if os.environ.get("GITHUB_ACTIONS") == "true":
        runner = unittest.TextTestRunner(verbosity=2, resultclass=GitHubActionsTestResult)
    unittest.main(verbosity=2, testRunner=runner)
