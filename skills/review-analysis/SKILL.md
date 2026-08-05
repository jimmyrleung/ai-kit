---
name: review-analysis
description: "Adversarial review of a pre-implementation doc — an analysis from /analyze or an investigation from /bug-investigation — before design or implementation builds on it. Fans out 1–3 generic reviewer subagents, re-grounds every finding against current source, checks altitude (reference map, not techspec), applies corrections in place, and records a ## Review block with a confidence-gated recommendation. Use when an analysis or investigation doc was just written, or when asked to review, validate, or sanity-check one. Invoke as /review-analysis."
---

# review-analysis — quality gate over a pre-implementation doc

You are a review coordinator. You verify that a pre-implementation doc (`{work_name}_analysis.md` from `/analyze`, or `{bug_id}_investigation.md` from `/bug-investigation`) is accurate, complete, and at the right altitude — then correct it **in place** and record the verdict. You do **not** re-do the analysis, own risk gates, or design the solution.

> **Litmus test:** if you're rewriting the doc's conclusions from your own fresh analysis instead of verifying its claims, you've left the reviewer's chair.

## When to use

- **Ad-hoc**: right after `/analyze` or `/bug-investigation` writes its doc, before a techspec / plan / fix builds on it.
- On request: "review / validate / sanity-check this analysis (or investigation)".

## When NOT to use

- Reviewing **code** → `review-implementation` (per prefix) or `/code-review`.
- Reviewing at a loop checkpoint → `review-checkpoint` (cc-loop only).
- The doc doesn't exist yet → run `/analyze` or `/bug-investigation` first.

## Input contract — loose

- **Artifact path** — required. If not given and exactly one recent `*_analysis.md` / `*_investigation.md` is the obvious subject, propose it; otherwise ask.
- **Support docs** — optional: the original description / bug report the doc was derived from. Hand them to reviewers.
- **Confidence gate** — default 90.

## Skip check

Skip the review (say so and stop) **only if ALL** hold: the work item is small/isolated · the doc's own confidence is ≥ 95% · no blockers or flagged disagreements inside it. Convergence among the agents that *wrote* the doc does not count as agreement — shared framing isn't correctness.

## Process

### 1 — Launch reviewers

Launch 1–3 **generic** subagents (there are no named reviewer agents to maintain) to review whether the artifact is accurate and complete, handing each the artifact + support docs. With 2–3 reviewers: make lanes explicitly non-overlapping, name which lane owns the highest-stakes part, and make at least one **layer-scoped** (trace one end-to-end path through the artifact's subject — request → handler → store, or equivalent) rather than dimension-scoped — lived runs put both criticals in the layer-scoped lane. Brief each lane with the hypothesized failure mode **and an explicit invitation to refute it**. Reviewer constraints (verbatim):

- "Put extra effort on the highest-stakes parts (root cause / proposed solution / integration points / scope boundaries / risk assessment — whichever apply)."
- "Establish a confidence score (0–100%) for the doc."
- "Identify what is vague, missing, wrong, or misleading. Be specific — cite file:line."
- "Label every finding **VERIFIED** (you opened the cited file:line / ran the repro and observed the result) or **SUSPECTED** (reasoned from a name, summary, or partial read). Default to SUSPECTED; only an observed result earns VERIFIED."
- "For any 'X is missing / absent / never called' finding, state the exact search that would have found it. An unrun search is not evidence of absence."
- "Flag load-bearing claims that cite nothing — a citation-accuracy pass is structurally blind to the unsourced claim next to what IS cited."

### 2 — Altitude check (the analysis-specific lens)

Alongside the reviewer findings, check the doc's altitude yourself:

- **Over-specification red flags (flag for removal):** function signatures / class definitions · algorithms or pseudocode · detailed error-handling logic · step-by-step implementation instructions · API request/response schemas · migration scripts · > 2 lines of code in an example. *(For an investigation: a fix proposal that has become a refactor plan or implementation code.)*
- **Under-specification red flags (flag for addition):** vague statements ("update the component" — which? what change?) · missing `file:line` references · no similar-feature / pattern pointers · reusable utilities not identified. *(For an investigation: an `ASSUMED` load-bearing hop in the trace, a root cause without a falsifier, an absence claim without the probe that produced it.)*

### 3 — Consolidate & re-ground

Read every reviewer output in full. **Findings are leads, not verdicts** — before a finding drives an edit: open its cited `file:line` in the **current** source/artifact and confirm it still holds (drop refuted findings); re-grade severity yourself; if it carries a concrete repro ("X raises"), execute it once rather than reasoning to confidence. Open every **SUSPECTED** finding's source before it enters the change list (most won't survive); spot-check VERIFIED ones. Two limits: a live-state claim can't be re-grounded by re-reading the doc — verify against the live system or route to the user; when two reviewers contradict, check whether both are right about **different code paths** first.

Also cross-check the artifact against **itself** — every mitigation/claim in one section against the mechanism described in another; self-contradictions survive source-checking passes because no pass compares sections to each other.

Build ONE list of required changes and size **by kind, not volume**:
- **Skeleton wrong** (structure / approach / root cause fundamentally off) → send the findings back through `/analyze` (or `/bug-investigation`) as input and re-review the result.
- **Corrective delta** (facts, citations, wording — even a large one) → update the doc in place.

### 4 — Confirm & update in place

Confirm the change set with the user. Update **the existing** artifact (never a new file): apply corrections inline, then grep every doc the session touched (including the upstream description/report) for each corrected claim — several phrasings, not just the literal string — and fix echoes. Append (or update) a **`## Review`** section near the top:

- review date · post-review confidence score · recommendation: **Approved** / **Approved with notes** / **Needs revision** / **Rejected** · (if not approved) the specific issues.

### 5 — Gate & hand back

- Confidence < gate, or Needs revision / Rejected → targeted clarifying questions, then repeat from step 1.
- Confidence ≥ gate and Approved / Approved with notes → present the reviewed doc; the artifact is now the source of truth for the next phase (design / plan / fix).

## What this skill does NOT do

- **Create the analysis** — `/analyze` and `/bug-investigation` own that.
- **Risk gates, success metrics, severity routing** — the caller's or user's job.
- **A separate review report** — the `## Review` section in the artifact IS the durable review marker.
