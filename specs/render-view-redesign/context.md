# Context — render-view page redesign

Process: `ui-process` skill. Started 2026-11-15. This file is the source of truth for the ask and for
what was agreed in each step. Siblings (added as each step closes): `research.md`, `branding.md`,
`design-system/`, `components/`.

## The ask

Redesign the HTML page that the `render-view` skill generates (`<spec>/.views/view.html`).

| Topic | Agreed with the owner (2026-11-15) |
|---|---|
| Problems to fix | The page looks generic and dated; long specs are tiring to read; navigation and layout feel clumsy |
| Scope | All three page types: spec view, decision round, implementation tour |
| Depth | Visual + layout. Same features, same Respond block format, same exhibit JSON contract |
| Direction | Editorial / document: strong typography, few boxes, calm |
| Fonts | Open-license fonts embedded in the file as base64, so the page works offline |
| Themes | Light + dark, following the OS, plus a manual toggle (the only new feature) |
| Branding | Not needed. Only a small visual identity for the page (name treatment, tone, colour and type character) |
| End point | The components library. Applying the design to the skill's files is a later task |
| Output folder | `specs/render-view-redesign/` |

## What the page is today

Source files, all in `skills/render-view/`:

| File | Role |
|---|---|
| `scripts/render_view.py` | Standard-library build. Parses markdown, writes every HTML fragment and the page shell (`build_page`), draws diagrams as inline SVG |
| `assets/view.css` | All styles, inlined into the page. Tokens on `:root`, dark theme by `prefers-color-scheme` |
| `assets/view.js` | Doc switching, outline tracking, collapse, comments, round answers, tour progress, Respond block, ID popover |
| `references/exhibits.md`, `rounds.md`, `tours.md` | The contracts for exhibits, decision rounds and tours |

Page parts that the design system must cover:

- **Shell:** top bar (generated badge, build info, Collapse all, Respond with count), sidebar (document
  list with a task-file group, outline with illustration dots, build report), main column.
- **Document:** kicker (file name), title, chips, notes block, intro, sections (level 2 and 3) with
  Comment and Collapse tools, comment box.
- **Prose:** paragraphs, lists, blockquote, rule, image, inline code, ID links with a hover popover, code
  links to the editor, tables with status chips, confidence table (bars), implementation headings
  (create / modify / delete marks).
- **Code:** code block with line numbers, highlighted lines and pins; diff block with hunks and +/−
  counts; text diagram block; syntax token colours.
- **Exhibits:** frame (tag, source, stamp, stale state, title, caption), and the types `claims`, `flow`,
  `tree`, `states`, `graph`, `sequence`, `walk`, `timeline`, `code`, `diff`, `decisions`.
- **Decision round:** round head, premise cards (confirm / needs correction), decision cards (headline,
  tags, state chips, fields, uses, failure walk, recorded answer, options form), filters, bulk accept,
  show more, Respond column (live block, count, copy, clear), "Built from" panel.
- **Tour:** step sections (previous / next, Reviewed, Comment), change-set table, coverage panel
  (repositories, folders, files, status marks, +/−, step links, "Not in any step" filter).
- **Overlays:** Respond dialog, ID popover, flash highlight on navigation.
- **Other:** print styles, focus states, reduced motion.

## What is wrong with it

Seen on three real built views (a spec view, a decision round and a tour; private, not in this repo) at
1440 px, light theme:

1. **Boxes inside boxes.** Each section is a bordered panel; tables, exhibits, code and sidebar panels
   are boxed again inside it. Nothing stands out.
2. **Lines are too long.** Body text runs about 140–150 characters per line.
3. **The top of a doc is heavy.** A chip row (some chips hold a full sentence) and a large blue notes
   box come before the content.
4. **Sidebar.** The document list and the outline are two small scrolling panels; long file names
   overflow and cause a horizontal scrollbar.
5. **Top bar.** The "GENERATED VIEW · DO NOT EDIT" badge has the most prominent place.
6. **Decision round.** Three columns (sidebar, cards, Respond) squeeze the cards.
7. **Exhibits and code.** Every exhibit has the same amber tint; dark code and diff blocks are heavy on
   the light page.
8. **Font.** The CSS names IBM Plex but ships no font, so the page shows the system font.

## Constraints

- One self-contained HTML file. Standard-library Python build. No network requests.
- Repeated items (premises, decisions, steps, findings) are full-width collapsible cards, never
  side-by-side grids.
- Print styles, keyboard focus and `prefers-reduced-motion` stay supported.
- Pages reach 1–4 MB with 150–200 sections and 70–360 tables, so the design must stay light to render.
- This repo is public: artifacts here use synthetic sample content only.

## Open items

- The current page was checked at one desktop width and in light theme only. Dark theme and narrow
  widths are checked during the design system step.

## Step log

| Step | Status | Result |
|---|---|---|
| 1. Context | Done 2026-11-15 | This file |
| 2. Research | Plan sent for approval | — |
| 3. Branding | Agreed: not needed, small visual identity only | — |
| 4. Design system | — | — |
| 5. Components library | — | — |
