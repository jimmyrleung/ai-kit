# Collected — D · Cards, forms, filters and theme tokens (Q4, Q7)

Agent output, verbatim. Collected 2026-11-15. Model: Opus 5.5.

---

## Q4 findings

### Collapsed summary row (decision and premise cards)

- **Make the whole row the hit area.** NN/g says the heading and the icon must both open the accordion, and it advises against split targets ([NN/g accordions on desktop](https://www.nngroup.com/articles/accordions-on-desktop/), [NN/g accordion icons](https://www.nngroup.com/articles/accordion-icons/)). In the GOV.UK accordion the user can click anywhere in the heading button, and the GOV.UK task list links the whole row ([GOV.UK accordion](https://design-system.service.gov.uk/components/accordion/), [GOV.UK task list](https://design-system.service.gov.uk/components/task-list/)).
- **Marker.** A caret was the only icon that did better than no icon at telling users "this opens in place". Plus and arrow icons did no better than nothing. The study put the caret on the right and says left placement may give different results ([NN/g accordion icons](https://www.nngroup.com/articles/accordion-icons/)). To hide the default triangle, use `list-style: none` and `summary::-webkit-details-marker { display:none }` for Safari ([MDN summary](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/summary)). *Inference:* put the caret at a fixed position at the start of the row. Its position then does not move when the number of chips changes.
- **Keep the summary text short.** In GOV.UK research, summary lines longer than a few words made the button text too long for screen reader users ([GOV.UK accordion](https://design-system.service.gov.uk/components/accordion/)). `<summary>` gets a button role in some browsers, and that removes the heading role of a heading inside it ([MDN summary](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/summary)).
- **Number of chips.** GOV.UK says every extra status makes the set harder to remember, so start with the fewest statuses you can ([GOV.UK tag](https://design-system.service.gov.uk/components/tag/)). Carbon says to keep tag text under about 20 characters and not to wrap it ([Carbon tag](https://carbondesignsystem.com/components/tag/usage/)). *Inference:* show one state chip and at most two topic tags, then "+N". Put the rest in the body.
- **Text vs coloured status.** In the GOV.UK task list, "Completed" is plain black text and "Incomplete" is a coloured tag. This pulls the eye to the items that still need action ([GOV.UK task list](https://design-system.service.gov.uk/components/task-list/)). This maps well to "answered" (plain text) vs "Needs you" (tag).
- **Answered progress across a long list.** GitHub collapses a file when you mark it "Viewed" and shows a viewed count in the PR header ([GitHub docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request)). A counter is a good model for this. Note that GDS found users rarely look at progress indicators in long forms ([GDS blog](https://userresearch.blog.gov.uk/2015/08/13/no-more-accordions-how-to-choose-a-form-structure/)), so keep the indicator modest.
- **Focus and hover.** A 2.4.13 (AAA) focus indicator must be at least as large as a 2 CSS px perimeter, with 3:1 contrast between focused and unfocused states. Under 2.4.11 (AA), a focused item must not be fully hidden by author content such as sticky bars ([WCAG 2.2](https://www.w3.org/TR/WCAG22/)). Users understand what a GOV.UK accordion button covers once they see its focus state ([GOV.UK accordion](https://design-system.service.gov.uk/components/accordion/)). NN/g says to make each button state visibly different: enabled, hover, focus, pressed and disabled ([NN/g button states](https://www.nngroup.com/articles/button-states-communicate-interaction/)).
- **Targets.** The minimum is 24×24 CSS px (AA). WCAG encourages 44×44 (2.5.5) for important controls ([Understanding 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)).

### Card visual treatment

- GOV.UK summary cards are for several summary lists about the same kind of thing. They are not for small amounts of content. Borders help users of zoom and assistive technology ([GOV.UK summary list](https://design-system.service.gov.uk/components/summary-list/)).
- Let several cards be open at the same time. Users compare items across sections ([NN/g](https://www.nngroup.com/articles/accordions-on-desktop/)). So **do not** use `<details name>` exclusive groups for decisions. `name` itself is widely supported: Chrome 120, Firefox 130, Safari 17.2 ([MDN details](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details)).
- Provide "Expand all" and "Collapse all" ([NN/g](https://www.nngroup.com/articles/accordions-on-desktop/)). GOV.UK stores which sections are open in session storage ([GOV.UK accordion](https://design-system.service.gov.uk/components/accordion/)).
- *Inference for an editorial page:* in the closed state, separate rows with dividers only (a list, not boxes). In the open state, give the body a container: a raised-surface background or a left rule, so it does not run into the next row. Do not use shadows (see the dark theme rules).
- Browser support:
  - `::details-content` is Baseline 2025 (Chrome 131, Firefox 143, Safari 18.4) ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/::details-content)).
  - `interpolate-size` is **not** Baseline: Chromium 129+ only, Firefox no, Safari only in Technology Preview ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/interpolate-size)). Treat height animation as optional or skip it.
  - Find-in-page now opens closed `<details>` in all engines: Chrome 97, Firefox 148, Safari 26.2 ([MDN details](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details)).

### Radio option cards ("Your decision")

- **No preselection.** GOV.UK: do not preselect radios, because it makes users more likely to miss the question or submit a wrong answer ([GOV.UK radios](https://design-system.service.gov.uk/components/radios/)). NN/g's general rule is the opposite ("select one by default in most cases"), but it allows exceptions ([NN/g](https://www.nngroup.com/articles/radio-buttons-default-selection/)). People read a default as the choice-maker's recommendation ([Collabra, default effects](https://online.ucpress.edu/collabra/article/12/1/160206/217926/Default-Effects-Across-Levels-of-Cognitive-Effort)). This supports the owner's "nothing preselected" rule.
- **Layout.** Use a vertical stack and make the whole label clickable ([NN/g](https://www.nngroup.com/articles/radio-buttons-default-selection/)). Use inline radios only for two short options ([GOV.UK radios](https://design-system.service.gov.uk/components/radios/)).
- **Hints.** One short sentence per option, no full stop, no links ([GOV.UK radios](https://design-system.service.gov.uk/components/radios/)).
- **Conditional reveal.** Reveal only simple follow-up questions, never other content, and never inside inline radios. Screen readers are not always told about the change ([GOV.UK radios](https://design-system.service.gov.uk/components/radios/)).
- **"Suggested" label.** The text label is what makes it not depend on colour. GOV.UK says not to use colour alone (SC 1.4.1) ([GOV.UK tag](https://design-system.service.gov.uk/components/tag/)). *Inference:* write the word "Suggested" as a neutral, uncoloured label after the option label. Keep options in source order and do not move the suggested one to the top. Show "Suggested" in only one place inside the open card. Each extra repeat is a stronger nudge.
- **Selected state.** *Inference:* thicker border, check mark and tint together, so the state is not colour-only. Option-card borders are a control boundary, so they need 3:1 non-text contrast (SC 1.4.11, [WCAG 2.2](https://www.w3.org/TR/WCAG22/)). `accent-color` is **not** Baseline ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/accent-color)), so use it only as an enhancement.

### Status and tag vocabulary

GOV.UK rules:
- Tags show status only. Never make them links or buttons, and use adjectives, not verbs.
- Use sentence case. Uppercase was dropped because it was harder to read.
- Use light backgrounds with dark text. Dark solid tags looked like buttons.
- Keep one colour per tag everywhere it appears.
- Source: [GOV.UK tag](https://design-system.service.gov.uk/components/tag/).

Atlassian agrees: sentence case, non-interactive, and use a *tag* (not a lozenge) for descriptive metadata ([Atlassian lozenge](https://atlassian.design/components/lozenge/usage)). Carbon requires at least two of colour, shape and symbol/text ([Carbon status indicators](https://carbondesignsystem.com/patterns/status-indicator-pattern/)).

| Item on page | Tone | Treatment (my inference, based on the sources above) |
|---|---|---|
| Needs you | warning | Tag: tinted background, dark text |
| Open | neutral | Outline tag or plain muted text |
| Answer: X (reader picked) | accent | Plain text with check icon, no tag (GOV.UK "Completed" model) |
| Decided / Recorded | neutral | Plain muted text "Decided: X" |
| Deferred | neutral | Grey tag |
| Suggested: X | none | Muted plain text, never a chip |
| Topic tags (money, timing) | none | Neutral outline metadata, no colour |
| Table ok / info / warn / neutral | success / info / warning / neutral | Tinted tag plus a word; add an icon if the column is dense |
| Failure-walk wrong step | danger | Only use of the danger tone; label it in words ("Wrong outcome") |

So: four tones plus neutral, and danger is used sparingly (inference).

### Filters

- **Toggle buttons** use `aria-pressed` true/false, and the label must not change when the state changes ([APG button](https://www.w3.org/WAI/ARIA/apg/patterns/button/)).
- **Single-select views** (All / Need you / Open / Decided / Deferred) are mutually exclusive. Primer's SegmentedControl is for picking one choice from a closely related set and applying it at once ([Primer](https://primer.style/product/components/segmented-control/)). M3 segmented buttons take 2–5 segments; above five, use chips ([M3 segmented](https://m3.material.io/components/segmented-buttons/guidelines)). *Inference:* build this as a radio-group-style segmented control.
- **Multi-select tag filters** fit M3 filter chips, which show a check mark when selected ([M3 chips](https://m3.material.io/components/chips/guidelines)). Build them as `aria-pressed` toggle buttons.
- **Counts and feedback.** Facet counts help users avoid zero results. Do not jump the page to the top after a filter changes ([NN/g applying filters](https://www.nngroup.com/articles/applying-filters/)).
- **"Show N more" vs pagination.** A Load More button shows that more content exists and keeps the footer reachable. Showing "X of Y" helps orientation ([NN/g infinite scrolling](https://www.nngroup.com/articles/infinite-scrolling-tips/)). *Inference:* at 20–45 collapsed rows, hiding cards conflicts with "jump to next unanswered" and with find-in-page. Showing all of them may be simpler.
- **Bulk action.** Carbon puts its batch bar at the top of the table and lets users cancel ([Carbon data table](https://carbondesignsystem.com/components/data-table/usage/)). GOV.UK asks for a confirmation step for destructive actions ([GOV.UK button](https://design-system.service.gov.uk/components/button/)). *Inference:* if "Accept suggested" fills only unanswered items, an inline "Undo" is enough. Ask for confirmation only if it overwrites answers the reader already gave.

### Respond pattern

- **GitHub** keeps review comments pending (visible only to you) until you submit. "Review changes" opens a summary box plus a Comment / Approve / Request changes radio choice ([GitHub docs](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request)).
- **GOV.UK check answers**: group answers into sections, give a Change link per item with hidden context text, show skipped items as "Not provided", and end with one clearly worded action button ([GOV.UK check answers](https://design-system.service.gov.uk/patterns/check-answers/)). Users like these review pages ([GDS blog](https://userresearch.blog.gov.uk/2015/08/13/no-more-accordions-how-to-choose-a-form-structure/)).
- **Copied confirmation.** GOV.UK success banners are page-level, one per page, and use `role="alert"` ([GOV.UK notification banner](https://design-system.service.gov.uk/components/notification-banner/)). *Inference:* for "Copied", a small inline `role="status"` message next to the button fits better.
- *Inference on placement:* use a sticky right rail on wide screens and a bottom bar on narrow screens. Add a "Check your answers" section at the end of the list. Use one owner only, not both a top-bar panel and a rail. Every sticky element needs `scroll-padding` so focused cards are not hidden (SC 2.4.11).

### Section tools (Comment, Collapse)

- Hover-only content and controls are a known accessibility problem. Content that appears on hover or focus must be dismissible, hoverable and persistent ([Understanding 1.4.13](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html)). Hover does not exist on touch screens ([NN/g tooltips](https://www.nngroup.com/articles/tooltip-guidelines/)). *Inference:* keep the tools always visible at low emphasis, and raise their emphasis on `:hover` and `:focus-within`.

### Comment reveal and "Clear my answers"

- The Comment button is a disclosure: a button with `aria-expanded`, activated with Enter or Space ([APG disclosure](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/)). *Inference:* move focus into the textarea when it opens.
- "Clear my answers" is destructive and cannot be undone easily. GOV.UK says: use a normal-style button first, then a warning button on a confirmation step. Do not rely on red alone ([GOV.UK button](https://design-system.service.gov.uk/components/button/)).

### ID-link definition popovers

- **Tooltip vs toggletip.** Tooltips hold labels or descriptions only and appear on hover and focus. A toggletip opens on click and works with mouse, keyboard and touch ([Inclusive Components](https://inclusive-components.design/tooltips-toggletips/)). The APG tooltip pattern is still "work in progress". It uses `aria-describedby`, Escape dismisses it, and it has no focusable content; for focusable content, use a non-modal dialog ([APG tooltip](https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/)).
- **Timing.** Show after 0.3–0.5 s of hover. Hide after more than 0.5 s ([NN/g timing](https://www.nngroup.com/articles/timing-exposing-content/)).
- **Platform features:**
  - `popover` auto/manual: Chrome 114, Firefox 125, Safari 17.
  - `popover="hint"`: MDN lists Chrome 151, Firefox 153, Safari 27.3, but caniuse shows Safari as unsupported. The sources disagree ([MDN popover](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/popover), [caniuse](https://caniuse.com/?search=popover%20hint)).
  - `interestfor` shipped in Chrome 142 ([web.dev](https://web.dev/blog/web-platform-10-2025)). Mozilla's position is neutral ([Mozilla](https://github.com/mozilla/standards-positions/issues/1181)).
  - Anchor positioning (`position-anchor`) has been Baseline 2026 since September 2026 (Chrome 151, Firefox 151, Safari 27) ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position-anchor)).

### Buttons

- Use one default (primary) button per page and only a few secondary ones. Write button text in sentence case, saying what the button does ([GOV.UK button](https://design-system.service.gov.uk/components/button/)).
- Do not use chips in place of primary actions ([M3 chips](https://m3.material.io/components/chips/guidelines)).

## Q7 findings

### Token structure

Use primitives (raw OKLCH values that are never used directly in components) and semantic tokens that change per mode. This is Primer's model ([Primer colour](https://primer.style/foundations/color/overview)). The step meanings follow the Radix 12-step scale: 1–2 backgrounds, 3–5 component backgrounds, 6–8 borders and focus, 9–10 solid fills, 11–12 text ([Radix](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale)). The values below are my starting points. Lightness numbers are approximate, so check them with a contrast tool.

| Role | Purpose | Notes (light / dark) |
|---|---|---|
| `--bg-page` | Paper | `oklch(98.5% .008 85)` / `oklch(20% .008 85)`, never pure black |
| `--bg-raised` | Open card body, rail | white-ish / `oklch(24% .008 85)`: lighter in dark mode, because elevation is shown by tone |
| `--bg-sunken` | Code, diff, pre | `oklch(95.5% .008 85)` / `oklch(16.5% .006 85)` |
| `--text-1` | Body, headings | `oklch(22% .01 85)` / `oklch(92% .008 85)`, not pure white |
| `--text-2` | Metadata, hints | about 42% / about 76% |
| `--text-3` | Non-essential only | about 55% / about 64% (both ≈4.6–5:1, so OK for small text) |
| `--border-subtle` | Row dividers (decorative) | about 90% / about 30% |
| `--border-control` | Option cards, inputs, toggle outlines | Needs 3:1 against the background (SC 1.4.11): ≤ about 65% L light, ≥ about 50% L dark |
| `--accent` / `--accent-subtle` | Links, selected state, primary button | Light `oklch(50% .12 250)`; dark lighter and less saturated, about `oklch(75% .09 250)` |
| `--{success,warning,danger,info}-fg / -bg / -border` | Tags, table status, failure walk | Light: fg about 45% L, bg about 95%, border about 80%. Dark: fg about 80%, bg about 28%, border about 40%. Lower chroma in dark |
| `--focus` | 2px outline | Must have 3:1 against nearby colours in both modes |
| `--selection` | `::selection` | Accent-subtle |
| `--flash` | Highlight after a "jump to" | Warning-subtle background, fades out |

### Toggle behaviour spec

- **Use three states (System / Light / Dark).** "System" means no stored value. Build it as a small labelled radio group ("Theme"), not a single cycling button: APG says a toggle's label must not change when its state changes ([APG button](https://www.w3.org/WAI/ARIA/apg/patterns/button/)). Argyle's switch puts the current value into `aria-label` and uses `aria-live` ([web.dev theme switch](https://web.dev/articles/building/a-theme-switch-component)). Apple HIG prefers respecting the system setting with no in-app override ([Apple HIG](https://developer.apple.com/design/human-interface-guidelines/dark-mode)), which is one more reason to keep "System" as the default.
- **Stop the flash of the wrong theme.** Put a blocking inline script in `<head>` before the CSS. It reads `localStorage`, and the CSS media preference does the rest ([Josh Comeau](https://www.joshwcomeau.com/react/dark-mode/), [web.dev](https://web.dev/articles/building/a-theme-switch-component)). Add `<meta name="color-scheme">` before the styles, so the browser paints the correct canvas before the CSS is parsed ([web.dev color-scheme](https://web.dev/articles/color-scheme), [MDN color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme)).
- **`light-dark()` is safe to use now.** It became Baseline in May 2024 (Chrome 123, Firefox 120, Safari 17.5). It needs `color-scheme: light dark` and now also accepts images ([MDN light-dark](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/light-dark)). Because it follows the *used* `color-scheme`, you write each token once. The toggle only changes `color-scheme`, and print can force light in one line. This is my inference from how the function works. In "System" mode, OS changes apply with no `matchMedia` listener.

```html
<meta name="color-scheme" content="light dark">
<script>try{var t=localStorage.getItem('rv-theme');if(t==='light'||t==='dark')document.documentElement.dataset.theme=t}catch(e){}</script>
<style>
:root{color-scheme:light dark;
  --bg-page:light-dark(oklch(98.5% .008 85),oklch(20% .008 85));
  --text-1:light-dark(oklch(22% .01 85),oklch(92% .008 85));}
:root[data-theme=light]{color-scheme:light}
:root[data-theme=dark]{color-scheme:dark}
@media print{:root{color-scheme:light}}
body{background:var(--bg-page);color:var(--text-1)}
</style>
```
```js
const root = document.documentElement;
document.querySelectorAll('input[name=theme]').forEach(r => {
  r.checked = (root.dataset.theme || 'system') === r.value;
  r.addEventListener('change', () => {
    if (r.value === 'system') delete root.dataset.theme; else root.dataset.theme = r.value;
    try {
      if (r.value === 'system') localStorage.removeItem('rv-theme');
      else localStorage.setItem('rv-theme', r.value);
    } catch (e) {}
  });
});
```

### Dark theme rules

- **Background.** M2 recommends `#121212`, dark grey rather than black, so it can show depth. The darkest surface needs about 15.8:1 with white text, so text still passes 4.5:1 on the lightest raised surface ([M2 dark theme](https://m2.material.io/design/color/dark-theme.html)). Higher surfaces get lighter: overlays go from 0% to 16% ([M2](https://m2.material.io/design/color/dark-theme.html)). Apple also uses base and elevated backgrounds ([Apple HIG](https://developer.apple.com/design/human-interface-guidelines/dark-mode)).
- **Text.** Avoid pure white. web.dev gives about `rgb(250,250,250)` as an example ([web.dev prefers-color-scheme](https://web.dev/articles/prefers-color-scheme)). Apple asks for at least 4.5:1, and 7:1 for small or custom-coloured text ([Apple HIG](https://developer.apple.com/design/human-interface-guidelines/dark-mode)).
- **Colour.** Desaturate primary and status colours. Saturated colours on dark backgrounds fail 4.5:1 and "vibrate" ([M2](https://m2.material.io/design/color/dark-theme.html)).
- **Borders over shadows.** *Inference:* shadows are almost invisible on dark backgrounds, so separate surfaces with tone steps and borders (as M2's overlays do).
- **Paper tint.** *Inference:* keep the paper hue (for example 85) in dark mode, but cut chroma to about .006–.01, so the result is warm charcoal, not brown.
- **Images and SVG.** Use `currentColor` in inline SVG. Invert simple line art. Dim photos with filters, or use `<picture media>` ([web.dev](https://web.dev/articles/prefers-color-scheme)). Soften white backgrounds in images ([Apple HIG](https://developer.apple.com/design/human-interface-guidelines/dark-mode)). Model-drawn diagrams should use the semantic tokens.

### OKLCH or hex

- `oklch()` has been widely available since May 2023. Relative colour syntax needs Chrome 122, Firefox 128 and Safari 18 ([MDN oklch](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/oklch)).
- OKLCH gives predictable lightness across hues and easy derived scales. Its risk is gamut clipping that shifts hue for colours outside sRGB ([Evil Martians](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl)). Tailwind v4 moved its whole palette to OKLCH ([Tailwind v4](https://tailwindcss.com/blog/tailwindcss-v4)).
- *Recommendation:* use OKLCH with low chroma that stays inside sRGB, so there is no P3 work.
- Check contrast with WCAG 2 ratios. APCA is non-normative: it was removed from the WCAG 3 draft in 2023, and the WCAG 3 contrast method is still open ([Adrian Roselli, Apr 2026](http://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html)).

### Forced colours and `prefers-contrast` (minimum worth doing)

- **`forced-colors`** (widely available) sets `box-shadow` to none, forces colours to system colours, and sets `color-scheme` ([MDN forced-colors](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/forced-colors)). So:
  - Give chips and cards a `1px solid transparent` border.
  - Draw focus with `outline`, not shadow.
  - Show selected and pressed states with `Highlight` / `SelectedItem` plus a check icon.
- **`prefers-contrast: more`** (widely available since May 2022) ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-contrast)): override only `--text-2`, `--text-3` and `--border-*`, moving them up the scale. Primer's high-contrast themes work the same way ([Primer](https://primer.style/foundations/color/overview)).

## What this means for render-view

1. **Decision summary row:** caret, ID, headline, one state chip, up to two topic tags then "+N". "Suggested: X" moves to muted text in the body. The whole row is the target, at least 44px tall, with a 2px focus outline.
2. **Answered state:** plain "✓ Answer: B" text in accent colour, no chip. "Needs you" is the only tinted warning tag (GOV.UK task-list model).
3. **Cards:** divider rows when closed. When open, the body gets `--bg-raised` and a left rule. Never side-by-side (owner rule). No `name` attribute, so several can be open. Find-in-page can now open closed cards.
4. **Decision form:** a `<fieldset>` with a legend, vertical option cards with the whole label clickable, one-sentence hints, nothing preselected, "Suggested" as a word, `--border-control` at 3:1, and the selected state shown by border, check and tint.
5. **Premise cards:** "Confirm" / "Needs correction" are mutually exclusive, so build them as a two-option radio group, not two `aria-pressed` buttons (inference from APG).
6. **Filters:** state views as a single-select segmented control with counts in the labels. Tag filters as `aria-pressed` buttons with a check mark. Labels never change. A `role="status"` line says "Showing 15 of 21".
7. **"Show N more":** consider removing it at 20–45 items. If you keep it, "Jump to next unanswered" must reveal hidden cards.
8. **"Accept suggested for N shown":** secondary button in the filter bar. It fills unanswered items only and offers inline "Undo"; no modal.
9. **Respond:** one owner. A sticky rail on wide screens and a bottom bar on narrow ones, holding "N to answer", "Next unanswered" and "Copy response" (the page's only primary button). Add a "Check your answers" list at the end, with "Change" links back to cards. Set `scroll-padding` for the sticky elements.
10. **"Clear my answers":** secondary button, then an inline confirmation with a warning-style button. "Copied" appears as an inline status, not a banner.
11. **Section tools:** always visible at low emphasis, stronger on hover and focus-within. Never hover-only.
12. **ID popovers:** the link still navigates. The preview uses `popover="manual"` with a 300–500 ms show delay, more than 500 ms hide delay, Escape to dismiss, and it stays open while hovered. Do not rely on `hint` or `interestfor` yet. Use anchor positioning only if older Safari can be ignored; otherwise position with a few lines of JS.
13. **Theme:** a System/Light/Dark radio group, the head script, `light-dark()` tokens, and a print rule that forces light. This replaces today's duplicated `prefers-color-scheme` token blocks.
14. **Status chips in tables:** four tones plus neutral, sentence case, a word always present, and a transparent border so they survive forced-colors mode.

## Sources

All checked 2026-11-15.

- GOV.UK: [Tag](https://design-system.service.gov.uk/components/tag/), [Radios](https://design-system.service.gov.uk/components/radios/), [Accordion](https://design-system.service.gov.uk/components/accordion/), [Details](https://design-system.service.gov.uk/components/details/), [Task list](https://design-system.service.gov.uk/components/task-list/), [Summary list](https://design-system.service.gov.uk/components/summary-list/), [Button](https://design-system.service.gov.uk/components/button/), [Notification banner](https://design-system.service.gov.uk/components/notification-banner/), [Check answers](https://design-system.service.gov.uk/patterns/check-answers/), [Form structure](https://www.gov.uk/service-manual/design/form-structure), [GDS blog](https://userresearch.blog.gov.uk/2015/08/13/no-more-accordions-how-to-choose-a-form-structure/)
- NHS: [Expander](https://service-manual.nhs.uk/design-system/components/expander) (adds little beyond GOV.UK)
- NN/g: [Accordions](https://www.nngroup.com/articles/accordions-on-desktop/), [Accordion icons](https://www.nngroup.com/articles/accordion-icons/), [Radio defaults](https://www.nngroup.com/articles/radio-buttons-default-selection/), [Tooltips](https://www.nngroup.com/articles/tooltip-guidelines/), [Filters](https://www.nngroup.com/articles/applying-filters/), [Infinite scroll / Load more](https://www.nngroup.com/articles/infinite-scrolling-tips/), [Timing](https://www.nngroup.com/articles/timing-exposing-content/), [Button states](https://www.nngroup.com/articles/button-states-communicate-interaction/) (search snippet only)
- W3C: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [1.4.13](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html), [2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html), [APG button](https://www.w3.org/WAI/ARIA/apg/patterns/button/), [APG disclosure](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/), [APG tooltip](https://www.w3.org/WAI/ARIA/apg/patterns/tooltip/). The [2.4.13 Understanding page](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html) returned no usable content, so I used the normative text instead.
- MDN: [details](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/details), [summary](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/summary), [::details-content](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/::details-content), [interpolate-size](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/interpolate-size), [popover](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/popover), [Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API), [interest invokers](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API/Using_interest_invokers), [position-anchor](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position-anchor), [light-dark()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/light-dark), [color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/color-scheme), [forced-colors](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/forced-colors), [prefers-contrast](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-contrast), [oklch()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/oklch), [accent-color](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/accent-color)
- Other platform sources: [caniuse popover hint](https://caniuse.com/?search=popover%20hint), [web.dev Oct 2025](https://web.dev/blog/web-platform-10-2025), [Mozilla interestfor position](https://github.com/mozilla/standards-positions/issues/1181)
- Theme and colour: [web.dev theme switch](https://web.dev/articles/building/a-theme-switch-component), [web.dev color-scheme](https://web.dev/articles/color-scheme), [web.dev prefers-color-scheme](https://web.dev/articles/prefers-color-scheme), [Josh Comeau](https://www.joshwcomeau.com/react/dark-mode/), [Radix scale](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale), [Primer colour](https://primer.style/foundations/color/overview), [M2 dark theme](https://m2.material.io/design/color/dark-theme.html), [M3 colour system](https://m3.material.io/styles/color/system/how-the-system-works) (extract looked too generic, so I did not rely on it), [Evil Martians OKLCH](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl), [Tailwind v4](https://tailwindcss.com/blog/tailwindcss-v4), [Apple HIG dark mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode), [Roselli on APCA](http://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html)
- Component systems: [M3 chips](https://m3.material.io/components/chips/guidelines), [M3 segmented](https://m3.material.io/components/segmented-buttons/guidelines), [Primer SegmentedControl](https://primer.style/product/components/segmented-control/) (description only), [Primer StateLabel](https://primer.style/product/components/state-label/), [Atlassian lozenge](https://atlassian.design/components/lozenge/usage), [Carbon tag](https://carbondesignsystem.com/components/tag/usage/), [Carbon status](https://carbondesignsystem.com/patterns/status-indicator-pattern/), [Carbon data table](https://carbondesignsystem.com/components/data-table/usage/), [GitHub PR review](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request)
- Research and accessibility: [Inclusive Components toggletips](https://inclusive-components.design/tooltips-toggletips/), [Collabra default effects](https://online.ucpress.edu/collabra/article/12/1/160206/217926/Default-Effects-Across-Levels-of-Cognitive-Effort) (abstract snippet only)
- **Could not reach or did not check:** Shopify Polaris filters and bulk actions (the URL redirected to a generic Shopify page), Primer Label and CounterLabel, Linear triage, Google Docs and Notion comments, CSS-Tricks, `@property`, Carbon progress indicator and accordion.

## Confidence

**Confidence score: 88%.** That is below your 90% threshold, so treat the inferred parts as proposals to confirm, not final decisions. The sourced facts are about 95%. The render-view mapping and the token values are about 80%.

**12% uncertainty:**
- **Page content came through an extraction tool.** Most pages were read with Firecrawl "query" mode, which summarises a page with a model. A few points may be paraphrased wrongly. The Material 3 colour extract looked generic, so I relied on M2.
- **Browser-support data is a snapshot from 2026-11-13 to 15.** The sources disagree on `popover="hint"` in Safari (MDN 27.3 vs caniuse unsupported). Anchor positioning only became Baseline in September 2026, so users on older Safari or Firefox will lack it.
- **`light-dark()` label.** MDN still shows it as "newly available". The 30-month mark for "widely available" falls in about November 2026.
- **`localStorage` on `file://`.** Its behaviour when the generated page is opened from disk differs by browser, and I did not test it. The try/catch only keeps the page working; it does not make the saved choice persist.
- **Token lightness values** are my estimates (luminance ≈ L³). Check them with a real contrast checker.
- **My inferences**, not sourced rules: the chip limit, caret on the left, the container for the open state, the respond placement, "undo instead of confirm", and removing "Show more".
- **NN/g's research is narrower than this page.** The accordion-icon study tested navigation menus with the icon on the right, and the radio-default guidance conflicts with GOV.UK. I followed GOV.UK because it matches the owner's "nothing preselected" rule.
- **Gaps:** Polaris, Linear, Notion and Google Docs precedents were not checked, so the respond-pattern evidence rests on GitHub and GOV.UK only.
