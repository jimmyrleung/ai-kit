# Collected — C · Code, diffs and diagrams (Q3, Q5)

Agent output, verbatim. Collected 2026-11-15. Model: Opus 5.5.

---

## Q3 findings: code and diffs in a reading page

**Light or dark code on a light page?** Both are common. Among the sites I checked, light code is the more usual choice for document-style pages, and dark code shows up on product and marketing-style docs.

| Site (screenshot or CSS checked 2026-11-15) | Code block in light theme | Separation method |
|---|---|---|
| GitHub markdown (github-markdown-css) | Light, `#f6f8fa` | Tint only: no border, radius 6px, padding 1rem |
| MDN | Light grey | 1px border, header bar with language label and a "Copy" text button |
| Vercel Geist | White | 1px hairline border, file-name header with icon, copy icon on the right |
| Stripe API reference | Request sample is dark, response is light | Dark panel for "run this", light panel for output |
| Tailwind docs | Dark, under a light preview card | Heavy dark slab |

Dark blocks seem to be used when code is the "product", meaning something you copy and run, like Stripe's request or Tailwind's class strings. This is my inference; neither site says why. For an editorial page full of excerpts, the GitHub, MDN and Geist pattern fits better: a light tint or a hairline frame.

### Syntax palette (6 tokens + plain)

Values come from Primer Primitives v11.10.0 (`prettylights-syntax-*`, which is current GitHub). The Shiki `github-*-default` mapping shows which token plays which role. I computed all contrast ratios with the WCAG formula.

