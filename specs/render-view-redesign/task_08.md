# Task 8 - Tour

## Description

Apply the design to the implementation tour: step tools with icons, and the coverage panel without the
repository box and with a segmented filter.

- Status: Done
- Complexity: S
- Estimated time: 1–2h
- Depends on: T7 (its check-icon helper; T5 through T7)
- Can run in parallel with: —

## AI guidance

- `components/COMPONENTS.md` table "Tour"; `components/index.html` shows the step section and the coverage
  panel.
- `skills/render-view/references/tours.md`: what the page adds and what comes back. Neither changes.
- `design-system/DESIGN.md` "Shapes": icons are inline SVG, no character glyphs as icons.
- Global rules: no comments, no commits.

## Requirements

- Step tools: previous and next are `a.tool` with an SVG arrow icon and the existing `aria-label`; the
  "Reviewed" button gets the check icon and keeps `data-action="reviewed"` and `aria-pressed`.
- Coverage panel: the uppercase label becomes one line of plain text; the two filter buttons are a `.seg`
  group, keep `data-cov-filter`, and lose the `btn` class; each repository is a plain block (no border).
- The reviewed count in the document head (from T5) still updates.

## Files involved

| File | Action |
|---|---|
| `skills/render-view/scripts/render_view.py` | Modify `Renderer.heading` (step tools) and `Renderer.coverage` |
| `skills/render-view/assets/view.js` | Read: `toggleReviewed`, `refreshTours`, `filterCoverage` must work unchanged |
| `skills/render-view/assets/view.css` | Modify only if a class has no rule |

## Implementation steps

1. `heading`: replace the "←" and "→" characters with `svg.icon` arrows; add the check icon (the helper from
   T7) to the Reviewed button.
2. `coverage`: write
   `<div class="coverage" data-coverage><p class="muted">Every changed file, from git</p><div class="filters"><div class="seg" role="group" aria-label="Show">…</div></div>…</div>`.
   Keep `.cov-repo`, `.cov-head`, `details.cov-dir`, `table.cov` and the `data-cited` / `data-uncited`
   attributes.

## Acceptance Criteria

- On the fixture tour: S2 has a previous and a next link with icons; S1 has only next; each link jumps to the
  right step.
- "Reviewed" on S1 turns green (`aria-pressed="true"`), dims the step heading, raises the count in the
  document head, and adds "Reviewed: S1 (1 of 3)." to the Respond text. It is still set after a reload.
- "Not in any step" hides the cited rows and the folders with no uncited file; "All files" restores them.
- The coverage panel lists the same files and +/− numbers as the T1 build.
- `getComputedStyle(document.querySelector('.cov-repo')).borderTopWidth` is `0px`.
- Looks like `components/index.html` in both themes. No console error; `py_compile` passes.

## Testing

Browser check on the fixture's tour with page scripts, as above. No automated test (decision 5).

## Additional relevant files

- `components/components.css` lines 364–379 — coverage rules.
