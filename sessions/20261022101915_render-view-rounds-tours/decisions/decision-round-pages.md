# Decision-round pages for walkthrough files

**Status:** accepted, 2026-10-22 (shipped in `0be9c62`, adjusted in `c9a634b`)

## Context

Walkthrough rounds reach 40+ items, and several items often rest on the same models (a lifecycle, a timeline). In
chat the agent re-explains those models per item, and a wrong shared premise once spread through three items
before the owner caught it. render-view already turned specs into pages with model-drawn exhibits.

## Decision

- The latest `## Walkthrough — <date> (round N)` section of any doc renders as a decision round: Round 0 premise
  cards, then one collapsible card per item with filters, a failure walk, the suggested option, and a live Respond
  column.
- Premises live in the round's markdown (`### Premises`, `- **P1 — Title.** statement`), confirmed or corrected on a
  nested line. Items come from the round's first ID table; IDs may be spec-style (`D4`) or numbers (`12`).
- Exhibits attach to items (`"item": "D4"`); a `decision` exhibit carries the headline, tags, used premises, options
  and confidence. Hashes leave out the answer, so recording one does not stale a drawing.
- Nothing is pre-selected: untouched cards come back open. "Accept suggested for N shown" selects each shown
  suggestion, and Respond still lists every item on its own line.
- `walkthrough` asks "page or chat?" as the only question before item 1 of a large round; answers return as a
  pasted Respond block that the skill records premises first, then one disposition per answered item.

## Alternatives

- **Default the suggestion, as the canvas mock showed ("not opened; default kept"):** rejected; the walkthrough
  skill never auto-dispositions.
- **Premises only as exhibits:** rejected; confirmations need a place in the source of truth.
- **Premise cards in a grid (the mock):** replaced after the owner's test; the exhibits were too narrow.

## Consequences

- A large round can be answered in one sitting while each decision stays separate in the record.
- The page stores answers only in the reader's browser; the markdown is updated only through the owning skill.
