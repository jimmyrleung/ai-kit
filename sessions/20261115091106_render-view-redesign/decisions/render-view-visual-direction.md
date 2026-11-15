# Decision — visual direction of the render-view page

**Date:** 2026-11-15. **Status:** accepted by the owner.

## Context

The generated page looked generic, was tiring to read and had a clumsy layout. Research gave three
directions that all keep sections unboxed and the reading column calm: A "Paper & Ink" (serif text, warm
paper), B "Swiss Ledger" (sans, strong rules, a signal accent), C "Quiet Studio" (sans, space and grey
levels, almost no lines). Each was built as a mockup of the same sample page.

## Decision

Direction C with a small amount of B's signal orange ("C2"):

- One page surface; hierarchy from space, size and three grey levels.
- Geist for text and UI; Geist Mono only for code, IDs and paths.
- One accent, signal orange, for position, change and focus. Status colours only for status, with a word.
- Light and dark themes composed separately, with a System / Light / Dark switch.

## Consequences

- Section panels, the chip row, the "generated" badge and the amber exhibit panels are removed.
- The outline moves to its own right column; one Respond panel takes that column when open.
- Emphasis is a browser-slanted roman, because Geist has no italic.
- The normative values are `specs/render-view-redesign/design-system/tokens.css`.

## Alternatives not chosen

- A: closest to the "editorial" look that AI output clusters around; serif beside dense tables looks mixed.
- B: many rules risk "boxes made of lines"; its left title column needs a wide screen.
