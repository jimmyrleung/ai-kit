---
name: review-artifact
description: Run the standard "review the artifact" sub-phase over a workflow document (investigation / integration analysis / techspec / refactor audit / incident diagnosis). Launches 1-3 reviewer agents, consolidates findings, decides re-run vs update vs minor-edits by % affected, updates the existing artifact in place, gates at a confidence threshold, then hands control back to the caller. Invoked as a sub-phase by the bugfix, feature-addition, refactoring-tech-debt and incident-response orchestrators and their standalone per-phase commands — not run as a top-level command itself.
---

# Review Artifact

A reusable review-the-artifact sub-phase. The calling workflow tells you *what* is being
reviewed and *who* reviews it; you run the standard loop below and return control. You do
NOT own risk gates, success-metric checks, or severity routing — those stay in the caller.

## Inputs the caller must provide (in the invoking message)

| Input | Required | Example | Notes |
|---|---|---|---|
| `artifact_path` | yes | `auth_bug_investigation.md` | The consolidated doc from the previous phase. **Updated in place — never create a new file.** |
| `artifact_label` | yes | `investigation` / `integration analysis` / `techspec` / `audit` / `diagnosis` | Used in prose, skip conditions, and reviewer constraints. |
| `reviewer_agent` | yes | `bug-investigation-reviewer-agent` | Agent to launch for the review. For the feature-dev techspec re-review this is `integration-techspec-creator-agent` told to *review*, not author. |
| `creator_agent` | yes | `bug-investigation-agent` | Agent to re-run if > 30% of the artifact needs changing. |
| `support_docs` | no | `auth_feature.md`, `auth_integration.md` | Extra context files to hand the reviewer agents (e.g. the original request + upstream analysis). |
| `confidence_gate` | no (default `90`) | `90` | Minimum consolidated confidence to advance. |
| `next_step` | yes | `Phase 3 — Impact Analysis` | Where to hand back to. |
| `mode` | no (default `full`) | `full` / `abbreviated` | `abbreviated` = the P1-incident fast path: quick sanity check only, no agents, no separate review doc (still leaves a one-line `## Review` note in the artifact). |

If a required input wasn't supplied, ask the caller (or the user) for it before starting.

## Procedure — mode = full

### Step 0 — Skip check
Read `artifact_path`. Skip the entire review (return immediately; advance to `next_step`)
**only if ALL** of these hold:
- the work item is small / isolated with a straightforward {artifact_label}
- every upstream agent scored ≥ 95% confidence AND the consolidated confidence is ≥ 95%
- all upstream agents agreed on the critical points (root cause / integration points / risks / etc.)
- no blockers (including auto-accept blockers) were flagged

Otherwise continue.

### Step 1 — Launch reviewers
Launch 1-3 `@{reviewer_agent}` agents to review whether `artifact_path` is accurate and
complete. Hand them `support_docs` if provided. Reviewer constraints:
- "Put extra effort on the highest-stakes parts of the {artifact_label} (root cause / proposed solution / risk assessment / integration points — whichever apply)."
- "Establish a confidence score (0-100%) for the {artifact_label}."
- "Identify what is vague, missing, wrong, or misleading. Be specific — cite file:line."

### Step 2 — Consolidate
Read every reviewer output in full. Build ONE list of issues and required changes. Estimate
**how much of the {artifact_label} must change**:
- **> 30%** → re-run 1-3 `@{creator_agent}` agents with the review findings as input, then come back to Step 1.
- **10-30%** → update the document with the review corrections.
- **< 10%** → minor edits only.

### Step 3 — Confirm & update (in place)
Confirm the change set with the user. Then update **the existing** `artifact_path` (do NOT
create a new file):
- apply the corrections inline; and
- append (or update, if already present) a **`## Review`** section near the top of the document recording:
  - the review date
  - the post-review confidence score
  - the recommendation: **Approved** / **Approved with notes** / **Needs revision** / **Rejected**
  - (if "Needs revision" / "Rejected") the specific issues that must be addressed

This `## Review` section is the durable signal that the review happened — downstream phases and
`/status`-style commands look for it instead of a separate `*_reviewed.md` file.

Then:
- post-review confidence < `confidence_gate`, **or** recommendation is "Needs revision" / "Rejected" → ask targeted clarifying questions about the uncertainty, then repeat from Step 1.
- post-review confidence ≥ `confidence_gate` and recommendation is "Approved" / "Approved with notes" → present the reviewed {artifact_label} to the user and ask if it's OK to proceed to `next_step`.

### Step 4 — Hand back
Once the user confirms, `artifact_path` is the source of truth. Return control to the caller,
which proceeds to `next_step` (and runs any workflow-specific post-review gate — e.g. the
refactoring risk gate, success-metric check).

## Procedure — mode = abbreviated  (P1 incident fast path)

Speed beats thoroughness. No agents, no separate review document. Check only:
- the root cause / conclusion is specific, not vague
- the evidence supports it
- there are no obvious internal contradictions

Pass → add a brief **`## Review`** note to `artifact_path` ("Reviewed — abbreviated P1 fast path:
quick sanity check passed, {date}") and advance to `next_step` immediately. Fail → one round of
clarifying questions with the user, fix, add the note, then advance. Do not produce a separate
review document.

## Notes
- This skill **always** updates the artifact in place and leaves a `## Review` section as the
  review marker — there is no separate `*_reviewed.md` file anywhere in the workflows. (If a
  caller ever genuinely needs a standalone review report, that would require adding an explicit
  output-mode input — not currently supported.)
- Risk gates, success metrics, and severity routing are the caller's job, not this skill's.
