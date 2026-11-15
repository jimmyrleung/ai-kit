---
name: render-view page
description: A calm reading page for long technical specs, with one signal colour
colors:
  bg: "light-dark(#fafafa, #0e0f11)"
  bg-raised: "light-dark(#ffffff, #16171a)"
  bg-sunken: "light-dark(#f0f0f1, #191a1d)"
  ink: "light-dark(#16171a, #ededee)"
  ink-2: "light-dark(#55575e, #a3a5ab)"
  ink-3: "light-dark(#6b6d75, #8b8d95)"
  rule: "light-dark(#e6e6e8, #232428)"
  border-control: "light-dark(#82848c, #6f717a)"
  signal: "light-dark(#b93a0a, #ff9466)"
  signal-bg: "light-dark(#fde9df, #3a2015)"
  highlight: "light-dark(#fdf1ea, #2a1d16)"
  ok: "light-dark(#1a6b3c, #7fd3a2)"
  ok-bg: "light-dark(#e2f3e8, #1a3226)"
  info: "light-dark(#1d4f9c, #9cc0f5)"
  info-bg: "light-dark(#e3ecfa, #1c2a44)"
  warn: "light-dark(#8a4a0b, #f0b77e)"
  warn-bg: "light-dark(#fbebd8, #3a2a1a)"
  danger: "light-dark(#b42318, #f6a39b)"
  danger-bg: "light-dark(#fde8e6, #3a1f1c)"
typography:
  h1: { fontFamily: "Geist, system-ui, sans-serif", fontSize: "1.875rem", fontWeight: 600, lineHeight: 1.2, letterSpacing: "-0.015em" }
  h2: { fontFamily: "Geist, system-ui, sans-serif", fontSize: "1.375rem", fontWeight: 600, lineHeight: 1.3, letterSpacing: "-0.015em" }
  h3: { fontFamily: "Geist, system-ui, sans-serif", fontSize: "1.125rem", fontWeight: 600, lineHeight: 1.35 }
  h4: { fontFamily: "Geist, system-ui, sans-serif", fontSize: "1rem", fontWeight: 600, lineHeight: 1.5 }
  body: { fontFamily: "Geist, system-ui, sans-serif", fontSize: "1rem", fontWeight: 400, lineHeight: 1.6 }
  ui: { fontFamily: "Geist, system-ui, sans-serif", fontSize: "0.875rem", fontWeight: 400, lineHeight: 1.4 }
  small: { fontFamily: "Geist, system-ui, sans-serif", fontSize: "0.8125rem", fontWeight: 400, lineHeight: 1.45 }
  code: { fontFamily: "Geist Mono, ui-monospace, monospace", fontSize: "0.84375rem", fontWeight: 400, lineHeight: 1.6 }
rounded:
  sm: "4px"
  md: "6px"
  lg: "10px"
spacing:
  "1": "4px"
  "2": "8px"
  "3": "12px"
  "4": "16px"
  "5": "24px"
  "6": "32px"
  "7": "48px"
  "8": "64px"
  "9": "88px"
components:
  button-primary: { backgroundColor: "{colors.ink}", textColor: "{colors.bg}", rounded: "{rounded.md}", height: "36px", padding: "0 14px" }
  button-secondary: { backgroundColor: "transparent", textColor: "{colors.ink}", rounded: "{rounded.md}", height: "36px", padding: "0 14px" }
  tool: { backgroundColor: "transparent", textColor: "{colors.ink-3}", rounded: "{rounded.sm}", height: "28px", padding: "0 8px" }
  tool-hover: { backgroundColor: "{colors.bg-sunken}", textColor: "{colors.ink}" }
  tag: { backgroundColor: "{colors.bg-sunken}", textColor: "{colors.ink-2}", rounded: "{rounded.sm}", padding: "1px 8px" }
  tag-warn: { backgroundColor: "{colors.warn-bg}", textColor: "{colors.warn}" }
  code-block: { backgroundColor: "{colors.bg-sunken}", textColor: "{colors.ink}", rounded: "{rounded.lg}" }
  card-open: { backgroundColor: "{colors.bg-sunken}", rounded: "{rounded.lg}" }
