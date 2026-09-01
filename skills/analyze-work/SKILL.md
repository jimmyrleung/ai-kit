---
name: analyze-work
description: "Pre-implementation analysis of upcoming work — a reference map (entry points, patterns to follow, similar features, scope boundaries, risks), not a design doc. Detects and adapts to the work type: integrating a feature into an existing codebase, starting a new project / greenfield build (vertical-slice guarded), or a refactor / tech-debt request. Produces {work_name}_analysis.md. Use when asked to analyze, audit, scope, or map a feature integration, a new project, or a refactor / tech debt before designing or implementing it."
---

# analyze-work — pre-implementation reference map (integration · greenfield · refactor)

Act as an expert code analyst to map where upcoming work will land and what it must respect:

- where changes happen
- which existing patterns to follow
- which similar features to copy
- what risks breaking (blast radius).

You must **LOCATE and REFERENCE**, and **must not** DESIGN and SPECIFY as design comes next (techspec / plan phase).

> **Litmus test:** if a developer can copy-paste your output and start coding, you've gone too deep. The analysis should leave them needing to make design decisions. "The implementation should…" is the design phase's job; yours is "the implementation will happen around here — and here's a similar example to look at."

## When to use

- **Ad-hoc**: about to integrate a feature, start a new project, or refactor / pay down tech debt — and you want the map before designing.
- **After recon**: the `lay-of-the-land` skill produced a current-state map and a concrete work item is now defined.

## When NOT to use

- Diagnosing a failure → prefer `bug-investigation` for an evidence-based root cause finding, not a work map.
- No concrete work item yet, just "what exists here?" → prefer `lay-of-the-land`.
- Being asked to design or spec the solution → that's the phase after this one.

## Detect mode

1. **integration** mode:
   - default for existing, non-empty codebase
   - Signal: New capability into an existing codebase
   - Extra lens: Consumer-defined coverage, caller closure

2. **greenfield** mode:
   - Signal: No codebase yet / empty repo / "new project"
   - Extra lens: First vertical slice + anti-scaffolding guards

3. **refactor** mode:
   - Signal: Restructure / consolidate / de-debt existing behavior, no new capability
   - Extra lens: Scope boundaries, preserved contracts, risk classes

Detect the mode from the request and repo state:

- **echo the detected mode + resolved `{work_name}` back before analyzing**
- If in a **genuinely** ambiguous scenario, ask which one to use
- For mixed work ("add X and clean up Y while there") → pick the dominant mode, note the secondary lens in the doc.

## Input contract — loose

The input can really be any of:

- A draft file with the work description
- Inline prose
- Pointer to a past implementation specs to be used as a reference
- A structured initial requirements file
- A folder containing files that provide context on what to analyze
- A lay-of-the-land document

Resolve `{work_name}` before starting: derive it from the description's filename; else propose one from the topic and confirm.

Come back to the user if the ask is not clear:

- Confirm the ask/scope with the user
- Ask for starting points if needed

## Subagents (optional breadth)

### Guidance - item size

Subagents usage should be done according to the following guidance:

- Small item → no subagents, analyze on the main thread.
- Medium to large → scope the work and launch **generic** subagents for exploring distinct areas of exploration.
- XL: if the feature is too large and you think one analyze-work run is not enough, come back to the user suggesting a phased approach, where each phase earns its own analyze-work run

### Guidance - spawning subagents

When spawning subagents, they should be explore / general-purpose ones for breadth. Each should be handed the work description + these constraints verbatim:

1. "Your output is a REFERENCE DOCUMENT, not a design document. Think tour guide showing someone around a codebase, not architect designing a building. Point to examples; don't create new designs. Max 2 lines of code per explanation. If it looks like a techspec, it won't be approved."
2. "DO NOT MAKE ASSUMPTIONS — if anything is unclear, return with clarification questions. You must be able to answer: what problem is being solved? what should the work deliver? what constraints apply?"
3. "End your report with a `## Confidence & unverified` footer: what you could NOT verify, and any absence claim stated as an OPEN QUESTION with the scope of the probe that produced it — never as a bare negative."

### Consolidation

Consolidate: consensus (high confidence) / disagreements (flag for the user) / confidence-weighted points. Critical disagreement (> 2-point confidence delta on a key point) → return to the user with specific questions. Workers never spawn further subagents and never write the file.

## Process

### Understand the work

Establish definition, expected outcome, constraints, edge cases, dependencies.

### Clarification questions [MANDATORY]

Before launching the analysis, ask clarification questions relentlessly until the work is fully understood. Append Q&A to the description file's "Clarifications" section (when the description is a file).

### Architecture & health (integration/refactor)

Identify:

- Architectural patterns in play
- Cross-cutting concerns (auth, logging, caching)
- Pattern consistency (High/Med/Low)
- Documentation quality
- Architectural clarity.
- If low/poor on an integration → recommend refactoring first.

### Exploration

Identify:

- Entry points (routes, controllers, jobs)
- Similar features and patterns
- Reusable utilities/services
- Feature boundaries
- Configuration
- For integration/refactor: Examine every file the description names
- For greenfield: explore the constraint space instead — chosen-stack conventions, comparable ecosystem examples, hard requirements

Additional guidance:

- **Coverage gaps are defined by the consumer, not the provider.** When the work is "find the missing API surface / proxies / handlers / subscribers", enumerate from the **consumer's** call list first and map each entry 1:1 to a provider entry by **literal route / signature / topic string** — not "it calls the same handler". Two routes hitting one handler are two contracts. A summary count hides gaps; a 1:1 `consumer file:line → outgoing URL/signature → provider route/handler` table exposes them.
- **Copy-from branch exists → diff it.** When the work copies from a spike/reference branch, diff each named entry-point file against that branch — mapping entry points without the diff missed a reworked controller guard.
- **Journaled / filename-keyed artifacts collide across branches.** For migrations or any artifact registered by filename (DbUp, flyway, generated manifests), check whether the base branch already ships a _different_ artifact under the same name (`git log <base> -- <path>` + content diff).

