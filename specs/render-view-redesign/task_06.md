# Task 6 - Exhibits and diagrams

## Description

Apply the design to illustrations: a plain figure with a numbered caption below, the new failure walk and
option markup, and diagram label sizes that match the 14px text.

- Status: Done
- Complexity: M
- Estimated time: 3–4h
- Depends on: T4 (the checks read the live Respond text)
- Can run in parallel with: T5 only in theory (same files); do them in sequence

## AI guidance

- `components/COMPONENTS.md` table "Illustrations (exhibits)"; `components/index.html` shows each type.
- `skills/render-view/references/exhibits.md`: the exhibit JSON contract. It must not change.
- `design-system/DESIGN.md` "Components → Figures": neutral strokes, signal only for "changed".
- Global rules: no comments, no commits.

## Requirements

- Frame: `figure.exhibit` holds the optional `.ex-title`, the body, then `figcaption.ex-caption`. The
  "Illustration" tag row (`.ex-head`) is removed.
- Caption: `<b>Figure N.</b>` and the caption text, then `span.ex-meta` with "model-drawn · from <source> ·
  <stamp>". A caption is always written, also when the exhibit has no `caption`. A stale exhibit shows
  `span.tag.warn` "Stale: …" at the start of the caption.
- N counts the exhibits of one document in page order and starts at 1 in each document. The failure walk
  inside a decision card is not a figure and has no number.
- Failure walk: the `.when` label holds only the time; the wrong step's text starts with
  `<b>Wrong outcome.</b>`.
- `decisions` exhibit: "suggested" is `span.suggested` with the word "Suggested"; the option note is
  `span.hint`. The suggested option stays preselected (choice d in `tasks.md`).
- Diagrams: the same SVG structure. Width estimates use the new sizes: node and actor labels 14px, message
  text 13px, edge labels 12px, notes 12.5px.
- A sequence message with `mark: "new"` shows its text with a leading "+ ", so the mark does not rest on
  colour.

## Files involved

| File | Action |
|---|---|
| `skills/render-view/scripts/render_view.py` | Modify `Renderer.exhibit`, `exhibit_walk`, `exhibit_decisions`, `exhibit_graph`, `exhibit_sequence`, `exhibit_states`, and `render_doc` (reset the figure counter); check `text_width`, `label_box`, `label_right` |
| `skills/render-view/assets/view.css` | Modify for classes without a rule (`.decisions`, `.exit-arrow`) |
| `skills/render-view/assets/view.js` | Read only: `lightEdges` and the `fieldset.decision` handling must still work |

## Implementation steps

1. Add a figure counter to `Renderer`, set to 0 at the start of `render_doc`, raised in `exhibit`. In
   `render_doc`, render the `top` exhibits before the block loop. Today they are rendered after it but placed
   first in the article, so they would get the last numbers.
2. Rewrite the return value of `exhibit` to the new frame. Keep `data-exhibit`, the `ex-<type>` class and
   `is-stale`.
3. `exhibit_walk`: remove " · wrong outcome" from `.when`; prefix the text of a wrong step.
4. `exhibit_decisions`: change the two spans. Do not change `name`, `value`, `data-label`,
   `data-suggested`, `data-decision`, `data-item`, `data-question` or `checked`.
5. Diagrams: in `exhibit_graph` and `exhibit_sequence` replace the `13.5` size arguments with `14`; message
   text is measured at 13 where a width depends on it. Prefix "+ " for a new message in the SVG text.
6. Build the fixture and look at every diagram: no label leaves its node, no edge label overlaps a node.
   Adjust the padding constants only where a label overflows.

## Acceptance Criteria

- Every `figure.exhibit` in the fixture has a `figcaption` as its last child that starts with "Figure N.",
  and the numbers run 1, 2, 3… in page order inside each document; the `claims` exhibit at `top` of
  `techspec.md` is "Figure 1.".
- The page has no element with class `ex-head`, and no text "Illustration" as a tag.
- For each diagram, every `text` element's `getBBox()` lies inside its node's `rect` (check with a page
  script over `.dg .node` and `.dg .actor`).
- The wrong step of the `walk` exhibit starts with bold "Wrong outcome."; its `.when` is the time only.
- The new sequence message reads "+ re-read status" (or the fixture's text) and is still green.
- Hovering a graph node turns its outgoing edges to the signal colour.
- Choosing an option in the `decisions` exhibit changes the Respond text from "not touched; default kept" to
  "kept as suggested" or "changed", as before.
- Build an exhibit with a changed source (edit a fixture section, rebuild without the `cp` step, see
  `tasks.md`): the figure shows the "Stale" tag in its caption. Restore the section and rebuild.
- All exhibit types look like `components/index.html` in both themes. No console error; `py_compile` passes.

## Testing

Browser check on the fixture in both themes, with the page script for label boxes. No automated test
(decision 5). Glyph coverage of the fonts (`↳`, `✕`, arrows) is checked in T9.

## Additional relevant files

- `components/components.css` lines 179–290 — exhibit and diagram rules.