---

# Design System: render-view page

Step 4 of the `ui-process` for the render-view redesign. Status: **approved by the owner**
(2026-11-15). The tokens above and in [tokens.css](tokens.css) are normative; `tokens.css` is the copy
the page uses. The specimen page is [index.html](index.html). Background: [../context.md](../context.md),
[../research.md](../research.md). Chosen direction: "Quiet Studio" with a small amount of signal orange
([directions/c2-quiet-studio-signal.html](directions/c2-quiet-studio-signal.html)).

## Overview

**North Star: "The working document"**

The page is a document first. A reader comes to understand a spec of 1,000–3,500 lines and to answer it.
Everything that is not the text stays quiet: one page surface, no section panels, hierarchy from space,
size and three grey levels. One colour, signal orange, marks where the reader is and what changed.

The reading column is calm and measured. Wide material (tables, code, diffs, diagrams, cards) takes a
wider track and uses the forms readers already know from GitHub and from document sites.

**Key characteristics**

- One surface. Boxes only for code and for an open card.
- Prose at most `--measure` wide: 700px at 16px (about 90–95 characters).
- One typeface family for text and UI; a monospace only for code, IDs and paths.
- One accent. Status colours appear only on status.
- Light and dark are composed separately and both meet the contrast rules below.

## Colors

All colours are semantic tokens written once with `light-dark()`. The theme switch changes only
`color-scheme` on the root element; print forces light.

| Role | Token | Use |
|---|---|---|
| Page | `--bg` | The one page surface |
| Raised | `--bg-raised` | Popover, Respond panel, a control inside a sunken area |
| Sunken | `--bg-sunken` | Code and diff blocks, an open card, inline code, the note, hover on a row |
| Text | `--ink` | Body text and headings |
| Text, second level | `--ink-2` | Metadata, captions, labels, hints |
| Text, third level | `--ink-3` | Low-emphasis tools and separators. Never for content |
| Rule | `--rule` | Decorative dividers (table rows, card rows) |
| Control border | `--border-control` | Borders that define a control: options, segmented control, text area |
| Signal | `--signal` | Current location, link underline and hover, highlighted line, "changed" in a diagram, focus ring, the Respond count |
| Signal background | `--signal-bg` | Text selection |
| Highlight | `--highlight` | Highlighted code line; the flash after a jump |
| Status | `--ok`, `--info`, `--warn`, `--danger` (each with `-bg`) | Tags, diff stat, the wrong step of a failure walk |

Syntax and diff colours are GitHub's current values (Primer Primitives v11.10.0); see `tokens.css`.

**Measured contrast (WCAG 2, both themes)**

| Pair | Light | Dark | Target |
|---|---|---|---|
| `--ink` on `--bg` | 17.2 | 16.4 | 7 |
| `--ink` on `--bg-sunken` | 15.7 | 14.9 | 7 |
| `--ink-2` on `--bg` | 6.9 | 7.8 | 4.5 |
| `--ink-3` on `--bg` | 4.9 | 5.8 | 4.5 |
| `--ink-3` on `--bg-sunken` | 4.5 | 5.3 | 4.5 |
| `--border-control` on `--bg` | 3.6 | 3.9 | 3 |
| `--signal` on `--bg` | 5.5 | 8.8 | 4.5 |
| Status text on its background | ≥ 4.5 | ≥ 4.5 | 4.5 |
| Each syntax colour on `--bg-sunken` | ≥ 4.5 | ≥ 4.5 | 4.5 |

**Named rules**

- **The One Accent Rule.** Signal orange is the only accent. It marks position, change and focus. It is
  never a fill for a large area, and never decoration.
- **The Status Rule.** Green, blue, amber and red mean status only, and always come with a word.
- **The Third Grey Rule.** `--ink-3` is for tools and separators. Anything the reader must read uses
  `--ink` or `--ink-2`.

## Typography