| Token | Light hex | Dark hex | Source / role in GitHub theme | Contrast, light (on #fff / #f6f8fa) | Contrast, dark (on #0d1117 / #151b23) |
|---|---|---|---|---|---|
| plain | `#1f2328` | `#f0f6fc` | Primer `fgColor-default` | 15.8 / 14.8 | 17.4 / 15.9 |
| keyword | `#cf222e` | `#ff7b72` | `prettylights-syntax-keyword` | 5.36 / 5.03 | 7.51 / 6.87 |
| string | `#0a3069` | `#a5d6ff` | `prettylights-syntax-string` | 12.8 / 12.0 | 12.3 / 11.3 |
| comment | `#59636e` | `#9198a1` | `prettylights-syntax-comment` | 6.11 / 5.74 | 6.50 / 5.94 |
| number | `#0550ae` | `#79c0ff` | `prettylights-syntax-constant` (Shiki: `constant`) | 7.59 / 7.13 | 9.73 / 8.90 |
| function | `#6639ba` | `#d2a8ff` | `prettylights-syntax-entity` | 7.34 / 6.90 | 9.72 / 8.89 |
| type | `#953800` | `#ffa657` | `prettylights-syntax-variable`; Shiki `entity.name` (class names) | 7.39 / 6.94 | 9.77 / 8.94 |
| line number | `#59636e` | `#9198a1` | Primer `fgColor-muted` | 6.11 | 6.50 |

Things to avoid:

- **Old Shiki light values.** In the Shiki `github-light-default` file, comment is `#6e7781` (4.27 on `#f6f8fa`, fails) and function is `#8250df` (4.74). Primer's newer values are darker and pass.
- **Shiki line-number grey.** `#8c959f` is only 3.04:1.
- **Word-level highlight backgrounds.** Some tokens fail there:
  - Light: keyword on `#ffcecb` is 3.81; comment on it is 4.35.
  - Dark: comment on the composited add-word background is 3.5; keyword is 4.05.
  - GitHub accepts this. If you want to avoid it, use a softer word background (see the bullets below).

**Higher-contrast option.** Shiki `github-light-high-contrast` and `github-dark-high-contrast` use: keyword `#a0111f` / `#ff9492`, string `#032563` / `#addcff`, comment `#66707b` / `#bdc4cc`, function `#622cbc` / `#dbb7ff`, constant `#023b95` / `#91cbff`, type `#702c00` / `#ffb757`.

### Diff colours (Primer `diffBlob-*`, v11.10.0)

| Token | Light | Dark (raw → composited on `#0d1117`) | Light colourblind | Dark colourblind |
|---|---|---|---|---|
| additionLine bg | `#dafbe1` | `#2ea04326` → `#12261e` | `#ddf4ff` (blue) | `#388bfd26` |
| deletionLine bg | `#ffebe9` | `#f851491a` → `#25181c` | `#fff1e5` (orange) | `#db6d2826` |
| additionNum bg (gutter) | `#aceebb` | `#3fb9504d` → `#1c4428` | `#b6e3ff` | `#58a6ff4d` |
| deletionNum bg | `#ffcecb` | `#f851494d` → `#542426` | `#ffd8b5` | `#db6d284d` |
| additionWord bg | `#aceebb` | `#2ea04366` → `#1a4a29` | `#b6e3ff` | `#388bfd66` |
| deletionWord bg | `#ffcecb` | `#f8514966` → `#6b2b2b` | `#ffd8b5` | `#db6d2866` |
| hunkLine bg / fg | `#ddf4ff` / `#59636e` | `#388bfd1a` / `#9198a1` | `#f6f8fa` | `#212830` |
| hunkNum bg | `#b6e3ff` | `#0c2d6b` | `#e6eaef` | `#2f3742` |
| emptyLine bg | `#f6f8fa` | `#151b23` | same | same |
| line text (all row types) | `fgColor-default` | `fgColor-default` | | |
| sign / stat colour | success `#1a7f37` (5.08), danger `#d1242f` (5.24) | `#3fb950` (7.45), `#f85149` (5.65) | `#0969da` / `#bc4c00` | `#58a6ff` / `#f0883e` |

Primer's colourblind themes swap green/red for blue/orange in every diff token. Do not rely on colour alone (WCAG 1.4.1). Keep these cues:

- a real `+` / `−` sign column
- the two number gutters, where one side is empty for adds and deletes
- a tinted gutter cell
- optionally, a 2–3px left bar in the success/danger colour

Expressive Code shows `+`/`-` indicators with a `content` pseudo-element, at 40% luminance in light themes and 67% in dark themes.

### Code frame spec, from sources

| Aspect | Source values |
|---|---|
| Font size | Expressive Code `0.85rem`; GitHub `pre` 85% of 16px body |
| Line height | Expressive Code `1.65`; GitHub `1.45` |
| Padding | Expressive Code `1rem` block / `1.35rem` inline; GitHub `1rem` |
| Border / radius | Expressive Code `1.5px` / `0.3rem`; GitHub none / 6px; Geist and MDN 1px hairline |
| Long lines | Expressive Code `wrap: false` (scroll) by default; `preserveIndent: true` when wrap is on. GitHub uses `overflow:auto; white-space:pre` |
| Highlighted line | Expressive Code `mark`: neutral blue hue 284 at 50% background, plus a `0.15rem` accent bar on the left; labels drawn as a small coloured box. Geist: "highlight only the lines under discussion" |
| Header | File name in a header strip (Geist, MDN, Expressive Code editor tab). Geist: show the filename when the snippet has a paste destination |
| Copy | Header right: icon (Geist, Stripe) or a "Copy" text button (MDN) |
| Inline code | GitHub: `padding:.2em .4em; font-size:85%; background:#818b981f; border-radius:6px; white-space:break-spaces`. Inside headings: `font-size:inherit; padding:0 .2em` |
| Pins | Code Hike renders the callout after the line, with a pointer at `left: <column>ch` |
| Print | Browsers may drop backgrounds and recolour text (`print-color-adjust: economy` is the default). Scrolling code gets cut off on paper, so wrap it for print |

No source found for ligatures or tab size. My proposal: `font-variant-ligatures:none`, and expand tabs to 4 spaces in the generator.

## Q5 findings: SVG diagrams

| Aspect | Rule | Source |
|---|---|---|
| Stroke weight | Tool defaults: D2 shapes and connections `StrokeWidth: 2`, connection corner radius 10; Graphviz `penwidth 1.0`, `arrowsize 1.0`. Proposal: node border 1px, edge 1.25px, emphasised edge 2px | d2target.go, Graphviz attrs |
| Contrast | Lines and borders the reader needs: at least 3:1 against what is next to them. Text in graphics: 4.5:1 | WCAG 1.4.11, 1.4.3 |
| Neutral colours | Primer light `#818b98` (`borderColor-emphasis`, 3.45:1) for node borders and `#59636e` (6.11:1) for edges and labels. Dark: `#656c76` (3.57) and `#9198a1` (6.50) | Primer + my computation |
| Fills | Muted fills alone fail: `#dafbe1` on white is 1.11:1. So state must come from stroke, shape or text | My computation, WCAG 1.4.1 |
| Colour count | Neutral first; colour only for meaning, used the same way across diagrams; plan for black-and-white print and colour blindness | C4 notation; Mermaid `neutral` theme exists for B&W print |
| Okabe-Ito | Orange `#E69F00` (2.25) and sky blue `#56B4E9` (2.31) fail as lines on white. Blue `#0072B2` (5.19) and vermillion `#D55E00` (3.87) are usable | Okabe-Ito hex list + my computation |
| Legend | Explain every shape, colour, border style, line type and arrowhead used; every diagram has a title | C4 notation |
| Edges | One direction per line, each with a descriptive label | C4 notation |
| Labels | Defaults: Mermaid 16px (actor/note 14, message 16); D2 shape font 16 (scale 13/14/16/20…), labels bold; Graphviz 14pt. Proposal: node labels 14px sans 500 weight, sub-labels 12px muted, edge labels 12px on a page-colour backing | Mermaid, d2fonts, Graphviz |
| Dark theme | Primer dark uses alpha fills (e.g. `#2ea04326`) so tints blend with any surface. Use CSS classes plus variables in the page stylesheet, not hard-coded hex | Primer dark.css |
| Accessibility | Non-interactive: `role="img"` + `<title>`/`<desc>` with `aria-labelledby`. Interactive nodes: `tabindex="0"`, a role, and `aria-label`. The interaction must not be shown only by colour | data.europa.eu, fizz.studio, a11y-collective |
| Figure | `figure` stays in the main column; a `fullwidth` class for wide figures; captions as margin or figure notes | Tufte CSS |
| Chartjunk | Make most of the ink carry information; erase non-data ink (panels, shadows, heavy frames) | Tufte summaries |

**Per diagram type**

- **State machine.** Use the UML conventions:
  - rounded-rect states
  - small solid filled circle for initial
  - a circle around a smaller filled circle for final
  - X for terminate
  - transition labels `trigger [guard] / effect`
  - diamond for choice

  Your "final state with inner border" is close to D2's `double-border`. Self-transitions: no source found. Proposal: a small loop arc on the top-right corner.
- **Sequence.**
  - Lifelines: rectangle head plus a vertical line, which may be dashed.
  - Activation bars: shown as thin rectangles in UML and optional in Mermaid. Proposal: leave them out.
  - Message lines: Mermaid uses solid lines for calls, dotted lines for replies, `-x` (a cross at the end) for lost/failed messages, and an open arrowhead for async.
  - Fragments: `alt`/`opt`/`break`/`critical`. Your failure-exit column maps to `break`.
  - New and removed messages: add a text cue as well as green/red. For removed, use strike-through plus a dashed line. For new, add a "+" or "new" tag.
- **Graph (new/changed/shared/removed/same).** Proposal: "same" is the plain neutral style.
  - new: solid 1.5px stroke in success colour + "new" tag
  - changed: attention-colour stroke + "~" or "changed" tag
  - removed: dashed stroke + strike-through label + 60% opacity
  - shared: double border or neutral fill

  The legend shows the same swatch plus the same word.
- **Timeline, failure walk, flow, tree.** Same neutral ink. Mark the "wrong outcome" with a word plus an icon, not only red.

## What this means for render-view

1. **Light theme code background.** Use `#f6f8fa` (Primer `bgColor-muted`), no border, with an optional 1px `#d1d9e0` rule at top and bottom, and radius 0–4px. Drop the dark `#16181D` slab.
2. **Dark theme code background.** Use `#151b23` on a `#0d1117`-like page, or one step off your own page background.
3. **Syntax palette.** Use the Primer prettylights values in the table above. All six tokens pass 4.5:1 on both backgrounds in both themes.
4. **Line numbers.** Colour `#59636e` / `#9198a1`, `font-variant-numeric: tabular-nums`, `user-select:none` (or CSS `content: attr()`), right-aligned.
5. **Diff rows.** Use the Primer `diffBlob` light/dark values. Keep the sign column, and tint the gutter with the stronger `*Num` colour. Use softer word backgrounds (alpha 0.25–0.4) where tokens fail.
6. **Hunk header.** Background `#ddf4ff` / `#388bfd1a`, muted text, mono, `@@ lines 56–78 · class Foo` at 0.85em.
7. **Diff stat.** `+12 −4` as text in success/danger colours with tabular figures. The signs carry the meaning, not the colour.
8. **Highlighted lines.** Neutral tint (`#eaeef280`, from the GitHub line-highlight colour) plus a 2–3px left accent bar, like Expressive Code. Highlight only the lines under discussion.
9. **Pins.**
   - Set them in the body sans font at 0.85em, outside the code font, so they do not look like code.
   - Indent them to the code column.
   - Add a 2px left rule in the tone colour and a tone word ("Risk:") as text.
   - Exclude them from copy.
10. **Caption bar.**
    - Show the file path in mono 0.8em in muted colour on the same tint as the block, separated by a 1px rule.
    - Put the line range and git ref on the right, with a copy icon at the far right.
11. **Code text and wrapping.** `0.85em` on a 16px body, line-height 1.5–1.6. Scroll long lines by default, and use `@media print { pre { white-space: pre-wrap } }`.
12. **Inline code.** Use the GitHub chip (`85%`, `.2em .4em`, `#818b981f`, radius 4–6px). In headings, use `font-size:inherit`. For path links, keep the link colour and underline on the chip text.
13. **Diagrams sit on the page, not in an amber panel.**
    - Use a `figure` with "Figure N." plus caption below.
    - Node border 1px `#818b98` / `#656c76`, edges 1.25px `#59636e` / `#9198a1`, emphasised edges 2px.
    - Labels 14px, sub-labels 12px; use one hue per status, always paired with a word, glyph or dash.
14. **Hover and focus.** Use the same highlight for `:hover` and `:focus-visible`: outgoing edges at 2px in the accent colour, everything else at about 35% opacity. Nodes get `tabindex="0"` plus `aria-label`. Link the SVG to the existing "As text" list with `aria-describedby`.

## Sources (all checked 2026-11-15)

- Primer Primitives CSS v11.10.0 (light, dark, light-colorblind, dark-colorblind): https://unpkg.com/@primer/primitives@11.10.0/dist/css/functional/themes/light.css (and `dark.css`, `light-colorblind.css`, `dark-colorblind.css`). Also downloaded `light-high-contrast.css` and `dark-dimmed.css`, but I did not extract values from them.
- Shiki themes: https://raw.githubusercontent.com/shikijs/textmate-grammars-themes/main/packages/tm-themes/themes/github-light-default.json, `github-dark-default.json`, `github-light-high-contrast.json`, `github-dark-high-contrast.json`
- github-markdown-css: https://raw.githubusercontent.com/sindresorhus/github-markdown-css/main/github-markdown-light.css
- Expressive Code: https://expressive-code.com/reference/style-overrides/ · https://expressive-code.com/key-features/text-markers/ · https://expressive-code.com/key-features/frames/ · https://expressive-code.com/key-features/word-wrap/ · https://expressive-code.com/plugins/line-numbers/
- Code Hike callout: https://codehike.org/docs/code/callout
- a11y-syntax-highlighting: https://github.com/ericwbailey/a11y-syntax-highlighting
- Screenshots: https://tailwindcss.com/docs/padding · https://docs.stripe.com/api/charges/create · https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for · https://vercel.com/geist/code-block
- MDN: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/print-color-adjust · https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/white-space · https://meta.stackoverflow.com/questions/269627/fix-css-to-word-wrap-code-blocks-when-printing
- WCAG: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html · https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
- D2: https://d2lang.com/tour/themes/ · https://d2lang.com/tour/style/ · https://raw.githubusercontent.com/terrastruct/d2/master/d2target/d2target.go · `d2themes/d2themescatalog/default.go` · `d2renderers/d2fonts/d2fonts_common.go`
- Mermaid: https://mermaid.js.org/config/theming.html · https://mermaid.js.org/syntax/sequenceDiagram.html
- Graphviz: https://graphviz.org/doc/info/attrs.html
- C4: https://c4model.com/diagrams/notation
- UML: https://www.uml-diagrams.org/sequence-diagrams.html · https://www.uml-diagrams.org/state-machine-diagrams.html
- Okabe-Ito: https://easystats.github.io/see/reference/okabeito_colors.html · https://jfly.uni-koeln.de/color/ (named as the origin; not opened)
- Tufte: https://edwardtufte.github.io/tufte-css/ · https://jtr13.github.io/cc19/tuftes-principles-of-data-ink.html
- Carbon: https://carbondesignsystem.com/data-visualization/color-palettes/ (reached; no line-weight or contrast rules found)
- SVG accessibility: https://data.europa.eu/apps/data-visualisation-guide/accessible-svg-and-aria · https://fizz.studio/blog/reliable-valid-svg-accessibility/ · https://www.a11y-collective.com/blog/svg-accessibility/
- GitLab Pajamas: https://design.gitlab.com/ (search only; I found no diff-colour page)
- **Not checked:** Graphite, Linear, Josh Comeau, Rauno, GitHub PR UI (live), GitHub docs on themes, Excalidraw, tldraw, Stripe diagrams, AWS/Azure icon rules, Material data-vis, Solarized/Rosé Pine/Catppuccin analyses.

## Confidence

**Confidence score: 85%.** The hex values are read directly from files, and the core conventions come from primary sources. The design proposals are my judgement.

**15% uncertainty:**

- **Primer version.** Primer values are from v11.10.0 (unpkg "latest" on 2026-11-15). github.com may run a different build.
- **Shiki theme.** Shiki values are from the `main` branch. They are older than Primer, which is why comment and function differ.
- **Contrast ratios.** I computed them with the WCAG luminance formula. Alpha colours were composited over `#0d1117` only. Over your real dark page colour, the results will differ a little.
- **Token mapping.** Matching your tokenizer's "function" and "type" classes to GitHub roles (`entity` → function, `entity.name`/`variable` orange → type) is my interpretation.
- **Light vs dark survey.** It is based on one screenshot per site, at desktop width.
- **No source found** for: arrowhead sizes, self-transition drawing, the UML lost-message dot, ligatures, tab size, minimum label size, and how GitHub draws the diff stat bar. I labelled all of these as proposals.
- **CSS variables in SVG.** I am not sure that `var()` inside SVG presentation attributes works the same in all browsers. That is why I suggest classes plus a stylesheet.
- **Not checked.** Several sources you listed were not checked (see the list above).
