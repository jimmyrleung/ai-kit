---
name: review-implementation
description: "Reviews implemented code for a work prefix after its repository tasks are complete, or at a named mid-run boundary. Use for a batched code review before qa-gates; accepts prefix and optional scope. Pre-implementation document review belongs to review-artifact, outcome verification to qa-gates, and cc-loop checkpoint review to review-checkpoint."
---

# Review Implementation — batched post-implementation code review

Apply the [confidence contract](references/shared/confidence.md) using the delivery rubric.
Record the effective policy and explicit score, evidence, uncertainty consequences, next
checks and advancement verdict; pass the policy to workers and downstream gates.

You review the code a prefix's tasks produced — once, as a batch — instead of paying for a
reviewer fan-out inside every `implement-task` run. Findings are verified against current
source, dispositioned with the user, and recorded in the prefix's artifact so `qa-gates`
can point at this run instead of re-reviewing.

Apply the [engineering change contract](references/shared/engineering-change.md):
inspect repository context, reuse suitable code/tests, and justify new files within scope.
Resolve bundled references relative to this skill folder.

Follow [authorized work](references/shared/authorized-work.md) for existing permission,
blocking questions, and requested discussion cadence; resolve from this skill folder.

## Inputs the caller must provide (in the invoking message)

| Input | Required | Example | Notes |
|---|---|---|---|
| `prefix` | yes | `auth_oauth_feature` | Source docs at `{prefix}_*.md`. |
| `base` | no (default = derive) | `main` / `<sha>` | Resolve the work boundary per change evidence; merge-base is only a candidate. Use empty-tree base for unborn history; ask if ambiguous. |
| `scope` | no (default `all`) | `tasks 1-4` | Mid-run boundary review for long task lists — names the tasks covered. |
| `artifact_path` | no (default = derive) | `auth_oauth_feature_techspec.md` | Doc to append the `## Review` section to — the same doc `qa-gates` appends `## QA` to. |

## Artifact convention

Append a `## Review — {date}` section to `artifact_path` (in place — no new file; same
convention as `review-artifact` / `qa-gates`). Use the versioned record and inline evidence
markers in the [change evidence contract](references/shared/change-evidence.md). SHA/dirty
status is informational; scoped content and dependency identities bind the verdict. One block
per run; mid-run and final reviews are separate records.

## Procedure

### 1 — Context + diff

Inspect the `{prefix}_*.md` docs (techspec, tasks — for ACs, pinned conventions, budgets).
Resolve the explicit base/task boundary and inspect committed, staged, unstaged, and
untracked content per the change evidence contract. Record exclusions and renames; status
alone is not content inspection. Give every reviewer the same scope and content manifest.

### 2 — Choose independent coverage

For a small isolated change, use one independent review pass covering correctness, repository
fit and simplicity together. Cross-component/service boundaries, auth/payments, migrations,
concurrency, or weak coverage require independent lanes: one traces the highest-risk boundary
end to end; others cover remaining distinct risks. State the scope/risk reason and required
coverage in the record; file count alone does not choose depth. No mandatory three-agent run.

Use native workers when available and authorized. If unavailable, perform separate scoped
passes without shared scratch conclusions and record the weaker independence; do not pretend
these are separate agents. Track each lane's required coverage; another lane's agreement cannot
replace a missing domain. Review focuses, combined or separated according to risk:

- **correctness** — bugs, missed acceptance criteria, broken invariants; **marker/alert
  ownership** — an event name an alert or scheduled query matches must be unique to the
  alert-worthy state (a shared marker could page on healthy work — caught in two runs);
  **mocked-variant reachability** — every mocked result variant a test introduces traces
  to a real production return site (a mocked failure branch proved unreachable: the real
  handler returns true or throws); financial/async ordering (webhook-vs-poller,
  confirm-vs-capture races).
- **conventions** — adherence to the codebase's documented and observed patterns:
  `docs/rules/`, AGENTS.md and loaded instruction-layer conventions, lint/format configs, and the idioms of
  the neighboring code the diff touches.
- **simplicity + repository fit** — unnecessary complexity, duplicated helpers, unjustified
  new test files, and unrelated cleanup, checked against the engineering change contract.
  Accept justified new files and preserve behavioral coverage. Unrelated refactor
  suggestions are opt-in; do not manufacture a mandatory refactor list.

Every reviewer prompt must also carry (blocks 2–3 absorbed from the retired
code-reviewer-agent — its confidence-filtered, actionable-output discipline):

1. "After writing your findings, take exactly ONE more deliberate pass over the parts of the
   diff you have not yet examined (files, hunks, or ACs you skimmed or skipped) before
   concluding — reviewers systematically stop early. One extra pass, then conclude; do not loop."
