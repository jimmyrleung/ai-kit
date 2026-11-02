---
name: consolidate-sessions
description: "Consolidate older /close sessions in a single weekly sessions folder. Use when the local repo's `sessions` folder grows too much."
---

# Consolidate sessions

## Goal

Consolidate sessions older than the current week (sunday to saturday) into a weekly sessions folder.

## Process

1. Read the `close` skill, especially the [Local repo] section, to understand what is persisted.

2. Identify the current week dates (sunday to monday).

3. Read the local repo `sessions/` folder to see what needs to be consolidated:
  - Sessions for the current week should stay the same
  - Sessions older than the current week should be consolidate into weekly folders
  - Sessions already consolidated into weekly folders should stay the same

4. Build a consolidation plan following the [Consolidation guidance] below, and confirm it with the user before starting.

5. Once approved, execute the consolidation.

6. Once finished, if this is a knowledge base where the user runs (`INGEST`, `QUERY`, `LINT`), make sure links to the `sessions/` folder are not broken as sometimes these are referenced as it is a support folder.

7. Display a summary to the user of what was executed.

### Consolidation guidance

For each weekly folder:

1. Build a single `SUMMARY.md` to consolidate the week's session summaries.

2. Build a single `LOGS.md` that can be read as a timeline, but in this case from the most recent session to the oldest:

  ```markdown
  [most recent session]
  
  ---

  [session before the most recent]

  ---

  [...]

  ---

  [older session for the week]
  ```

3. For each `long_term_memory.md` file generated throughout the week, extract each memory into a separate `[slug]_memory.md` and add it to the `long_term_memory/` folder. `[slug]` is a meaningful name that helps identify the long term memory suggestion. The idea is that we can review each memory individually, one by one.

4. Add skill drafts into the `skills/[slug]/` folder, where `[slug]` is the meaningful name for the skill. Rename the `[skill_draft].md` to `SKILL.md` as it will have its own folder within `skills`.

5. Decisions generated throughout the week should be copied into `decisions/[decision].md` as is.

6. Any other files generated throughout the session should be copied into `artifacts/[slug]/` where `[slug]` is a meaningful name for the artifacts, and any references to it on `LOGS.md`, `SUMMARY.md`, etc. should be updated.
