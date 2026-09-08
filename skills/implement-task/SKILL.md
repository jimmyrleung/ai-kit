---
name: implement-task
description: "Implements and verifies one task from an implementation tasks doc, or applies a bug fix after its investigation is reviewed. Use to implement, work on, or pick up a task or reviewed fix. Accepts a prefix, tasks-doc path, task number, bug ID, investigation doc, or short description; a tasks doc is optional for fixes. Batched code review belongs to review-implementation."
---

# Goal

Apply the [confidence contract](references/shared/confidence.md) using the delivery rubric.
Record the effective policy and explicit score, evidence, uncertainty consequences, next
checks and advancement verdict; pass the policy to workers and downstream gates.

Implement a specific task from the tasks document — or a reviewed bug fix — end-to-end.

Apply the [engineering change contract](references/shared/engineering-change.md):
inspect repository context, reuse suitable code/tests, and justify new files within scope.
Resolve bundled references relative to this skill folder.

Follow [authorized work](references/shared/authorized-work.md) for existing permission,
blocking questions, and requested discussion cadence; resolve from this skill folder.

## Input contract — resolve the target first

Accept whatever the invocation provides and resolve three things before starting: the
**tasks doc**, the **task** (its section in that doc), and the **prefix** (the
reference-file family). Any of these forms is enough:

- **Prefix + task number** (`implement-task auth_oauth 3`) — the tasks doc is the doc
  owning the prefix (typically `{prefix}_tasks.md`); the task is its Task 3 section.
- **Tasks-doc path alone** — pick the first task that is not Done and whose dependencies
  are met within the requested lifecycle boundary (default `pre-merge`); when the request authorizes the task stream, use document order among equally ready tasks. Ask only if priority or scope requires an owner decision. Do not select deployment/live work merely because repository tasks finished.
- **A short description** ("the retry-logic task in the payments tasks doc") — locate the
  matching task heading in the named (or only plausible) tasks doc; if the match isn't
  certain, ask.
- **A bug target** ("implement the fix for BUG-123", an investigation-doc path) — the
  reference files are `{bug_id}_investigation.md` and the fix-mode techspec if one exists.
  A tasks doc is optional — many fixes have none: then the "task" is the investigation's
  proposed minimal fix and the investigation doc stands in for the tasks doc. The **fix
  lens** below applies. Validate investigation review content/scope/dependencies using the [change evidence contract](references/shared/change-evidence.md). If review is missing, stale, or not approved, flag it and suggest
  the review-artifact skill first — confirm with the user before implementing on an unreviewed
  investigation.
- **Nothing usable** — if exactly one `*_tasks.md` with open tasks exists in the working
  tree, use it; otherwise ask rather than guess.

Derived: **prefix** = the tasks doc's base-name family; **reference files** = the prefix's
sibling docs (analysis / techspec / tasks; for fixes: investigation / techspec). Echo the
resolved (tasks doc, task, prefix) triple back before implementing.

## Pre-Implementation Checklist

- [ ] Task dependencies and lifecycle prerequisites are met; write/resource conflicts are
      serialized or have explicit isolation and reconciliation (verify in tasks file)
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
> diff). Code review now happens once per prefix, batched, via the review-implementation skill —
> see the last-task hook in Workflow 3. Numbering keeps Workflow 3's name for symmetry with
> `implement-task-loop`.

### Workflow 1 - Implementation

1. Create todo list with all steps for that process.
2. Context: inspect all relevant files, starting with the prefix's reference files
3. Plan implementation: Create a step-by-step implementation plan. Resolve the effective
   confidence policy from the task/spec/investigation and applicable instructions; calculate
   the delivery rubric before the first dependent edit. Below threshold or with missing
   load-bearing evidence, block that edit and name the next check; continue independent
   authorized inspection and partial drafting. Refresh the assessment at verification handoff.
4. Implement: Write the code following the techspec and coding standards

   - Follow chosen architecture
   - Follow codebase conventions strictly
   - Write clean, well-documented code
   - Update todos as you progress

5. Test: add/extend meaningful tests in the suitable existing home (or justify a new file)
   and run required checks. Capture command/output and source/test/config/environment/build
   identities under the change evidence contract.
6. Build with no errors when the repository/change requires a build. Pass fresh executed
   evidence to verification so identical checks need not run twice; record any inapplicable
   check with its reason. Missing required execution remains BLOCKED.
7. **Verify (use the `verify-task` skill).** Run with:
   - `task_id`: the resolved task (for a tasks-doc-less fix: the bug id)
   - `tasks_doc_path`: the resolved tasks doc (for a tasks-doc-less fix: the
     investigation doc)
   - `prefix`: the resolved prefix
   - `check_evidence`: actual executed check records with identities, commands, results and output locators
   - `confidence_policy`: the complete effective policy, assessment and unresolved consequences; retain fix severity/causal requirements and stricter gates
   - `base`, task/fix locator and designated AC sources, intended paths and dependencies:
     resolved per the change evidence contract; no fixed history window
   - `artifact_path`: (default — the task's section in `tasks_doc_path`)

   The skill runs gates 1+2+3 (build/test, AC checklist, cross-cutting) against just this
   task's ACs / files / budgets and records a properly nested, delimited Verify block in the task's
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
5. **Last-task suggest hook:** if every `pre-merge` task in the prefix's tasks document is now marked Done (existing repository-only docs default to `pre-merge`), suggest the review-implementation skill with `prefix={prefix}` (batched code review) followed by the qa-gates skill with `prefix={prefix}` before declaring the feature/refactor complete. (Suggestions only — the user invokes them.) Keep pending `deploy`/`live` tasks visible with their evidence requirements; repository GO does not complete or authorize them. If earlier repository tasks remain, do not suggest yet — unless the task list is long (>~6 tasks) and a natural boundary was just crossed, in which case a mid-run review-implementation pass with `prefix={prefix}` and `scope=…` may be worth suggesting. A tasks-doc-less fix is its own last task: suggest both immediately after Workflow 3.
