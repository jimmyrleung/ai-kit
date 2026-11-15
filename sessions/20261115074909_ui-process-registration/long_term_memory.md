# Long-term memory candidates

Proposals for `AGENTS.md` or `rules/`. The owner decides what goes in.

1. **Adding a skill to ai-kit (second confirmation).** Same rule as candidate 1 in
   `../20261102055822_consolidate-sessions-install/long_term_memory.md`: a new `skills/<name>/SKILL.md` also needs an
   `INVENTORY.md` row, the live count in `INVENTORY.md` ("contains N skills") and in `README.md` (three places,
   including "N live skills"), and a `sync-skills.py` run (`--dry-run`, apply, `--check`). Commit the skill and its
   registration together.
   New evidence: `create-implementation-tasks` was committed with its docs on 2026-11-09, so CI passed, but it was
   never linked. CI does not check host links, so only the sync step catches this. Suggested extra line: "after
   pulling or committing a new skill, run `sync-skills.py --check`".
