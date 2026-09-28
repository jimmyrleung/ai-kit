# Long-term memory candidates

These are drafts for owner review. They are not repository rules yet.

## Skill ownership

- An ai-kit skill is a tracked, real directory under `skills/`.
- Symlinks and Windows junctions under `skills/` are local external installations unless the
  repository explicitly adopts their content.
- Catalog, validation, and synchronization logic must ignore linked source directories so a
  local checkout and a clean clone have the same owned skill population.
- `grill-me`, `grill-with-docs`, `improve-codebase-architecture`, and `teach` are distributed by
  Matt Pocock's skills repository. They may be installed locally but are not ai-kit content.
- The owned v3 catalog contains 23 skills. An isolated full sync plans 46 links across the two
  managed roots.

## Junction safety

- Before moving a linked directory, inspect both the apparent source and destination with a
  link-aware API. Do not infer link direction from matching file contents.
- Preserve a recoverable real source before changing junction topology, and verify a known file
  such as `SKILL.md` through the final path before considering the move complete.

## Existing local constraint

- On this workstation, `~/.claude/skills` is itself linked. The current sync engine deliberately
  requires managed roots to be real directories and therefore refuses normal-home operation.
  Treat any change to that policy as separate work.
