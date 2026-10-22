# Implementation tours as a doc plus a generated page

**Status:** accepted, 2026-10-22 (shipped in `0be9c62`)

## Context

`walkthrough-implementation` explains finished work step by step in chat. Real change sets span several
repositories and hundreds of files (the test case: 4 repositories, about 420 files, 61k added lines), mixing
commits, unstaged edits and untracked files. A chat tour cannot show the real diffs or what it skipped.

## Decision

- The tour is a markdown doc in the spec folder, `tour_<YYYY-MM-DD>.md`: a `## Change set` table (prefix, repo,
  base, head), a roadmap, one `## S<n> — <layer>` section per step (why, notice, not done, verified vs inferred,
  `prefix:path:line` citations), and a `## Not toured` section. It is the one exception to the skill's "no new
  artifact" rule.
- render-view reads the repositories from the table. Diffs run from the merge base to the working tree (or a head
  ref), untracked files shown as new; only cited hunks are embedded.
- A coverage panel lists every changed file from git with the steps that cite it and a "Not in any step" filter.
- Steps get previous/next links, Reviewed marks and comments; `check` fingerprints each repository's change set.
- The whole tour is written first and then discussed; the owner sets the pace on the page.

## Alternatives

- **Exhibits only, no markdown:** rejected; nothing would persist for later agents or PR review.
- **One step per turn:** rejected for large change sets; slower, and the page already lets the owner steer.
- **Embedding every diff:** rejected; tens of thousands of lines, and coverage shows what is skipped instead.

## Consequences

- A reviewer sees every changed file and which ones the tour did not explain.
- Tour prose that cites line numbers can drift after code edits; `check` reports the code change, not the stale text.
