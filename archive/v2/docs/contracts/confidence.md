# Confidence assessment and advancement

Use an explicit 0–100% assessment for the scoped conclusion or next workflow step.
This is a structured judgment of evidence and remaining uncertainty, not a calibrated
probability of correctness, success, or safety. A score never supplies facts, turns
worker agreement into proof, passes an unrun/failed check, or grants authorization.

## Resolve one effective policy

Record `confidence_policy` with the assessment subject/scope, rubric and weights,
advancement threshold, policy source, required evidence, and authorized action boundary.
For incidents also record severity, active/resolved state, and pass depth. Resolve it from
applicable instructions and a supplied caller policy; without either, use these defaults:

- Normal advancement threshold: **90%**. Scores **90–94%** permit the bounded next step
  with explicit uncertainty and follow-up checks; **95–100%** indicate stronger support
  within the inspected scope. Neither band means ship-ready or approved by the owner.
- An **active P1 incident** uses the investigation's declared streamlined depth and
  **70%** threshold through its investigation, review, fix-design and verification
  handoffs. This adjusts urgency/depth, never causal evidence or permission. Do not
  infer P1 merely to lower a threshold. After resolution, record the state change and
  restore normal depth/threshold for new work.
- Preserve every applicable stricter user/repository requirement. A caller may supply
  a stricter threshold or rubric; an inherited incident policy is not silently replaced
  by a downstream normal default. If multiple applicable minimums exist, use the highest.
  Missing scope-critical policy information is a precise question, not an assumed waiver.

Pass the complete effective policy in worker briefs and downstream input bundles, including
its source and any stricter gates. Workers use the caller's rubric and threshold, return
their own evidence/uncertainty, and do not relax the policy. Downstream stages use their
stage rubric below unless explicitly overridden, while preserving the effective threshold,
causal requirements and authorization boundary. Reassess changed evidence; do not copy an
upstream score or average worker scores into the final assessment. If a legacy caller passes
only `confidence_gate`, treat it as an explicit minimum and combine it with applicable
stricter requirements; it cannot replace the rest of the effective policy.

## Calculate from a workflow-appropriate rubric

Rate each factor 0–100 against the actual inspected evidence, then calculate
`N = round(sum(weight × factor_rating) / 100)`. Weights are percentage points and total 100.
Show factor ratings and weighted contributions so the result can be checked. These anchors
must be applied to checked arithmetic: use an available calculator or execute an arithmetic
expression to verify each contribution, their sum and the rounded score. Read the actual result;
do not claim a tool-checked calculation from mental arithmetic. If no calculation tool is
available, show the manual calculation and label its arithmetic unverified.
The following anchors
guide judgment: **0** no supporting evidence; **50** partial evidence with major gaps;
**75** mostly supported with material unknowns; **90** directly supported with bounded
residual uncertainty; **100** all required evidence for this factor and scope checked,
with no known unresolved gap. Intermediate ratings require a concrete reason; do not
raise ratings to cross a threshold. A difficult change can score well when its complexity
and impact are understood and controlled. Unread or unrun evidence cannot earn full credit.

| Stage / rubric | Factors and weights |
|---|---|
| `analysis` — analyze-work | Requirements clarity 40%; codebase-or-constraint understanding 40%; change-path clarity at reference-map altitude 20%. Greenfield uses verified constraints and ecosystem precedents for codebase understanding. |
| `design` — techspec | API/docs and requirements clarity 30%; suitable inspected patterns 25%; data-flow/dependency understanding 20%; complexity understood and controlled 15%; cross-system impact understood and bounded 10%. |
| `decomposition` — tasks-breakdown | Fidelity to approved design/locked decisions and requirement coverage 35%; dependency, lifecycle and resource closure 25%; test/AC ownership and executable checks 25%; task boundaries, sizing and path grounding 15%. |
| `diagnosis` — bug-investigation | Causal clarity and evidence 40%; codebase/execution-path understanding 30%; proposed solution or next-probe simplicity and fit 15%; similar-pattern coverage 15%. State whether the subject is a confirmed diagnosis, candidate hypothesis, or mitigation. |
| `delivery` — implement-task, verify-task, qa-gates, review-implementation | Requirement/AC and changed-scope coverage 30%; direct source and executed-check evidence for the claimed stage 35%; data-flow, dependency and environment understanding 20%; risk, regressions and rollback control 15%. Planned tests are not executed-check evidence. |
| Artifact review — review-artifact | Use the producing artifact's rubric to assess the post-review artifact, with current evidence and the caller's effective threshold. Assess a worker's lane only within its assigned scope; a partial lane cannot establish whole-artifact coverage. |

