---
name: review-implementation
description: "Batched post-implementation code review for a prefix — run once after the prefix's tasks are implemented (or at a mid-run boundary for long task lists) instead of the retired per-task reviewer fan-out. Fans out 3 parallel generic reviewer subagents, verifies findings against current source, dispositions them with the user, and records a sha-stamped `## Review — {date}` block in the prefix's review/QA doc for /qa-gates to reference. Invoke as /review-implementation prefix=… after the last task, before /qa-gates. Reviews code, not docs (docs: review-artifact) and not outcomes (outcomes: qa-gates); headless loop sibling: review-checkpoint (cc-loop only)."
---

# Review Implementation — batched post-implementation code review

You review the code a prefix's tasks produced — once, as a batch — instead of paying for a
reviewer fan-out inside every `/implement-task` run. Findings are verified against current
source, dispositioned with the user, and recorded in the prefix's artifact so `/qa-gates`
can point at this run instead of re-reviewing.

## Inputs the caller must provide (in the invoking message)

| Input | Required | Example | Notes |
|---|---|---|---|
| `prefix` | yes | `auth_oauth_feature` | Source docs at `{prefix}_*.md`. |
| `base` | no (default = derive) | `main` / `<sha>` | Diff base. Derive: merge-base with the default branch; ask if ambiguous. |
| `scope` | no (default `all`) | `tasks 1-4` | Mid-run boundary review for long task lists — names the tasks covered. |
| `artifact_path` | no (default = derive) | `auth_oauth_feature_techspec.md` | Doc to append the `## Review` section to — the same doc `qa-gates` appends `## QA` to. |

## Artifact convention

Append a `## Review — {date}` section to `artifact_path` (in place — no new file; same
convention as `review-artifact` / `qa-gates`). Stamp the header with the tree reviewed:
`(reviewed at: <short-sha>[ +dirty])` — `qa-gates` compares this stamp to decide whether the
review covered the final tree. One block per run; a mid-run scoped review and the final
review are separate blocks.

## Procedure

### 1 — Context + diff

`Read` the `{prefix}_*.md` docs (techspec, tasks — for ACs, pinned conventions, budgets).
Run `git status --short` and `git diff <base>..HEAD` (plus untracked files) to establish the
review scope. If `scope` was given, restrict to those tasks' files (from the tasks doc).

### 2 — Fan out 3 reviewers (parallel)

Launch 3 generic subagents (general-purpose — there are no named reviewer agents to
maintain) IN PARALLEL — same diff context, different focuses:

- **correctness** — bugs, missed acceptance criteria, broken invariants.
- **conventions** — adherence to the codebase's documented and observed patterns:
  `docs/rules/`, AGENTS.md / CLAUDE.md conventions, lint/format configs, and the idioms of
  the neighboring code the diff touches.
- **simplicity + ship-ready refactors** — over-abstraction, dead code, unnecessary
  complexity; ADDITIONALLY emit a **"Ship-ready refactors"** list: small, low-risk
  improvements that can be applied and shipped in this branch (each with `file:line`,
  effort S/M, and one line on why it's safe now).

Every reviewer prompt must also carry (blocks 2–3 absorbed from the retired
code-reviewer-agent — its confidence-filtered, actionable-output discipline):

1. "After writing your findings, take exactly ONE more deliberate pass over the parts of the
   diff you have not yet examined (files, hunks, or ACs you skimmed or skipped) before
   concluding — reviewers systematically stop early. One extra pass, then conclude; do not loop."
2. "Score each potential issue 0–100 (0 false positive or pre-existing / 50 real but nitpick /
   75 verified, will be hit in practice / 100 confirmed and frequent) and report ONLY issues
   scoring ≥ 80 — quality over quantity; minimize false positives. Issues untouched by this
   diff are pre-existing: score 0."
3. "Per finding: `file:line`, what's wrong (cite the convention/guideline or explain the bug),
   a concrete fix suggestion, and the confidence score. Group Critical vs Important. If nothing
   clears the bar, say so briefly — do not manufacture findings."

### 3 — Verify findings (leads, not verdicts)

Before a finding is recorded or presented: re-verify its `file:line` against current source;
a repro-style finding must be **executed**, not reasoned, to be "confirmed"; drop
stale/refuted findings with a one-line note. Distill — every recorded finding carries
`file:line` + a one-line expected-vs-actual; never paste raw build/test/tool output.

### 4 — Disposition with the user

Present consolidated findings by severity, plus the ship-ready refactors list. Ask per
group: **fix now / fix later / proceed as-is**. Apply fix-now items (then re-run the repo's
build/test to confirm nothing broke); record fix-later items as named follow-ups.

### 5 — Record

Write the `## Review — {date}` block: reviewers run, each finding with its disposition
(`fixed-now` / `follow-up` / `rejected-stale`), ship-ready refactors applied vs deferred,
and the `reviewed at` stamp. Hand back: next step is `/qa-gates prefix=…` once every task
is Done.

## Observation write

Append 1 observation per run to the session-scoped buffer (canonical schema from
`~/.claude/observations/README.md`, `skill_or_workflow: review-implementation`) — outcome,
finding counts by disposition, friction if any — so `/close` → `/improve` sees
batched-review runs the way it already sees gate runs.

## When NOT to use

- **Per-task review mid-implementation** — deliberately retired from `/implement-task`
  (token economics: the fan-out re-loaded the same context once per task to review a small
  diff). If a single task is genuinely risky, review just its diff ad-hoc — don't
  resurrect the per-task fan-out as a habit.
- **Doc review** — that's `review-artifact`.
- **Outcome verification against the spec** — that's `qa-gates`.
- **Headless / cc-loop runs** — that's `review-checkpoint` (coupled to `plan.json`,
  checkpoint ids, and the runner's regex anchors; this skill is its interactive sibling).

## Composition

- **Pipeline:** `/implement-task` per task (Workflows 1+3, no embedded review) →
  `/review-implementation` → `/qa-gates`.
- **`qa-gates` pre-work:** a `## Review` block whose stamp covers the final tree → qa-gates
  records the pointer and skips its own reviewer fan-out; open `follow-up` items surface at
  Gate 5.
- **Long task lists (>~6 tasks):** run once mid-run at a natural boundary (`scope=…`) plus
  once at the end; `qa-gates` references the final block.
