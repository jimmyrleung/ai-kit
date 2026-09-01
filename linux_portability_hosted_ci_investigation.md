# Hosted portability CI investigation

## Executive summary

The portability workflow passed on Ubuntu but failed in the isolated sync harness on macOS and Windows. Hosted tracebacks proved five platform assumptions: Windows junction commands were nested-quoted before reaching `cmd.exe`; created junctions exposed a namespaced substitution target; Python test hooks were launched as native executables on Windows; a POSIX-wrapper test ran on Windows; and two macOS fixtures used the lexical `/var` path where the filesystem resolves through `/private/var`.

The approved fix is limited to command construction, Python-hook invocation, and fixture normalization. The sync ownership model and migration behavior do not change.

## Confidence

- Confidence score: 96% — every root-cause hop is backed by a hosted traceback and current source.
- 4% uncertainty — only a new hosted Ubuntu/macOS/Windows run can prove the fixes on all target runners.

## Bug understanding

- Expected: `.github/workflows/portability.yml` completes successfully on Ubuntu, macOS, and Windows.
- Actual: Ubuntu passed; macOS and Windows failed at `Run isolated sync harness`.
- Reproduction: push the affected commits and inspect runs `33539563300` and `33541996829`.
- Scope: `scripts/sync-skills.py`, its isolated fixtures, and CI diagnostics. No live home was used as a test destination.

## Entry point

The failing workflow entry point is `.github/workflows/portability.yml:75`, which runs `python tests/test_sync_skills.py`.

## Execution-path trace

### Windows junction creation

1. **VERIFIED** — fixture apply operations call `SyncEngine.execute_action`, which reaches `create_link()` at `scripts/sync-skills.py:401` for absent managed entries.
2. **VERIFIED** — the failed implementation built one string containing `mklink /J` and embedded quotes, then passed that string as one argument to `cmd.exe /d /s /c`.
3. **VERIFIED** — Windows annotations reported `The filename, directory name, or volume label syntax is incorrect` from `create_link()` for paths that otherwise existed and were valid fixture paths.
4. **VERIFIED** — passing `mklink`, `/J`, the link path, and the target as separate subprocess arguments removes the nested quoting while preserving the junction operation.

### Windows action hook

1. **VERIFIED** — `test_action_time_race_leaves_prepared_transaction_without_false_records` supplies a `.py` file through `AI_KIT_SYNC_ACTION_HOOK`.
2. **VERIFIED** — `invoke_hook()` at `scripts/sync-skills.py:819` launched the path directly.
3. **VERIFIED** — the Windows annotation reported `[WinError 193] %1 is not a valid Win32 application`.
4. **VERIFIED** — invoking `.py` hooks through `sys.executable` uses the same Python runtime as the sync engine on every platform.

### Windows junction post-state

1. **VERIFIED** — run `33543082378` passed on Ubuntu and macOS; Windows created its junctions but rejected them at `execute_action()` with `did not reach the planned post-state`.
2. **VERIFIED** — `states_equal()` required exact `raw_target` equality for all links, while the planned junction stored a normal drive path.
3. **VERIFIED** — Python's `os.readlink()` contract says Windows directory junctions return the substitution path, which typically includes a `\\?\` namespace prefix.
4. **VERIFIED** — stripping the namespace prefix during path normalization and comparing junction targets by normalized path preserves target identity while retaining exact raw-target comparison for POSIX symbolic links.

### macOS temporary-path fixtures

1. **VERIFIED** — macOS `tempfile` returned a lexical path under `/var`, while `Path.resolve()` and the engine canonicalized it under `/private/var`.
2. **VERIFIED** — `test_canonical_directory_links_are_enumerated_and_deployed` compared those two lexical forms directly and failed despite equivalent filesystem identity.
3. **VERIFIED** — `test_relative_current_links_are_adopted_and_uninstall_preserves_raw_targets` calculated a relative link from the unresolved `/var` parent; when the kernel resolved the parent through `/private/var`, the raw target pointed to `/private/Users/...` and became invalid.
4. **VERIFIED** — resolving the temporary base and relative-link parent before constructing expectations preserves the fixture's intended target.

