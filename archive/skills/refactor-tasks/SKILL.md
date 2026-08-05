---
name: refactor-tasks
description: Break a reviewed refactoring plan into an ordered list of implementation tasks by exploring three sizings in parallel — granular / balanced / pragmatic — then committing to one with the user. Each task has dependencies, rollback, and testing requirements. Produces {refactor_name}_tasks.md. Use ad-hoc, or as Phase 4 of /refactor-techdebt-dev.
---

# Refactor Tasks Skill (3-way exploration)

You break a refactoring plan into small, specific, testable tasks that can be implemented one at a time — each independently completable, each with a rollback path. Refactoring is high-risk; sequencing for safety matters as much as decomposing for clarity. This skill explores three sizings side by side and then commits to one.

> **Litmus test:** if a task can't be tested in isolation, or has no rollback path, it's not done. If you can't say "this task is finished" with a single observable check, split it further.

## When to use

- **Ad-hoc**: you have an approved refactor plan and need a sequenced task list to drive implementation.
- **Orchestrated**: Phase 4 of `/refactor-techdebt-dev`.

## When NOT to use

- No plan yet — produce the plan first (`refactor-plan`). Tasks without a plan drift into re-designing the refactor.
- The plan hasn't been approved by the user — tasks generated against an unapproved plan are throwaway work.

## Coordinator vs worker

