---
name: define-reqs
description: "Maps entry points, existing patterns, scope, and risks for a defined feature integration, new project, or refactor / tech debt, producing a complete requirements document. Use when asked to analyze, audit, scope, or map upcoming work before design or implementation. Produces requirements.md; should not be used to explore/investigate current-state without a defined change/new work; solution design belongs to techspec."
---

# define-reqs - pre-implementation reference map and scope definition

## Goal

Your goal is to map where upcoming work will land and what it must respect:

- where changes happen
- which existing patterns to follow
- which similar features to copy
- what risks breaking (blast radius)

You must **LOCATE and REFERENCE**, and **must not** DESIGN and SPECIFY as design comes next (techspec / plan phase).

- If a developer can copy-paste your output and start cooding, you've gone too deep.

## Approach

**The approach should follow each subsection below sequentially.**

### Initial context

Ensure you have enough information to get started on defining requirements. It is expected that the user shares one of the following:

- An inline prompt with details
- An input file with initial requirements and past implementation specs to be used as reference or any relevant context
- A folder containing a set of relevant files to be analyzed
- A `lay-of-the-land` document

> If not provided, or it is too vague, pause and ask the user what's the initial context.

### Detect mode

1. Detect what type of work are you going to do:

- feature integration: implement a new feature or updating an existing feature in an existing codebase
- greenfield: new implementation on an empty or non-existing repo (or an existing repo but no codebase detected)
- refactor or techdebt: reestructuring, consolidating, eliminating tech-debt, etc. - any work that indicates no new capability
- If you find out it is a bugfix, an investigation, or an exploration, suggest the following skills:
  - bugfix → `bug-investigation`
  - investigation/exploration → `lay-of-the-land` or simply fan-out of explore agents

2. Confirm with the user the detected mode.

3. Once confirmed, read the additional guidance for the detected mode:

- feature integration: `./references/feature-integration-guidance.md`
- greenfield: `./references/greenfield-guidance.md`
- refactor or tech debt: `./references/refactor-techdebt-guidance.md`

### Understand the work

Based on the initial context, ask clarification questions until you can establish: definition, scope (what's in-scope and out-of-scope), expected outcome, constraints, edge cases, dependencies. Record the Q&A.

For technical requirements (like package upgrade, using a new lib, etc.), use `web search` or `context7` to query relevant docs

### Explore

Once you have clear definition of the work, start the exploration phase to identify:

- Entry points (routes, controllers, jobs)
- Similar features and patterns
- Reusable utilities/services
- Feature boundaries
- Configuration
- For integration/refactor: Examine every file the description names
- For greenfield: explore the constraint space instead — chosen-stack conventions, comparable ecosystem examples, hard requirements

#### Exploration guidance

- **Coverage gaps are defined by the consumer, not the provider.** When the work is "find the missing API surface / proxies / handlers / subscribers", enumerate from the **consumer's** call list first and map each entry 1:1 to a provider entry by **literal route / signature / topic string** — not "it calls the same handler". Two routes hitting one handler are two contracts. A summary count hides gaps; a 1:1 `consumer file:line → outgoing URL/signature → provider route/handler` table exposes them.
- **Copy-from branch exists → diff it.** When the work copies from a spike/reference branch, diff each named entry-point file against that branch — mapping entry points without the diff missed a reworked controller guard.
- **Journaled / filename-keyed artifacts collide across branches.** For migrations or any artifact registered by filename (DbUp, flyway, generated manifests), check whether the base branch already ships a _different_ artifact under the same name (`git log <base> -- <path>` + content diff).

#### Subagents guidance

1. When available, use subagents for doing the exploration for distinct areas.

2. Each subagent should be doing one focused exploration for reduced degradation.

3. For each subagent, provide the work description + the following constraints:

- "Your output is a REFERENCE DOCUMENT, not a design document. Think tour guide showing someone around a codebase, not architect designing a building. Point to examples; don't create new designs. Max 2 lines of code per explanation. If it looks like a techspec, it won't be approved."
- "Distinguish inspected facts from unknowns. Return missing load-bearing facts as precise questions; continue independent exploration. State the problem, intended outcome, and constraints without inventing decisions."
- "End your report with a `## Confidence & unverified` footer: what you could NOT verify, and any absence claim stated as an OPEN QUESTION with the scope of the probe that produced it — never as a bare negative."

4. Subagents should use balanced models, for instance:

- On Claude Code, use Opus agents
- On Codex, use gpt 5.6 terra agents
- On Cursor, use Grok agents

5. Confirm your fan-out plan with the user before proceeding.

### Consolidate

Files modified / created, APIs called or created, DB tables / models, state management, external services.

- **Caller closure (mechanical, before writing):** for every symbol/file the analysis proposes to touch, grep the whole repo (not the work slice) for its callers/consumers and record the command + count in the doc. Prose summaries of caller sets ("3–4 places") are forbidden — the enumerated list with provenance replaces them.

#### Evidence and drafting boundary

Check the map against the request and inspected source. A missing load-bearing fact blocks the
dependent recommendation; record the uncertainty and next probe. Write the useful authorized
draft, clearly marking unverified portions. Calculate and report the analysis rubric from the confidence contract. Below the effective
threshold, block dependent recommendations and phase advancement while continuing authorized
independent exploration and an explicitly partial draft. A score or worker agreement is neither
evidence nor permission.

#### Confidence score

Use an explicit 0–100% assessment for the scoped conclusion or next workflow step.
This is a structured judgment of evidence and remaining uncertainty, not a calibrated
probability of correctness, success, or safety. A score never supplies facts, turns
worker agreement into proof, passes an unrun/failed check, or grants authorization.

Factors and weights:

- Requirements clarity 40%
- Codebase-or-constraint understanding 40%
- Change-path clarity at reference-map altitude 20%.
- Note: greenfield uses verified constraints and ecosystem precedents for codebase understanding.

You should include it in the final requirements document, but also reporta summary of it to the user at the end after writing the document in the following format:

```
Confidence: X% - {justification}
Remaining uncertainty: {justification}
```

### Write requirements doc

1. With the exploration consolidated:

- Read `./references/TEMPLATE.md` thoroughly
- According to the detected mode (feature integration/greenfield/refactor or techdebt) additional guidance, define the final template structure
- Write the requirements document following the final template structure defined
- This step can be considered done when every section of the template is filled out

2. Write the requirements doc: write it within `./specs/[slug]/requirements.md` where slug is a given task/user story identifier (an id, a snake_case_meaningful_name, etc.)

### Review

At the end, provide a copy-paste prompt to launch a separate agent for an adversarial review for the written requirements doc according to this whole process.
