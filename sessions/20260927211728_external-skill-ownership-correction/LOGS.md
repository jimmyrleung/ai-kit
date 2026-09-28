## 2026-09-27 — Exclude linked third-party skills

**Summary:** Corrected ai-kit's catalog to 23 owned skills, preserved four Matt Pocock skills as ignored local junctions to global installations, and made synchronization and portability checks ignore linked source directories.
**Next:** Run `git add -A`, review the combined staged diff, commit and push, then confirm the Linux, macOS, and Windows GitHub Actions jobs pass.
**Blockers:** Hosted CI requires a push. Normal-home sync also refuses the pre-existing linked `~/.claude/skills` root; isolated-home sync passes and no real-home ai-kit ownership manifest exists.
**Didn't work:** Counting visible directories included external junctions; reversing `teach` without checking both link directions created a temporary cycle; normal-home dry-run validation stopped at the linked managed root.
**Artifacts:** [`SUMMARY.md`](SUMMARY.md), [ownership decision](decisions/exclude-linked-third-party-skills.md), [`README.md`](../../README.md), [`INVENTORY.md`](../../INVENTORY.md), [portability workflow](../../.github/workflows/portability.yml), and [`sync-skills.py`](../../sync-skills.py).
