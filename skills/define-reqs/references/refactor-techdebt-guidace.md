# Additional guidance for refactor / tech debt work

Follow these instructions when working on a refactor/tech debt (reestructuring, consolidating, eliminating tech-debt, etc. - any work that indicates no new capability)

## Additional mapping

- **Scope definition** — In scope (+ clear boundaries) / Out of scope (+ clear exclusions) / Gray areas (**needs decision**).
- **Preserved contracts** — public APIs, data formats, anything that cannot change.
- **Anti-patterns found** — why problematic, locations, impact — alongside the good patterns to keep.
- **Risk classification** — Breaking changes (High: impact + mitigation) / Non-breaking (Low) / Unknown (needs investigation).
- **Executive-summary extras** — Complexity: Low/Medium/High/Critical · Risk: Low/Medium/High · Scope: Small/Medium/Large.
- Map existing behavior/test protection and rollback constraints; transition design remains with the techspec.

## Architecture & health (integration/refactor)

Identify:

- Architectural patterns in play
- Cross-cutting concerns (auth, logging, caching)
- Pattern consistency (High/Med/Low)
- Documentation quality
- Architectural clarity.
- If weak architecture affects the requested change, name the concrete impact and relevant source;
  do not make unrelated cleanup an automatic prerequisite.