### Windows POSIX-wrapper fixture

1. **VERIFIED** — `test_compatibility_posix_wrappers_forward_and_reject_private_home_override` at `tests/test_sync_skills.py:728` executes Bash wrappers.
2. **VERIFIED** — the workflow has separate POSIX and PowerShell adapter exercise steps, selected by runner OS.
3. **VERIFIED** — Windows reported the POSIX test returning exit 1 with no sync-engine error, while PowerShell syntax checks passed.
4. **VERIFIED** — limiting this fixture to POSIX runners matches its stated surface; Windows remains covered by junction tests and the PowerShell adapter step.

## Root causes

1. **Integration — Windows command-line quoting:** a pre-quoted command string was nested inside Python's Windows subprocess command-line conversion.
   - Falsifier: the same argument-vector implementation fails with the same syntax error on a hosted Windows runner.
2. **State comparison — Windows namespace representation:** junction substitution targets use a `\\?\` prefix that is semantically equivalent to the planned drive path but failed exact raw-string equality.
   - Falsifier: a hosted Windows junction still fails its post-state check after both raw and resolved targets compare through namespace-aware path normalization.
3. **Integration — script execution:** Windows cannot execute a `.py` hook as a native executable.
   - Falsifier: a hosted traceback still reports WinError 193 when the hook command begins with `sys.executable`.
4. **Configuration — macOS path alias:** fixtures treated lexical and canonical temporary paths as interchangeable when constructing relative symlinks.
   - Falsifier: resolved fixture paths still produce `/private/Users/...` or direct `/var` versus `/private/var` assertion failures.
5. **Test scope — adapter mismatch:** a POSIX execution test ran on Windows despite dedicated PowerShell coverage.
   - Falsifier: the Windows-specific adapter or junction coverage is skipped after the POSIX fixture is gated.

## Proposed solution

- In `scripts/sync-skills.py:401`, pass the `cmd.exe`, `mklink`, option, link, and target tokens as separate subprocess arguments.
- Normalize Windows `\\?\` / `\??\` namespace prefixes and compare junction targets by normalized path while preserving exact raw-target equality for symbolic links.
- In `scripts/sync-skills.py:819`, prefix `.py` action hooks with `sys.executable`.
- In `tests/test_sync_skills.py:330` and `tests/test_sync_skills.py:356`, resolve the macOS temporary parent before direct comparison or relative-target calculation.
- In `tests/test_sync_skills.py:728`, run the POSIX-wrapper fixture only when `os.name != "nt"`.
- Keep per-test GitHub annotations because they expose future public runner failures without requiring authenticated log access.

## Alternatives considered

- Use `shell=True` for `mklink`: rejected because it broadens shell parsing and weakens argument boundaries.
- Replace junctions with Windows symbolic links: rejected because that can require privileges or Developer Mode and changes the selected Windows deployment mechanism.
- Skip the entire Windows harness: rejected because junction lifecycle and transaction recovery are core portability requirements.
- Compare macOS paths as raw strings: rejected because aliases make lexical equality weaker than filesystem identity.

## Impact assessment

- Files changed for behavior: `scripts/sync-skills.py` and `tests/test_sync_skills.py`.
- Test requirements: Python syntax, isolated sync harness, JavaScript portability fixtures, final portability checker, adapter syntax, and hosted Ubuntu/macOS/Windows matrix.
- Side effects: `.py` action hooks now explicitly use the active interpreter; non-Python hooks keep direct execution. Junction paths compare by filesystem identity across equivalent namespace representations. Junction type, ownership evidence, transaction format, preserve policy, and live-home boundaries are unchanged.

## Approval

The owner approved this five-file implementation on 2026-09-01 after the hosted tracebacks and scope were presented.
