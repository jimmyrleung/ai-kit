# Additional guidance for greenfield work

Follow these instructions when working on greenfield work (new implementation on an empty or non-existing repo or an existing repo but no codebase detected)

## Scope

Make sure the greenfield work is scoped: the spec answers "how do we ship THIS slice", never "how does the whole product work".

Decisions that only matter at slice N+2 are deferred to slice N+2's techspec.

## Design approach

For greenfield work, we should consider both **pragmatic-balance** and **clean-architecture**.

Launch separate subagents to explore the different design approaches when in doubt of which one would be better.
