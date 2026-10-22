# Standard-library Python over html-plan blocks and diagram libraries

**Status:** accepted, 2026-10-21

## Context

Option B was first described with html-plan's blocks for exhibits and node for its pack step. Both versions were built and compared on the same real spec.

## Decision

Keep one engine in standard-library Python. Draw diagrams as inline SVG from author-supplied grids (state machines, graphs, sequences); read code excerpts and git diffs from the repo; render `// before` / `// after` code blocks as diffs automatically.

## Alternatives

- **html-plan blocks + node pack:** richer interactions out of the box, but its runtime owns the whole page (global CSS, its own contents rail and comment buttons), it is single-doc, it adds node and ~200 KB of third-party code to a public repo with an unresolved MIT vs Apache-2.0 note, and the owner preferred the Python version overall.
- **mingrammer `diagrams`:** draws cloud-architecture icon diagrams, not state machines or sequences, and needs pip plus a Graphviz install.

## Consequences

- One runtime the kit already requires; works the same on Claude Code, Codex and Cursor.
- Diagram quality depends on the grid the model provides; there is no automatic layout.
- The highlighter is lightweight (keywords, strings, comments, types), not language-complete.
