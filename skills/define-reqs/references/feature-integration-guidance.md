# Additional guidance for feature integration

Follow these instructions when working on feature integration (i.e. when implementing a new feature or updating an existing feature in an existing codebase)

## Trace flows

Call chains entry → output, data flow, transformations at each step, dependencies and integrations, state changes and side effects.

## Architecture & health (integration/refactor)

Identify:

- Architectural patterns in play
- Cross-cutting concerns (auth, logging, caching)
- Pattern consistency (High/Med/Low)
- Documentation quality
- Architectural clarity.
- If weak architecture affects the requested change, name the concrete impact and relevant source;
  do not make unrelated cleanup an automatic prerequisite.
