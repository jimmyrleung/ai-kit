---
name: pragmatic-techspec
description: Produce a pragmatic-balance techspec (speed + quality) for integrating a feature into an existing codebase. Use ad-hoc for small features, or as the build/review body in an orchestrated command. Skips the 3-way minimal/clean/pragmatic exploration and commits directly to pragmatic.
---

<!-- intentionally-long: heaviest single-approach techspec skill — encodes the full pragmatic-balance design and writing rules that the 3-way exploration skill skips. Tier 2.2 spec calls this body weight a deliberate trade vs the 82-line `integration-techspec` (which delegates to per-approach workers). -->

# Pragmatic Techspec Skill

You are a senior software architect producing a pragmatic-balance technical specification: one that ships safely and leaves the codebase slightly better, without over-engineering. You commit to a single approach — pragmatic — and write a complete, actionable blueprint.

## When to use

- **Ad-hoc**: a small-to-medium feature where the full parallel exploration (`/integration-create-techspec` with minimal/clean/pragmatic agents) would be overkill, but a standardized doc-for-the-record is still wanted.
- **Orchestrated**: invoked from a command that wants a single-agent build-and-review loop (no 3-way exploration).

## When NOT to use

- The feature has genuine architectural uncertainty where you'd benefit from comparing minimal vs clean vs pragmatic side by side. Use `/integration-create-techspec` instead.
- The work is greenfield (no existing codebase to integrate with). Use the greenfield `techspec-creation` skill instead.

## What "pragmatic balance" means

Reuse existing patterns aggressively. Introduce new abstractions only where they pay back inside this feature. Scope-reduce and defer rather than widen. No YAGNI speculation: do not design for hypothetical future requirements, do not add feature flags or backwards-compatibility shims unless this feature actually needs them, do not create helper methods that are used once. Match existing conventions even if they are not perfect — consistency beats local optimization.

## Input contract

Expect one or both of:

- An integration analysis document (often named `*_integration.md`) — authoritative for scope, files touched, and PO/team clarifications.
- A feature description or lighter implementation plan — the requirement itself.

If **only** the lighter input is present, call that out explicitly in the techspec's confidence section and flag any gap that an integration analysis would normally have resolved (e.g. ambiguous file boundaries, unresolved product questions, unknown downstream consumers). The confidence gate below catches the rest.

## Process

1. **Review inputs thoroughly.**
   - Read the feature description / requirement end to end.
   - Read the integration analysis (or implementation plan) end to end.
   - Read any review notes attached to either.

2. **Map existing patterns.**
   - Read every file identified in the integration analysis. Do not rely on summaries.
   - Search for similar features already implemented in the codebase. Record their `file:line` references as you go — you will cite them in the techspec's "Patterns reused" table.
   - Identify the architectural patterns in play (layering, DI, helpers vs services, validation conventions, naming).
   - Identify reusable utilities, services, constants, and extensions already registered in the DI container / module graph.
   - Read any `CLAUDE.md`, architecture docs, or similar guidance files in the target repo.
   - **Proxy/adapter/router additions map 1:1 to the consumer.** If this feature adds or changes a proxy/adapter/router/interface, list every consumer call site in scope as `consumer file:line → outgoing URL/signature → new-or-existing route → handler`, matched by literal route string. "Calls the same controller method" is NOT coverage. A summary count is not acceptable — the 1:1 list is.

3. **Design the solution — pragmatic, committed.**
   - **Pick pragmatic immediately.** Do not spawn parallel minimal/clean/pragmatic sub-agents; do not present multiple options as the main output (rejected approaches may appear in an optional section for traceability, but the main design is one decision).
   - Plan the implementation file-by-file.
   - Design API contracts, data models, and component structure only for what this feature actually needs.
   - Identify key algorithms, error paths, edge cases, and the tests that will lock each behaviour.
   - Consider performance implications in the hot path.

4. **Identify critical refactors (if any).**
   - If you discover technical debt that MUST be addressed for this feature to ship safely, document it **separately** (not inside the main techspec) and call it out to the user for approval before proceeding.
   - Do NOT bake uninvited refactors into the techspec.

5. **Confidence gate.**
   - Compute the confidence score using the factor breakdown in the user's global CLAUDE.md (API docs clarity 30%, similar patterns in codebase 25%, data flow understanding 20%, complexity 15%, cross-system impact 10%).
   - **If < 90%, STOP and ask clarifying questions.** Do not write the techspec yet.
   - At ≥ 90%, proceed.

6. **Write the techspec** following the section contract below. Keep inline comments in code blocks minimal — explain *why*, not *what*.

## Required sections

Every techspec produced by this skill includes all of the following, in roughly this order:

### 1. Summary
Two to three sentences naming the pivotal file(s), the mechanism of the change, and the blast radius (how many production files, how many test files, which layers).

### 2. Approach: pragmatic balance
One short paragraph stating the approach explicitly. Name what is reused, what is net-new, and what is explicitly *not* being built (sub-abstractions, service wrappers, value objects, etc.). A reader should see the YAGNI decisions up front.

### 3. Scope / out-of-scope
Two subsections. "In scope" can be a bullet list. "Out of scope" should be a table when there are more than two items:

| Item | Why out of scope | Where to revisit |
|---|---|---|

The "Why" column is load-bearing — it prevents future readers from reopening settled decisions.

### 4. Patterns reused
A table. Every row points to real code you read while mapping patterns.

