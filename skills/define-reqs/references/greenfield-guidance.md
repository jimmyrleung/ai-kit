# Additional guidance for greenfield work

Follow these instructions when working on greenfield work (new implementation on an empty or non-existing repo or an existing repo but no codebase detected)

## Additional mapping

- **First vertical slice**: the smallest user-observable behavior to build first. The goal must be user-observable ("user can Y"), never "set up X".
- **Slice requirement (the PRD stand-in)**: create a `## Slice requirement` section including (keep these header names stable — downstream phases may read them by name):
  - **Goal**: the slice goal (user-observable, one sentence)
  - **Done-when**: checkboxes of specific, testable acceptance criteria (including error/empty-state handling)
  - **Building on**: the existing code / prior slices this slice builds on ("nothing — first slice" is a valid answer)
  - **Constraints**: the constraints that bind THIS slice only. Requirement-level, not design: _what_ done looks like, never _how_.
- If the user provides a PRD, the [Slice requirement] section should just link it
- **Deliberately NOT building yet** — deferred capabilities, each with what would earn it a place.
- **Anti-scaffolding guards (reject in the doc):** horizontal layers before a slice demands them (logging pipelines, middleware stacks, CI/CD polish, monitoring, performance/security sections) · "set up X" framed as a goal · success metrics with baselines.
- **Proposed structure** — directories / modules + the conventions to adopt, pointing at ecosystem-standard examples, not class designs.

## Architecture & health (integration/refactor)

Identify:

- Architectural patterns in play
- Cross-cutting concerns (auth, logging, caching)
- Pattern consistency (High/Med/Low)
- Documentation quality
- Architectural clarity.
- If weak architecture affects the requested change, name the concrete impact and relevant source;
  do not make unrelated cleanup an automatic prerequisite.
