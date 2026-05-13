---
description: Break down the technical specification into implementation tasks to help a developer to implement a new feature in an existing codebase.
argument-hint: Prefix of files to read.
---

# Goal

Break down the technical specification into implementation tasks by exploring three sizings in parallel — granular / balanced / pragmatic — and committing to one.

(For a small feature where balanced sizing is obviously right, use `/integration-balanced-tasks` instead — it commits directly to balanced.)

This command is a thin shim: the `integration-tasks` skill owns the 3-way exploration, the consolidation, and the output contract.

## Process

1. Create a todo list with all steps for this command.
2. Read the feature description, integration analysis, and techspec files (all files starting with `$ARGUMENTS`) to get context. If the techspec is missing, stop and surface this to the user — the skill refuses to generate tasks from a feature description alone.
3. Use the `integration-tasks` skill with those inputs. The skill handles: launching the three `integration-tasks-creator-agent` variant workers (granular / balanced / pragmatic), comparing them, presenting the trade-offs and a recommendation, asking which sizing you prefer, inventorying the techspec, ordering by dependencies, proposing an implementation order, the ≥ 90% confidence gate, and writing `{feature_name}_tasks.md`.

When the skill hands back, this command is complete.