Judge each factor against the stage's obligations: analysis does not need future implementation
tests to pass, while verification does need its required executed checks. A missing analysis
input is a named gap, not automatically a zero when equivalent verified evidence is available.
Before implementation, assess readiness from the inspected design/source and required baseline
checks; do not claim future post-change tests passed. Reassess outcomes after the change.
Do not omit a factor merely because evidence is missing. If a factor truly does not apply,
explain why and redistribute its weight proportionally across applicable factors; show the
effective weights. An explicit caller rubric replaces the default weights, not evidence rules.

## Apply the gate separately from the arithmetic

First check required evidence, applicable failed/blocked gates, causal requirements and
authorization; then compare the score to the effective threshold. A weighted average can
hide a critical gap, so **any missing load-bearing evidence blocks the dependent conclusion
even at 99%**. State both the calculated score and the actual advancement verdict.

Below threshold, do not advance the dependent design/implementation step, issue an Approved
review, mark a task Done, or treat a QA conclusion as passing. Record exactly what is blocked,
why, and the next confirming/refuting check. Continue authorized independent inspection,
tests and factual/partial drafting that do not rely on the uncertain premise. Ask the owner
only for a missing fact or decision they must supply; a low score alone does not require a
routine permission round. Honor an explicit stricter instruction to pause the whole task.

At or above threshold, proceed only when the relevant evidence gates and existing
authorization also allow it. A build/test command with exit zero retains that observed
result even if overall confidence is below threshold; the workflow still cannot advance.
An unavailable required test stays BLOCKED, a failed check stays FAIL, and stale review
evidence stays stale. Any accepted limitation needs the workflow's actual owner acceptance
and reason; the score cannot provide it, relabel it PASS, or waive a non-waivable gate.
Final human GO remains the human's decision where the workflow requires it.

Severity is impact, certainty is support for a claim, and causal evidence links mechanism
to failure. Keep them separate. Retain SOURCE / OBSERVED / INFERRED labels in diagnosis and
review: inspecting a possible branch does not prove it caused an incident. Preserve a
plausible severe uncertain issue with its next probe, even when its score is low. Active
P1 can support an explicitly authorized reversible mitigation with rollback and monitoring;
neither mitigation success nor its threshold proves the diagnosis.

## Required report and handoff

In the artifact's **Confidence score** section or the existing review/verification record,
include this compact format without relying on private instructions:

1. `Confidence score: N% — <subject/scope and one-line reason>`.
2. `Effective policy: <rubric, threshold, source, stricter requirements; incident state/depth when applicable>`.
3. A factor table: `Factor | Weight | Rating | Contribution | Evidence / gap`, with source
   locators or executed-check record IDs. Show the calculation total.
4. **Why N%**: concrete supporting evidence; refer to the factor rows without duplicating
   long descriptions.
5. **100−N% uncertainty**: each remaining gap, its consequence (which conclusion/task/gate
   it blocks, or why nonblocking), and the next check/owner decision. This label describes
   the heuristic score remainder, not a measured error probability. At 100%, state no known
   remaining gap in the assessed scope and preserve the scope's limits.
6. `Advancement: proceed within <boundary> | blocked on <gap>`, with independent work still
   permitted and any existing accepted limitation. Name the actual authorization boundary.

Analysis/spec/task documents carry one scoped assessment; implementation records it before
the first dependent edit and refreshes it at handoff when evidence changes. Reviews assess
the reviewed subject after corrections. Verification/QA records the scoped assessment and
each selected gate's score/reason where its evidence differs; a shared factor table may be
cited by gates with the same subject/evidence, avoiding duplicate tables. Every gate still
records its own actual check result and blocker. Gate 5 records actual human GO, not an
assistant confidence score for the owner's decision.
