# Research — render-view page redesign

Step 2 of the `ui-process`. Done 2026-11-15 by five research agents (Opus 5.5); their full reports, with
every source link, are the `collect_*.md` files beside this one. This file is the consolidation: what
the research says, where the reports disagree, and what is still to decide. Context: [context.md](context.md).

| Report | Questions | Confidence |
|---|---|---|
| [collect_reading-and-fonts.md](collect_reading-and-fonts.md) | Reading typography, open-license fonts | 87% |
| [collect_document-layouts.md](collect_document-layouts.md) | Document shells, editorial inspiration | 82% |
| [collect_code-diff-diagrams.md](collect_code-diff-diagrams.md) | Code, diffs, SVG diagrams | 85% |
| [collect_cards-forms-themes.md](collect_cards-forms-themes.md) | Cards, forms, filters, theme tokens | 88% |
| [collect_anti-slop-reference.md](collect_anti-slop-reference.md) | `taste-skill` compared with `impeccable` | 90% |

Statements marked *(inference)* are a report's own proposal, not a sourced rule.

## 1. Reading typography

| Property | Value | Basis |
|---|---|---|
| Measure | About 66 characters, never above 75 | Butterick 45–90; GOV.UK ≤ 75; WCAG 1.4.8 ≤ 80 |
| Body size | 16–17px (17px for a serif with a small x-height) | Butterick 15–25px; Material 16px; GOV.UK 19px |
| Line height | 1.5 | WCAG 1.4.8 needs ≥ 1.5; Butterick allows up to 1.45 |
| Paragraphs | Space between them (50–100% of body size), no indent | Butterick |
| Headings | At most 3 visible levels; small size steps; weight and space carry the hierarchy; no capitals | Butterick |
| Scale | Fixed, ratio about 1.125–1.2; about 32 / 24 / 20px, H4 at body size in semibold | impeccable; GOV.UK and Material scales |
| UI text | 14px, line height about 1.4; nothing read below 12px; no Light weight | Material, Apple |
| Contrast | Body ≥ 7:1, secondary ≥ 4.5:1, controls and focus ≥ 3:1 | WCAG 2.2 AA/AAA |
| Serif or sans | No reading-speed evidence for either on current screens; the choice is one of character | NN/g, Wallace et al. 2022 |
| CSS features | `text-wrap: balance` on headings (Baseline); `pretty` on body (ignored safely by Firefox); `tabular-nums` in tables; hyphenation off, because it breaks IDs | MDN data |

Today's lines are 140–150 characters, about twice the maximum of every source. Line length is the
largest single fix.

## 2. Fonts

Measured with fontTools from the foundries' files. Sizes are custom subsets, before base64 (+33%).

- **The Google `latin` subset has no → ← ↳ ✓ ≤ ≥ or box-drawing characters.** The page uses all of
  them, so the build needs its own subset per font.
- **Licence.** All candidates are SIL OFL. The OFL FAQ allows embedding in a document; for webfonts,
  subsetting counts as a modification, which a Reserved Font Name forbids. A base64 font in a shared
  HTML file sits between the two cases. Safe choice: fonts without a Reserved Font Name, or rename the
  family in the subset.
- **Optical size axis.** Keeping it costs about 3× the size (Source Serif 4: 36 → 121 KB). Pin it.

| Pairing | Text | UI | Mono | Size → base64 | Notes |
|---|---|---|---|---|---|
| A | Source Serif 4, roman + italic | Inter | JetBrains Mono | 133 → ~177 KB | Classic editorial serif; no Reserved Font Name in the Google builds; inline code at 0.86em |
| B | Literata, roman + italic | system UI font (or Geist, +19 KB) | Commit Mono (italic included) | 100 → ~133 KB | Serif made for long screen reading; smallest; Commit Mono's last release is Dec 2023 |
| C | IBM Plex Serif | IBM Plex Sans | IBM Plex Mono | ~125 → ~167 KB | One family, matching x-heights, hinted for Windows; Reserved Font Name "Plex" needs a rename |

