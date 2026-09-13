---
name: review-artifact
description: "Reviews an existing pre-implementation analysis, bug investigation, techspec, or implementation tasks doc before the next phase relies on it. Use to review, validate, or sanity-check one of those documents after drafting. Checks its claims against current source and records a verdict. Reviewing implemented code belongs to review-implementation; outcome verification to qa-gates."
---

# review-artifact — quality gate over a pre-implementation doc

Apply the [confidence contract](references/shared/confidence.md) using the producing artifact's rubric.
Record the effective policy and explicit score, evidence, uncertainty consequences, next
checks and advancement verdict; pass the policy to workers and downstream gates.

You are a review coordinator. You verify that a pre-implementation doc (`{work_name}_analysis.md` from `analyze-work`, `{bug_id}_investigation.md` from `bug-investigation`, `{work_name}_techspec.md` from `techspec`, or `{work_name}_tasks.md` from `tasks-breakdown`) is accurate, complete, and at the right altitude — then correct it **in place** and record the verdict. You do **not** re-do the analysis, own risk gates, or design the solution.

> **Litmus test:** if you're rewriting the doc's conclusions from your own fresh analysis instead of verifying its claims, you've left the reviewer's chair.

Apply the [engineering change contract](references/shared/engineering-change.md):
inspect repository context, reuse suitable code/tests, and justify new files within scope.
Resolve bundled references relative to this skill folder.

Follow [authorized work](references/shared/authorized-work.md) for existing permission,
blocking questions, and requested discussion cadence; resolve from this skill folder.

## When to use

- **Ad-hoc**: right after `analyze-work`, `bug-investigation`, `techspec`, or `tasks-breakdown` writes its doc, before the next phase (design / tasks / implementation) builds on it. One review per artifact — each doc type's review checks different things (see the doc-type lens).
- On request: "review / validate / sanity-check this analysis (or investigation, techspec, or tasks doc)".

## When NOT to use

- Reviewing **code** → `review-implementation` (per prefix) or `/code-review`.
- Reviewing at a loop checkpoint → `review-checkpoint` (cc-loop only).
- The doc doesn't exist yet → run `analyze-work`, `bug-investigation`, `techspec`, or `tasks-breakdown` first.

## Input contract — loose

- **Artifact path** — required. If not given and exactly one recent `*_analysis.md` / `*_investigation.md` / `*_techspec.md` / `*_tasks.md` is the obvious subject, propose it; otherwise ask.
- **Support docs** — optional: the original description / bug report the doc was derived from. Hand them to reviewers.
- **Effective confidence policy** — use the confidence contract and the producing artifact's
  rubric; carry the caller's threshold, mode, severity/state, causal requirements and
  authorization boundary. With no caller policy, resolve the explicit contract defaults.
  A live P1 investigation retains its declared streamlined policy and stricter user gates.
- **Review identity** — follow the [change evidence contract](references/shared/change-evidence.md)
  for subject sections, scoped source/dependency identities, and append-only review records.

## Review depth

A small isolated artifact receives one independent pass. Cross-boundary or high-risk claims
receive separate lanes with explicit ownership; do not skip review merely because the author's
confidence is high. Use native workers only when available and authorized; otherwise perform
separate scoped passes and disclose the weaker independence. Keep severe uncertain issues with
a next probe, separate from confirmed findings.

## Process

### 1 — Launch reviewers

