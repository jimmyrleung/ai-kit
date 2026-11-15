# Task 9 - Modes, scale and final checks

## Description

Test what the earlier tasks did not: print, reduced motion, forced colours, "more contrast", a large page,
classes without a rule, and the characters the fonts do not have. Fix what fails.

- Status: Done
- Complexity: M
- Estimated time: 2–3h
- Depends on: T7, T8
- Can run in parallel with: —

## AI guidance

- `components/COMPONENTS.md` table "Responsive and other modes": the four rows marked "not tested".
- `context.md` "Constraints": pages reach 1–4 MB with 150–200 sections and 70–360 tables.
- `design-system/DESIGN.md` "Fonts shipped": the subsets have arrows, `−`, `≤ ≥ ≠` and box-drawing
  characters, and do not have `✓` or `✗`.
- Global rules: scratch files go to the session scratch folder, not the repository; ask before `rm`-type
  commands.

## Requirements

- Each mode is tested, or reported plainly as "not tested" with the reason. Do not mark a mode as passed
  from reading the CSS.
- Fixes stay inside the approved design. A problem that needs a design change goes to the owner.

## Files involved

| File | Action |
|---|---|
| `skills/render-view/assets/view.css`, `assets/view.js`, `scripts/render_view.py` | Modify only where a check fails |
| `specs/render-view-redesign/components/COMPONENTS.md` | Modify: the "Checked" column of the modes table |
| Scratch folder | A generated large spec, the old build for comparison, the check scripts |

## Implementation steps

1. **Print.** Use the browser tool's print-media emulation if it has one; otherwise ask the owner to open
   print preview. Check the list in the acceptance criteria.
2. **Reduced motion, forced colours, more contrast.** Same approach: emulate, or ask the owner (Windows
   contrast themes cover forced colours).
3. **Large page.** In the scratch folder, generate one `techspec.md` with 200 sections, 300 tables and 60
   code blocks, and a round with 150 items. Build it with this version and with the version from
   `git show main:` (see `tasks.md`). Compare file size and, in the browser, the load time
   (`performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd`; `view.js` runs before it), and
   the time of one answer on the round.
4. **Classes.** With a short script in the scratch folder: list every class written by `render_view.py` and
   `view.js`, and every class selector in `view.css`. Classes built from variables count as written by their
   prefix: `k-*`, `m-*`, `tone-*`, `st-*`, `lvl*`, `ex-*`, `dg-*`. For each class written without a rule,
   add the rule or drop the class. List each rule whose class is never written and leave it in place: the
   owner decides (some are design variants, such as `.tag.danger`).
5. **Characters.** List every non-ASCII character that `render_view.py` and `view.js` write into the page
   (`↳ ← → ✕ ⇠ − – — · § …` and others). Check each against the two subsets
   (`uv run --with fonttools python` on the `.woff2` files in `design-system/fonts/`). Replace a missing one
   that acts as an icon with an inline SVG; leave missing text characters to the fallback font and list them.
6. **Phone width.** Load each of the three fixture documents in a 390px iframe. On the round, open and
   close the Respond panel.

## Acceptance Criteria

- Print: the top bar, both side columns, the Respond panel, section tools and filters are not printed;
  collapsed sections and closed or filtered cards are printed open; code wraps; the theme is light even when
  the page is set to Dark.
- Reduced motion: `getComputedStyle` of a `.btn` and of a flashed element gives a transition duration of
  `0s`.
- Forced colours: tags, cards, options, code blocks and the note have a visible border; the current outline
  item is underlined.
- More contrast: `--ink-2`, `--ink-3`, `--rule` and `--border-control` take the stronger values of
  `tokens.css`.
- Large page: the file is not more than 10% plus the font size (about 50 KB) larger than the old build; load
  time and the time of one answer are not more than 1.5 times the old build's. Report the four numbers.
- Classes: the script reports no class without a rule, apart from a short list of state classes set only
  by `view.js`, which the report names. Rules without a class are listed for the owner, not removed.
- Characters: the report lists each non-ASCII character as "in the subset", "replaced by an icon" or "falls
  back"; no icon-like character falls back.
- 390px: `scrollWidth <= clientWidth` on all three documents.
- The modes table in `COMPONENTS.md` says "Yes" or "Not tested: <reason>" in every row.
- The fixture builds with no console error; `py_compile` passes; nothing from the scratch folder is in
  `git status`.

## Testing

This task is the test of the modes. No automated test is added (decision 5).

## Additional relevant files

- `components/components.css` lines 389–442 — the media rules, now in `view.css`.
- `sessions/20261115091106_render-view-redesign/LOGS.md` — the "Untested" list this task closes.
