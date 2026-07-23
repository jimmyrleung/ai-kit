# Skill authoring — repo rules

## Validate frontmatter with a strict YAML parser (node + js-yaml)

Before shipping any SKILL.md / command / agent frontmatter change, parse it with node + js-yaml —
Claude Code is lenient, but Codex / claude.ai / the API are strict (an unquoted `: ` inside a
`description` is the classic failure). This repo ships no `node_modules`: run node from a directory
where js-yaml is installed (e.g. `~`), or the `require()` fails with MODULE_NOT_FOUND from the repo
root.

**Why:** strict parsers silently drop mis-parsed skills at load time (5 skills broke at once on
2026-06-04), and the no-local-node_modules gotcha kept recurring because it lived only in archived
session-log narrative.
*(added 2026-07-23 — /close repo-memory bootstrap; sources: 2026-06-04 strict-YAML sweep, 2026-07-07 and 2026-07-23 audit runs)*

## Loop skills/commands are symlinks — enumerate and edit accordingly

Six skill dirs (`document-workflow-loop`, `implement-task-loop`, `map-tasks`, `qa-loop`,
`qa-loop-docs`, `review-checkpoint`) and `commands/tasks-loop.md` are Windows symlinks to the
canonical copies under `~/projects/cc-looper/claude-config/`; `skills/find-skills` and
`skills/teach` are external junctions. All show as untracked (`??`) in this repo's `git status` —
never commit them here; loop-entry changes are committed in cc-looper's repo.

- **Detection:** `Get-Item <path> -Force | Select-Object FullName, LinkType, Target` — `ls -la`
  does not mark them on Windows.
- **Editing:** the Edit tool cannot write through a symlink path (its atomic tmp-rename fails with
  ENOENT). Read + Edit the **canonical** cc-looper path; reserve the link paths for Read/Glob only.
- **Scanning:** Glob and Grep do NOT traverse directory symlinks — a full-population scan silently
  excludes all 7 linked entries. Enumerate via `Get-ChildItem` / Node `fs.readdirSync`, and grep
  the cc-looper tree explicitly. cc-looper's templates live at its repo **root** `templates/`, not
  `claude-config/templates/`.

**Why:** the cc-looper runner consumes its own canonical copies at runtime; the symlinks keep one
physical file per entry. Scans that trust Glob nearly emitted false audit findings (2026-07-07),
and committing the links here would duplicate cc-looper's ownership.
*(added 2026-07-23 — migrated from the ai-kit auto-memory `cc-looper-symlink-topology` (2026-05-15, last verified 2026-07-19) during the /close repo-memory bootstrap)*
