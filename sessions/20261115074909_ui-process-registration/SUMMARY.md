# Session summary — ui-process registered for Claude Code, Codex and CI

## What happened

1. Linked the new `ui-process` skill into `~/.claude/skills/` and `~/.agents/skills/` with `sync-skills.py`
   (dry run first: 4 creates, 50 unchanged, nothing removed). The run also linked `create-implementation-tasks`,
   which was committed on 2026-11-09 but never linked. `--check` passed for 27 skills (54 links); Claude Code listed
   `ui-process` in the same session.
2. `INVENTORY.md`: count 26 → 27, new "UI design" section with the `ui-process` row, and a bullet under "External and
   retired dependencies" for `taste-skill` and `impeccable`.
3. `README.md`: three counts 26 → 27 and a "UI design" bullet under "Other live capabilities".
4. Ran the "Validate live skill format and links" step from `.github/workflows/portability.yml` locally:
   `Validated 27 live skills and local Markdown links.` Python and bash syntax checks also passed. The PowerShell
   parse and adapter dry-run steps were not run (adapters not touched).
5. Fixed `skills/ui-process/SKILL.md`: the unfinished sentence at the start of "Approach" and "he" → "the user".

## Decisions

1. `ui-process` gets its own "UI design" inventory section, not "Discovery, requirements, and design": it covers UI,
   branding and design systems, not specs.
2. `taste-skill` and `impeccable` are recorded as external dependencies, the same way `teach` is for
   `breakout-session`: recommended, not bundled or installed.
3. No `agents/openai.yaml`: no live skill has one, so Codex needs nothing extra.

## Learnings

- `create-implementation-tasks` stayed invisible to both hosts for about 6 days because nobody ran the sync after it
  was committed. CI checks only the docs (rows and counts), not the host links.
- The 2026-11-02 long-term memory candidate for adding a skill
  (`../20261102055822_consolidate-sessions-install/long_term_memory.md`) was not adopted into `AGENTS.md`, and the same
  gap came back.
- CRLF line endings in `SKILL.md` do not break the frontmatter check: the validator reads with universal newlines, and
  other skills (for example `techspec`) are CRLF too.

## References

- `taste-skill`: https://github.com/Leonxlnx/taste-skill
- `impeccable`: https://github.com/pbakaus/impeccable

## Files touched

Staged by the owner, not committed: `INVENTORY.md`, `README.md`, `skills/ui-process/SKILL.md` (new).
Outside the repo: links `ui-process` and `create-implementation-tasks` in `~/.claude/skills/` and `~/.agents/skills/`.
