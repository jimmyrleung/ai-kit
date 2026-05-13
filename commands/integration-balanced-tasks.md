---
description: Break down a technical specification into a balanced implementation tasks document (mid-size tasks, "okay" quantity). Single-approach variant of /integration-create-tasks.
argument-hint: Prefix of files to read.
---

# Goal

Break down the technical specification into implementation tasks using a **balanced** approach — mid-size tasks, "okay" quantity (usually 4–10 tasks, mostly S/M with occasional L).

Based on:

- Feature description file(s)
- Integration analysis file(s)
- Techspec file(s) — authoritative for all technical detail

This is the single-approach variant of `/integration-create-tasks`. It skips the granular / balanced / pragmatic parallel exploration and commits directly to balanced. Use it when:

- You already know the balanced sizing is the right fit and don't want to re-decide per feature, OR
- The feature is small-to-medium and the 3-way exploration would be overkill.

If the feature has genuine uncertainty about the right granularity, use `/integration-create-tasks` instead.

## Process

**MUST DO**: Execute Workflows 1 and 2.

Workflow 1 produces the tasks doc directly using the `@balanced-tasks-creation` skill. Workflow 2 hands the produced doc to an independent subagent for a fresh-eyes review against the same skill's contract.

### Workflow 1 — Build (skill, main thread)

1. Create a todo list with all steps for this workflow.
2. Read the feature description, integration analysis, and techspec files to get context (all files starting with `$ARGUMENTS`). If the **techspec is missing**, stop and surface this to the user — the skill refuses to generate tasks from a feature description alone. If the **integration analysis is missing** but the techspec is present, proceed and note the gap so the skill's confidence gate accounts for it.
3. Use the `@balanced-tasks-creation` skill with the input files above. The skill handles:
   - Reviewing inputs and inventorying the work per the techspec.
   - Grouping the inventory into balanced-size tasks (mid-size, "okay" quantity).
   - Ordering tasks by dependencies and identifying parallelizable work.
   - Proposing an implementation order and confirming with the user when non-obvious.
   - Running the confidence gate (≥ 90% before writing; < 90% stops and asks clarifying questions).
   - Producing the tasks content.
4. Before writing the file, spot-check `file:line` references and "Files involved" paths against the current codebase to confirm they were taken from the techspec (not invented). Fix any that don't resolve.
5. Write the tasks document to `{feature_name}_tasks.md` alongside the feature description, integration analysis, and techspec.

### Workflow 2 — Review (subagent, fresh eyes)

The review uses an independent subagent so the doc gets checked by someone that didn't write it. The subagent reviews against `@balanced-tasks-creation`'s contract — not against its own creation-mode defaults.

1. Create a todo list with all steps for this workflow.
2. Launch a single `@integration-tasks-creator-agent` in **review mode** with a prompt that:
   - States the task is **review**, not creation — the agent must not rewrite the tasks doc, only produce a review list.
   - Names the exact files the agent must read: the tasks doc from Workflow 1, the feature description, the integration analysis, and the techspec.
   - Points the agent at the `@balanced-tasks-creation` SKILL as the authoritative contract for what the tasks doc should contain. This overrides the agent's own internal `[Process]` and `[Output Guidelines]` sections.
   - Asks the agent to check specifically:
     - All 6 **required sections** are present (Header / companion docs, Tasks overview, Implementation order when non-obvious, Detailed tasks, Notes & decisions, Confidence score).
     - The **balanced sizing** holds: task count in the 4–10 range for the feature's size, most tasks S or M, any L is justified, no task exceeds 8h without being split.
     - No task is silently untested — each task either includes testing requirements or explicitly defers them to a named later task.
     - Every task's **dependencies** are consistent (no circular refs, no forward refs to tasks that don't exist, parallel-with claims match the depends-on graph).
     - Every `file:line` ref and "Files involved" path is taken from the techspec or resolves to real code — not invented.
     - Every requirement from the feature description / integration analysis / techspec has a home in the tasks doc (an implementation task, a test task, or an explicit deferral in Notes & Decisions).
     - No section from the skill's **Do not include** list has been added (generic S/M/L recaps, generic task-category recaps, architecture-decisions tables copied from the techspec, empty Started/Completed placeholders, TBD test scenarios, standalone Documentation Needs checklists).
     - No required section is a placeholder — if empty, a one-sentence "why this section has no substance" explanation is present.
     - Confidence score follows the global CLAUDE.md format: numeric score, "Why X%" bullets, "X% uncertainty" bullets.
   - Asks for a structured review output: sizing/granularity issues, coverage gaps (requirements without a task), dependency-graph issues, unverified file refs, violated section rules, untested tasks, confidence-score gaps — plus a numeric reviewed-confidence score.
3. When the agent returns, read its review output and consolidate it into a single actionable list.
4. Confirm the list with the user before applying changes. Only edit the tasks doc after approval.
5. Ensure the post-review confidence score is ≥ 90% before completing.
6. Update the tasks doc to incorporate the approved review changes.