All three are well under the 300 KB target. Not tested: how each looks on Windows at 13–16px. This must
be checked on screen in step 4.

## 3. Shell and layout

Patterns that repeat across 20 document sites (Stripe, Linear, Vercel, Tailwind, Starlight, MDN, GitHub
Docs, Furo, Apple and others):

1. **One page surface, no section panels.** Sections are separated by space and heading size, at most a
   hairline. Boxes stay only for code and figures.
2. **A measured prose column** of 40–48rem. Wide content (tables, code, diffs, diagrams) gets a wider
   track of its own and scrolls inside its block.
3. **Left = documents, right = "On this page".** The right outline is the first thing to hide on narrow
   screens; it becomes a dropdown or a drawer.
4. **The active item is quiet:** a 2px bar, a tint, or brighter text.
5. **Long labels wrap**; they are not cut.
6. **Page metadata is one line of plain text** (or a small two-column list), not a chip row.
7. **Notes are a left rule with a faint tint or no fill**, not a filled box.
8. **Tables: bold header, horizontal hairlines, no zebra, no outer box.**
9. **A "generated" notice is quiet text** in the footer or the metadata line (Go, Kubernetes), not a badge.
10. **Body sections are not collapsed** on any of these sites. Collapse is a reader tool (GitHub's
    "Viewed"), expanded by default.

No site adds a third content column for an action panel. They use a popover, a drawer that replaces a
column, or a bar at the bottom.

## 4. Code and diffs

- **Light code on a light page** is the norm for document sites (GitHub, MDN, Vercel Geist): a faint
  tint or a hairline frame. Dark blocks appear where code is the product to copy (Stripe requests,
  Tailwind).
- **Syntax colours:** GitHub's current values (Primer Primitives v11.10.0) cover the tokenizer's six
  classes and pass 4.5:1 in both themes. The older Shiki GitHub theme fails for comments in light theme.
- **Diff colours:** Primer's `diffBlob` tokens for both themes. Meaning must not rest on colour: keep the
  `+`/`−` column, the two number gutters and a tinted gutter cell. Primer's colour-blind themes swap
  green/red for blue/orange.
- **Frame:** code at about 0.85em, line height 1.5–1.6, long lines scroll, wrap for print. File path in a
  quiet header strip. Highlighted lines get a neutral tint and a 2–3px bar.
- **Pins** (notes on a line) are set in the body sans font, with a tone word ("Risk:") in text, so they do
  not read as code.
- **Inline code:** a faint chip at about 85% of the body size; no size change inside headings.

The report gives GitHub's cool greys (`#f6f8fa`). On a warm page they need to be re-derived from the
page's own tokens, keeping the contrast ratios *(my note)*.

## 5. Diagrams

- Diagrams sit on the page as a `figure` with a caption below, not in a tinted panel (Tufte: remove ink
  that carries no information).
- Neutral first: node border 1px, edge 1.25px, emphasised edge 2px *(inference; tool defaults are 1–2px)*.
  Lines that carry meaning need 3:1 contrast (WCAG 1.4.11).
- A pale fill alone cannot show state (`#dafbe1` on white is 1.11:1). New / changed / shared / removed
  need a stroke, dash or word as well as colour, and a legend that repeats the same mark and word (C4).
- Labels: node 14px, sub-label and edge label 12px *(inference from Mermaid, D2 and Graphviz defaults)*.
- Colours come from CSS classes and variables, so diagrams follow the theme.
- Hover and keyboard focus share one highlight; nodes are focusable and labelled.

## 6. Cards, options, filters

- **Summary row:** the whole row is the target (NN/g, GOV.UK), at least 44px tall. A caret is the only
  icon that tests better than no icon. Keep the summary short.
