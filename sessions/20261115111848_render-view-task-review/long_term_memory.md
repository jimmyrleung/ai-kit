# Long-term memory candidates

Proposals for `AGENTS.md` or `rules/`. The owner decides what goes in.

1. **Installed skills are live links to this repo.** `sync-skills.py` installs each skill as a directory
   junction (a symlink on other systems) from `~/.claude/skills/<name>` and `~/.agents/skills/<name>` to
   `skills/<name>/` in this working tree. Every edit, and every branch switch, changes the installed skill for
   all sessions at once; there is nothing to "sync later". For multi-task changes to a skill that other
   sessions use, work in a separate git worktree. `sync-skills.py --dry-run` lists one action per skill, so it
   cannot confirm that a new file inside a skill is installed; check the folder instead.
   Evidence: checked on 2026-11-15 for `render-view` (both roots point to this repository's
   `skills/render-view/`).