| Role | Token | Size / line height | Weight |
|---|---|---|---|
| Document title | `--text-h1` | 30px / 1.2 | 600 |
| Section (H2) | `--text-h2` | 22px / 1.3 | 600 |
| Subsection (H3) | `--text-h3` | 18px / 1.35 | 600 |
| H4 and deeper | `--text-h4` | 16px / 1.5 | 600 |
| Body | `--text-body` | 16px / 1.6 | 400 |
| UI (navigation, tables, cards) | `--text-ui` | 14px / 1.4 | 400; 500 for emphasis |
| Small (captions, metadata, tags) | `--text-small` | 13px / 1.45 | 400 |
| Code block | `--text-code` | 13.5px / 1.6 | 400 |
| Inline code | `--code-inline-size` | 0.88em | 400 |

- **Families.** Geist for text and UI; Geist Mono for code, IDs, paths, line numbers and times.
- **Measure.** Prose is at most `--measure` (66ch). The `ch` unit is the width of "0", which is wide in
  Geist (0.663em), so 66ch is 700px at 16px and holds about 90–95 characters of text, not 66. The owner
  kept this width (2026-11-15).
- **Headings.** Sentence case, roman, `text-wrap: balance`, tracking −0.015em on H1 and H2. More space
  above a heading than below it.
- **Body.** `text-wrap: pretty`. Paragraphs are separated by space (14px), not indented. No hyphenation.
- **Numbers.** `font-variant-numeric: tabular-nums` in tables, counts and diff stats.
- **Weights.** 400, 500 and 600 only.
- **Emphasis.** Geist has no italic. `*emphasis*` in a doc renders as a browser-slanted roman (owner's
  decision, 2026-11-15).

**Fonts shipped.** Two subsets in [fonts/](fonts/), 34 KB in total (46 KB as base64 in `fonts/fonts.css`):
Latin, Latin-1, punctuation, arrows, `−`, `≤ ≥ ≠`; Geist Mono also has box-drawing characters. Both are
under the SIL Open Font License 1.1 with no reserved font name; the licence texts are beside them. Neither
subset has `✓` or `✗`, so marks are drawn as SVG icons.

**Named rules**

- **The Mono Rule.** Monospace is for code and identifiers. Never for labels, headings or running text.
- **The No-Capitals Rule.** No uppercase labels and no label above a heading.

## Layout

**Shell.** A sticky top bar (`--bar-height`, 56px) and three columns inside `--shell-max` (1440px):

| Column | Width | Content |
|---|---|---|
| Documents | `--nav-width` (208px) | Document list; task files in a collapsible group |
| Main | flexible | The document |
| On this page | `--outline-width` (208px) | Outline of the open document, "Collapse all" |

Columns are separated by `--shell-gap` (72px) of space, not by lines. Both side columns are sticky and
scroll on their own.

**Tracks in the main column.** Prose, headings and lists use `--measure`. Tables, code, diffs, figures,
filters and cards use `--wide` (54rem). A block wider than its track scrolls inside itself.

**Vertical rhythm.** Sections are `--space-9` (88px) apart. A subsection heading has `--space-6` above it.
Blocks inside a section are 14–24px apart.

**Narrow screens.**

| Width | Change |
|---|---|
| Below 1200px | The outline column hides; "On this page" becomes a menu in the top bar |
| Below 860px | The document list becomes a menu too; the main column takes the full width with 16px gutters |

**Print.** Light theme. Top bar, side columns, tools and filters are hidden. Collapsed sections and cards
are printed open. Code wraps.

**Named rules**

- **The Two-Track Rule.** Prose never exceeds the measure; wide material never shrinks to it.
- **The Space-First Rule.** Group with space before adding a line, and add a line before adding a box.

## Elevation & Depth

The page is flat. Depth is shown by tone:

- `--bg-sunken` for things set into the page (code, an open card).
- `--bg-raised` for things above the page (popover, Respond panel) and for controls inside a sunken area.

Only the two floating elements have a shadow: `0 8px 28px rgb(0 0 0 / 0.16)` with a 1px `--rule` border.
Nothing else has a shadow.

