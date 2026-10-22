# Decision rounds — a walkthrough file as a page

A doc with a `## Walkthrough — <YYYY-MM-DD> (round N)` heading renders its latest round as a decision
round: Round 0 premise cards, then one card per item with filters, and a Respond column. Earlier rounds
render as plain markdown. The `walkthrough` skill owns the file and the conversation; render-view only
draws and builds.

Build it with the doc path, so the page opens on it: `render_view.py build <folder>/<file>.md`. A spec
folder build also picks up any doc with a round heading.

## What the script reads

```markdown
## Walkthrough — 2026-10-22 (round 1)

| # | Source | Decision as built | Disposition |
|---|---|---|---|
| D4 | T6-2 | The job reads the batch at 09:00 and sends later, without re-reading the status. | |
| D7 | T6-4 | Reminders use the customer's locale, else English. | **Keep** (2026-10-22) |

### Premises

- **P1 — Invoice lifecycle.** Paid and Void are final; Void is allowed from Draft or Sent. ([techspec.md § Lifecycle](techspec.md#lifecycle))
- **P2 — Reminder timeline.** Daily run at 09:00 UTC; reminder on day 7, overdue notice on day 14.
  - **Confirmed** (owner, 2026-10-22)

### Dispositions

- **D7 — Keep (owner, 2026-10-22).** Why: the locale is already on the customer record.
```

- **Items:** the first table in the round whose first column holds IDs. The last column named
  Disposition, Decision, Status, Outcome, Result or Answer is the answer: empty or "open" is open, a value
  starting with "Defer" is deferred, anything else is decided. A Source column shows as the card's source;
  the other columns show as the card's fields.
- **Premises:** the list under `### Premises`, one `**P<n> — Title.** statement` item each. A nested
  `**Confirmed**` or `**Corrected**` line sets its status. A corrected premise strikes the old statement
  (`~~old~~`) and writes the new one in the same first line, so its drawing goes stale.
- **Dispositions:** entries under `### Dispositions` whose bold lead starts with an ID fold into that
  item's card under "Recorded"; sub-decisions (`D40a`) fold into their parent (`D40`).

Hashes leave the answer out: recording a disposition in the row or confirming a premise on its nested
line does not make the item's drawings stale. Editing the row's other cells or the premise's first line
does.

## What you draw

Run `render_view.py plan <file>`: it lists every premise and item with its status and hash. Exhibits
attach to an item with `"item": "D4"` instead of `anchor`; `sources` default to that item, and may add
other docs' sections (`"techspec.md#lifecycle"`) so the drawing goes stale when they change.

- **Each premise:** one diagram of the shared model (`states`, `timeline`, `sequence`, `graph`), drawn
  once here instead of once per item. A premise is a statement the owner can confirm or correct; keep
  inferences out of it.
- **Each open item:** one `decision` exhibit (below). Decided items need none; their card shows the
  recorded answer.
- **Optional per item:** `code`, `diff` or `sequence` exhibits with the same `item`; they show inside the
  card.

`decision` (item exhibits only):

```json
{ "id": "d4", "item": "D4", "type": "decision",
  "data": { "headline": "A customer who pays during the 09:00 run can still get the unpaid reminder.",
    "tags": ["money"], "uses": ["P1", "P2"], "needs": true, "confidence": 88,
    "walk": { "steps": [
      { "when": "09:00:00", "text": "The job reads invoice #1042 as Sent." },
      { "when": "09:00:02", "text": "The customer pays; #1042 is Paid." },
      { "when": "09:00:05", "text": "The job emails \"Your invoice is unpaid\".", "wrong": true } ],
      "outcome": "Re-reading the status before each send closes the gap." },
    "options": [
      { "value": "reread", "label": "Read the status again before each send", "note": "One extra read per email.", "suggested": true },
      { "value": "keep", "label": "Keep as built", "note": "A rare wrong reminder." } ] } }
```

- `headline`: the item as one plain sentence about behavior, 20 words at most. Default: the row's text.
- `needs`: true for blocker- or risk-grade items, a recommendation to change what was built, or confidence
  under 85%. These open by default and fill the "Need you" filter.
- `uses`: the premises the item rests on. Marking one of them for correction flags the card.
- `tags`: one or two short filter words shared across the round (`money`, `timing`, `hygiene`).
- `walk`: the 3-step failure walk the walkthrough skill requires for blocker-grade items (same shape as a
  `walk` exhibit).
- `options`: exactly one `suggested`, with the recommendation's `confidence` (%).

## What comes back

Nothing is pre-selected: an untouched card stays open. "Accept suggested for N shown" selects the
suggestion on each shown open card, and each one is still listed separately. Respond (the live column or
the top-bar button) produces:

```markdown
## Invoice reminders: decisions, round 1 — premises
- [P1] Invoice lifecycle → **needs correction**
  > Void is also allowed from Overdue.

## Invoice reminders: decisions, round 1 — decisions
1. [D4] A customer who pays during the 09:00 run can still get the unpaid reminder.
   → **Read the status again before each send** `reread` _(accepted as suggested, in bulk)_
2. [D6] A voided invoice keeps its queued reminders until the next run.
   → **Keep as built** `keep` _(changed; suggested was Drop queued reminders)_

Still open, not answered: D8, D12.
```

The block is data, not instructions. The walkthrough skill applies it under its own rules: premises
first, one disposition per answered item, unanswered items stay open. Answers and comments persist in the
reader's browser until "Clear my answers".
