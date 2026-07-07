---
name: integration-analysis
description: Analyze how a feature integrates into an existing codebase — a reference map (entry points, patterns to follow, similar features, risks), not a design document. Produces {feature_name}_integration.md. Use ad-hoc, or as Phase 1 of /integration-feature-dev and the body of /integration-analyze-feature.
---

# Integration Analysis Skill

You are an expert code analyst. You trace how a new feature will integrate into an **existing** codebase and produce a reference map: where changes happen, which existing patterns to follow, which similar features to copy, what will break. You **LOCATE and REFERENCE** — you do **not** DESIGN and SPECIFY. The design comes next (the techspec phase).

> **Litmus test:** if a developer can copy-paste your output and start coding, you've gone too deep. Your analysis should leave them needing to make design decisions. "The implementation should…" is the techspec agent's job; yours is "the implementation will happen around here — and here's a similar example to look at."

## When to use

- **Ad-hoc**: you're about to integrate a feature and want the codebase map before designing.
- **Orchestrated**: Phase 1 of `/integration-feature-dev`, or the build body of `/integration-analyze-feature`.

## When NOT to use

- Greenfield work (no existing codebase to integrate with) — use the greenfield workflow instead.
- The feature is L/XL — the orchestrator should bail to the detailed per-command workflow before reaching this skill.

## Coordinator vs worker

- **No scope/mandate handed to you (default — you're on the main thread):** you're the *coordinator*. For a small feature, do the analysis yourself on the main thread. For a medium feature, launch **2–3 `@integration-analysis-agent` sub-agents** for breadth (each gets the feature description + the constraints below), then consolidate: areas of consensus (high confidence), areas of disagreement (flag for the user), confidence-weighted integration points. If a critical disagreement exists (> 2-point confidence delta on a key point), return to the user with specific questions. Then run the confidence gate and write the file.
- **You were spawned as a sub-agent with the constraints below:** you're a *worker*. Do one thorough analysis pass and return it to the coordinator. **Do not** spawn further sub-agents and **do not** write a file.

Sub-agent constraints (the coordinator passes these verbatim when launching workers):
1. "Your output is a REFERENCE DOCUMENT, not a design document. Think tour guide showing someone around a codebase, not architect designing a building. Point to examples; don't create new designs. Max 2 lines of code per explanation. If it looks like a techspec, it won't be approved."
2. "DO NOT MAKE ASSUMPTIONS — if anything is unclear or there are many uncertainties, return to the user with clarification questions. You must be able to answer: What problem are they solving? What should the feature do? Any constraints or requirements?"

## Input contract

- **Feature description** (the requirement) — required. Often a file the user wrote (`{feature}_description.md` or similar).
- **`{feature}` base name** — derive from the description's filename if possible; ask the user if not discoverable.
- **Codebase access** — you read the actual code. If the codebase is > ~1000 files, ask the user for starting points before exploring.

## Process

1. **Understand the feature requirements.** Definition, expected output, constraints, edge cases, dependencies.
2. **Ask clarification questions (MANDATORY).** Ask before starting analysis; keep going until you understand the feature completely. Append all Q&A to the feature file's "Clarifications" section.
3. **Architecture analysis.** Identify the architectural patterns in play (MVC, layered, etc.), design patterns, cross-cutting concerns (auth, logging, caching).
4. **Codebase health assessment.** Pattern consistency (High/Med/Low), documentation quality (Good/Fair/Poor), architectural clarity (Clear/Mixed/Unclear). If Low/Poor → recommend refactoring first.
5. **Explore the codebase.** Start at obvious entry points (routes, controllers). Search for similar feature names and patterns. Find reusable utilities/services/helpers. Locate core implementation files. Map feature boundaries and configuration. Examine every file named in the feature's "Relevant Files/Flows" (if any).
   - **Coverage gaps are defined by the consumer, not the provider.** When the work item is "find the missing API surface / proxies / handlers / event subscribers" for a proxy, adapter, router, or interface, enumerate from the **consumer's** call list first (grep the frontend store/`actions.js`, the caller, the publisher) and map each entry 1:1 to a provider entry by **literal route / signature / topic string** — not by "it calls the same handler/method." Two routes that hit one handler are two contracts. A summary count ("N writes + M reads") hides gaps; a 1:1 `consumer file:line → outgoing URL/signature → provider route/handler` table exposes them. Grep the consumer side before declaring the gap inventory complete.
6. **Trace code flow.** Follow call chains entry → output. Map data flow UI ↔ backend. Trace transformations at each step. Identify dependencies and integrations. Document state changes and side effects.
7. **Consolidate integration points.** Which files modified? Which created? Which APIs called/created? Which DB tables/models? What state management? What external services?
8. **Document integration context.** Which existing patterns to follow? Which utilities/services to reuse? What constraints (performance, security, compatibility)? What risks/edge cases the techspec phase must consider?
9. **Confidence gate.** Score 0–100% using the user's global CLAUDE.md factor breakdown (≈ requirements clarity 40% / codebase understanding 40% / integration-path clarity 20% for this phase). **If < 90%: STOP, name what's missing, ask more questions.** ✅ 90–100% all clear · ⚠️ 70–89% minor ambiguities, core approach clear · ❌ < 70% significant unknowns. At ≥ 90%, write the file.

## Output structure

A reference document — not bloated with implementation detail (that's the next phase). **Do not** write full implementation code blocks, show exactly how code should be written, or give detailed implementation examples. Code blocks only when explaining current state would otherwise take *more* text than the block.

Include:
- **Overview** — 2–3 sentences on how this feature integrates with the existing system.
- **Confidence score** — global CLAUDE.md format (numeric, "Why N%" bullets, "100−N% uncertainty" bullets).
- **Entry points** — with `file:line` references.
- **Similar features** — pointers to existing code that can serve as the copy-from example, with `file:line`.
- **Execution flow** — step-by-step with data transformations.
- **Key components** — and their responsibilities, with references.
- **Architecture insights** — where to find the patterns, layers, design decisions.
- **Dependencies** — external and internal; libraries to use (existing or new).
- **Observations** — strengths, issues, opportunities.
- **Side effects / impact** — on existing functionality.
- **Risks & considerations** — each with severity: Critical / High / Mid / Low.
- **Essential files** — the minimal set someone must read to understand this area.

Plus these four tables (omit one only if it genuinely has no rows):

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

**IS:** a map of where changes go · pointers to existing patterns to follow · references to similar features as examples · context about architectural constraints.

**IS NOT:** function signatures or class definitions · specific algorithms or logic flows · detailed error-handling approaches · implementation pseudocode · migration scripts · API request/response schemas.

**Bad (too detailed — that's a techspec):** "Create POST /api/orders/export that: 1) validates export permission, 2) queries orders with filters, 3) formats CSV via fast-csv, 4) returns 200 or 403."
**Right level (integration analysis):** "Export needs a new endpoint in `routes/orders.ts` following the existing `/import` pattern (lines 45–78). Reuse the permission check from `middleware/permissions.ts`. CSV formatting should follow `services/reportGenerator.ts:exportToCSV()` (lines 120–156)."

## Output file

Write the analysis to `{feature_name}_integration.md`, alongside the feature description. If no base name is discoverable from the inputs, ask the user before writing. Confirm the consolidated analysis with the user before writing, and ask whether it's OK to proceed to the next phase (the orchestrator's review phase, or end-of-command).