2. "State severity (Critical/High/Medium/Low) separately from certainty and evidence type
   (SOURCE/OBSERVED/INFERRED). Report supported actionable defects; keep a plausible high-impact
   uncertain issue visible with its next confirming/refuting probe. Do not discard it because
   a blended score is low. Mark pre-existing issues separately rather than attributing them to
   this change; avoid unsupported low-impact nits."
3. "Per finding: file:line, expected versus actual, impact/severity, evidence/uncertainty, and
   a concrete fix or next probe. If no issues remain after coverage checks, say so; do not
   manufacture findings or unrelated refactor suggestions."

Record the complete effective confidence policy, scoped content/dependency manifest and
record ID in each reviewer's brief. Require the delivery rubric calculation for the lane's
assigned scope, evidence and uncertainty consequences with next checks. Do not average
worker scores or let an uncertain severe finding disappear behind the overall score. If an edit
lands mid-review, dispositions require a current-tree probe and a fresh pass — two
reviewers read pre-fix and post-fix states of the same marker and "disagreed".

### 3 — Verify findings (leads, not verdicts)

Before a finding is recorded or presented: re-verify its `file:line` against current source;
a repro-style finding must be **executed**, not reasoned, to be "confirmed"; drop
stale/refuted findings with a one-line note. Distill — every recorded finding carries
`file:line` + a one-line expected-vs-actual; never paste raw build/test/tool output.

### 4 — Disposition with the user

Present consolidated findings by severity, plus requested refactor suggestions. Apply fixes
already authorized within scope; otherwise ask **fix now / fix later / proceed as-is** for
the owner decision. Apply fix-now items (then re-run the repo's
build/test to confirm nothing broke); record fix-later items as named follow-ups.

After applying fix-now items, **recompute the evidence** (test counts, vectors, DI
signatures) from a fresh run before recording — pre-fix evidence goes stale (a 180-test
figure survived its own fix round). When the diff changed operator-visible behavior
(runtime ordering, statuses, alert semantics), sweep sibling runbooks/deploy docs for the
old terms, reconcile runbook SQL identifiers against the schema (6 inconsistencies
survived QA in one run), and reset or date-pin any live PASS rows the change invalidates.

### 5 — Record

Write the `## Review — {date}` block: reviewers run, each finding with its disposition
(`fixed-now` / `follow-up` / `rejected-stale`), requested refactors applied vs deferred,
and the content-bound evidence record, including the confidence contract assessment and
advancement verdict. A below-threshold result or missing load-bearing evidence cannot earn an
approved review; name the blocker and next probe while preserving independent authorized work.
Pass the effective policy to `qa-gates prefix=…` once every
`pre-merge` task is Done. List pending `deploy`/`live` tasks separately with required evidence;
they do not block repository review/QA or become completed operations by implication.

## Observation handoff

Use the [feedback contract](references/shared/feedback.md) to resolve the configured
recorder/store; recording is optional and never requires a private home layout. With no
configured recorder, report `disabled` and continue the main workflow without a feedback write.
If recording is an enabled acceptance gate, unavailable storage or failed validation stays
`unavailable`/`failed`, never PASS.

Return supported observation candidates to the one recorder for this `execution_id`; nested
calls do not write duplicates. A standalone run may be its own recorder. Use the common envelope
and observation schema: `skill_or_workflow: review-implementation`, `phase_area`, the schema's outcome values,
`evidence_kind`, subject/task identity, and actual evidence/locators. Gate verdicts remain in the
verification artifact; they are not silently substituted for observation outcome enum values.
Emit only supported findings, with one approved tag each; no fixed number of entries per run.
The recorder validates and deduplicates by execution plus evidence/subject before any receipt.
Do not treat observation counts as invocation telemetry.

## When NOT to use

- **Per-task review mid-implementation** — deliberately retired from `implement-task`
  (token economics: the fan-out re-loaded the same context once per task to review a small
  diff). If a single task is genuinely risky, review just its diff ad-hoc — don't
  resurrect the per-task fan-out as a habit.
- **Doc review** — that's `review-artifact`.
- **Outcome verification against the spec** — that's `qa-gates`.
- **Headless / cc-loop runs** — that's `review-checkpoint` (coupled to `plan.json`,
  checkpoint ids, and the runner's regex anchors; this skill is its interactive sibling).

## Composition

- **Pipeline:** `implement-task` per task (Workflows 1+3, no embedded review) →
  `review-implementation` → `qa-gates`.
- **`qa-gates` pre-work:** a valid content-bound `## Review` record covering the final repository scope → qa-gates
  records the pointer and skips its own reviewer fan-out; open `follow-up` items surface at
  Gate 5.
- **Long task lists (>~6 tasks):** run once mid-run at a natural boundary (`scope=…`) plus
  once at the end; `qa-gates` references the final block.
