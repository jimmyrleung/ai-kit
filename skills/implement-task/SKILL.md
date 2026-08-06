---
name: implement-task
description: "Implement one task from an implementation tasks document — or a reviewed bug fix — end-to-end: implement per the techspec and codebase conventions, test, build, then run the verify-task gates before marking it Done. A fix target (reviewed investigation + fix-mode techspec; tasks doc optional) gets the fix lens: minimal root-cause change, bug-scenario + edge-case tests. No per-task code review — that is batched per prefix via /review-implementation. Accepts a loose target: a prefix, a tasks-doc path, a task number, a bug id or investigation doc, or a short description — it resolves the rest. Use when asked to implement, work on, or pick up a task from a tasks doc, or to implement or apply a bug fix after its investigation is reviewed. Invoke as /implement-task."
---

# Goal

Implement a specific task from the tasks document — or a reviewed bug fix — end-to-end.

## Input contract — resolve the target first

Accept whatever the invocation provides and resolve three things before starting: the
**tasks doc**, the **task** (its section in that doc), and the **prefix** (the
reference-file family). Any of these forms is enough:

- **Prefix + task number** (`/implement-task auth_oauth 3`) — the tasks doc is the doc
  owning the prefix (typically `{prefix}_tasks.md`); the task is its Task 3 section.
- **Tasks-doc path alone** — pick the first task that is not Done and whose dependencies
  are met; if several are equally next, ask which.
- **A short description** ("the retry-logic task in the payments tasks doc") — locate the
  matching task heading in the named (or only plausible) tasks doc; if the match isn't
  certain, ask.
- **A bug target** ("implement the fix for BUG-123", an investigation-doc path) — the
  reference files are `{bug_id}_investigation.md` and the fix-mode techspec if one exists.
  A tasks doc is optional — many fixes have none: then the "task" is the investigation's
  proposed minimal fix and the investigation doc stands in for the tasks doc. The **fix
  lens** below applies. If the investigation has no `## Review` block, flag it and suggest
  `/review-artifact` first — confirm with the user before implementing on an unreviewed
  investigation.
- **Nothing usable** — if exactly one `*_tasks.md` with open tasks exists in the working
  tree, use it; otherwise ask rather than guess.

Derived: **prefix** = the tasks doc's base-name family; **reference files** = the prefix's
sibling docs (analysis / techspec / tasks; for fixes: investigation / techspec). Echo the
resolved (tasks doc, task, prefix) triple back before implementing.

## Pre-Implementation Checklist

- [ ] Task dependencies are completed (verify in tasks file)
- [ ] I understand the acceptance criteria (for a fix: the investigation's expected
      behavior plus the techspec's ACs)
- [ ] I have reviewed related files in the techspec
- [ ] For vertically-ordered (greenfield) tasks: I understand the user-observable behavior
      this task moves forward

## Fix lens — applies whenever the target is a bug fix

Orthogonal to the workflows below, not a separate mode:

- Implement the reviewed investigation's proposed solution as described, honoring the
  fix-mode techspec's blast-radius notes; work at the exact `file:line` the investigation
  identified.
- Keep changes minimal and focused on the root cause — no drive-by cleanup (the scope
  guard below is binding).
- Tests must cover the bug scenario that was fixed and the edge cases the techspec's
  impact section names; update existing tests affected by the change; all pass before Done.
- Note any deviation from the proposed solution — and why — in the task's (or
  investigation's) section rather than deviating silently.

## Scope guard — all work types

When implementation surfaces work beyond the task's boundaries:

- **Critical issues** (bugs in surrounding code, architectural problems, code that needs
  refactoring for safety) → STOP, document the issue, propose it separately, and get
  explicit approval before proceeding. Never fold it into the current task — even in
  auto-accept mode.
- **Nice-to-haves** ("while we're here" improvements not required by the task) → capture
  them as named follow-ups in the prefix's reference files; do not implement them now.

## Process

**MUST DO**: Execute Workflows 1 and 3

> **No per-task code review.** The reviewer fan-out that used to run here as Workflow 2 was
> retired (token economics: it re-loaded the same context once per task to review a small
> diff). Code review now happens once per prefix, batched, via `/review-implementation` —
> see the last-task hook in Workflow 3. Numbering keeps Workflow 3's name for symmetry with
> `implement-task-loop`.

### Workflow 1 - Implementation

1. Create todo list with all steps for that process.
2. Context: Read all relevant files, starting with the prefix's reference files
3. Plan implementation: Create a step-by-step implementation plan
4. Implement: Write the code following the techspec and coding standards

   - Follow chosen architecture
   - Follow codebase conventions strictly
   - Write clean, well-documented code
   - Update todos as you progress

5. Test: Write/run tests according to the testing requirements
6. Build with no errors
7. **Verify (use the `verify-task` skill).** Run with:
   - `task_id`: the resolved task (for a tasks-doc-less fix: the bug id)
   - `tasks_doc_path`: the resolved tasks doc (for a tasks-doc-less fix: the
     investigation doc)
   - `prefix`: the resolved prefix
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
3. Update the prefix's reference files with any decisions made during the implementation.
   If implementation revealed gaps in the analysis/techspec, note them in the task's
   section — don't silently rewrite the upstream doc. Record deviations from the spec with
   rationale.
4. Provide summary with modified/created files
5. **Last-task suggest hook:** if every task in the prefix's tasks document is now marked Done, suggest `/review-implementation prefix={prefix}` (batched code review) followed by `/qa-gates prefix={prefix}` before declaring the feature/refactor complete. (Suggestions only — the user invokes them.) If earlier tasks remain, do not suggest yet — unless the task list is long (>~6 tasks) and a natural boundary was just crossed, in which case a mid-run `/review-implementation prefix={prefix} scope=…` may be worth suggesting. A tasks-doc-less fix is its own last task: suggest both immediately after Workflow 3.