### Trace flows (integration / refactor)

Call chains entry → output, data flow, transformations at each step, dependencies and integrations, state changes and side effects.

### Consolidate the change surface

Files modified / created, APIs called or created, DB tables / models, state management, external services.

- **Caller closure (mechanical, before writing):** for every symbol/file the analysis proposes to touch, grep the whole repo (not the work slice) for its callers/consumers and record the command + count in the doc. Prose summaries of caller sets ("3–4 places") are forbidden — the enumerated list with provenance replaces them.

### Apply the mode lens

Check [Mode lenses] section below.

### Confidence gate

1. Calculate the confidence score 0–100%:
   - requirements clarity (40%)
   - codebase-or-constraint understanding (40%)
   - change-path clarity (20%).

2. Once calculated, act according to the result:

- ✅ 90–100% all clear - confirm the consolidated analysis with the user, then write the file
- ⚠️ 70–89% minor ambiguities
- ❌ < 70% significant unknowns

**If < 90% → STOP, name what's missing, ask more questions.**

## Mode lenses

### integration

The core process and output shape ARE the integration lens — nothing extra.

### greenfield

There is no current state to map, so the map is the **proposed starting shape** — still reference-level, not a design:

- **First vertical slice**: the smallest user-observable behavior to build first. The goal must be user-observable ("user can Y"), never "set up X".
- **Slice requirement (the PRD stand-in)**: create a `## Slice requirement` section including (keep these header names stable — downstream phases may read them by name):
  - **Goal**: the slice goal (user-observable, one sentence)
  - **Done-when**: checkboxes of specific, testable acceptance criteria (including error/empty-state handling)
  - **Building on**: the existing code / prior slices this slice builds on ("nothing — first slice" is a valid answer)
  - **Constraints**: the constraints that bind THIS slice only. Requirement-level, not design: _what_ done looks like, never _how_.
- If the user provides a PRD, the [Slice requirement] section should just link it
- **Deliberately NOT building yet** — deferred capabilities, each with what would earn it a place.
- **Anti-scaffolding guards (reject in the doc):** horizontal layers before a slice demands them (logging pipelines, middleware stacks, CI/CD polish, monitoring, performance/security sections) · "set up X" framed as a goal · success metrics with baselines.
- **Proposed structure** — directories / modules + the conventions to adopt, pointing at ecosystem-standard examples, not class designs.

### refactor

Add to the doc:

- **Scope definition** — In scope (+ clear boundaries) / Out of scope (+ clear exclusions) / Gray areas (**needs decision**).
- **Preserved contracts** — public APIs, data formats, anything that cannot change.
- **Anti-patterns found** — why problematic, locations, impact — alongside the good patterns to keep.
- **Risk classification** — Breaking changes (High: impact + mitigation) / Non-breaking (Low) / Unknown (needs investigation).
- **Executive-summary extras** — Complexity: Low/Medium/High/Critical · Risk: Low/Medium/High · Scope: Small/Medium/Large.

## Output structure

The expected output is a reference document — not a bloated document with implementation details:

- No full implementation code blocks
- No "exactly how to write it"

**IMPORTANT**: the only scenario code blocks are allowed is when explaining current state would take _more_ text than the block.

Core sections (all modes): **Overview** (2–3 sentences) · **Confidence score** (loaded confidence format) · **Entry points** (`file:line`; greenfield: proposed entry surface) · **Similar features / examples** (`file:line`; greenfield: ecosystem examples) · **Execution flow** · **Key components & responsibilities** · **Architecture insights** · **Dependencies** (internal / external / libraries) · **Observations** (strengths, issues, opportunities) · **Side effects / impact** · **Risks & considerations** (severity Critical/High/Mid/Low) · **Essential files** — plus the mode-lens sections above.

Four tables (omit one only if it genuinely has no rows; greenfield: "Files to Modify" is usually empty):

```markdown
### Files to Modify

| File | Purpose | Changes Needed |
| ---- | ------- | -------------- |

### Files to Create

| File | Purpose | Type (Component/Service/Util) |
| ---- | ------- | ----------------------------- |

### APIs Affected

| Endpoint | Method | Changes |
| -------- | ------ | ------- |

### Database Changes

| Table | Change Type | Details |
| ----- | ----------- | ------- |
```

### What this analysis IS / IS NOT

**IS:** a map of where changes go · pointers to existing patterns to follow (and, refactor mode, anti-patterns to fix) · references to similar features as examples · honest scope boundaries · risks tied to specific files.

**IS NOT:** function signatures or class definitions · specific algorithms or logic flows · detailed error handling · implementation pseudocode · migration scripts · API request/response schemas.

**Bad (too detailed — that's a techspec):** "Create POST /api/orders/export that: 1) validates export permission, 2) queries orders with filters, 3) formats CSV via fast-csv, 4) returns 200 or 403."

**Right level:** "Export needs a new endpoint in `routes/orders.ts` following the existing `/import` pattern (lines 45–78). Reuse the permission check from `middleware/permissions.ts`. CSV formatting should follow `services/reportGenerator.ts:exportToCSV()` (lines 120–156)."

## Output file

Write to `{work_name}_analysis.md`, alongside the description file (or where the user says). No discoverable base name → ask before writing. After writing, **offer the `review-artifact` skill** before anything designs or implements on top of the doc (the design phase is `techspec`).
