## 2026-09-27 — Refresh v3 inventory and portability

**Summary:** Refreshed the repository for its 27-skill v3 state, removed the unsolicited v2 eval/tooling stack, preserved the sync engine at the root, and replaced the failing portability action with focused cross-platform checks.
**Next:** Review the working tree, run `git add -A`, commit and push, then confirm all three GitHub Actions matrix jobs pass.
**Blockers:** The hosted Linux, macOS, and Windows workflow cannot be verified until the branch is pushed.
**Didn't work:** Repairing the stale npm fixtures was outside the intended eval scope; Windows `python` aliases were unusable; checking every bare skill link produced false missing-file failures for external dependencies.
**Artifacts:** [`SUMMARY.md`](SUMMARY.md), [`README.md`](../../README.md), [`INVENTORY.md`](../../INVENTORY.md), [portability workflow](../../.github/workflows/portability.yml), and [`sync-skills.py`](../../sync-skills.py).
