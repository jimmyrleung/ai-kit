# Task 4 - Respond panel

## Description

Replace the floating Respond dialog and the decision round's side column with one page-level Respond panel.
The panel shows the live response on every page type, is always open on a decision round at 1200px and
wider, and opens on demand everywhere else.

- Status: Done
- Complexity: M
- Estimated time: 3–4h
- Depends on: T3
- Can run in parallel with: T5, T6 only in theory (same files); do them in sequence
- Bulk-accept "Undo" in the status line is part of T7.

## AI guidance

- `components/COMPONENTS.md` table "Respond" and "Decided points"; `components/page.html` lines 132–151 and
  its script (lines 153–166) show the markup and the open/close behaviour.
- `skills/render-view/references/rounds.md` and `tours.md`, "What comes back": the Respond text format. It
  must not change.
- Global rules: no comments, no commits.

## Requirements

- `aside.respond-panel#respond` is the last child of `.layout`. `body.respond-open` shows it and hides the
  outline column (CSS exists). The Respond button toggles it and carries `aria-expanded`.
- When the open document has a `.round` and the window is 1200px or wider, the panel is open and its close
  button is hidden. Below 1200px the panel is an overlay (CSS exists) that would cover the cards, so on a
  round it works as on other documents: closed at first, opened by the Respond button, with a close button.
  On other documents it keeps the state the reader chose, closed at first.
- When the window crosses 1200px (`matchMedia("(min-width: 1200px)")`), the panel state is set again.
- Panel content: heading and close tool, progress line, actions ("Next unanswered" only on a round, "Copy
  response" as a secondary `.btn`, not `.primary`: Respond is the page's only primary button), status line (`role="status"`), the live text (`pre.live`), "Clear my
  answers" with a `.confirm` block, "Built from".
- The live text is `compose()` and updates on every change, on every page type.
- "Clear my answers" opens the `.confirm` block ("Clear every answer and comment?" with Cancel and Clear).
  The "click again" text and its timer are removed.
- "Built from" lists every document of the view with its short hash, then the repository heads (choice c).
- The round keeps its cards and filters; only the side column goes.

## Files involved

| File | Action |
|---|---|
| `skills/render-view/scripts/render_view.py` | Modify `build_page` (panel markup, remove the dialog); modify `Renderer.round_panel` (drop `.round-main` and the call); delete `Renderer.round_side` after moving its "Built from" rows |
| `skills/render-view/assets/view.js` | Modify `refresh`, `refreshRound`, `showDoc`, `clearAnswers`, `copyText` callers, the click and key handlers; remove `openRespond` and `closeRespond` as they are today |
| `skills/render-view/assets/view.css` | Modify only if a panel class has no rule |

## Implementation steps

1. `build_page`: write the panel as in `page.html`. Keep `data-live` on the `pre`, `data-action` values
   `close-respond`, `next-open`, `copy`, `clear-answers`, and add `confirm-clear` and `cancel-clear`.
2. `round_panel`: return `<div class="round" data-label="…">{head}{premise_html}{items_html}</div>`.
3. `view.js`:
   - One function sets the panel state: toggles `respond-open` on `body`, sets `aria-expanded`, hides the
     close button on a round at 1200px and wider. `showDoc` and the `change` listener of the 1200px
     `matchMedia` call it.
   - `refresh`: write `compose()` into `[data-live]` once, and the progress line. On a round: "A of B
     answered · P premises to confirm" (B = open items of the round). On other documents: the number of
     answers and comments in the response.
   - `copy`: one action that copies the live text; "Copied" goes to `.respond-status` and clears after 1.6 s.
     Remove `copy-live`, the `textarea#respond-text` and the `[data-copied]` elements.
   - `next-open` works from the panel: use the round of the open document.
   - Escape closes the panel only when it was opened on demand.
4. Delete `[data-open-count]` handling (the count is in the progress line now).

## Acceptance Criteria

- At 1440px on `decisions_walkthrough.md`: the panel is open on load, has no close button, and the outline
  column is hidden. On `techspec.md`: the panel is closed; the Respond button opens it and `aria-expanded`
  follows.
- In a 1000px iframe and in a 390px iframe on `decisions_walkthrough.md`: the panel is closed on load and the
  cards are not covered; the Respond button opens it as an overlay with a close button; the close button and
  Escape close it. Widening the iframe from 1000px to 1300px opens the panel and hides the close button.
- Respond text is unchanged: apply the same scripted actions (answer two cards, confirm one premise, mark one
  for correction with a comment, comment on a section, pick an option in the `decisions` exhibit, mark a tour
  step reviewed) on this build and on a build from `git show main:` (see `tasks.md`), with `localStorage`
  cleared before each run. The two texts are equal, except the "built" time.
- Typing in a comment box on `techspec.md` updates the live text while the panel is open.
- "Copy response" puts the live text on the clipboard and shows "Copied" in the status line.
- "Clear my answers" shows the confirm block; Cancel changes nothing; Clear empties answers, comments and
  reviewed steps, and they stay empty after a reload.
- In a 1000px iframe the open panel is an overlay (`position: fixed`) and Escape closes it on `techspec.md`.
- The page has no element with class `round-side`, `round-main` or id `respond-text`. No console error.

## Testing

Browser check on the fixture with page scripts, as above, in both themes. The comparison with the old build
is the regression check for the Respond format. No automated test (decision 5).

## Additional relevant files

- `components/components.css` lines 345–362 — the panel rules.
