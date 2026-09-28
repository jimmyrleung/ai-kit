# Decision: exclude linked third-party skills from ai-kit ownership

- **Status:** Accepted in session; pending repository commit
- **Date:** 2026-09-27

## Context

Four skills authored and distributed through Matt Pocock's skills repository were visible under
ai-kit's `skills/` directory. Git tracked the files reached through those local paths, so the
catalog, documentation, and portability checks incorrectly treated them as ai-kit-owned work.
Clean clones and the local checkout therefore had different conceptual ownership boundaries.

## Decision

- Repository ownership requires a tracked, real directory beneath `skills/`.
- Untrack `grill-me`, `grill-with-docs`, `improve-codebase-architecture`, and `teach` without
  deleting their global installations.
- Keep their repository paths as explicitly ignored local junctions.
- Ignore source symlinks and Windows junctions in both sync and portability enumeration.
- Publish a 23-skill owned catalog and a 46-link full synchronization plan.

## Rationale

Installed third-party tools must not be redistributed or attributed to ai-kit merely because a
developer's checkout links to them. Using tracked real directories as the ownership boundary is
simple, produces the same catalog in clean and customized checkouts, and avoids a hard-coded
third-party allowlist in the sync engine.

## Consequences

- The four external skills remain usable from their global installation.
- Local links do not affect documentation, CI, or sync output.
- `breakout-session` may still use an externally installed `teach`, but ai-kit does not provide
  it.
- The repository's staged index removals must be committed together with `.gitignore`, docs, and
  enumeration changes.
- Supporting a linked managed destination such as `~/.claude/skills` remains separate work.
