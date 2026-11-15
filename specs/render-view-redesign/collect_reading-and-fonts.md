# Collected — A · Reading typography and fonts (Q1, Q6)

Agent output, verbatim. Collected 2026-11-15. Model: Opus 5.5.

---

## Q1 findings

| Property | Recommended value | Source |
|---|---|---|
| Measure (body) | 45–90 chars, average about 66. GOV.UK: no more than ~75. WCAG AAA: ≤ 80 | [Butterick line length](https://practicaltypography.com/line-length.html), [webtypography.net 2.1.2](http://webtypography.net/2.1.2), [GOV.UK layout](https://design-system.service.gov.uk/styles/layout/), [WCAG 1.4.8](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html) |
| Measure in CSS | About 0.5em per character on average, so 33em ≈ 66 chars | [webtypography.net 2.1.2](http://webtypography.net/2.1.2) |
| Body size (web) | 15–25px (Butterick). M3 body-large is 16/24px. GOV.UK body is 19/25px | [Butterick summary](https://practicaltypography.com/summary-of-key-rules.html), [M3 tokens (@material/web 2.5.0)](https://cdn.jsdelivr.net/npm/@material/web@2.5.0/tokens/versions/latest/sass/_md-sys-typescale.scss), [GOV.UK type scale](https://design-system.service.gov.uk/styles/type-scale/) |
| Line height | Butterick: 120–145%. WCAG 1.4.8 (AAA): at least 1.5 | [Butterick summary](https://practicaltypography.com/summary-of-key-rules.html), [WCAG 1.4.8](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html) |
| Paragraph spacing | 50–100% of the body size (4–10pt), or first-line indents, never both. AAA: paragraph spacing at least 1.5 × line spacing | [Butterick paragraphs](https://practicaltypography.com/space-between-paragraphs.html), [WCAG 1.4.8](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html) |
| Secondary / UI text | M3: body-medium 14/20, body-small 12/16, label-small 11/16. GOV.UK body-s 16/20 | [M3 tokens](https://cdn.jsdelivr.net/npm/@material/web@2.5.0/tokens/versions/latest/sass/_md-sys-typescale.scss), [GOV.UK](https://design-system.service.gov.uk/styles/type-scale/) |
| Minimum sizes | Apple: macOS default 13pt / minimum 10pt, iOS 17 / 11pt. Avoid Light and Thin weights at small sizes | [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/typography) |
| Headings | At most 3 levels (2 is better). Small size steps. Bold rather than italic. Space above and below is the main signal. No all caps | [Butterick headings](https://practicaltypography.com/headings.html) |
| Heading scale examples | GOV.UK 19 → 24 → 36 → 48px. M3 title 14/16/22, headline 24/28/32 | [GOV.UK](https://design-system.service.gov.uk/styles/type-scale/), [M3 tokens](https://cdn.jsdelivr.net/npm/@material/web@2.5.0/tokens/versions/latest/sass/_md-sys-typescale.scss) |
| Text contrast | AA 4.5:1 (large text 3:1). AAA 7:1 (large 4.5:1). Large = 18pt, or 14pt bold | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) |
| UI / border contrast | 3:1 for components and graphics that are needed to understand content. A border is not required if the control is already clear from its text or icon | [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [Understanding 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) |
| User text overrides | Layout must survive line-height 1.5, paragraph spacing 2×, letter spacing 0.12em, word spacing 0.16em | [WCAG 2.2 SC 1.4.12](https://www.w3.org/TR/WCAG22/) |
| Resize / reflow | 200% zoom, and 320 CSS px width with no 2D scroll. Data tables and diagrams are exempt | [WCAG 2.2 SC 1.4.4 / 1.4.10](https://www.w3.org/TR/WCAG22/) |
| Dark theme | Surface #121212, not pure black. Text at 87% / 60% / 38% white for high / medium / disabled. Desaturated accents | [Material dark theme](https://m2.material.io/design/color/dark-theme.html) |
| Polarity | Light mode gives better performance for normal vision. Offer dark mode for long-form reading | [NN/g dark mode (2020)](https://www.nngroup.com/articles/dark-mode/) |
| Serif vs sans | No strong guideline on good screens. The research is inconclusive and the differences are small. Individual differences are large: fastest font vs slowest font was 35% | [NN/g (2012)](https://www.nngroup.com/articles/serif-vs-sans-serif-fonts-hd-screens/), [Wallace et al. 2022, ACM TOCHI](https://dl.acm.org/doi/10.1145/3502222) |
| Tables | Start with all cell borders off and add back only what helps. Increase cell padding; top and bottom can be larger than the sides | [Butterick tables](https://practicaltypography.com/tables.html) |
| Inline code size | GitHub's markdown CSS uses 85% of the body size for code (body is 16px / 1.5) | [github-markdown-css 5.9.0](https://cdn.jsdelivr.net/npm/github-markdown-css/github-markdown.css) |
| `text-wrap: balance` | Chrome/Edge 114, Firefox 121, Safari 17.5. Baseline since 2024-05. Works only on ≤ 6 lines (Chromium) or ≤ 10 (Firefox), so use it for headings | [MDN BCD 8.1.9](https://cdn.jsdelivr.net/npm/@mdn/browser-compat-data@8.1.9/data.json), [MDN text-wrap-style](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap-style) |
| `text-wrap: pretty` | Chrome/Edge 117, Safari 26, no Firefox. Not Baseline. It costs some performance; use it for body text | [MDN BCD](https://cdn.jsdelivr.net/npm/@mdn/browser-compat-data@8.1.9/data.json), [Chrome blog](https://developer.chrome.com/blog/css-text-wrap-pretty) |
| `hyphens: auto` | Baseline widely available since 2026-03. Needs a `lang` attribute | [web-features 3.46.0](https://cdn.jsdelivr.net/npm/web-features@3.46.0/data.json), [MDN hyphens](https://developer.mozilla.org/en-US/docs/Web/CSS/hyphens) |
| `font-optical-sizing`, `font-variant-numeric` | Both Baseline widely available (2022) | [web-features](https://cdn.jsdelivr.net/npm/web-features@3.46.0/data.json) |
| `font-size-adjust` | Chrome 127, Firefox 118, Safari 17. Baseline since 2024-07. Matches x-height across fonts | [MDN font-size-adjust](https://developer.mozilla.org/en-US/docs/Web/CSS/font-size-adjust), [web-features](https://cdn.jsdelivr.net/npm/web-features@3.46.0/data.json) |

Notes:
- The sources disagree on line height. Butterick says 1.2–1.45, but WCAG AAA wants ≥ 1.5. Using 1.5 meets both. SC 1.4.12 is about *user* overrides: chips and cells must not have fixed heights that clip text.
- Your current lines (140–150 characters) are about 2× every source's maximum. Line length is the biggest problem to fix.
- **No source gives a number for** right-aligning numbers in tables, row density, or how much space to put above a heading compared with below. My values for those below are inference.

## Q6 findings

**How I measured.** I downloaded each font from the google/fonts repo (or the foundry) into memory and used fontTools 4.68 to check licence, glyph coverage, x-height and sizes. No files were written. "Full" means the whole font compressed to woff2. "GF latin" means the Fontsource/Google `latin` subset, read from the jsDelivr API.

"Custom subset" means my own character set. It includes the Google `latin` range plus → ← ↳ − ≤ ≥ ≠ ✓ ✔ ✗ ✕ ▸ and box drawing U+2500–257F. It keeps only these features: kern, liga, calt, ccmp, locl, mark, mkmk, tnum, zero, case, lnum, pnum. Weight is narrowed to 400–700 and other axes are pinned. Hinting is removed.

**Critical finding: the Google `latin` subset does not contain → ← ↳ ✓ ≤ ≥ ≠ or box drawing.** It has only ↑ ↓ and −; I checked the actual unicode-range in the Google Fonts CSS. So you must make your own subset.

| Font | Licence / RFN | Axes | Full / GF latin / custom subset (KB) | Notes |
|---|---|---|---|---|
| Source Serif 4 | OFL. The Google build has **no RFN**. The Adobe release has RFN "Source" | wght 200–900, opsz 8–60 | 418 / 50 (wght) or 120 (+opsz) / **36**, italic **38** | Default digits are already tabular. Has tnum, onum, zero. x-height 0.475. No ↳ ✔ ✗. Keeping opsz makes the custom subset 121 KB |
| Literata | OFL, no RFN | opsz 7–72, wght 200–900 | 388 / 51 or 108 / **37**, italic **39** | Digits are proportional, so set `tabular-nums` in tables (it has tnum). x-height 0.507. No ↳ ✓ |
| Newsreader | OFL, no RFN | wght 200–800, opsz 6–72 | 210 / 57 or 129 / 40, italic 44 | **No arrows and no ✓.** Small x-height (0.426). Better for display |
| Charis SIL (Charter design) | OFL, **RFN "Charis", "SIL"** | static, 4 files | 258 per style / 22 / 13–14 unhinted, 21–26 hinted | Tabular digits. x-height 0.482. No tnum feature (not needed) |
| IBM Plex Serif | OFL, **RFN "Plex"** | static | 50 / 19 / 12–15 unhinted, **19 hinted** per style | Tabular digits. x-height 0.516, same as Plex Mono |
| Inter | OFL, no RFN | opsz 14–32, wght 100–900 | 343 / 47 or 71 / **29** | Proportional digits (has tnum). x-height 0.546. Has → ↳ ✓ |
| IBM Plex Sans | OFL, RFN "Plex" | wght 100–700, wdth 75–100 | 224 / 45 / 30, 35 hinted | Tabular digits |
| Geist | OFL, no RFN | wght 100–900 | 68 / 29 / **19** | Proportional digits. No ✓ |
| Public Sans | OFL, no RFN | wght 100–900 | 41 / 26 / 21 | **No arrows, no ✓** |
| Atkinson Hyperlegible Next | OFL, no RFN | wght 200–800 | 47 / 33 / 19 | **No arrows, no ✓** |
| JetBrains Mono | OFL, no RFN | wght 100–800 | 70 / 40 / **30** | Dotted zero. Box drawing yes. No ↳ ✓ ✔ ✗. x-height 0.55 |
| Commit Mono | OFL, no RFN. Last release v1.143, Dec 2023 | wght 200–700, **ital 0–1** | 84 (foundry VF) / – / **24, italic included** | Slashed zero (from glyph geometry). Box drawing, ✓ ✗ present; only ↳ missing. x-height 0.54. Unhinted |
| Geist Mono | OFL, no RFN | wght 100–900 | 69 / 23 / **17** | Zero is slashed (from glyph geometry; medium confidence). Box drawing yes. No ✓ |
| IBM Plex Mono | OFL, RFN "Plex" | static | 38 / 14 / 9–10 unhinted, **16–17 hinted** | Dotted zero. Box drawing yes; missing only ✔ ✗ ✕ ▸ |
| Source Code Pro | OFL, **RFN "Source"** (also in the Google build) | wght 200–900 | 88 / 22 / 21 | Dotted zero. Box drawing yes |
| Fira Code | OFL, no RFN | wght 300–700 | 104 / 35 / 33 | Oval-dot zero. Programming ligatures (calt) can change sequences like `->` |
| Atkinson Hyperlegible Mono | OFL | wght 200–800 | 25 / 17 / 16 | **No arrows, no box drawing** |
| Fraunces / Instrument Serif | OFL | Fraunces: opsz, wght, SOFT, WONK. Instrument: static | 190 / 36 / 31; 27 / 21 / 14 | Display only. No arrows. Instrument Serif also has no ≤ ≥ |

All the monospace fonts above have tabular digits by default. All of them mark the zero.

**Licence.** OFL FAQ 1.11–1.12 says fonts embedded in a document may be embedded in full or as a subset, and the modification rules do not apply. FAQ 2.2–2.6 says that for *webfonts*, subsetting counts as modification, which normally means a Reserved Font Name cannot be used. A base64 `@font-face` in a shared HTML file sits between these two cases (my inference). The safe options are to pick fonts without an RFN, or to rename the family in the subset's `name` table ([OFL FAQ](https://openfontlicense.org/ofl-faq/)).

**Windows rendering.** Google recommends shipping variable fonts unhinted ([gf-guide](https://googlefonts.github.io/gf-guide/variable.html)). In my measurements, narrowing a variable font with the fontTools instancer appears to drop its hinting (hinted and unhinted sizes came out the same). Static Plex and Charis keep their hinting for about +5–8 KB per file. DirectWrite renders unhinted webfonts reasonably ([Smashing, 2012](https://www.smashingmagazine.com/2012/04/a-closer-look-at-font-rendering/)). *Inference:* hinted static Plex is the safest choice for 13–14px UI text at 100% display scaling. At 125% scaling or more, the difference is small.

**Pairings** (custom subset, before base64):

| # | Text | UI | Mono | Character | Total → base64 |
|---|---|---|---|---|---|
| A | Source Serif 4 R + I (36 + 38) | Inter (29) | JetBrains Mono (30) | Classic editorial serif with a crisp, neutral UI face and a very clear code face | **133 KB → ~177 KB** |
| B | Literata R + I (37 + 39) | system-ui (0), or Geist (+19) | Commit Mono, italic included (24) | Warm serif built for long screen reading, with a quiet neutral mono. Smallest set | **100 KB → ~133 KB** (119 → 159 with Geist) |
| C | IBM Plex Serif R / I / B (19 × 3, hinted) | Plex Sans VF (35, hinted) | Plex Mono R / B (17 + 16) | One designed system: mono and serif x-heights match exactly; hinted for Windows; RFN "Plex" means renaming the subset | **~125 KB → ~167 KB** |

**Inline code sizing** = body x-height ÷ mono x-height (my calculation):
- A: 0.475 / 0.55 ≈ 0.86, which is close to GitHub's 85%.
- B: 0.507 / 0.54 ≈ 0.94.
- C: 1.0 by metrics. In practice about 0.92, because mono letters are wider (inference).

**Fallback stacks** (from my knowledge, not checked against a source):
- Serif: `Charter, "Sitka Text", Cambria, Georgia, serif`
- UI: `system-ui, "Segoe UI", -apple-system, Roboto, Arial, sans-serif`
- Mono: `ui-monospace, "Cascadia Mono", Consolas, "SF Mono", Menlo, monospace`
- Add `"Segoe UI Symbol"` at the end of each stack, for ✓ ✗ ↳.

**Tools.** Make the subset with `pyftsubset` (`--unicodes=… --layout-features=… --flavor=woff2`). Narrow the axes with `fonttools varLib.instancer font.ttf wght=400:700 opsz=17`. glyphhanger is an alternative.

## What this means for render-view

- Prose column `max-width: 34em` (about 66 characters; check with a real paragraph). Never wider than about 75 characters.
- Tables, code blocks, diffs and SVGs may extend past the prose column up to the full main area (about 1100–1200px next to the sidebar), with horizontal scroll inside the block. WCAG reflow exempts data tables and diagrams. (The width is my inference.)
- Body text 17px serif, line-height 1.5 (meets AAA 1.4.8). Use 16px only for the Plex pairing, because of its large x-height.
- UI text (sidebar, chips, table cells) 14px with line-height about 1.4. Nothing read below 12px. Weight 400 minimum, never Light.
- Headings in at most 3 visible levels, roughly 32 / 24 / 20px, with H4 = body size in semibold. Space above about 2× the space below (inference from Butterick). `text-wrap: balance` on headings.
- `text-wrap: pretty` on `p` and `li`. Firefox ignores it safely. Leave `hyphens` off, because hyphenation would break IDs and code-like words.
- Inline code: `font-size: 0.86em` (pairing A) or `0.94em` (pairing B). Or, more simply, set `font-size-adjust: ex-height from-font` on code and keep it at 1em.
- Tables: `font-variant-numeric: tabular-nums` (needed for Literata and Inter), right-align number columns (inference), horizontal rules only, cell padding about 6–8px vertical and 10–12px horizontal.
- Light theme: body text ≥ 7:1, secondary text ≥ 4.5:1, focus rings and controls ≥ 3:1. Decorative rules can be lighter.
- Dark theme: background about #121212 and body text about 87% white (#dedede ≈ 13.9:1, my calculation). Desaturate the accent colours.
- Build one custom subset per file that includes arrows, math, checks and box drawing (box drawing in the mono file only). Do not use Google's latin subset files.
- Pin `opsz` at the body size when instancing. Keeping the full opsz axis costs about 3× the size (Source Serif 4: 36 → 121 KB).
- Font budget: 4 files at about 100–135 KB raw, about 135–180 KB as base64. This is well under the 300 KB target.

## Sources
All checked 2026-11-15.
- https://practicaltypography.com/summary-of-key-rules.html, /line-length.html, /headings.html, /space-between-paragraphs.html, /tables.html, /monospaced-fonts.html
- https://www.w3.org/TR/WCAG22/
- https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html
- https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- http://webtypography.net/2.1.2
- https://design-system.service.gov.uk/styles/type-scale/ and /styles/layout/
- https://cdn.jsdelivr.net/npm/@material/web@2.5.0/tokens/versions/latest/sass/_md-sys-typescale.scss (the m3.material.io page itself did not render)
- https://m2.material.io/design/color/dark-theme.html
- https://developer.apple.com/design/human-interface-guidelines/typography
- https://www.nngroup.com/articles/serif-vs-sans-serif-fonts-hd-screens/
- https://www.nngroup.com/articles/dark-mode/
- https://dl.acm.org/doi/10.1145/3502222
- https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap-style, /hyphens, /font-size-adjust
- https://developer.chrome.com/blog/css-text-wrap-pretty
- https://cdn.jsdelivr.net/npm/@mdn/browser-compat-data@8.1.9/data.json
- https://cdn.jsdelivr.net/npm/web-features@3.46.0/data.json
- https://cdn.jsdelivr.net/npm/github-markdown-css/github-markdown.css (5.9.0)
- https://openfontlicense.org/ofl-faq/
- https://googlefonts.github.io/gf-guide/variable.html
- https://www.smashingmagazine.com/2012/04/a-closer-look-at-font-rendering/
- https://fonts.googleapis.com/css2?family=Source+Serif+4 (latin unicode-range)
- https://github.com/google/fonts (ofl/* TTF files and OFL.txt files)
- https://raw.githubusercontent.com/adobe-fonts/source-serif/release/LICENSE.md
- https://github.com/eigilnikolajsen/commit-mono (v1.143 via jsDelivr)
- https://data.jsdelivr.com/v1/packages/npm/@fontsource-variable/* and @fontsource/*

## Confidence
**Confidence: 87%.** Licences, coverage, x-heights and sizes were measured directly, and the WCAG, Butterick, GOV.UK, M3 and browser-support numbers come from current primary data. What I could not confirm is listed below.

- My custom subset sizes are real fontTools output, but `pyftsubset` with other options (hinting, feature list, name table) will differ by about ±10–20%.
- Narrowed variable fonts appear to lose hinting. I inferred this because hinted and unhinted sizes were equal; I did not check the output tables.
- Windows ClearType quality at 13–16px was not tested visually. Those statements are inference, plus one source from 2012.
- Zero shapes (dotted or slashed) come from contour geometry, not a visual check. Geist Mono is the least certain. I did not check Il1 / O0 shapes in code.
- Whether a base64 HTML file counts as "embedding" or "webfont" under the OFL is not settled by the FAQ. That is why I suggest avoiding RFN fonts or renaming them.
- These numbers have no source and are my inference: heading space above vs below, table row density, right-aligning numbers, the breakout width, the fallback stacks (Sitka and Cascadia shipping with Windows 11), and the 0.5em-per-character estimate (from Rutter, not measured per font).
- The m3.material.io page did not render, so I used the official @material/web token file instead. The NN/g serif article is from 2012.
- Safari support data for `hyphenate-limit-chars` looks odd (BCD lists 27.3), so I left it out.
- I did not measure a full woff2 for Commit Mono myself; the 84 KB is the foundry's file. I did not check Literata italic coverage separately.
