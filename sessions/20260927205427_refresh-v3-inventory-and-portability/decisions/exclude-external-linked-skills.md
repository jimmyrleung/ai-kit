# Decision: exclude locally linked third-party skills

- **Status:** Accepted in session; pending repository commit
- **Date:** 2026-09-27

## Context

`grill-me`, `grill-with-docs`, `improve-codebase-architecture`, and `teach` were tracked beneath
`skills/` and therefore counted as ai-kit skills. The first three paths were Windows junctions
to `~/.agents/skills/`; `teach` used the inverse layout, with its global installation linked back
to the real repository directory. All four originate from Matt Pocock's skills repository and
were installed for local use, not authored or adopted by ai-kit.

## Decision

- Remove the four skill trees from Git ownership without deleting their global installed copies.
- Keep them as ignored local junctions.
- Make the global `teach` installation its real source and link the local repository path to it,
  matching the direction used by the other three skills.
- Define repository-owned skills as real, tracked directories under `skills/`.
- Make synchronization and portability enumeration ignore symlinks and Windows junctions.
- Correct the live catalog from 27 to 23 skills.

## Rationale

Filesystem presence does not establish repository ownership. Ignoring external links preserves
the user's installed tools while preventing accidental redistribution, misleading attribution,
and count drift between a local checkout and a clean clone.

## Consequences

- Clean clones contain 23 ai-kit skills.
- A checkout may contain additional ignored local skill links without changing documentation,
  validation, or synchronization results.
- `breakout-session` may still hand off to an externally installed `teach`, but ai-kit does not
  bundle or install it.
