---
description: Implement a specific task from a slice's tasks document.
argument-hint: <slice> <task>
arguments: slice task
---

# Goal

Implement one task from a slice's tasks document.

**Slice**: $slice
**Task**: $task

## Pre-implementation checklist

- [ ] Task dependencies are completed (verify in the slice's `tasks.md`)
- [ ] I've read the slice's PRD, techspec, and the task's acceptance criteria
- [ ] I understand the user-observable behavior this task moves forward (check the task's "Why this task is on the list" line)

## Process

**MUST DO**: Execute Workflows 1, 2, and 3.

### Workflow 1 — Implementation

1. Create todo list.
2. Context: read all relevant files in `specs/slices/$slice/` (PRD, techspec, tasks).
3. Plan: step-by-step implementation plan for the task.
4. Implement:
   - Follow the techspec's chosen approach
   - Follow codebase conventions strictly (or the host repo's conventions in exploratory mode)
   - Update todos as you progress
5. Test: write/run tests according to the techspec's test approach.
6. Build with no errors.
7. **Verify (use the `verify-task` skill).** Run with:
   - `task_id`: $task
   - `tasks_doc_path`: `specs/slices/$slice/tasks.md`
   - `prefix`: `specs/slices/$slice`
   - `artifact_path`: (default — the task's section in `specs/slices/$slice/tasks.md`)

   The skill runs gates 1+2+3 (build/test, AC checklist, cross-cutting) against just this
   task's ACs / files / budgets and records a `## Verify — {date}` block in the task's
   section. Halt on any gate fail until resolved (fix the code, or record `accepted: <reason>`
   in the gate-line). Do NOT advance to Workflow 2 — Review until every gate is `pass` or
   `accepted`. Skip the skill call for trivial tasks (one-line config tweak, typo,
   doc-only edit) — see the skill's "When NOT to use" section.

### Workflow 2 — Review

1. Create todo list.
2. **DO NOT SKIP**: evaluate the need for code-review. If non-trivial, launch the @code-reviewer-agent.
3. Consolidate findings. Identify highest-severity issues.
4. Present to user. Ask: fix now / fix later / proceed as-is.
5. Address based on user decision.

### Workflow 3 — Post-implementation

1. Create todo list.
2. Update task status in `specs/slices/$slice/tasks.md` (Not started → Done). Update the slice's overview table progress %.
3. If implementation revealed gaps in the PRD or techspec, write a brief note in the task's section. Don't silently rewrite the PRD/techspec.
4. Provide summary: modified/created files.

## Slice-close hook

If this is the last task in the slice, also:

5. Run through the slice PRD's Done-when checklist. Confirm every box passes.
6. Run the techspec's manual smoke test.
7. **"While we're here" guard:** any additions or improvements that surfaced during the slice but weren't required by the slice PRD — **don't** add them now. Capture them in the next slice's backlog (a brief edit to the next slice's row in the master roadmap §N+4, or a stub PRD if the next slice doesn't have one yet).
8. **Suggest `/qa-gates prefix=specs/slices/$slice`** — the gates verify the implementation against the slice's techspec/tasks (build/test → AC → cross-cutting → docs → human go/no-go). Skip the suggestion only if you've already run it this session.
