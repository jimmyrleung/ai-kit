---
name: walkthrough-implementation
description: "Explains completed work, step by step, with the code and reasons behind its decisions. Use for “walk me through the implementation,” “explain what we built,” “show me the code,” or a tour before commit/shipping. Start only on request or acceptance of an offer. An existing findings list belongs to walkthrough."
---

# walkthrough-implementation

Goal: guide the user through work just built:

- explain it layer by layer, stating the _why_ behind each decision so the owner's domain knowledge can collide with it — that collision is the review.
- do **not** quiz the owner, run adversarial reviewers, or commit.

> When you don't have artifacts that provide the exact context for a given change, it is okay to list possible reasons why something was done, but you must make it explicit. 

## When to use

- "Walk me through the (entire) implementation", "explain what we built", "show me the code",
  "not file by file, but also not everything at once".
- Offer a tour when owned work is ready for commit but has not been explained; start only
  when the user requests or accepts it. A tour is not an automatic commit prerequisite.

## When NOT to use

- Dispositioning an existing list of open items/findings → `walkthrough` (this skill _produces_
  items by explaining; that one consumes a list).
- Adversarial review → `review-implementation`; spec verification → `qa-gates`.

## Input contract

- The change set: working tree (`git status`, `git diff --stat`) or a named commit range.
- The feature's docs if they exist (techspec/tasks) — changes made mid-walkthrough sync to them.
- A specific branch or commit, with inline context.

## Process

1. **Inspect the change set first.** Enumerate the files, read the ones you will explain. Never
   explain from memory of a diff.
2. **Publish a roadmap before step 1.** N steps (4–7 for a feature-sized change; ~4–6 files per
   step as a guide, not a rule), each a coherent layer, in a small table. The user redirects
   here — before you invest in the wrong order.
3. **Order by dependency, never by file or task number.** (Lived example: token format → auth +
   wiring → read path → write paths → HTTP surface → issuance.) Task order scatters related code.
4. **Each step = code + why + what to notice.** Trim code to the load-bearing lines, cite
   `file:line` for every claim. The _why_ is not optional — it is the review mechanism. Call out
   what was deliberately **not** done, and why.
5. **Honor discussion cadence.** One step per turn for a requested interactive tour; pause at
   each boundary. If the user explicitly requests a batch recap, provide that batch while
   retaining separate steps and unresolved owner decisions.
6. **When a change is requested: apply, verify, sync, record — in the same turn.** Build + tests +
   any repo-specific format/encoding check; update the techspec/tasks docs; record the _rationale_
   in a dated notes entry, not just the change.
7. **When a decision needs the user,** mirror the walkthrough skill's discipline inline — one decision per
   question, options with a recommendation, record the answer verbatim. If a batch of decisions
   accumulates, hand the list to the walkthrough skill proper.
8. **Close with a summary table** of the steps plus an ordered list of open items, blockers first.
   Score confidence per the loaded confidence format, naming what remains unverified.

## Important rules

1. **Verify before declaring a defect.** Trace the _whole_ chain — base types, property
   initializers, model binding — before using the word "blocking". (A `default(enum)` read as a
   confirmed contract defect had a base-type initializer that made it correct; four corroborating
   evidence pieces were all downstream of the unchecked premise.)
2. **Cite `file:line` for every claim** — clickable, and it lets the owner check you.
3. **Scope discipline holds mid-walkthrough.** Honor any user-required scope gate; reuse
   existing approval for the same change. New scope or a pattern outside that authorization
   needs a summarized decision, not an automatic repeated file-count permission request.
4. **Record why something was left alone**, not only what changed — otherwise the next reader
   "fixes" it.
5. **Preserve history.** Superseded decisions get a new dated entry; never rewrite the earlier one.
6. **Distinguish verified from inferred** in every step's claims.
7. **Review opportunity** It is totally acceptable that you suggest fixes/improvements when walking the user through the implementation, and you detect something could be done better or a given implementation could be simplified. 

## What this skill does NOT do

- Disposition an existing findings list → `walkthrough`.
- Adversarial review → `review-implementation`; gates → `qa-gates`.

## Output file

No new artifact. Changes and rationale land in the feature's existing techspec/tasks docs; follow-up
work becomes a proper task in the tasks doc, written cold-start for a fresh session.