- **No mandate handed to you (default — you're on the main thread):** you're the *coordinator*.
  1. Read the inputs (refactor description + reviewed audit + approved plan) carefully, every dependency / rollback / metric.
  2. Launch **1–3 `@refactoring-tasks-creator-agent` sub-agents in parallel**, each handed the inputs and one mandate:
     - **granular** — smaller tasks, higher quantity; maximum checkpointing, easier rollback per task, more overhead.
     - **balanced** — mid-size tasks, reasonable overhead; each big enough to be its own checkpoint, small enough to finish without fatigue.
     - **pragmatic** — bigger tasks, fewer; faster but more risk per task.
  3. When they return, compare. Form your opinion on which fits *this* refactor, considering: team experience, risk tolerance, urgency, complexity — and that tasks will be executed one at a time.
  4. Present to the user: a brief summary of each sizing, a trade-offs comparison, your recommendation with reasoning.
  5. Ask the user which sizing they prefer.
  6. Build the final tasks document at the chosen sizing, run the confidence gate, and write the file.
- **You were spawned as a `@refactoring-tasks-creator-agent` worker with a mandate:** you're a *worker*. Decompose the plan **at your assigned sizing only** and return your draft tasks list to the coordinator. **Do not** spawn further sub-agents and **do not** write a file.

## Input contract

Expect, in order of authority:
1. **Approved refactor plan** (`{refactor_name}_plan.md`) — authoritative for phases, rollback strategy, success metrics, testing strategy. **Required.** If missing, stop and tell the user — don't generate tasks from an audit alone.
2. **Reviewed audit** (`{refactor_name}_audit.md`) — authoritative for files affected, dependencies, scope boundaries.
3. **Refactor description** — the requirement.

Derive the `{refactor_name}` base name from the inputs; ask if not discoverable.

## Process (per sizing — what each worker does, and what the coordinator does for the final)

1. **Review previous phases' outputs.** Refactor description → audit → plan, in order. The tasks doc lives or dies on how accurately it translates the plan into a sequence.
2. **Extract work items from the plan.** Every code change called for: group related changes, look for dependencies between changes.
3. **Break into atomic tasks at your sizing.** Each task should modify only related files, have a single clear objective, be testable in isolation, fit in one session (< 4h ideal — see size guidelines below). Granular pushes toward S; pragmatic tolerates more L; balanced stays in the middle (4–10 tasks total, usually).
4. **Sequence for safety.** Start with low-risk tasks. Build infrastructure before using it. Add tests before refactoring code. Validate each step before moving forward. Order by dependencies (topological sort). Mark parallelizable tasks ("Can run in parallel with: Task X").
5. **Define per-task rollback.** Every task names how to undo it — specific commands or steps, not generic "git revert." If a task has no clean rollback, flag it and consider splitting.
6. **Define per-task testing.** Each task contains tests **or** explicitly says "tests covered in Task X" — no task silently has zero coverage. Specify unit / integration / manual; name the target test file.
7. **Coordinator: present sizings & gate.** Present to the user: brief summary of each sizing, trade-offs, your recommendation. Ask which to take. Build the final tasks doc.
8. **Confidence gate.** Score 0–100% using the user's global CLAUDE.md factor breakdown (≈ plan completeness 30% / pattern fit 25% / dependency clarity 20% / testability 15% / rollback viability 10%). **If < 90%: STOP and ask clarifying questions.** At ≥ 90%, write the file.

### Task size guidelines

- **S** (1–2h): single file or small focused change, clear straightforward implementation, minimal risk. *e.g. "Extract constant to config file."*
- **M** (2–4h): multiple related files, some complexity, moderate risk. *e.g. "Move authentication logic from controller to service."*
- **L** (4–6h): many files or complex logic, requires careful planning, higher risk. *e.g. "Migrate DB schema and update all queries."*
- **> 6h → split it further.**

## Required sections

The final tasks document includes:

- **Header / companion docs** — names the refactor, links the companion docs (refactor description, audit — *"authoritative for scope/files/dependencies"* — plan — *"authoritative for phases/rollback/metrics"*), and states the chosen sizing + task count: `**Approach:** Balanced (N tasks, mid-size grouping)` (or Granular / Pragmatic).
- **Tasks overview** — a progress table:
  | Task | Title | Complexity | Est. Time | Depends On | Status |
  with `**Overall Progress**: 0/N tasks completed (0%)`, `**Last Updated**: {YYYY-MM-DD}`, and a parallelism note if relevant.
- **Tasks dependency graph** — short ASCII or numbered list showing the order; parallel opportunities called out explicitly.
- **Detailed tasks** — per task:
  - **Status**: Not Started
  - **Description** (1–3 sentences, why it's its own task)
  - **Complexity** / **Risk** (Low/Med/High) / **Estimated Time** / **Depends On** / **Can Run In Parallel With**
  - **Objective** (what + why)
  - **Files to modify** (`path` — what changes)
  - **Implementation steps** (numbered, specific; reference the plan — "Apply pattern from plan §3.2" — don't re-derive it)
  - **Testing requirements** — Unit / Integration / Manual; or "Tests covered in Task X"
  - **Implementation checklist** — read related code, write failing tests first (TDD), implement, all tests pass
  - **Rollback plan** — specific instructions for undoing this task
  - **Notes** — running log
- **Confidence score** — global CLAUDE.md format.

## Optional sections (include only with substance)

Parallel opportunities (if the dependency graph doesn't make them obvious) · Deployment sequencing (multi-service / multi-repo refactors) · Definition of Done (when per-task criteria aren't enough — e.g. a multi-PR ship checklist) · Task-level risks (where acceptance criteria don't cover the risk).

**Rule:** if a section has no substance, delete it — don't leave a placeholder.

## Task writing best practices

**Good task names** (specific verb + specific noun): "Extract user validation logic into UserValidator class" · "Replace hardcoded product IDs with ProductConfig enum."

**Bad task names** (vague): "Refactor code" · "Fix issues" · "Improve architecture."

**Granularity rules:**
- Too large (> 6h): "Refactor entire checkout module" → break into setup / migration / testing / cleanup.
- Just right (2–4h): "Move authentication logic from controller to service."
- Too small (< 30 min): "Rename variable x to y" → combine with related tasks unless high-impact.

**Dependency rules:**
- Task X depends on Task Y when X literally cannot start without Y done — don't create fake dependencies for ordering preferences.
- Be explicit about what each task unblocks.

## Important rules

1. **One task, one objective** — don't combine unrelated changes.
2. **Testable in isolation** — each task verifiable independently.
3. **Small wins** — prefer many small tasks over few large ones.
4. **Low-risk first** — start with infrastructure, tests, low-risk changes.
5. **Update as you go** — keep task status current.

## Output file

Write the final tasks document to `{refactor_name}_tasks.md`, alongside the refactor description, audit, and plan. If no base name is discoverable, ask the user before writing. (Workers return drafts and write nothing.)
