# Keep the prose measure at 66ch, which is 700px in Geist

- Date: 2026-11-15
- Status: accepted by the owner
- Scope: `specs/render-view-redesign/design-system/` (`--measure` in `tokens.css`), the page `render-view`
  generates

## Context

The approved design system sets `--measure: 66ch` and said "about 66 characters per line of prose". The
review of the tasks measured the shipped Geist subset with fonttools: the `ch` unit is the width of "0",
which in Geist is 0.663em. At 16px, `66ch` is 700px, and a line of average text holds about 90–95
characters, not 66. Task 5 expected paragraphs under 620px, so its check would have failed with the approved
CSS.

## Decision

Keep `66ch` (700px). Correct the text instead: `DESIGN.md` states the real width and the owner's choice, and
task 5 checks for a width of 695–705px.

## Why

- The owner approved the page as seen at this width, with the real font.
- The old page ran 140–150 characters per line; 90–95 still fixes the main reading problem.

## Consequences

- `DESIGN.md` ("Key characteristics", "Typography", "Decided points"), `context.md`, `tasks.md` (decision 8),
  `components/index.html` and task 5 now say 700px.
- `research.md` keeps its "about 66 characters" finding: it records the research, not the decision.

## Alternatives not taken

| Alternative | Why not |
|---|---|
| About 30–35rem (66–75 characters) | Changes the approved look; the owner preferred the current width |