- **Fewer chips.** GOV.UK: each extra status makes the set harder to remember. Its task list shows
  "Completed" as plain text and only the items that need action as a coloured tag. Applied here: "Needs
  you" is the one tinted tag; an answered card shows plain "✓ Answer: X" *(inference)*.
- **Tags:** sentence case, pale background with dark text, never a button, always a word (GOV.UK,
  Atlassian, Carbon). Four tones plus neutral.
- **Several cards open at once** (NN/g: readers compare), with Expand all / Collapse all.
- **Card look:** rows separated by dividers when closed; the open body gets a raised surface or a rule
  *(inference)*. This keeps the owner's rule: full-width collapsible cards, never grids.
- **Options:** vertical, whole label clickable, nothing preselected (GOV.UK; matches the current rule),
  one-sentence hints. "Suggested" is a plain word, shown once.
- **Filters:** the state views (All / Need you / Open / Decided / Deferred) are exclusive, so a segmented
  control; tag filters are toggle buttons. Counts stay in the labels.
- **Find-in-page now opens closed `<details>`** in all engines. `interpolate-size` is not Baseline, so no
  height animation is needed.
- **ID popovers:** show after 0.3–0.5 s, stay open while hovered, close with Escape (WCAG 1.4.13).

## 7. Themes

- **Tokens:** raw values plus semantic roles (Primer's model): page, raised and sunken surfaces; three
  text levels; subtle and control borders; accent; success / warning / danger / info as text + background
  + border; focus, selection, flash.
- **`light-dark()`** has been Baseline since May 2024. Each token is written once; the toggle changes only
  `color-scheme`; print forces light in one line. This replaces today's duplicated token blocks.
- **Toggle:** three states (System / Light / Dark), stored in `localStorage`, applied by a small script in
  `<head>` before the styles, so the page does not flash.
- **Dark theme:** dark grey, not black; raised surfaces are lighter; text is not pure white; accents and
  status colours are less saturated; borders and tone steps replace shadows.
- **OKLCH** is widely supported and gives even lightness steps; keep chroma low to stay inside sRGB.
- **Minimum extra support:** `forced-colors` (transparent borders on chips and cards, outline for focus)
  and `prefers-contrast: more` (stronger secondary text and borders).
- Not tested: whether `localStorage` keeps the theme when the page is opened from disk (`file://`).

## 8. Reference skill for steps 4 and 5

**Use `impeccable`, as reading material only.**

- `taste-skill` on `main` (rebuilt 2026-11-05) is now a kit for company marketing sites: one section per
  screen, required motion, Google Fonts, photos, no accordions, nothing on tables, code or print. The
  "dials" exist only in the older `taste-skill-classics` repo.
- `impeccable` has an explicit **Read mode** for documents, is stack-neutral, and gives a ready
  design-system document format (`document.md`).
- Do not run its engine, hooks, live mode or network catalog. Both skills tell an agent to run binaries
  or hooks; none of that is needed here.
- Borrow one idea from `taste-skill`: the "one strict system per page" check (one button shape, one
  radius family, one card recipe, one hairline, one link look; two boxes deep at most).

`impeccable` warns that this exact direction is a look AI output clusters around: "broadsheet-editorial
hairlines, italic display serif, and small tracked mono labels", and a cream ground. To stay out of it:
roman headings, no tracked-capitals labels, no kicker above headings, a paper tone that is not cream, and
one quiet signature (the ID and numbering system) instead of decoration.

## 9. Where the reports disagree

| Topic | Positions | Resolution proposed for step 4 |
|---|---|---|
| Section tools (Comment, Collapse) | Layouts: hidden until hover. Cards: always visible, low emphasis (hover-only controls fail on touch and keyboard) | Always visible at low emphasis, stronger on hover and focus |
| Label above the title | Layouts: an "eyebrow". impeccable: kickers are a banned pattern | No eyebrow. File name goes in the metadata line |
| Respond placement | Layouts: a drawer that takes the outline's column. Cards: a sticky right rail, bottom bar on narrow screens | **Owner decision**, shown as mockups in step 4 |
| "Show N more" on rounds | Cards: showing all 20–45 rows is simpler and keeps find-in-page working | **Owner decision**: it changes a current behaviour |
| Premise Confirm / Needs correction | Cards: a two-option radio group fits better than two toggle buttons | Keep the behaviour (click again clears); decide the markup in step 5 |
| Prose width | 34em (fonts report) and 42–46rem (layouts report) | One rule: about 68 characters, set in `ch` and checked with real text |
| Code colours | GitHub cool greys | Keep the ratios, derive the greys from the page's own neutrals |
| Mono labels | Direction B uses mono capitals; impeccable and GOV.UK advise against both | Mono only for code, IDs and paths; labels in sentence case |

## 10. Visual directions

Three directions from the layouts report, each paired here with a font set from section 2. All three keep
sections unboxed and the reading column calm.

| | A · Paper & Ink | B · Swiss Ledger | C · Quiet Studio |
|---|---|---|---|
| Mood | A printed technical report: warm paper, serif text | A ledger: neutral paper, one strong accent, full-width hairlines | A product-team tool: greys and spacing, almost no lines |
| Body type | Serif (Source Serif 4 or Literata); sans for tables and UI | Sans (Inter or Geist) | Sans (Geist or Inter) |
| Section opening | Large serif H2, number in the margin, hairline above | Full-width hairline, a left column for number, IDs and status | Space only |
| Palette | Warm off-white, near-black ink, one deep accent | Near-white, near-black, one signal accent | Near-white / near-black, a grey ramp, one highlight |
| Draws on | Tufte, Distill, Stripe Press, Anthropic research | Works in Progress, Increment, Linear changelog | Linear, Vercel Geist, Rauno Freiberg |
| Fits "editorial / document" | Strongest | Strong | Weakest: closer to a dev tool |
| Main risk | Closest to the AI "editorial" cluster; serif beside dense tables looks mixed | Many rules become "boxes made of lines"; needs a wide screen | Low-contrast greys tire the eye over long docs; can look generic |

## 11. Gallery check (browser, 2026-11-15)

The galleries blocked the research agent, so they were opened in a real browser afterwards. Seen as
result thumbnails only; no shot was opened in detail.

| Site | Searches | What the results show |
|---|---|---|
| Dribbble | "documentation page", "knowledge base article", "code review", "editorial article layout", "long form reading" | Documentation shots are near-identical: three columns, dark theme, boxed callouts and code, a blue or purple accent. "Editorial" and "long form" return magazine spreads, landing pages and brand work, not reading pages. Code-review shots are dark, with saturated red and green rows |
| Pinterest | "editorial web design long article typography" | Results load behind a log-in wall. The visible pins are magazine layouts: very large display headlines, photography, multi-column print grids |
| SiteInspire | Category "Typographic" | Studio, portfolio and culture sites built on oversized display type. No document or reading pages on the first screens |

What this adds:

- **No new direction.** The galleries hold marketing and magazine work; nothing there is a model for a
  dense reading page with tables and code. The curated sites in section 10 stay the reference set.
- **What to avoid is clear.** The common "docs" look on Dribbble (dark three-column shell, boxed
  everything, purple accent) is the generic result this redesign moves away from, and it is close to
  today's page structure.
- **Display type is the gallery idea of "editorial".** That does not transfer: this page's headings are
  working section titles, repeated 150–200 times.

## 12. Gaps

- Gallery research is shallow: thumbnails only, and Pinterest only as far as its log-in wall allows.
- Layout widths for Stripe, Linear and Apple are estimates from one desktop screenshot; hover and mobile
  behaviour were read from CSS, not seen.
- Font rendering on Windows, zero and `Il1` shapes in the mono fonts, and all colour values are untested
  on screen.
- Several listed sources were not reached (Graphite, Polaris, Notion and Google Docs layouts, Excalidraw).
- About half of each anti-slop repo's reference files were searched by keyword, not read in full.
