---
name: techspec
description: "Designs the implementation blueprint for a defined feature, greenfield, refactor / tech-debt, bug-fix, hotfix, or incident-remediation work. Use to write a technical specification, design doc, implementation/refactor plan, or impact analysis from an analysis, reviewed investigation, requirements, or high-level plan. Produces techspec.md; task decomposition belongs to tasks-breakdown."
---

# techspec - committed design blueprint

## Goal

Produce the committed technical specification for defined work: the blueprint a developer implements from. You DECIDE and SPECIFY — one approach, file-by-file, with the tests that lock each behavior.

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

1. When available, use subagents for doing the exploration for distinct areas.

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

### QA-scenario pass

With the spec written, make an independent QA-scenario pass (one authorized worker when available; otherwise a separate pass with that limitation stated) to derive scenarios that would exercise it: happy path, error conditions, the edge cases called out by the design, and integration points when the change crosses a component or system boundary.

- Every behavior the spec commits to maps to at least one scenario
- Each scenario gets a priority (High/Med/Low) and an automatable-or-manual flag.
- Proportionality: heavyweight matrices (browser/device, full accessibility sweep, security audit) enter only when the work demands them; for most work a tight functional scenario list is enough.
- **Perf/regression scenarios:** when the work touches a perf-sensitive surface (hot path, DB query shape, caching, payload size), consult the repo-local perf/regression skill if the repo has one (baselines are repo-specific — never invent generic thresholds); no local skill → name the perf risk as a manual scenario and flag the gap (a candidate for the `close` skill's repo-local skill mint).

### Write the Techspec

1. With the exploration, consolidation and design done:

- Read `./references/TEMPLATE.md` thoroughly
- According to the detected mode additional guidance, define the final template structure
- Write the techspec document following the final template structure defined
- This step can be considered done when every section of the template is filled out

2. Write the techspec doc: write it within `./specs/[slug]/techspec.md` where slug is a given task/user story identifier (an id, a snake_case_meaningful_name, etc.). If the input was a requirements doc, put the techspec alongside it.

### Review

At the end, provide a copy-paste prompt to launch a separate agent for an adversarial review for the written techspec doc according to this whole process.
