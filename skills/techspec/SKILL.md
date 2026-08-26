---
name: techspec
description: "Design-phase technical specification — the committed blueprint (approach, implementation map, test plan with prioritized QA scenarios, risks) built on an /analyze-work reference map, a reviewed bug investigation, or a high-level implementation plan. Detects the work type and adapts: feature integration, greenfield slice, refactor / tech debt, or bug fix / hotfix / incident remediation / risky change. Produces {work_name}_techspec.md. Use when asked to write a techspec, technical spec, design doc, implementation plan, refactor plan, or impact analysis for defined work. Invoke as /techspec."
---

# techspec — committed design blueprint (integration · greenfield · refactor · fix)

Act as a senior software architect producing the committed technical specification for defined work: the blueprint a developer implements from. You DECIDE and SPECIFY — one approach, file-by-file, with the tests that lock each behavior.

> **Litmus test:** if the doc presents options without committing, or a section has no substance for THIS work item, you're not done. One decision per fork; delete, don't placeholder.

## When to use

- **Ad-hoc**: the work is defined (ideally with a reviewed analysis or investigation) and needs a design-for-the-record before implementation — too big to hold in plan mode, not big enough for a multi-session program.
- **After** `/analyze-work` (integration / greenfield / refactor work) or `/bug-investigation` + `/review-artifact` (fixes).

## When NOT to use

- Investigation → suggest explore or `lay-of-the-land`
- No map yet of where the work lands → `/analyze-work` first
- Diagnosing a failure → `/bug-investigation`.
- Trivial change or small well-understood fix → plan mode / the investigation's minimal-fix proposal. No techspec.
- Breaking an approved spec into tasks → `/tasks-breakdown`, not this skill.

## Detect mode

1. **integration** mode:
   - Signal: add feature into an existing codebase (default when a repo exists)
   - Lens: Core contract below

2. **greenfield** mode:
   - Signal: New project / slice with a PRD or an analysis carrying a `## Slice requirement`, little or no code yet
   - Lens: Slice-scoped guards

3. **refactor** mode:
   - Signal: Restructure / de-debt existing behavior, no new capability
   - Lens: Phased plan + rollback + metrics

4. **fix** mode:
   - Signal: A reviewed bug investigation proposes a change
   - Lens: Impact (blast radius + risk level)

Detect from the request and inputs:

- **echo the detected mode + resolved `{work_name}` + chosen depth back before designing**;
- If in a **genuinely** ambiguous scenario, ask which one to use
- Mixed work → dominant mode, secondary lens noted in the doc. The **risk lens** below is orthogonal — any mode can trigger it.

## Depth

### Single-approach by default

By default, commit to **pragmatic balance**:

