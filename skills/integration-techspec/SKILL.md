---
name: integration-techspec
description: Produce a technical specification for integrating a feature into an existing codebase by exploring three approaches in parallel — minimal-changes / clean-architecture / pragmatic-balance — then committing to one with the user. Produces {feature}_techspec.md. Used ad-hoc, or as Phase 3 (M-size path) of /integration-feature-dev and the body of /integration-create-techspec. For small features where a 3-way comparison is overkill, use `pragmatic-techspec` instead.
---

# Integration Techspec Skill (3-way exploration)

You produce a lightweight-but-complete technical specification for fitting a feature into an **existing** codebase. This skill explores three approaches side by side and then commits to one — use it when the feature has enough architectural latitude that comparing options genuinely helps. (When it doesn't, `pragmatic-techspec` skips straight to the committed answer.)

## When to use

- **Ad-hoc**: a feature where minimal-changes vs clean-architecture vs pragmatic-balance would land in materially different places and you want to see them before deciding.
- **Orchestrated**: Phase 3 (M-size path) of `/integration-feature-dev`, or the build body of `/integration-create-techspec`.

## When NOT to use

- Small features, or features where you already know "pragmatic" is the answer — use `pragmatic-techspec` (skips the 3-way parade).
- Greenfield work — use the greenfield `techspec-creation` skill.
- No integration analysis yet, and the feature isn't trivial — produce the analysis first (`integration-analysis`).

## Coordinator vs worker

- **No mandate handed to you (default — you're on the main thread):** you're the *coordinator*.
  1. Read the inputs (feature description + integration analysis + any review notes) end to end.
  2. Launch **3 `@integration-techspec-creator-agent` sub-agents in parallel**, each handed the inputs and one mandate:
     - **minimal-changes** — smallest diff, maximum reuse of what exists.
     - **clean-architecture** — maintainability, elegant abstractions, willing to refactor a little.
     - **pragmatic-balance** — speed + quality; ships safely and leaves the codebase slightly better, no over-engineering.
  3. When they return, compare the three. Form your own opinion on which fits *this* feature, considering: small fix vs large feature, urgency, complexity, team context.
  4. Present to the user: a brief summary of each approach, a trade-offs comparison, your recommendation with reasoning, and the concrete implementation differences.
  5. Ask the user which approach they prefer.
  6. Build the final techspec for the chosen approach (folding in anything worth keeping from the other two), run the confidence gate, and write the file.
- **You were spawned as a sub-agent with a mandate:** you're a *worker*. Map existing patterns, design the solution **for your assigned mandate only**, and return your draft techspec to the coordinator. **Do not** spawn further sub-agents and **do not** write a file.

## Input contract

Expect, in order of authority:
1. **Integration analysis** (`*_integration.md`) — authoritative for scope, files touched, PO/team clarifications.
2. **Feature description** — the requirement itself.

If only a lighter implementation plan exists (no integration analysis) and the feature isn't trivial, say so in the techspec's confidence section and flag the gaps an analysis would normally have closed. The confidence gate catches the rest. Derive the `{feature}` base name from the inputs; ask if not discoverable.

## Process (per approach — what each worker does, and what the coordinator does for the final)

1. **Review previous phases' outputs.** Feature requirements, integration analysis, review notes — all the way through.
2. **Map existing patterns.** Read the files named in the integration analysis (don't trust summaries). Search for similar features. Identify the architectural patterns, coding standards, module boundaries, abstraction layers, and any `CLAUDE.md`/architecture-doc guidance. Note reusable utilities, services, constants, DI registrations. Record `file:line` refs as you go — you'll cite them.
3. **Design the solution for your approach and prepare implementation.** Commit to your assigned approach (workers) / the user-chosen approach (coordinator). Plan the implementation file-by-file. Design API contracts, data models, component structure — only for what this feature actually needs. Identify key algorithms, data structures, error paths, edge cases. Plan the test approach. Note performance considerations in the hot path. Flag technical debt you'd touch.
4. **Identify critical refactors (if any).** If technical debt MUST be addressed for this to ship safely, document it **separately** — not inside the main techspec — and get explicit user approval before baking any of it in.
5. **Confidence gate.** Score 0–100% using the user's global CLAUDE.md factor breakdown (API docs clarity 30% / similar patterns in codebase 25% / data-flow understanding 20% / complexity 15% / cross-system impact 10%). **If < 90%: STOP and ask clarifying questions** — don't write the techspec yet. At ≥ 90%, proceed. Target ≥ 95% for ship-ready.
6. **Write the techspec** (coordinator only) following the section contract below. Keep inline comments in code blocks minimal — explain *why*, not *what*.

## Required sections

The final techspec includes, roughly in this order:

1. **Summary** — 2–3 sentences: the pivotal file(s), the mechanism of change, the blast radius (how many production files, how many test files, which layers).
2. **Approach** — name the chosen approach (minimal-changes / clean-architecture / pragmatic-balance) and why it won here, in one short paragraph. State what's reused, what's net-new, and what is explicitly *not* being built.
3. **Patterns & conventions found** — a table; every row points to real code you read. `| Pattern | Source (file:line) | Usage here |`. Every `file:line` verified, not guessed.
4. **Component design** — each component: file path, responsibilities, dependencies, interfaces.
5. **Implementation map** — file-by-file. For each touched file: path + change type (Create/Modify), what changes and **why** (one sentence), before/after snippets for non-trivial edits (no placeholder `[NewThing]` — use the real names), and which pattern from §3 it follows.
6. **Data flow** — entry points → transformations → outputs. Short ASCII diagram or numbered list, whichever is clearer.
7. **Test plan** — a scenario table: `| # | Scenario | Inputs | Expected |`. Prefer concrete test outlines (the repo's framework) over prose. Include at least one explicit "tests NOT needed here, because…" where you're deliberately skipping a surface.
8. **Critical details** — error handling, state management, performance, security — only the ones with real substance for this feature.
9. **Confidence score** — global CLAUDE.md format: `Confidence score: N% — <one-line why>`, then **Why N%** (3–5 bullets of concrete evidence: files verified, patterns matched, deps confirmed) and **100−N% uncertainty** (2–4 bullets, each with an impact note: blocks implementation? operational? minor judgement call?).

## Optional sections (include only with substance — never a placeholder)

Rollback (when changes aren't independently revertible) · Deployment sequencing (when deploy order matters) · Risks table `| Risk | Likelihood | Impact | Mitigation |` (failure modes the test plan doesn't lock down) · Rejected approaches (a short Option A / Option B with rationale — natural here since you explored three) · Revision banner (when scope pivoted mid-spec) · Open technical questions (only if you proceeded with user-approved residual uncertainty).

## Do not include

Generic "Framework/Library: [what and why]" prose for the stack the repo already uses · "Styling: [approach]" for features that don't touch styling · Monitoring & Observability by default · Documentation Needs checklist (surface as implementation tasks instead) · Estimated Complexity S/M/L/XL (the files-changed count is the better signal) · Mocking Strategy as its own subsection (fold into the test plan) · placeholder Environment Variables / Feature Flags sections when none are touched · separate Timeline/Dependency Risks subsections (use the one Risks table).

**Rule:** if a section has no substance for this feature, delete it — don't leave a placeholder.

## Output guidance

Be specific (code examples + `file:line`, not "somewhere in the cart layer"). Be practical (design for the codebase you have). Be consistent (reuse patterns; new patterns need justification). Be minimal (don't over-engineer; don't add error handling for impossible cases). Document the decision (one sentence on why the chosen approach beat the others). Delete, don't placeholder.

## Output file

Write the final techspec to `{feature_name}_techspec.md`, alongside the feature description and integration analysis. If no base name is discoverable, ask the user before writing. (Workers return drafts and write nothing.)
