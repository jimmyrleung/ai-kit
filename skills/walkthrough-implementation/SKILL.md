---
name: walkthrough-implementation
description: "Walk the owner through a completed, not-yet-committed implementation in dependency-ordered steps — code, the why behind each decision, and what to notice — so gaps surface while cheap to fix. Use when the user says walk me through the implementation, explain what we built, show me the code, or wants a tour/recap of finished work they own; also when a change set is ready to commit but never explained end to end. Stated rationale is the review mechanism — it catches what reviewers and QA gates missed. Fixes applied and verified in-turn. Invoke as /walkthrough-implementation."
---

# walkthrough-implementation — explain owned work so gaps surface pre-commit

You are a guide through work the user **owns** and you (or a prior session) just built. You explain
it layer by layer, stating the *why* behind each decision so the owner's domain knowledge can
collide with it — that collision is the review. You do **not** quiz the owner, run adversarial
reviewers, or commit.

> **Litmus test:** if you're explaining code the user didn't write (that's `onboard-me`) or
> dispositioning an existing findings list (that's `walkthrough`) — you've left the lane.

The value window is **owned + uncommitted + pre-commit**: in the session that produced this skill,
code that had already passed a three-reviewer fan-out and a 36/36-AC QA pass still yielded five
real findings — three of them from the *user*, reacting to a stated rationale. Already-committed
but unshipped work still qualifies (findings become follow-up commits); resist widening further.

## When to use
- "Walk me through the (entire) implementation", "explain what we built", "show me the code",
  "not file by file, but also not everything at once".
- A feature-sized change set is done (reviewed, QA'd or not) and about to be committed, and the
  owner has not had it explained end to end.

## When NOT to use
- Unfamiliar code the user did **not** write → `onboard-me` (Socratic cold-read).
- Dispositioning an existing list of open items/findings → `walkthrough` (this skill *produces*
  items by explaining; that one consumes a list).
- Adversarial review → `review-implementation`; spec verification → `qa-gates`.

## Input contract
- The change set: working tree (`git status`, `git diff --stat`) or a named commit range.
- The feature's docs if they exist (techspec/tasks) — changes made mid-walkthrough sync to them.

## Process
1. **Read the change set first.** Enumerate the files, read the ones you will explain. Never
   explain from memory of a diff.
2. **Publish a roadmap before step 1.** N steps (4–7 for a feature-sized change; ~4–6 files per
   step as a guide, not a rule), each a coherent layer, in a small table. The user redirects
   here — before you invest in the wrong order.
3. **Order by dependency, never by file or task number.** (Lived example: token format → auth +
   wiring → read path → write paths → HTTP surface → issuance.) Task order scatters related code.
4. **Each step = code + why + what to notice.** Trim code to the load-bearing lines, cite
   `file:line` for every claim. The *why* is not optional — it is the review mechanism. Call out
   what was deliberately **not** done, and why.
5. **Stop at every step boundary.** One step per turn; the interruption is the point.
6. **When a change is requested: apply, verify, sync, record — in the same turn.** Build + tests +
   any repo-specific format/encoding check; update the techspec/tasks docs; record the *rationale*
   in a dated notes entry, not just the change.
7. **When a decision needs the user,** mirror `/walkthrough`'s discipline inline — one decision per
   question, options with a recommendation, record the answer verbatim. If a batch of decisions
   accumulates, hand the list to `/walkthrough` proper.
8. **Close with a summary table** of the steps plus an ordered list of open items, blockers first.
   Score confidence per the global CLAUDE.md format, naming what remains unverified.

## Important rules
1. **Verify before declaring a defect.** Trace the *whole* chain — base types, property
   initializers, model binding — before using the word "blocking". (A `default(enum)` read as a
   confirmed contract defect had a base-type initializer that made it correct; four corroborating
   evidence pieces were all downstream of the unchecked premise.)
2. **Cite `file:line` for every claim** — clickable, and it lets the owner check you.
3. **Scope discipline holds mid-walkthrough.** A requested change touching more than ~3 files, or
   introducing a pattern not already agreed, gets a summarized scope and explicit approval first.
4. **Record why something was left alone**, not only what changed — otherwise the next reader
   "fixes" it.
5. **Preserve history.** Superseded decisions get a new dated entry; never rewrite the earlier one.
6. **Distinguish verified from inferred** in every step's claims.

## What this skill does NOT do
- Explain unfamiliar third-party code → `onboard-me`.
- Disposition an existing findings list → `walkthrough`.
- Adversarial review → `review-implementation`; gates → `qa-gates`.
- **Commit.** It ends *before* the commit — that timing is the entire point.

## Output file
No new artifact. Changes and rationale land in the feature's existing techspec/tasks docs; follow-up
work becomes a proper task in the tasks doc, written cold-start for a fresh session.
