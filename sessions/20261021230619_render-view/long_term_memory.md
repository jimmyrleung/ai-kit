# Long-term memory candidates

Proposals for `AGENTS.md` or `rules/`. The owner decides what goes in.

1. **Skill examples are fictional.** Before committing a new or edited skill, grep it for client repo names, ticket IDs, real file paths and commit hashes. Examples drift toward the data a skill was tested on (this session's exhibit reference picked up real paths and a merge hash).
2. **Scripts do not assume `python3` on PATH.** Skill instructions that run a bundled script name the interpreter options: `python3`, `py -3`, or `uv run --no-project python`.
3. **Generated views are build output.** Anything under a spec's `.views/` is regenerated, never edited, never committed, and a client spec's view is never published to a hosted page.
