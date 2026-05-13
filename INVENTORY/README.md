# ai-kit Inventory

Quick-reference inventories for every component kind in this repo. Keep open during day-to-day use.

> Stored here (not inside each folder) because `agents/`, `commands/`, and `skills/` are auto-scanned by Claude Code via `~/.claude/` junctions — any `.md` file inside `commands/` would register as a slash command, etc.

| Inventory | Covers |
|---|---|
| [agents.md](agents.md) | All subagents (file → `name` → model pin → role), grouped by workflow family |
| [commands.md](commands.md) | All slash commands (orchestrators + per-phase) grouped by workflow family |
| [skills.md](skills.md) | All skills (the methodology, one `SKILL.md` per folder) grouped by workflow family |
| [docs.md](docs.md) | Reference docs |
| [templates.md](templates.md) | Top-level map of `templates/` subfolders |
| [templates-bugfix.md](templates-bugfix.md) | `templates/bugfix/` — bug report input |
| [templates-feature-addition.md](templates-feature-addition.md) | `templates/feature-addition/` — feature definition + per-type variants |
| [templates-greenfield-dev.md](templates-greenfield-dev.md) | `templates/greenfield-dev/` — product requirement |
| [templates-incident-response.md](templates-incident-response.md) | `templates/incident-response/` — incident report |
| [templates-refactoring-tech-debt.md](templates-refactoring-tech-debt.md) | `templates/refactoring-tech-debt/` — refactor proposal |
