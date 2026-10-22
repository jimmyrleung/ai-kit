# Generated HTML views of specs (Option B, "Assemble")

**Status:** accepted, 2026-10-21

## Context

Specs in this workflow run to 1,000–3,500 lines, and decision walkthroughs to 40+ items. Reviewing them in markdown or chat is the bottleneck. HTML can add progressive disclosure, diagrams, real code and a structured way to answer, but a second source of truth would drift from the markdown that downstream agents read.

## Decision

Build `render-view`: the markdown stays the source of truth; a script turns a spec folder into one local, git-ignored page. The model writes only per-section exhibits as JSON (claims, state machines, graphs, sequences, code excerpts, diffs, walks, decisions). Each exhibit is stamped with the hash of its source sections and, for code, of the code it shows; `plan`, `build` and `check` report stale ones. Answers leave the page as a markdown Respond block that the owning skill writes back.

## Alternatives

- **A, Compile** (script only): free and reproducible, but cannot draw anything the markdown lacks.
- **C, Author** (the model writes the whole page, html-plan style): most expressive, but every build is a full model pass, builds differ, and the page is stale after each recorded batch.

## Consequences

- Rebuilds after a source edit cost no model call; only stale exhibits need redrawing.
- Template-aware touches (header chips, confidence bars, change marks) depend on template wording; template edits can silently degrade them.
- A static page cannot detect staleness itself; `render_view.py check` does.