- reuse existing patterns aggressively, including naming convention
- new abstractions should only be introduced where they pay back inside this work and must be brought with details to the user - do not commit to any new abstractions on your own
- added code should be minimal - do not overengineer
- scope-reduce and defer rather than widen
- no YAGNI speculation (no feature flags, compat shims, or single-use helpers this work doesn't need)
- match existing conventions even when imperfect — consistency beats local optimization.

### When and how to escalate

When the architectural latitude is genuinely open:

- Implementing a new feature in an existing codebase, and there are no strong references to follow
- Explicitly introducing a new pattern
- Greenfield work

Escalate to a 3-way multi-agent exploration:

- default: minimal-changes / clean-architecture / pragmatic-balance
- refactor: refactor mode: minimal-risk / clean-architecture / pragmatic-balance

If you judge worthwhile, suggest extra fan-outs.

Before spawning, ALWAYS get the user's explicit approval on the fan-out, and record the justification in the doc.

- A lived run fanned out against the documented default and the oversized design propagated into 14 tasks before review caught it. The ~3× token cost must buy real divergence.

## Input contract — loose

Accept whatever the invocation provides, in order of authority:

1. **Reviewed analysis** (`{work_name}_analysis.md`, `## Review`-stamped)
2. **Reviewed investigation** (`{bug_id}_investigation.md`) — authoritative for scope, files touched, and clarifications when present.
3. **Work description / PRD / bug report** — the requirement itself. Greenfield without a user-written PRD: the analysis's `## Slice requirement` section (Done-when + Building on) is the requirement.
4. Plan built with plan mode.

**NOTE:** for lighter inputs (no analysis, work not trivial) → proceed, but name the gaps an analysis would have closed in the confidence section. Fix mode without a reviewed investigation → run `/bug-investigation` first. Derive `{work_name}` from the input filenames; else propose one from the topic and confirm.

## Subagents guidance (3-way depth only)

Single-approach → design on the main thread; no subagents.

3-way → launch 3 **generic** subagents (there are no named techspec agents to maintain), each handed the inputs + one mandate + these constraints verbatim:

1. "Design for YOUR mandate only. Return a draft techspec; do not write files or spawn further subagents."
2. "Read the files the analysis names — don't trust summaries. Cite file:line for every pattern you reuse."
3. "Score confidence 0–100%; if the inputs leave you below 90%, return clarification questions instead of guessing."

When they return:

- **Convergence-risk:** what ALL drafts agree on at the same level of detail is the _highest-risk_ region — agreement measures shared framing, not correctness. Verify it against code before recommending.
- **Harvest:** factual corrections found by any draft, including losing ones, port into the winner.
- Present per-approach summaries + a trade-offs comparison + your recommendation with reasoning; the user picks; build the final spec for the chosen approach, folding in the harvest.

## Process

### Gather Context

**Read the inputs end-to-end.** Description, analysis/investigation, review notes.

### Map Existing Patterns

Read every file the analysis names — don't rely on summaries. Then:

- Search for similar features; record `file:line` as you go.
- Note layering, DI, naming and validation conventions, reusable utilities/services, `AGENTS.md`/architecture-doc guidance.
- **Proxy/adapter/router changes map 1:1 to the consumer:** list every consumer call site as `consumer file:line → outgoing URL/signature → new-or-existing route → handler`, matched by literal route string
  - "calls the same method" is not coverage, and a summary count is not acceptable
  - For greenfield: map the "Building on" code named by the PRD or the analysis's `## Slice requirement`, plus prior-slice techspec precedents.

### Design, committed

Plan file-by-file. API contracts, data models, components — only what this work actually needs. Key algorithms, error paths, edge cases, and the tests that lock each behavior. Apply the mode lens.

- **Complexity checkpoint (brownfield):** before writing sections, produce a production-delta map — the smallest delta that satisfies the requirement — and a reuse/modify/add table. Every net-new mechanism (flag, protocol, monitor, identity scheme, config switch, retry/dedup layer) names the observed failure or stated requirement forcing it; a mechanism with no named forcing observation is out (8 such were stripped by review in a lived run after propagating into tasks, infra, and code).

### Critical refactors surface separately

Debt that MUST move for this to ship safely is documented apart from the main spec and user-approved before baking any of it in. No uninvited refactors.

### Confidence gate

1. Calculate the confidence scoreScore 0–100% per the following factor breakdown:

- API/docs clarity (30%)
- Similar patterns in codebase (25%)
- Data-flow understanding (20%)
- Complexity (15%)
- Cross-system impact (10%)

2. Once calculated, act according to the result:

- ✅ ≥ 95% - Ideal, ship-ready. Confirm the consolidated analysis with the user, then write the file
- ✅ ≥ 90% - all clear, proceed. Confirm the consolidated analysis with the user, then write the file
- ❌ < 90% → STOP and ask clarifying questions.

### Write the spec

Write the spec following the section contract.

### QA-scenario pass

With the spec written, launch a separate agent to re-read it as a QA engineer and derive the scenarios that would exercise it: happy path, error conditions, the edge cases the design sections called out, and integration points when the change crosses a component or system boundary.

- Every behavior the spec commits to maps to at least one scenario
- Each scenario gets a priority (High/Med/Low) and an automatable-or-manual flag.
- Fold the result into the Test plan (§6) — the final doc carries the spec _and_ how to test it — then confirm with the user.
- Proportionality: heavyweight matrices (browser/device, full accessibility sweep, security audit) enter only when the work demands them; for most work a tight functional scenario list is enough.
- **Perf/regression scenarios:** when the work touches a perf-sensitive surface (hot path, DB query shape, caching, payload size), consult the repo-local perf/regression skill if the repo has one (baselines are repo-specific — never invent generic thresholds); no local skill → name the perf risk as a manual scenario and flag the gap (a candidate for `/close`'s repo-local skill mint).

## Mode lenses

### greenfield (slice-scoped)

- Stick to the slice scope: the spec answers "how do we ship THIS slice" — never "how does the whole product work". Decisions that only matter at slice N+2 are deferred to slice N+2's techspec.
- **Key decisions** (required section) get Choice / Rationale / Alternatives.
- **Reject:**
  - locking a final file structure for the whole project
  - pre-designing components future slices will introduce
  - caching/optimization before measured slowness
  - OWASP/auth sections unless the slice ships auth or untrusted-input handling
  - deployment sections unless this slice deploys
  - coverage-percentage targets (name the specific tests instead)
  - Escape-hatch sections (performance / security / migration / monitoring / deployment) unless the slice demands them.

### refactor (phased plan)

- **Confirm success metrics with the user before designing** — "what specific metrics prove this worked?" and the minimum acceptable improvement; if they can't be defined, the scope is too vague → back to `/analyze-work`,
  - Each metric names **how it will be measured** (the command, query, or observation) and its current baseline — a metric with no measurement method is a wish, not a metric.
- Then choose the transition pattern (strangler fig / branch-by-abstraction / incremental / big-bang only if unavoidable) and define **phases**: each independently deployable, delivering value or reducing risk on its own, with a **rollback point** (method / data plan / trigger), measurable success criteria, and a **deployment strategy** — how THIS phase reaches production (sequencing, feature flags, canary/gradual rollout, coordination with releases in flight).
- Spec the testing strategy against the analysis's gap list — including **transitional-state tests**: the mid-migration states where old and new paths are both live are states the end-state suite never exercises; name the tests that cover each one.
- Add the rollback decision tree (success → continue / minor → fix forward / major → roll back) and a **Contingency & unknowns** block: the known unknowns, and trigger → response pairs for the failures you can anticipate ("if phase 2's dual-write diverges, then …"). A phase with no viable rollback gets flagged loudly — consider feature flags or smaller increments; DB migrations get extra scrutiny (data rollback is often impossible).
- The implementation map and test plan live inside the phases.

### fix (impact)

- Design the fix the reviewed investigation proposed — **no re-diagnosis** (that's done) and no drift into a refactor plan.
- The impact half is required, not optional: **direct dependencies** (who imports / calls / instantiates the changed code — grep, don't assume), **indirect** (shared state, side effects, events, config), **test coverage** of the changed paths and — explicitly — the gaps, plus the risk lens below.
- Keep it proportional: the design half may be short when the fix is small; the blast radius is why this doc exists.

**Hotfix variant** (live incident remediation): the implementation map becomes an executable playbook — exact commands, expected result and a validation step per action, rollback **triggers** ("if X, roll back") with exact rollback steps, and success criteria that declare victory. Severity sets the tone: P1 accepts documented technical debt for speed — record what this fix does NOT address as a hand-off list for `/post-mortem`. Escalate (flag `ESCALATION RECOMMENDED: [reason]`, don't just proceed) if remediation needs a breaking change, a data migration, a production-DB change, or compliance review.

## Risk lens (fix mode always; any mode when the change is risky)

Triggers: shared/core code, DB migration, auth/payments/hot path, hard-to-reverse data effects. Adds to the spec:

- **Risk level** in the Summary — LOW (single file, well-tested, easy rollback) / MEDIUM (multiple files, moderate coverage, some external deps) / HIGH (many files, limited coverage, critical deps, hard rollback) / CRITICAL (core system, production data at risk, no rollback — escalate before proceeding).
- **Recommendation** in the Summary — SAFE TO IMPLEMENT / IMPLEMENT WITH CAUTION / REQUIRES ADDITIONAL REVIEW.
- **Rollback** and the **Risks table** promoted from optional to required.

## Section contract

Required, in roughly this order:

1. **Summary** — 2–3 sentences: the pivotal file(s), the mechanism of change, the blast radius (production/test file counts, layers) — plus risk level & recommendation when the risk lens is on.
2. **Approach** — the chosen approach and why it won here; what's reused, what's net-new, what is explicitly _not_ being built. A reader sees the YAGNI decisions up front.
3. **Scope / out-of-scope** — out-of-scope as a table (`| Item | Why out of scope | Where to revisit |`) beyond two items; the Why column stops future readers reopening settled decisions.
4. **Patterns reused** — `| Pattern | Source | Usage here |`. Every citation **verified, not guessed — and anchored on a stable token** (symbol name / unique literal / nearest heading), with the line number a _hint that drifts_: write `AppContext.tsx → useAuth() (≈:55)`, never a bare `:NN`. Re-locate and re-verify any inherited citation against current source before relying on it — never reuse one verbatim.
5. **Implementation map** — file-by-file: path + Create/Modify, what changes and **why** (one sentence), before/after snippets for non-trivial edits with the real names (no placeholder `[NewThing]`), and which §4 pattern each follows. Verification extends to **test-file locations** (one Glob per named test file/project — a spec that guessed the wrong test project survived two reviewers) and to **lifted code's closure** (when a step says "lift/copy X verbatim", enumerate X's imports, helpers, and config keys, and diff the whole source file per environment — verbatim lifts carried compile-breaking references twice). **Config keys** follow the repo's nesting convention, describe their value, and split secret-vs-static. _(Refactor mode: the phase plan replaces this section.)_
6. **Test plan** — `| # | Scenario | Inputs | Expected | Priority | Automatable |`, populated by the QA-scenario pass (Process 7): happy path, error conditions, called-out edge cases, integration points — every committed behavior covered by ≥1 scenario. Concrete test outlines in the repo's framework over prose; at least one explicit "tests NOT needed here, because…" where a surface is deliberately skipped.
7. **Files changed summary** — table + explicit count: `N production files, M test files. No new files / no DB migration / no DI changes.` (whichever apply).
8. **Confidence score** — `Confidence score: N% — <one-line why>`, then **Why N%** (3–5 bullets of concrete evidence: files verified, patterns matched, deps confirmed) and **100−N% uncertainty** (2–4 bullets, each with an impact note: blocks implementation? operational? minor judgement call?).

Mode additions (required there, absent elsewhere): greenfield → **Key decisions**; refactor → **Phases** (each with its deployment strategy), **Success metrics** (with measurement method + baseline), **Testing strategy** (incl. transitional-state tests), **Rollback strategy**, **Contingency & unknowns**; risk lens → **Rollback**, **Risks table**.

Optional (only with substance — delete, don't placeholder): Data flow (spans > 2 layers or a system boundary) · Rollback · Deployment sequencing · Risks table (`| Risk | Likelihood | Impact | Mitigation |`) · Rejected approaches (short Option A/B with rationale) · Revision banner (scope pivoted mid-spec) · Open technical questions (only with user-approved residual uncertainty).

**Do not include:** generic framework/library prose for the stack the repo already uses · styling notes for non-styling work · Monitoring & Observability by default · documentation-needs checklists (surface as implementation tasks) · S/M/L/XL complexity estimates (the files-changed count is the better signal) · Mocking Strategy subsections (fold into the test plan) · placeholder env-var / feature-flag sections when none are touched · separate timeline/dependency-risk subsections (one Risks table).

## Output guidance

Be specific (`file:line` and real names, not "somewhere in the cart layer") · practical (design for the codebase you have) · consistent (reuse patterns; new ones need justification) · minimal (no error handling for impossible cases) · decisive (one sentence on why A beat B — never A and B as equal options in the main design).

## Output file

Write to `{work_name}_techspec.md`, alongside the inputs — all modes, refactor included (the archived `_plan.md` suffix is retired). No discoverable base name → ask before writing. After writing, **offer `/review-artifact`** before tasks or implementation build on the doc.
