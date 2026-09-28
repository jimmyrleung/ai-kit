# Long-term memory candidates

These are drafts for owner review. They are not repository rules yet.

## Current live surface

- The live v3 catalog is the tracked set of `skills/<name>/SKILL.md` files. At this session it
  contains 27 skills.
- `README.md` and `INVENTORY.md` should derive skill claims from that live tree rather than from
  historical fixtures or archived specifications.
- Support references required by a skill are maintained within that consuming skill's folder.
  The archived v2 top-level documents are historical sources, not a live generation pipeline.

## Evaluation boundary

- Do not introduce a skill evaluation framework without an approved evaluation requirement and
  design. Basic repository portability checks must remain separate from outcome evaluation.
- Historical eval output is recoverable from Git history and should not be treated as a live
  test contract.

## Synchronization boundary

- The root `sync-skills.py` is the common deployment engine for the Codex and Cursor adapters.
  Adapter scripts are compatibility wrappers and must not duplicate its synchronization logic.
- On Windows, wrappers should prefer `py -3` before `python3` or `python` to avoid Microsoft Store
  aliases that resolve as commands but cannot execute Python.
