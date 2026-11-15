# Task 7 - Decision round

## Description

Apply the design to the decision round: the round counts in the metadata line, premise and decision cards,
the segmented state filter with topic filters, all cards shown, and bulk accept with "Undo".

- Status: Done
- Complexity: L (kept as one task: the card markup, the filters and the answer logic in `view.js` change
  together and cannot be checked apart)
- Estimated time: 5–6h
- Depends on: T4, T5, T6
- Can run in parallel with: —

## AI guidance

- `components/COMPONENTS.md` tables "Decision round" and "States", and "Decided points";
  `components/page.html` lines 73–110 is the target markup.
- `skills/render-view/references/rounds.md`: what the script reads and "What comes back". Neither changes.
- Memory `render-view-collapsible-cards`: cards are full-width collapsible `details`, never a grid.
- Global rules: no comments, no commits.

## Requirements

**Markup (`render_view.py`)**

- No round head (as in `components/page.html`): the round's heading already names the round. Its counts
  become items of the document's `p.doc-meta`, after the round and date items from T5: "14 items: 3 need
  you, 9 open, 4 decided, 1 deferred" and "2 premises, 1 to confirm". `round_panel` keeps the counts in
  `self.round_stats[doc.id]` (as `coverage` does with `tour_stats`), and `doc_head` writes them.
- Section labels: `.round-label` "Premises" and "Decisions" (sentence case, no "Round 0"); "Expand all" is a
  `.tool`. Keep `section.round-premises` (it carries the id of the `### Premises` heading) and
  `section.round-items`, each around its label row and its cards: the `expand-cards` action finds its cards
  with `button.closest("section")`. `page.html` leaves these sections out; the script must not.
- Filters, in one `.filters` row: a `.seg` group for the state views (All, Need you, Open, Decided, Deferred;
  a view with count 0 is left out, except All; the buttons inside `.seg` have no `btn` class); one
  `.btn[aria-pressed]` per topic tag; the bulk-accept button; `span.status[role="status"]`.
- Card summary: an SVG caret as first child, `.cid`, `.c-headline`, `.c-state`. In `.c-state`: at most two
  `.tag.topic`; an open item that needs the owner shows `.tag.warn` "Needs you"; another open item shows a
  plain `.tag` "Open"; a decided or deferred item shows `.c-answer` (check icon and the answer text). The
  reader's answer shows as `.c-answer.yours` ("Your answer: …", or "Bulk: …"). "Suggested: …" leaves the
  summary.
- Card body: one `dl.c-fields` (Source, the row's fields, then "Uses" with the premise links and the
  "Rests on a premise marked for correction" `.tag.warn`); the failure walk as `ol.walk` with
  `aria-label="Failure walk"`; other exhibits; `.c-recorded` with `.c-label` "Recorded"; `fieldset.rdecision`
  with `.suggested` and `.hint`; `.c-foot` with the confidence and "model-drawn · stamp" text and the Comment
  tool; the comment slot.
- Premise card: same recipe. State: `.tag` "Not confirmed", `.c-answer` "Confirmed", `.tag.warn`
  "Corrected"; the reader's mark as `.c-answer.yours`.
- All `data-*` attributes that `view.js` and the Respond text read stay as they are (`data-ckey`,
  `data-item`, `data-status`, `data-needs`, `data-tags`, `data-uses`, `data-ctitle`, `data-recorded`,
  `data-label`, `data-suggested`, `data-filter`, `data-premise-flag`, `data-bulk-count`, `data-value`, and
  the `data-action` values `premise`, `bulk-accept`, `expand-cards`, `comment`). `page.html` has none of
  them; add them to its markup.
- A card with a comment keeps a mark: its Comment tool uses the signal colour, as a section's does
  (`.card.has-comment .c-foot [data-action="comment"]`; today `view.css` line 363).

**Behaviour (`view.js`)**

