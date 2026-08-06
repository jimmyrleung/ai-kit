---
description: Implement specific task part of the implementation tasks document.
argument-hint: <prefix> <task>
arguments: prefix task
---

# Goal

Implement a specific task from the tasks document.

**Task Number**: $task

**Reference files**: $prefix

## Pre-Implementation Checklist

- [ ] Task dependencies are completed (verify in tasks file)
- [ ] I understand the acceptance criteria
- [ ] I have reviewed related files in the techspec

## Process

**MUST DO**: Execute Workflows 1 and 3

> **No per-task code review.** The reviewer fan-out that used to run here as Workflow 2 was
> retired (token economics: it re-loaded the same context once per task to review a small
> diff). Code review now happens once per prefix, batched, via `/review-implementation` —
> see the last-task hook in Workflow 3. Numbering keeps Workflow 3's name for symmetry with
> `implement-task-loop`.

### Workflow 1 - Implementation

1. Create todo list with all steps for that process.
2. Context: Read all relevant files starting with $prefix
3. Plan implementation: Create a step-by-step implementation plan
4. Implement: Write the code following the techspec and coding standards

   - Follow chosen architecture
   - Follow codebase conventions strictly
   - Write clean, well-documented code
   - Update todos as you progress

5. Test: Write/run tests according to the testing requirements
6. Build with no errors
7. **Verify (use the `verify-task` skill).** Run with:
   - `task_id`: $task
   - `tasks_doc_path`: the tasks-doc that owns `$prefix` (typically `{$prefix}_tasks.md`)
   - `prefix`: $prefix
   - `artifact_path`: (default — the task's section in `tasks_doc_path`)

   The skill runs gates 1+2+3 (build/test, AC checklist, cross-cutting) against just this
   task's ACs / files / budgets and records a `## Verify — {date}` block in the task's
   section. Halt on any gate fail until resolved (fix the code, or record `accepted: <reason>`
   in the gate-line). Do NOT advance to Workflow 3 — Post implementation until every gate is
   `pass` or `accepted`. Skip the skill call for trivial tasks (one-line config tweak, typo,
   doc-only edit) — see the skill's "When NOT to use" section.

### Workflow 3 - Post implementation

1. Create todo list with all steps for that process.
2. Document: Update task progress in the tasks file
3. Update the reference files $prefix with any decisions made during the implementation
4. Provide summary with modified/created files
5. **Last-task suggest hook:** if every task in `$prefix`'s tasks document is now marked Done, suggest `/review-implementation prefix=$prefix` (batched code review) followed by `/qa-gates prefix=$prefix` before declaring the feature/refactor complete. (Suggestions only — the user invokes them.) If earlier tasks remain, do not suggest yet — unless the task list is long (>~6 tasks) and a natural boundary was just crossed, in which case a mid-run `/review-implementation prefix=$prefix scope=…` may be worth suggesting.
