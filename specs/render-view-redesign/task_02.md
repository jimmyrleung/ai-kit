# Task 2 - Stylesheet, fonts and theme

## Description

Replace the skill's stylesheet with the approved tokens and components, embed the two font subsets in the
page, and add the three-state theme switch. The page markup does not change yet, apart from `<head>`, the
switch and the class of the collapse icon.

- Status: Done
- Complexity: M
- Estimated time: 2–3h
- Depends on: T1
- Can run in parallel with: —

## AI guidance

- `design-system/DESIGN.md` sections "Colors" and "Typography": the tokens are normative.
- `AGENTS.md` (public repo): a font file must travel with its licence text.
- Global rules: no comments, no commits, ask before `rm`-type commands.

## Requirements

- One self-contained HTML file, no network request (context.md, "Constraints").
- `assets/view.css` = `design-system/tokens.css` followed by `components/components.css`, with no other
  change. Later tasks edit `view.css` when a class needs a rule.
- Fonts are read at build time from `assets/fonts.css` and inlined before the stylesheet.
- The theme is applied before the styles load, so the page does not flash the wrong theme.

## Files involved

| File | Action |
|---|---|
| `skills/render-view/assets/view.css` | Replace the content |
| `skills/render-view/assets/fonts.css` | Create: copy of `specs/render-view-redesign/design-system/fonts/fonts.css` |
| `skills/render-view/assets/OFL-Geist.txt`, `OFL-GeistMono.txt` | Create: copies from `design-system/fonts/` |
| `skills/render-view/scripts/render_view.py` | Modify `build_page` (the `<head>` and the top bar) and `Renderer.heading` (one class) |
| `skills/render-view/assets/view.js` | Modify: theme switch |
| `specs/render-view-redesign/design-system/tokens.css`, `components/components.css` | Read |

## Implementation steps

1. Copy the three font files into `assets/`. Write `view.css` from the two source stylesheets.
2. In `build_page`, change `<head>`: add `<meta name="color-scheme" content="light dark">`; add the theme
   script before the styles; inline `read_asset("fonts.css")` and then `read_asset("view.css")`.

   ```html
   <script>try{var t=localStorage.getItem('rv-theme');if(t==='light'||t==='dark')document.documentElement.dataset.theme=t}catch(e){}</script>
   ```

3. Add `fieldset.theme` to the top bar, before the Respond button, with the three radios (`system`, `light`,
   `dark`) as in `components/page.html` lines 32–36.
4. In `view.js`, set the checked radio from `document.documentElement.dataset.theme` and handle `change`:
   set or delete `data-theme`, store or remove `rv-theme` (inside `try`, as the existing storage code does).
5. In `Renderer.heading`, add `class="icon"` to the collapse `svg`. The new stylesheet sizes only
   `svg.icon`; without the class each section heading shows a 300×150 shape until T5.
6. Remove nothing else. The old top bar, sidebar and Respond dialog stay until T3 and T4.

## Acceptance Criteria

- The fixture builds; `py_compile` passes; the console has no error.
- `(await document.fonts.load('16px Geist')).length` and `(await document.fonts.load('13px "Geist Mono"')).length`
  are both above 0, and `getComputedStyle(document.body).fontFamily` starts with `Geist`. (Do not use
  `document.fonts.check()`: it also returns `true` when no font face matches.)
- The section headings show a 16px collapse icon.
- The Network panel (or `performance.getEntriesByType('resource')`) shows no request other than the page.
- `grep -o "url([^d][^)]*" skills/render-view/assets/*.css` returns nothing (only `data:` URLs).
- Choosing Dark sets `data-theme="dark"` and `getComputedStyle(document.body).backgroundColor` to
  `rgb(14, 15, 17)`; after a reload the page is still dark and the Dark radio is checked. System removes the
  attribute and the stored key.
- The page file grows by about 50 KB compared with the T1 build (fonts), not more than 80 KB.
- From the repository root,
  `diff <(cat specs/render-view-redesign/design-system/tokens.css specs/render-view-redesign/components/components.css) skills/render-view/assets/view.css`
  is empty.

## Testing

Browser check on the fixture, as listed above, in both themes. No automated test (decision 5).

## Additional relevant files

- `specs/render-view-redesign/design-system/index.html` — the specimen page, to compare type and colour.