- All matching cards are shown. `CARD_LIMIT`, `data-expanded`, the `show-more` action and its button go.
- Filters combine: one state view AND at most one topic (choice b). Pressing the active topic again clears it.
- The status line reads "Showing N of M".
- Bulk accept applies at once to the shown open cards with a suggestion. The Respond status line then shows
  "Accepted N suggestions." with an "Undo" button. Undo makes those cards unanswered again (bulk accept only
  changes unanswered cards). The offer goes away at the next answer, at "Copy response", at "Clear my
  answers", and on reload.
- Nothing is preselected on a round card.

## Files involved

| File | Action |
|---|---|
| `skills/render-view/scripts/render_view.py` | Modify `Renderer.round_panel`, `premise_card`, `item_card`, `doc_head` (round counts) |
| `skills/render-view/assets/view.js` | Modify `reveal`, `matches`, `applyFilter`, `bulkTargets`, `bulkAccept`, `refreshRound`, the click handler; remove `CARD_LIMIT` |
| `skills/render-view/assets/view.css` | Modify for classes without a rule; remove nothing that T9 has not checked |

## Implementation steps

1. `item_card` and `premise_card`: rewrite the summary and the body to the markup of `page.html` lines
   92–104. Use one small helper on `Renderer` for the caret and one for the check icon, since both cards and
   T8 use them.
2. `round_panel`: no head line; store the counts in `self.round_stats`; labels inside the two kept
   sections; the `.filters` row. State buttons keep `data-filter`; topic buttons use `data-topic`. In
   `doc_head`, write the counts as two items.
3. `view.js` filters: `round.dataset.filter` (state) and `round.dataset.topic`; `matches` tests both;
   `applyFilter` sets `aria-pressed` on both groups and writes the status line.
4. `reveal`: when the target card is hidden, reset both filters to show it. Drop the `expanded` flag.
5. `refreshRound`: fill `.c-answer.yours` in place of the two hidden chips (`data-answer-chip`,
   `data-premise-chip` stay as hooks on the new elements).
6. Bulk undo: `bulkAccept` keeps the keys of the cards it answered in one variable; the `undo-bulk` action
   deletes their `state.answers` and `state.bulk` entries, unchecks their radios, and refreshes. The
   `change` handler, `copy` and `clearAnswers` drop the variable.
7. Check print: `.card[hidden]` still prints (rule exists).

## Acceptance Criteria

- The fixture round shows all 14 cards with "Showing 14 of 14"; the page has no "Show more" button and
  `view.js` has no `CARD_LIMIT`.
- "Need you" shows only the cards with `data-needs="1"`; adding a topic narrows the list and the status line
  follows; pressing the topic again restores the state view.
- An ID link to a card hidden by a filter resets the filters, opens the card and flashes it.
- Answering a card shows "Your answer: <label>" with the check icon in its summary and counts in the Respond
  progress line. Marking a premise "Needs correction" opens its comment box and flags the cards that use it.
- Bulk accept on a view with 3 targets answers 3 cards and shows "Accepted 3 suggestions. Undo". Undo
  returns the 3 cards to unanswered, and a card answered by hand before the bulk accept keeps its answer.
  After answering one more card, or after "Copy response", the Undo button is gone.
- Answers, premise marks and comments are still there after a reload.
- Respond text is unchanged: the scripted actions of T4 give the same text on this build and on a build from
  `git show main:`, with `localStorage` cleared before each run, except the "built" time.
- `#…__premises` links still jump to the premises; "Expand all" above the decisions opens only decision
  cards.
- The round document's `p.doc-meta` shows the round, the date, the item counts and the premise counts as
  separate items.
- The open card looks like `page.html` in both themes: sunken background, code block on the page colour, one
  level of surface inside the card. In a 390px iframe the summary wraps and there is no horizontal scroll.
- The page has no element with class `chip`, `c-suggest`, `c-field`, `c-meta`, `bulk-row`, `linkish` or
  `round-head`. No console error; `py_compile` passes.

## Testing

Browser check on the fixture's `decisions_walkthrough.md` with page scripts, as above; the comparison with
the old build is the regression check for the Respond format. No automated test (decision 5).

## Additional relevant files

- `components/components.css` lines 292–343 — round and card rules.
- `sessions/20261022101915_render-view-rounds-tours/skills/check-view-page.md` — the round checks to script.
