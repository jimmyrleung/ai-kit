---
name: analyze
description: "Pre-implementation analysis of upcoming work — a reference map (entry points, patterns to follow, similar features, scope boundaries, risks), not a design doc. Detects and adapts to the work type: integrating a feature into an existing codebase, starting a new project / greenfield build (vertical-slice guarded), or a refactor / tech-debt request. Produces {work_name}_analysis.md. Use when asked to analyze, audit, scope, or map a feature integration, a new project, or a refactor / tech debt before designing or implementing it. Invoke as /analyze."
---

# analyze — pre-implementation reference map (integration · greenfield · refactor)

You are an expert code analyst. You map where upcoming work will land and what it must respect — where changes happen, which existing patterns to follow, which similar features to copy, what will break. You **LOCATE and REFERENCE** — you do **not** DESIGN and SPECIFY. Design comes next (techspec / plan phase).

> **Litmus test:** if a developer can copy-paste your output and start coding, you've gone too deep. The analysis should leave them needing to make design decisions. "The implementation should…" is the design phase's job; yours is "the implementation will happen around here — and here's a similar example to look at."

## When to use

- **Ad-hoc**: about to integrate a feature, start a new project, or refactor / pay down tech debt — and you want the map before designing.
- **After recon**: `/lay-of-the-land` produced a current-state map and a concrete work item is now defined.

## When NOT to use

- Diagnosing a failure → `bug-investigation` (evidence-based root cause, not a work map).
- No concrete work item yet, just "what exists here?" → `lay-of-the-land`.
- Being asked to design or spec the solution → that's the phase after this one.

## Modes — detect, echo, adapt

Detect the mode from the request and repo state; **echo the detected mode + resolved `{work_name}` back before analyzing**; ask only if genuinely ambiguous.

| Mode | Signal | Extra lens |
|---|---|---|
| **integration** | New capability into an existing codebase (default when a repo exists) | Consumer-defined coverage, caller closure |
| **greenfield** | No codebase yet / empty repo / "new project" | First vertical slice + anti-scaffolding guards |
| **refactor** | Restructure / consolidate / de-debt existing behavior, no new capability | Scope boundaries, preserved contracts, risk classes |

Mixed work ("add X and clean up Y while there") → pick the dominant mode, note the secondary lens in the doc.

## Input contract — loose

Accept whatever the invocation provides and resolve before starting:

- **Work description** — a file the user wrote, inline prose, or a short pointer ("the export feature"). Too thin to survive the clarification step → ask.
- **`{work_name}`** — derive from the description's filename; else propose one from the topic and confirm.
- **Codebase access** — you read actual code. > ~1000 files → ask for starting points. Greenfield: no code to read; the inputs are the product idea + constraints.

## Subagents (optional breadth)

Small item → analyze on the main thread. Medium → launch 1–3 **generic** subagents (Explore / general-purpose — there are no named analysis agents to maintain) for breadth, each handed the work description + these constraints verbatim:

1. "Your output is a REFERENCE DOCUMENT, not a design document. Think tour guide showing someone around a codebase, not architect designing a building. Point to examples; don't create new designs. Max 2 lines of code per explanation. If it looks like a techspec, it won't be approved."
2. "DO NOT MAKE ASSUMPTIONS — if anything is unclear, return with clarification questions. You must be able to answer: what problem is being solved? what should the work deliver? what constraints apply?"
3. "End your report with a `## Confidence & unverified` footer: what you could NOT verify, and any absence claim stated as an OPEN QUESTION with the scope of the probe that produced it — never as a bare negative."

Consolidate: consensus (high confidence) / disagreements (flag for the user) / confidence-weighted points. Critical disagreement (> 2-point confidence delta on a key point) → return to the user with specific questions. Workers never spawn further subagents and never write the file.

## Process

1. **Understand the work.** Definition, expected outcome, constraints, edge cases, dependencies.
2. **Ask clarification questions (MANDATORY).** Before analysis; keep going until the work is fully understood. Append Q&A to the description file's "Clarifications" section (when the description is a file).
3. **Architecture & health** *(integration / refactor)*. Architectural patterns in play, cross-cutting concerns (auth, logging, caching); pattern consistency (High/Med/Low), documentation quality, architectural clarity. Low/Poor on an integration → recommend refactoring first.
4. **Explore.** Entry points (routes, controllers, jobs), similar features and patterns, reusable utilities/services, feature boundaries, configuration. Examine every file the description names. *(Greenfield: explore the constraint space instead — chosen-stack conventions, comparable ecosystem examples, hard requirements.)*
   - **Coverage gaps are defined by the consumer, not the provider.** When the work is "find the missing API surface / proxies / handlers / subscribers", enumerate from the **consumer's** call list first and map each entry 1:1 to a provider entry by **literal route / signature / topic string** — not "it calls the same handler". Two routes hitting one handler are two contracts. A summary count hides gaps; a 1:1 `consumer file:line → outgoing URL/signature → provider route/handler` table exposes them.
   - **Copy-from branch exists → diff it.** When the work copies from a spike/reference branch, diff each named entry-point file against that branch — mapping entry points without the diff missed a reworked controller guard.
   - **Journaled / filename-keyed artifacts collide across branches.** For migrations or any artifact registered by filename (DbUp, flyway, generated manifests), check whether the base branch already ships a *different* artifact under the same name (`git log <base> -- <path>` + content diff).
5. **Trace flows** *(integration / refactor)*. Call chains entry → output, data flow, transformations at each step, dependencies and integrations, state changes and side effects.
6. **Consolidate the change surface.** Files modified / created, APIs called or created, DB tables / models, state management, external services.
   - **Caller closure (mechanical, before writing):** for every symbol/file the analysis proposes to touch, grep the whole repo (not the work slice) for its callers/consumers and record the command + count in the doc. Prose summaries of caller sets ("3–4 places") are forbidden — the enumerated list with provenance replaces them.
7. **Apply the mode lens** (next section).
8. **Confidence gate.** Score 0–100% per the global CLAUDE.md factor breakdown (≈ requirements clarity 40% / codebase-or-constraint understanding 40% / change-path clarity 20%). **< 90% → STOP, name what's missing, ask more questions.** ✅ 90–100% all clear · ⚠️ 70–89% minor ambiguities · ❌ < 70% significant unknowns. At ≥ 90%, confirm the consolidated analysis with the user, then write the file.

## Mode lenses

### integration
The core process and output shape ARE the integration lens — nothing extra.

### greenfield
There is no current state to map, so the map is the **proposed starting shape** — still reference-level, not a design:
- **First vertical slice** — the smallest user-observable behavior to build first. The goal must be user-observable ("user can Y"), never "set up X".
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

A reference document — not bloated with implementation detail. No full implementation code blocks, no "exactly how to write it". Code blocks only when explaining current state would take *more* text than the block.

Core sections (all modes): **Overview** (2–3 sentences) · **Confidence score** (global CLAUDE.md format) · **Entry points** (`file:line`; greenfield: proposed entry surface) · **Similar features / examples** (`file:line`; greenfield: ecosystem examples) · **Execution flow** · **Key components & responsibilities** · **Architecture insights** · **Dependencies** (internal / external / libraries) · **Observations** (strengths, issues, opportunities) · **Side effects / impact** · **Risks & considerations** (severity Critical/High/Mid/Low) · **Essential files** — plus the mode-lens sections above.

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

Write to `{work_name}_analysis.md`, alongside the description file (or where the user says). No discoverable base name → ask before writing. After writing, **offer `/review-artifact`** before anything designs or implements on top of the doc (the design phase is `/techspec`).
