## 2026-09-27 — Refresh v3 inventory and portability

**Summary:** Refreshed the repository for its 23-skill v3 state, excluded four locally installed Matt Pocock skills from kit ownership, removed the unsolicited v2 eval/tooling stack, preserved the root sync engine, and replaced the failing portability action with focused cross-platform checks.
**Next:** Review the working tree, run `git add -A`, commit and push, then confirm all three GitHub Actions matrix jobs pass.
**Blockers:** The hosted Linux, macOS, and Windows workflow cannot be verified until the branch is pushed. Normal-home sync currently refuses the pre-existing linked `~/.claude/skills` root; isolated-home sync passes, and no ai-kit ownership manifest exists in the real home.
**Didn't work:** Repairing the stale npm fixtures was outside the intended eval scope; Windows `python` aliases were unusable; checking every bare skill link produced false missing-file failures for external dependencies.
**Artifacts:** [`SUMMARY.md`](SUMMARY.md), [`README.md`](../../README.md), [`INVENTORY.md`](../../INVENTORY.md), [portability workflow](../../.github/workflows/portability.yml), and [`sync-skills.py`](../../sync-skills.py).
