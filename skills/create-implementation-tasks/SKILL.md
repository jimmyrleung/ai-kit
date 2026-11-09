---
name: create-implementation-tasks
description: "Designs the implementation blueprint for a defined feature, greenfield, refactor / tech-debt, bug-fix, hotfix, or incident-remediation work already broken down in tasks. Use to write a technical specification, design doc, implementation/refactor plan, or impact analysis from an analysis, reviewed investigation, requirements, or high-level plan, including task decomposition; Produces all implementation tasks required to complete that implementation;"
---

# create-implementation-tasks

## Goal

Produce the committed technical specification for defined work broken down in tasks: a developer can complete the implementation by following each task of the designed blueprint. You DECIDE and SPECIFY — one approach, file-by-file, with the tests that lock each behavior.

## Approach

**The approach should follow each subsection below sequentially.**

### Initial context

Ensure you have enough information to get started on designing the solution. It is expected that the user shares one of the following:

- A reviewed requirements document, usually produced with the `define-reqs` skill
- A reviewed investigation with enough details and high confidence score to proceed
- A high-level implementation plan, usually built with plan mode

> If not provided, or it is too vague, pause and ask the user what's the initial context.

Inspect the input(s) end-to-end and confirm its understanding.

### Detect mode

1. Detect what type of work (usually can be inferred from the input):

- feature integration: implement a new feature or updating an existing feature in an existing codebase
- greenfield: new implementation on an empty or non-existing repo (or an existing repo but no codebase detected)
- refactor or techdebt: reestructuring, consolidating, eliminating tech-debt, etc. - any work that indicates no new capability
- bugfix:
- if you detect it is an initial analysis/scope definition, an investigation, or an exploration, suggest the following skills:
  - initial analysis / scope definition → `define-reqs`
  - investigation/exploration → `lay-of-the-land` or simply fan-out of explore agents

2. If you can't infer from the input, confirm with the user the detected mode.

3. Once confirmed, read the additional guidance for the detected mode:

- feature integration: `./references/feature-integration-guidance.md`
- greenfield: `./references/greenfield-guidance.md`
- refactor or tech debt: `./references/refactor-techdebt-guidance.md`
- bugfix: `./references/bugfix-guidance.md`

### Explore

Explore the references from the input(s) provided and double check it. Do not assume they are 100% correct, and do not rely on summaries. It is expected that you at least:

- Explore affected files and modules
- Understand interfaces and integration points
- Identify callers and who is called
- Identify which data is involved with that feature
- Explore existing configuration, persistence layers, error handling patterns, tests, and infrastructure

Then, explore anything else that might be relevant and was not pointed out in the requirements doc or needs more depth: relevant docs, repos, components, libs, config, etc.

Exploration should only be considered complete when we can name each new or modified components involved with the implementation and where they land.

#### AGENTS.md

Read the `AGENTS.md` / `CLAUDE.md` and any associated rules and architectural guidance docs that exist on the involved repos to make sure the implementation plan follows their standards and conventions.

#### Subagents guidance

1. When available and applicable, use subagents for doing the exploration for distinct areas.

2. Each subagent should be doing one focused exploration for reduced degradation.

### Ask clarification questions

Ask any questions to the user that the previous exploration couldn't answer or any decisions that the user needs to make. Examples are: domain questions, workflows and data flows, expected behavior, external dependencies, interfaces, critical path, testing, etc.

### Consolidate and design

With full context gathered and questions answered, consolidate everything and proceed to consolidating everything.

Plan file-by-file. API contracts, data models, components — only what this work actually needs. Key algorithms, error paths, edge cases, and the tests that lock each behavior.

#### Design approaches

Techspecs should always follow one of the following design approaches:

- **minimal-changes** — smallest diff, maximum reuse of what exists.
- **clean-architecture** — maintainability, elegant abstractions, willing to refactor a little.
- **pragmatic-balance** — speed + quality; ships safely and leaves the codebase slightly better, no over-engineering.

You must decide which approach to follow according to the additional guidance for the detected mode.

If you explored multiple approaches, present a comparison to the user with key information so they can make the decision on which one to choose with their respective confidence score.

#### Anti-overengineering

This is a mandatory guidance you should follow when designing the solution. Identify the following:

- Overengineering, unnecessary abstractions, and unnecessary complexity
- Excessive validation, safety checks, fallbacks, or defensive branches
- Handling of unrealistic or unsupported edge cases
- Duplicate checks or layers with no clear owner
- Code made harder to understand for minor benefits
- Unrelated cleanup
- Excessive test files and tests
- Introducing new patterns/conventions instead of using existing ones
- Variables and methods with names that doesn't follow existing naming conventions or patterns

