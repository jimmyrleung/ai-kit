# The Respond panel is always open on a decision round only at 1200px and wider

- Date: 2026-11-15
- Status: accepted by the owner
- Scope: the page `render-view` generates; `specs/render-view-redesign/` (task 4)

## Context

Earlier the same day the owner decided that the Respond panel is always open on a decision round (the reader
is there to answer) and opens on demand on other pages. On a round its close button is hidden. The approved
stylesheet makes the open panel a fixed overlay below 1200px: `min(360px, 100vw − 32px)` wide, on the right.
The adversarial review of the tasks found that the two rules together cover the cards with no way to close
the panel: about 40% of the main column at 1000px, and 358 of 390px on a phone. No task checked a round below
1200px.

## Decision

At 1200px and wider, the panel on a round is open and has no close button, as decided. Below 1200px it works
as on other pages: closed at first, opened by the Respond button, with a close button, and Escape closes it.
When the window crosses 1200px (`matchMedia`), the panel state is set again.

## Why

- At 1200px and wider the panel takes the outline's column and covers nothing.
- Below 1200px it is an overlay; forcing it open makes the round unreadable.

## Consequences

- Task 4 has new checks at 1000px and 390px on the round, and for a resize across 1200px.
- `DESIGN.md`, `COMPONENTS.md`, `context.md` and `tasks.md` (decision 1) state the width rule.

## Alternatives not taken

| Alternative | Why not |
|---|---|
| Keep it always open at every width | Covers the cards on narrow screens with no close button |
| Put the panel in the page flow below 1200px | A new layout that the approved design does not have |
