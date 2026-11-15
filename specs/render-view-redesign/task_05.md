# Task 5 - Document, tables, code and popover

## Description

Apply the design to the document itself: the head with one metadata line, the note, section tools, tags in
place of chips in tables, code and diff captions, and the timing of the ID popover.

- Status: Done
- Complexity: M
- Estimated time: 3–4h
- Depends on: T4 (the checks read the live Respond text)
- Can run in parallel with: T6 only in theory (same files); do them in sequence

## AI guidance

- `components/COMPONENTS.md` tables "Document" and "Tables and code"; `components/index.html` shows each
  component.
- `design-system/DESIGN.md`: "The No-Capitals Rule" (no label above a heading), "The Mono Rule".
- Global rules: no comments, no commits.

## Requirements

- Document head: no kicker. `p.doc-meta` holds one `span` per item; the file name is first, in
  `span.mono`. The items are today's chips as plain text; "Illustrations N" becomes "N illustrations". The
  tour's `data-reviewed-count` span stays inside its item. On a round, "Walkthrough, round N" and the date
  are two items, as in `components/page.html` line 56 (T7 adds the round's counts).
- Notes at the top of a doc: `aside.note` with the quote's content, without the "Notes at the top" label.
- Section tools: same buttons and `data-action` values. The collapse icon is `svg.icon` (class added in T2);
  it turns by `aria-expanded="false"` (CSS exists).
- Table status cells: `span.tag` with `ok`, `info` or `warn`; the neutral class gives a plain `.tag`.
- A right-aligned column gets `class="num"` on its `th` and `td` in place of the inline style. A
  center-aligned column keeps its inline style.
- Popover: appears 400 ms after the pointer enters an ID link and at once on keyboard focus; stays open
  while the pointer is on the link or on the popover; closes on Escape, on scroll, and about 200 ms after
  the pointer leaves both. The popover sits 6px below the link, so the pointer crosses other elements on its
  way; the delay keeps the popover open across that gap.
- Every class this task's code writes has a rule in `view.css`, or is removed from the markup.

## Files involved

| File | Action |
|---|---|
| `skills/render-view/scripts/render_view.py` | Modify `Renderer.doc_head`, `render_doc` (notes), `table` and `align`, `STATUS_CLASSES` use |
| `skills/render-view/assets/view.js` | Modify the popover block (`showPopover`, `hidePopover`, the `mouseover` and `focusin` listeners) |
| `skills/render-view/assets/view.css` | Modify for classes found without a rule (`.cap`, `.small` if kept) |

## Implementation steps

1. `doc_head`: build the list of items as text and write
   `<header class="doc-head"><h1>…</h1><p class="doc-meta"><span class="mono">file</span><span>…</span></p></header>`.
2. `render_doc`: `notes_html` becomes `<aside class="note">…</aside>`. The note holds the blocks of the
   quotes, not nested `blockquote` elements.
3. `table`: write `<span class="tag ok">`; for the neutral class write `<span class="tag">`.
4. Popover: one timer for the show delay and one for the hide delay. `mouseover` on `a.idref` starts the
   show timer; `mouseover` on `#popover` or on the same link cancels the hide timer; `mouseover` elsewhere
   starts the hide timer. Focus shows at once. Keep `aria-describedby`.
5. Build the fixture and list the classes in the document area that have no rule; add a rule or drop the
   class.

## Acceptance Criteria

- `techspec.md` in the fixture: the head has no element with class `kicker` or `chip`; the first
  `.doc-meta span` is the file name; the items are separated by "·" (from CSS).
- The page has no element with class `doc-notes`, `chip` (outside round cards and exhibits, which T6 and T7
  change) or `label` in the document head and notes.
- Prose paragraphs are `--measure` wide (66ch, 700px in Geist at 16px): at 1440px
  `document.querySelector('.sec-body > p').getBoundingClientRect().width` is between 695 and 705, and a
  table in the same section is wider than the paragraph.
- The Status column shows one tag per status with the colours of `components/index.html`; the number column
  is right-aligned.
- Collapse hides the section body and turns the icon; Comment opens the box, and the comment appears in the
  live Respond text.
- Hovering an ID link for 400 ms shows the popover. A `mouseover` on the paragraph, then within 100 ms one
  on the popover, keeps it open (the path of a real mouse across the gap). Leaving both closes it after the
  hide delay; Escape closes it at once. A fast pass over a link shows nothing.
- Code block, diff block (from the `// before` … `// after` block) and text diagram look like
  `components/index.html` in both themes; a highlighted line has the signal mark.
- No console error; `py_compile` passes.

## Testing

Browser check on the fixture's `techspec.md` in both themes, with page scripts for collapse, comment and
popover (dispatch `mouseover`, wait, read `hidden`). No automated test (decision 5).

## Additional relevant files

- `components/components.css` lines 79–177 — document, table and code rules.