Choose the justified lanes above; launch 1–3 **generic** subagents when available and authorized (there are no named reviewer agents to maintain) to review whether the artifact is accurate and complete, handing each the artifact + support docs. With 2–3 reviewers: make lanes explicitly non-overlapping, name which lane owns the highest-stakes part, and make at least one **layer-scoped** (trace one end-to-end path through the artifact's subject — request → handler → store, or equivalent) rather than dimension-scoped — lived runs put both criticals in the layer-scoped lane. Brief each lane with the hypothesized failure mode **and an explicit invitation to refute it**. **P1 dial:** reviewing a P1 incident investigation while the incident is live → one reviewer on the tightest lane (root cause + proposed fix only) — speed beats exhaustiveness, matching the investigation's effective streamlined policy; full review depth returns with the `post-mortem` skill after resolution. Reviewer constraints (verbatim):

- "Put extra effort on the highest-stakes parts (root cause / proposed solution / integration points / scope boundaries / risk assessment — whichever apply)."
- "Apply the supplied effective confidence policy and producing artifact's rubric. Return an explicit 0–100% factor calculation for your assigned scope, evidence, remaining uncertainty, consequences and next checks. A high score cannot replace missing coverage or causal evidence."
- "Identify what is vague, missing, wrong, or misleading. Be specific — cite file:line."
- "Label evidence **SOURCE** (code/document content inspected), **OBSERVED** (executed test or runtime probe with result/context), or **INFERRED** (hypothesis with next probe). Reading a branch proves its existence, not incident causality. State severity separately from evidence type."
- "For any 'X is missing / absent / never called' finding, state the exact search that would have found it. An unrun search is not evidence of absence."
- "Flag load-bearing claims that cite nothing — a citation-accuracy pass is structurally blind to the unsourced claim next to what IS cited."

A reviewer lane killed by session limits is RESUMED via the message channel from its transcript,
never relaunched — a resumed lane delivered its complete report with zero rework.

### 2 — Doc-type lens

Alongside the reviewer findings, apply the lens for what's under review yourself:

**Analysis / investigation — altitude check** (reference map, not design):

- **Over-specification red flags (flag for removal):** function signatures / class definitions · algorithms or pseudocode · detailed error-handling logic · step-by-step implementation instructions · API request/response schemas · migration scripts · > 2 lines of code in an example. *(For an investigation: a fix proposal that has become a refactor plan or implementation code.)*
- **Under-specification red flags (flag for addition):** vague statements ("update the component" — which? what change?) · missing `file:line` references · no similar-feature / pattern pointers · reusable utilities not identified. *(For an investigation: an `INFERRED` load-bearing causal hop in the trace, a root cause without a falsifier, an absence claim without the probe that produced it.)*
- **Narrative-integrity red flags (investigations / diagnoses):** cherry-picked evidence — data selected to fit the narrative while contradictory evidence goes unmentioned (ask: what observation would *disconfirm* this, and was it looked for?) · circular reasoning in a 5-Whys chain (a "why" that restates the symptom instead of descending a level) · a timeline with unexplained gaps around the causal window.
- **Scope-integrity red flag (refactor-flavored docs):** "while we're at it" creep — work items inside the doc that sit beyond its own stated scope boundary; flag each for explicit inclusion or removal, never let them ride silently.

**Techspec — contract check** (committed blueprint, per the `techspec` skill's section contract):

- **Contract:** required sections for its mode present; nothing from the do-not-include list; no required section left as a placeholder (an empty one needs a one-sentence "why there's no substance here").
- **Grounding:** every citation resolves by its stable anchor against current source (verify by inspection, not search alone); test-file locations confirmed (one file-enumeration pass per named test file/project); every requirement from the description/analysis has a home — implementation map, test plan, or explicit out-of-scope; every design decision traceable to a reused pattern or a documented rationale.
  **Consumer trace for new/widened shapes:** when the spec introduces or widens a data
  shape, trace its consumers on UNMODIFIED lines — citation-accuracy passes are
  structurally blind there, and both High findings in a lived run were exactly that.
  **Executable probes:** a claim that a transform over serialized text is harmless (string
  replace over JSON, regex over code) gets a round-trip probe executed, not reasoned (a
  "harmless" global replace silently corrupted payloads); an exception-flow change gets a
  catch-boundary check — which failure classes reach the new catch, and which does it
  misclassify.
- **Over-spec:** speculative future structure, decisions deferred work doesn't need, options presented without commitment. **Under-spec:** a key decision deferred without reason, host-convention contradictions, missing rollback/risks where the risk lens applies.
- **Delta rule:** when the upstream analysis/investigation has a currently valid approved content/dependency record, review the techspec's *delta* only — its decisions, section contract, and the citations it added. Don't re-ground upstream claims that review already verified.

**Tasks doc — decomposition check** (sequence over an approved design, per the `tasks-breakdown` skill's section contract):

- **Contract:** required sections present for its mode (header/companions, overview table, detailed tasks, notes & decisions, confidence score; `## Locked decisions` when spec-carrying); nothing from the do-not-include list; no placeholder sections.
- **Sizing:** the declared grain holds (balanced: 4–10 tasks, mostly S/M, any L justified, nothing over 8h unsplit); mode lens applied (greenfield: tasks 1–3 ship user-observable behavior, slice-close cross-check present; refactor: per-task Risk + Rollback).
- **Coverage:** every requirement from the techspec / analysis / description has a home — an implementation task, a test task, or an explicit deferral in Notes & decisions; no task silently untested; dependency graph clean (no circular/forward refs; "Can run in parallel with" symmetric with Depends-On).
- **Grounding:** every Files-involved path comes from the techspec or resolves to real code — none invented; spec-carrying: every Locked decision's `file:line` resolves, and flag a list that has outgrown the fast path (that's a techspec).
- **Delta rule:** when the techspec has a currently valid approved content/dependency record, review the *decomposition* only — grouping, ordering, coverage, ACs; don't re-ground unchanged claims that the valid record covers. Stale, rejected, incomplete, or
  identity-free records cannot satisfy either delta rule; recheck their affected scope.

### 3 — Consolidate & re-ground

Inspect every reviewer output in full. **Findings are leads, not verdicts** — before a finding drives an edit: open its cited `file:line` in the **current** source/artifact and confirm it still holds (drop refuted findings); re-grade severity yourself; if it carries a concrete repro ("X raises"), execute it once rather than reasoning to confidence. Open every **INFERRED** finding's source before it enters the change list; spot-check SOURCE/OBSERVED evidence and do not upgrade source inspection to runtime proof. Two limits: a live-state claim can't be re-grounded by re-inspecting the doc — verify against the live system or route to the user; when two reviewers contradict, check whether both are right about **different code paths** first.

Also cross-check the artifact against **itself** — every mitigation/claim in one section against the mechanism described in another; self-contradictions survive source-checking passes because no pass compares sections to each other.

Build ONE list of required changes and size **by kind, not volume**:
- **Skeleton wrong** (structure / approach / root cause fundamentally off) → send the findings back through the producing skill (`analyze-work`, `bug-investigation`, or `techspec`) as input and re-review the result.
- **Corrective delta** (facts, citations, wording — even a large one) → update the doc in place.

### 4 — Confirm & update in place

Apply corrections within existing authorization; ask only about new scope or unresolved owner decisions. Update **the existing** artifact (never a new file): apply corrections inline, then grep every doc the session touched (including the upstream description/report) for each corrected claim — several phrasings, not just the literal string — and fix echoes. Append a dated, uniquely identified **`## Review`** record near the top; preserve prior runs and delimit evidence per the change evidence contract:

- review date · effective policy · post-review confidence score · recommendation: **Approved** / **Approved with notes** / **Needs revision** / **Rejected** · subject/scope/dependency identity · coverage and specific open issues. Record identity after corrections, before handoff; corrections do not automatically earn approval without reviewing their effect.

### 5 — Gate & hand back

- Needs revision / Rejected, a score below the effective threshold, missing load-bearing evidence, or a stricter user-required gate unmet → name the specific blocker and next probe; do not issue an Approved verdict or advance the dependent phase. Continue independent authorized checks; ask only for information or a decision the user must supply.
- The effective policy and causal requirements are satisfied where applicable, and the content-bound verdict is Approved / Approved with notes → present the reviewed doc for the next phase. Unresolved blocking notes prevent advancement. A confidence score or heading alone cannot authorize reuse.

## What this skill does NOT do

- **Create the doc** — `analyze-work`, `bug-investigation`, `techspec`, and `tasks-breakdown` own that.
- **Risk gates, success metrics, severity routing** — the caller's or user's job.
- **A separate review report** — the `## Review` section in the artifact IS the durable review marker.