Once identified, evaluate what's really important and should be kept or not.

- What's really important guidance: anything that **really** prevents performance, scalability, availability, maintainability, or security issues.

Confirm with the user what to keep and what to remove.

#### Confidence score

Use an explicit 0–100% assessment for the scoped conclusion or next workflow step.
This is a structured judgment of evidence and remaining uncertainty, not a calibrated
probability of correctness, success, or safety. A score never supplies facts, turns
worker agreement into proof, passes an unrun/failed check, or grants authorization.

Factors and weights:

- API/docs and requirements clarity 30%
- Suitable inspected patterns 25%
- Data-flow/dependency understanding 20%
- Complexity understood and controlled 15%
- Cross-system impact understood and bounded 10%

You should include the breakdown in the final techspec document, but also report a summary of it to the user at the end after writing the document in the following format:

```
Confidence: X% - {justification}
Remaining uncertainty: {justification}
```

### Write the techspech

1. With the exploration, consolidation and design done:

- Read `./references/TEMPLATE.md` thoroughly
- According to the detected mode additional guidance, define the final template structure
- Write the techspec document following the final template structure defined
- This step can be considered done when every section of the template is filled out

2. Write the techspec doc: write it within `./specs/[slug]/techspec.md` where slug is a given task/user story identifier (an id, a snake_case_meaningful_name, etc.). If the input was a requirements doc, put the techspec alongside it.

### Break it down in tasks

1. Inventory the work: requirements, acceptance criteria, technical decisions, components, test scenarios, migrations, config. change, infrastructure, DI registration, etc. and group by logical boundary.

2. Size each candidate to the grain using Sizing; keep an atomic L task only with the stated reason rather than applying a conflicting fixed time cutoff.

3. Identify cross-task dependencies (compile-time, runtime, deploy-time).

4. Identify cross-repo work: if possible, we should tackle the work repo-by-repo:

- good: work on repo 1 → work on repo 2 (which depends on repo 1 work) → work on repo 3 → complete work
- bad: work on repo 1 → work on repo 2 → work on repo 1 again → work on repo 3 → work on repo 2 again → ...

5. Order the work by dependencies and resource conflicts, identifying which ones could run in parallel.

- Ideally, we should follow an order that makes sense: infra → config → database → backend → frontend → tests
- For multi-repo work, follow the previous structure, but within each repo: repo 1 (infra → config → database → backend → frontend → tests), then repo 2 (infra → config → database → backend → frontend → tests), then repo 3 (infra → config → database → backend → frontend → tests)

6. Ensure every task contains tests or explicitly says "tests for this task are covered in Task X" - none should be silently uncovered.

7. Propose the implementation order: Build a list of tasks and also the dependency graph according to the following guidance:

- It is expected a list of at most 15 tasks
- we should try to follow a balanced approach: mid-size tasks, "okay" quantity, where each task is big enough to be its own checkpoint, and small enough to finish without fatigue/context deprecation pressure

8. Present the list and the dependency graph to the user and ask for confirmation. Include the confidence score summary according to the following guidance:

    ````markdown
    ```
    Confidence: X% - {justification}
    Remaining uncertainty: {justification}
    ```

    and for getting these numbers, you should follow the following confidence score guidance:

    Use an explicit 0–100% assessment for the scoped conclusion or next workflow step.

    This is a structured judgment of evidence and remaining uncertainty, not a calibrated probability of correctness, success, or safety. A score never supplies facts, turns worker agreement into proof, passes an unrun/failed check, or grants authorization.

    Factors and weights:

    - Fidelity to approved design/locked decisions and requirement coverage 35%
    - Dependency, lifecycle and resource closure 25%
    - Test/AC ownership and executable checks 25%
    - Task boundaries, sizing and path grounding 15%

    **IMPORTANT**: You should include the breakdown details in the final tasks-breakdown document.
    ````

9. Once approved, write the tasks document:

- Read `./references/TEMPLATE_TASKS.md` thoroughly and write the `./specs/[slug]/tasks.md` document following the template structure. This should be a summary of all tasks with their respective dependency graph.
- Then, read `./references/TEMPLATE_TASK.md` and write one document for each task following the template structure. Use sequence numbers for each document like `task_01.md`, `task_02.md`, [...], and persist them alongside the `tasks.md` document written in the previous step.

  > The [slug] mentioned in the paths are: a given task/user story identifier (an id, a snake_case_meaningful_name, etc.)

### Review

At the end, provide a copy-paste prompt to launch a separate agent for an adversarial review for the written techspec doc and tasks breakdown according to this whole process.