## Shapes

| Radius | Token | Use |
|---|---|---|
| 4px | `--radius-sm` | Tags, inline code, tools, pins |
| 6px | `--radius-md` | Buttons, options, segmented control, text areas |
| 10px | `--radius-lg` | Code and diff blocks, open cards, the note, popover, Respond panel |
| Full | — | The theme switch only |

Borders are 1px. A 2px line appears only as a mark of state: the current outline item, a highlighted code
line, a "changed" node in a diagram, and the focus ring.

Icons are inline SVG, 16px, 1.5px stroke, round caps. No emoji and no character glyphs as icons.

**Named rule**

- **The Two-Deep Rule.** At most two levels of surface: the page, and one sunken or raised area on it. A
  card never holds another card.

## Components

The components library (step 5) specifies each component with all its states. The rules it must follow:

- **One of each.** One button shape, one tag shape, one card recipe, one divider, one link look.
- **Buttons.** One primary button per page (Respond). Others are secondary (1px `--border-control`) or
  tools (text only, `--ink-3`, sunken on hover).
- **Section tools** (Comment, Collapse) are always visible at low emphasis and stronger on hover and
  focus. They are never hover-only.
- **Links.** Ink text with a 1px signal underline; signal text on hover. ID links use a dotted underline.
- **Tags.** Sentence case, pale background, dark text, always a word. On a card, only "Needs you" is a
  coloured tag; an answered card shows plain text with a check icon.
- **Tables.** Header in `--ink-2` at weight 500 with a `--rule` line; rows divided by `--rule`; no zebra,
  no vertical lines, no outer box.
- **Code and diff.** Sunken block, a quiet header with the path, line numbers in `--code-line-number`.
  A diff keeps its `+`/`−` column and tinted gutters, so it does not rely on colour.
- **Figures.** A diagram sits on the page with a numbered caption below. Neutral strokes; signal only for
  "changed"; status never by fill alone.
- **Cards.** Full-width rows, never a grid. Closed: one row, sunken on hover. Open: sunken background with
  `--radius-lg`. Several can be open at once.
- **Options.** Vertical, whole label clickable, nothing preselected. "Suggested" is a plain word.
  Exception: a `decisions` exhibit in a spec keeps the doc's recommendation preselected, because the
  Respond text reports "not touched; default kept" (owner, 2026-11-15).
- **States.** Every interactive component defines default, hover, focus-visible, active and disabled.
- **Focus.** `outline: 2px solid var(--signal); outline-offset: 2px`. Never a shadow.
- **Motion.** Only state feedback: `--duration` (150ms) with `--ease`. No entrance animation. With
  `prefers-reduced-motion`, no transitions.
- **Forced colours.** Tags and cards carry a transparent 1px border, so they keep a shape.

## Do's and Don'ts

**Do**

- Keep prose at the measure and let wide material use the wide track.
- Write metadata as one line of text.
- Put the "generated" notice in the footer as plain text.
- Use the signal colour for position, change and focus only.
- Pair every status colour with a word.

**Don't**

- Don't put a section in a panel, or a box in a box.
- Don't add a label above a heading, uppercase labels or letter-spaced text.
- Don't use monospace for anything that is not code or an identifier.
- Don't use a coloured side stripe wider than 1px on a note or a card (a diff gutter is the exception).
- Don't add gradients, glows or shadows to page content.
- Don't show cards side by side.
- Don't rely on hover to show a control.

## Decided points

| Point | Decision | Decided |
|---|---|---|
| Respond placement | One panel that takes the outline's column. Always open on a decision round at 1200px and wider. Below 1200px the panel is an overlay, so it opens on demand and has a close button, also on a round. On demand on other pages | Step 5 and the owner, 2026-11-15 |
| "Show N more" on decision rounds | Show all cards | The owner, 2026-11-15 |
| Prose measure | Keep `66ch` (700px in Geist at 16px) | The owner, 2026-11-15 |
| Copy response | A secondary button; Respond stays the only primary button | The owner, 2026-11-15 |
