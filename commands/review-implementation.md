---
description: "Batched code review of a prefix's implementation — runs the review-implementation skill (3-reviewer fan-out: correctness, conventions, simplicity + ship-ready refactors) once per prefix, before /qa-gates."
argument-hint: <prefix>
arguments: prefix
---

# Goal

Review the implementation referenced by `$prefix` — batched, once — before `/qa-gates`.

**Reference files:** `$prefix`

## Process

1. Use the `review-implementation` skill with:
   - `prefix`: `$prefix`
   - `base`: derive (merge-base with the default branch) unless the user supplied one
   - `scope`: `all` unless the user asked for a mid-run boundary review
   - `artifact_path`: derive from prefix (the same doc `/qa-gates` appends `## QA` to)

2. When the skill hands back, the `## Review` block in the prefix's review/QA doc is the
   source of truth. If every task in the prefix's tasks document is Done, suggest
   `/qa-gates prefix=$prefix`. (Suggestion only — the user invokes it.)
