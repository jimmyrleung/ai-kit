# Task 3 - Page shell

## Description

Rebuild the page shell: the top bar, the document list on the left, the outline in its own right column, the
Contents menu for narrow screens, and a footer that takes the "generated" notice and the build report.

- Status: Done
- Complexity: M
- Estimated time: 3–4h
- Depends on: T2
- Can run in parallel with: —

## AI guidance

- `components/COMPONENTS.md` table "Shell" and `components/page.html`: the target markup.
- `design-system/DESIGN.md` section "Layout": columns, widths, narrow screens.
- Global rules: no comments, no commits; keep existing naming in `view.js` (`showDoc`, `markOutline`, …).

## Requirements

- Top bar: spec name and document count, Contents menu, theme switch, Respond button. No badge, no build text.
- Left column `nav.side`: document list, no panel boxes, no file name beside the label; the task-file group
  shows its count in `span.n`.
- Right column `nav.rail`: "On this page", the outline of the open document, "Collapse all" as a `.tool`.
- The link of the open document has `aria-current="page"`; the outline link in view has
  `aria-current="location"`. The class `active` is no longer used for either.
- Contents menu `details.menu`: a second copy of the document list and of the outlines, plus "Collapse all"
  (choice a in `tasks.md`). CSS shows it below 1200px.
- Footer `footer.doc-foot` at the end of `main`: generated notice, build time, document count, git head, and
  the build report as `details`.

## Files involved

| File | Action |
|---|---|
| `skills/render-view/scripts/render_view.py` | Modify `build_page` (page template, `nav_docs`, `report_html`) |
| `skills/render-view/assets/view.js` | Modify `showDoc`, `markOutline`, the `collapse-all` action; add menu closing |
| `skills/render-view/assets/view.css` | Modify only if a shell class has no rule |
| `components/page.html`, `components/components.css` lines 54–77, 384–387 | Read |

## Implementation steps

1. `build_page`: write the top bar as in `page.html` lines 23–38. The Respond button keeps
   `data-action="respond"` and the `data-count` badge.
2. Document links: `<a class="doclink" href="#id" data-doc="id">Label</a>`. Build the list once and place the
   same string in `nav.side` and in `.menu-body`.
3. Place `"".join(outlines)` in `nav.rail` and again in `.menu-body`, each under a `div.nav-title`.
4. Footer text: "Generated from `<spec>/` on <date time> · N documents · vault at <head>. This page is build
   output: edit the markdown, then rebuild." followed by the report `details` (same content as today).
5. `view.js`:
   - `showDoc`: set `aria-current="page"` on every matching `.doclink`; stop toggling `active`. Open only
     the task-file group of the link (`link.closest("li.group details")`). Today's `link.closest("details")`
     returns `details.menu` for a link in the menu copy, so it would open the Contents menu on load and on
     every document change.
   - `markOutline`: set or remove `aria-current="location"` on every `ol.outline a`.
   - `collapse-all`: update the text of every `[data-action="collapse-all"]` button.
   - Close the open `details.menu` on a click on a link inside it, on a click outside it, and on Escape.
6. Remove the classes that no longer exist from the template (`badge`, `build`, `spacer`, `panel`,
   `outline-panel`, `label` in the shell).

## Acceptance Criteria

- At 1440px: three columns; `getComputedStyle(document.querySelector('.layout')).gridTemplateColumns` has
  three tracks; both side columns stay in place while the main column scrolls.
- Clicking a document link shows that document, sets `aria-current="page"` on its link in both lists, and
  shows only that document's outline in both places.
- While scrolling, exactly one visible outline link has `aria-current="location"`.
- In a 1000px iframe: the outline column is hidden, the Contents button is visible, the menu opens, a click
  on an outline link jumps and closes the menu. In a 390px iframe: the document list is in the menu, and
  `document.documentElement.scrollWidth <= clientWidth`.
- In a 390px iframe, a click on a document link in the Contents menu shows that document, and the menu
  stays closed after the hash change. After a reload the menu is closed. A task-file link still opens its
  group.
- "Collapse all" collapses the level-2 sections of the open document and its text becomes "Expand all", in
  the column and in the menu.
- The text "GENERATED VIEW" is not in the page; the footer shows the notice, and the build report opens.
- `render_view.py check specs/render-view-redesign/fixture` still reads the manifest and prints "Fresh".
- No console error; `py_compile` passes.

## Testing

Browser check on the fixture at 1440px, and in 1000px and 390px iframes, in both themes. No automated test
(decision 5). Print is checked in T9.

## Additional relevant files

- `sessions/20261022101915_render-view-rounds-tours/skills/check-view-page.md` — the iframe method for
  narrow widths.
