---
name: tasks-breakdown
description: "Turns an approved and reviewed spec or plan into ordered implementation tasks with dependencies, files, tests, and acceptance criteria. Use to break work into tasks or create a tasks doc/list for a new implementation. Produces tasks.md and sequential tasks documents (task_01.md, task_02.md, ...). A deliberate spec-carrying path embeds design decisions when the user chooses to skip a separate techspec."
---

# tasks-brakdown - ordered implementation tasks

## Goal

Goal: Decompose an approved and reviewed spec or plan into an ordered, executable implementation tasks document, where:

- Each task is an increment with clear scope and explicit dependencies
- Each task is independently startable, testable, and completable.

**IMPORTANT**: You TRANSLATE the spec or plan into a sequence; you do **not** re-design it (that's the `techspec` skill) or implement it (that's the `implement-task` skill).

## Approach

### Initial context

Ensure you have enough information to get started on the tasks breakdown. It is expected that the user provides one of the following:

- An approved and reviewed techspec document, usually produced with the `techspec` skill
- An implementation plan with enough details and high confidence score to proceed
- A detailed implementation request with solid references, like similar past implementations, examples, etc.

1. Inspect the input(s) end-to-end and confirm they have no blockers to proceed with the breakdown.

2. Read the AGENTS.md file(s) and any referenced documents (especially rules) to gather context from each project involved.

### Inventory

1. Inventory the work: requirements, acceptance criteria, technical decisions, components, test scenarios, migrations, config. change, infrastructure, DI registration, etc. and group by logical boundary.

2. Size each candidate to the grain using Sizing; keep an atomic L task only with the stated reason rather than applying a conflicting fixed time cutoff.

### Define the order

1. Identify cross-task dependencies (compile-time, runtime, deploy-time).

2. Identify cross-repo work: if possible, we should tackle the work repo-by-repo:

- good: work on repo 1 → work on repo 2 (which depends on repo 1 work) → work on repo 3 → complete work
- bad: work on repo 1 → work on repo 2 → work on repo 1 again → work on repo 3 → work on repo 2 again → ...

3. Order the work by dependencies and resource conflicts, identifying which ones could run in parallel.

- Ideally, we should follow an order that makes sense: infra → config → database → backend → frontend → tests
- For multi-repo work, follow the previous structure, but within each repo: repo 1 (infra → config → database → backend → frontend → tests), then repo 2 (infra → config → database → backend → frontend → tests), then repo 3 (infra → config → database → backend → frontend → tests)

### Testing double-check

Ensure every task contains tests or explicitly says "tests for this task are covered in Task X" - none should be silently uncovered.

### Propose the implementation order

Build a list of tasks and also the dependency graph according to the following guidance:

- It is expected a list of at most 15 tasks
- we should try to follow a balanced approach: mid-size tasks, "okay" quantity, where each task is big enough to be its own checkpoint, and small enough to finish without fatigue/context deprecation pressure

Present the list and the dependency graph to the user and ask for confirmation.

This step is complete when the user approves the proposal.

#### Confidence score

When presenting the proposed list of tasks and the dependency graph, you should also provide the confidence score summary in the following format:

```
Confidence: X% - {justification}
Remaining uncertainty: {justification}
```

and for getting these numbers, you should follow the following confidence score guidance:

Use an explicit 0–100% assessment for the scoped conclusion or next workflow step.
This is a structured judgment of evidence and remaining uncertainty, not a calibrated
probability of correctness, success, or safety. A score never supplies facts, turns
worker agreement into proof, passes an unrun/failed check, or grants authorization.

Factors and weights:

- Fidelity to approved design/locked decisions and requirement coverage 35%
- Dependency, lifecycle and resource closure 25%
- Test/AC ownership and executable checks 25%
- Task boundaries, sizing and path grounding 15%

**IMPORTANT**: You should include the breakdown details in the final tasks-breakdown document.

### Write the tasks document

With the proposal approved by the user:

1. Read `./references/TEMPLATE_TASKS.md` thoroughly and write the `./specs/[slug]/tasks.md` document following the template structure. This should be a summary of all tasks with their respective dependency graph.

2. Then, read `./references/TEMPLATE_TASK.md` and write one document for each task following the template structure. Use sequence numbers for each document like `task_01.md`, `task_02.md`, [...], and persist them alongside the `tasks.md` document written in the previous step.

> The [slug] mentioned in the paths are: a given task/user story identifier (an id, a snake_case_meaningful_name, etc.)