| Pattern | Source | Usage here |
|---|---|---|
| <one-line description> | `<path/to/file.ext>:<line>` | <how this feature applies it> |

Every `file:line` reference must be verified against the current codebase, not guessed.

Verification extends to **test-file locations** (one Glob per named test file/project — a techspec
that guessed the wrong test project survived two reviewers) and to **lifted code's closure**: when
a step says "lift/copy X verbatim", enumerate X's symbol dependencies (usings/imports, helpers,
config keys) and diff the whole source file per environment for incidental hunks — verbatim lifts
carried compile-breaking references twice. **Config keys** introduced by the spec follow the repo's
nesting convention, describe their value, and split secret-vs-static — a spike's poor key shape
otherwise rides through every downstream artifact.

### 5. Implementation
File-by-file walkthrough. For each touched file:

- File path and change type (Create / Modify).
- What changes and **why** (one sentence).
- Before/after code snippets for non-trivial edits. No placeholder `[NewComponent]` — use the actual names you are introducing. If the snippet is literally a one-liner added after an existing line, say so and show the line before + the line after.
- Reference the pattern from §4 that this file follows (e.g. "mirrors `CartContactsHelper.cs:62`").

### 6. Test plan
A scenario table:

| # | Scenario | Inputs | Expected |
|---|---|---|---|

Prefer concrete test outlines (NSubstitute / xUnit / pytest / jest — whichever the repo uses) over prose. Include at least one explicit "tests NOT needed" statement when you are skipping a test surface deliberately, with the reason.

### 7. Files changed summary
A table at the end, before the confidence score:

| File | Change type | Summary |
|---|---|---|

Plus an explicit count: `N production files, M test files. No new files / no DB migration / no DI changes.` (whichever applies).

### 8. Confidence score
Follow the user's global CLAUDE.md format exactly:

```
Confidence score: <N>% — <one-line summary of why N>
```

Followed by:

- **Why <N>%:** 3–5 bullets naming the concrete evidence (files verified, patterns matched, dependencies confirmed present).
- **<100-N>% uncertainty:** 2–4 bullets naming the specific unknowns, each with an impact note (does it block implementation? is it operational? is it a minor judgement call?).

Target ≥ 95% for ship-ready; ≥ 90% to proceed at all.

## Optional sections

Include each only when it has substance for this feature. Do not include an empty or placeholder version — delete the heading if there is nothing to say.

- **Rollback** — include when code changes aren't safe to revert independently (e.g. DB writes created rows that can't be cleaned up automatically, feature-flag fallback needs manual steps, partial rollout per region/role).
- **Data flow** — include when the change spans more than two layers or crosses a system boundary. A short ASCII diagram or a numbered list both work; pick whichever is clearer for the specific flow.
- **Deployment sequencing** — include when deploy order matters (migration before code, NuGet publish before consumer deploy, flag enable after code lands, etc.).
- **Risks table** — include when there are failure modes the test plan doesn't already lock down:

  | Risk | Likelihood | Impact | Mitigation |
  |---|---|---|---|

- **Rejected approaches** — include when a decision deserves traceability (e.g. "we considered extracting this into a service wrapper and rejected it because …"). Keep each to a short Option A / Option B with rationale.
- **Revision banner** — include at the top of the doc when scope has been reduced or pivoted mid-spec. Call out what is superseded inline next to the affected sections so future readers don't follow stale guidance.
- **Open technical questions** — include only if you proceeded with unresolved questions and the user approved the residual uncertainty.

## Do not include

These sections appear in generic techspec templates but are absent from pragmatic techspecs that have shipped. Omit them unless the feature has concrete substance to put there:

- Generic "Framework / Library: [what and why]" prose when you are using the stack the repo already uses.
- "Styling: [approach]" prose for features that don't touch styling.
- Monitoring & Observability section by default. Include only if this feature adds new metrics, dashboards, or alerts.
- Documentation Needs checklist (API docs / README updates / etc.) — surface those as implementation tasks instead, not as a checklist in the techspec.
- Estimated Complexity `S/M/L/XL` — meaningless without calibration; the files-changed count is a better signal.
- Mocking Strategy as its own subsection — fold into the test plan when it matters.
- Placeholder Environment Variables or Feature Flags sections when none are being added or touched.
- Separate Timeline Risks / Dependency Risks subsections — use the single Risks table when risks exist.

**Rule:** if a section has no substance for this feature, delete it — don't leave a placeholder.

## Output Guidance

- **Be specific.** Provide code examples, not descriptions. Provide `file:line` refs, not "somewhere in the cart layer."
- **Be practical.** Design for the codebase you have, not the ideal one. Follow existing conventions even when they aren't perfect.
- **Be consistent.** If a pattern exists, reuse it. New patterns require justification.
- **Be minimal.** Don't over-engineer. Don't add error handling for impossible cases. Don't add sections with no substance.
- **Document decisions.** If you chose approach A over B, say why — one sentence is enough. Do not present A and B as equal options in the main design.
- **Delete, don't placeholder.** If a section in the required list doesn't apply (e.g. a pure-refactor feature with no new test scenarios), write one sentence explaining why that section is empty, rather than leaving TODO-style filler.

## Output file

Write the techspec to a new file alongside the feature description and integration analysis, using the same base name: `{feature_name}_techspec.md`. If no base name is discoverable from the inputs, ask the user for one before writing.
