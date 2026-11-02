# Long-term memory candidates

Proposals for `AGENTS.md` or `rules/`. The owner decides what goes in.

1. **Adding a skill to ai-kit.** A new `skills/<name>/SKILL.md` also needs: a row in `INVENTORY.md`, the live skill
   count updated in `INVENTORY.md` ("contains N skills") and in `README.md` (three places, including "N live
   skills"), and a `sync-skills.py` run (`--dry-run`, apply, `--check`) to link it for Claude Code and Codex. The
   portability workflow fails on any missing row or count. Commit the skill and its registration together.
