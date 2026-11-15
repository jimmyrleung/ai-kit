# Components library — render-view page

Step 5 of the `ui-process`. Status: **approved by the owner** (2026-11-15); the three points left open were decided the same day (see "Decided points"). Built on the approved
design system: [../design-system/DESIGN.md](../design-system/DESIGN.md) and
[../design-system/tokens.css](../design-system/tokens.css).

| File | What it is |
|---|---|
| [index.html](index.html) | The library: every component with its variants, in both themes |
| [page.html](page.html) | A full test page: shell, document, decision round and the Respond panel, with a switch for the Respond point below |
| [components.css](components.css) | The styles. With `tokens.css` and `fonts/fonts.css`, this is the candidate replacement for `skills/render-view/assets/view.css` |

Open the HTML files in a browser. Sample content is made up ("invoice reminders").

## How to read the class names

Class names follow today's page (`skills/render-view/scripts/render_view.py`) wherever the element stays,
so the later implementation changes little markup. The "Markup change" column says what the build script
must output differently.

## Shell

| Component | Classes | Markup change from today |
|---|---|---|
| Top bar | `.topbar`, `.spec` | The "GENERATED VIEW" badge and the build text are removed (see Footer). "Collapse all" moves to the outline column. New: theme switch, and a Contents menu for narrow screens |
| Theme switch | `fieldset.theme` with three radios | New. Stores `rv-theme` in `localStorage`; a script in `<head>` applies it before the styles |
| Contents menu | `details.menu`, `.menu-body` | New. Holds the outline, and the document list below 860px. Shown below 1200px, or when Respond is open |
| Document list | `nav.side`, `ul.docs`, `a.doclink` | The panel boxes are removed. The active link gets `aria-current="page"`. The file name is no longer shown beside the label |
| Outline | `nav.rail`, `ol.outline`, `li.lvl2` / `li.lvl3` | Moves from the left sidebar to its own right column. The link in view gets `aria-current="location"` (today: class `active`) |
| Layout | `.layout` | Three columns (was two). `body.respond-open` gives the third column to the Respond panel |
| Footer | `footer.doc-foot` | New place for the generated notice, build time, document count and the build report (`details`) |

## Document

| Component | Classes | Markup change from today |
|---|---|---|
| Document head | `header.doc-head`, `h1`, `p.doc-meta` | The kicker above the title is removed. The chip row becomes one metadata line of `<span>`s; the file name is its first item |
| Notes | `aside.note` | Replaces `.doc-notes` and its label |
| Section | `section.sec.lvl2` / `.lvl3`, `.sec-head`, `.sec-tools`, `.sec-body` | Same structure. The panel around level-2 sections is gone |
| Section tools | `button.tool` | Same buttons. Collapse uses `aria-expanded` on the button, as today |
| Comment box | `.comment-box` | Same |
| Implementation heading | `.impl`, `.mark.create` / `.modify` / `.delete`, `.impl-action` | Same |
| Prose | `p`, `ul`, `ol`, `blockquote`, `hr`, `img`, `h4`–`h6`, `code` | Same |
| Links | `a`, `a.idref`, `a.code-ref` | Same |
| Popover | `.popover`, `.pop-src` | Same. Behaviour to add: show after 0.3–0.5 s, stay open while hovered, close with Escape |

## Tables and code

| Component | Classes | Markup change from today |
|---|---|---|
| Table | `.tbl > table` | Same. Number columns can take `class="num"` |
| Status tag | `.tag`, `.tag.ok` / `.info` / `.warn` / `.danger`, `.tag.topic` | Replaces `.chip` and the old amber `.tag`. `.chip.neutral` becomes a plain `.tag` |
| Confidence table | `.confidence`, `.conf-row`, `.conf-bar` | Same |
| Code block | `figure.codeblock`, `.cl`, `.ln`, `.lc`, `.cl.hl`, `.pin.tone-*` | Same |
| Diff block | `figure.codeblock.diffblock`, `.dl.add` / `.del` / `.ctx` / `.hunk`, `.sg`, `.diffstat` | Same |
| Text diagram | `figure.codeblock.diagram` | Same |
| Syntax tokens | `.tk-kw`, `.tk-str`, `.tk-com`, `.tk-num`, `.tk-fn`, `.tk-ty` | Same |

## Illustrations (exhibits)

| Component | Classes | Markup change from today |
|---|---|---|
| Frame | `figure.exhibit`, `.ex-title`, `figcaption.ex-caption`, `.ex-meta` | The tinted panel and the "Illustration" tag row are removed. The caption moves below, starts with "Figure N.", and carries the source and stamp in `.ex-meta`. A stale exhibit shows a `.tag.warn` in the caption |
| Diagrams | `svg.dg` with `.node`, `.edge`, `.elabel`, `.actor`, `.msg`, `.life`, `.note`, `.divider`, `.fail`, marks `.m-new` / `.m-changed` / `.m-shared` / `.m-removed` / `.m-same` | Same SVG output. Labels are 14px (were 13px), so the build's text-width estimate needs the new size. A new sequence message should start its text with "+" |
| Diagram extras | `.dg-notes`, `.dg-legend`, `details.dg-text` | Same |
| Claims | `ol.claims` | Same |
| Flow | `ol.flow`, `.step.k-key` / `.k-new` / `.k-end`, `.box`, `.exit` | Same. Step numbers are drawn by CSS |
| Tree | `.tree`, `.node.m-*`, `.mark-chip` | Same |
| Failure walk | `ol.walk`, `li.wrong`, `.when` | The wrong step's text starts with "Wrong outcome." in `<b>` (today the words are in the time label) |
| Timeline | `ol.timeline`, `.t-dot`, `.tone-warn` / `.tone-ok` | Same |
| Decisions in a spec | `fieldset.decision`, `label.opt` | Same. The "suggested" chip becomes `span.suggested`; the option note becomes `span.hint` |

## Decision round

| Component | Classes | Markup change from today |
|---|---|---|
| Round | `.round`, `.round-label`, `.round-label-row` | The two-column `.round-main` / `.round-side` wrapper is removed; the Respond column becomes the page-level Respond panel |
| Filters | `.filters`, `.seg` (state views), `.btn[aria-pressed]` (topic filters), `.status` | State filters move into one segmented control. New: a `role="status"` line "Showing N of M" |
| Card | `details.card`, `summary`, `.cid`, `.c-headline`, `.c-state`, `.c-body` | The summary gets an SVG caret as its first child (today a CSS triangle). The "Suggested: …" text leaves the summary |
| Card state | `.tag.warn` "Needs you", `.c-answer`, `.c-answer.yours` | An answered or decided card shows text with a check icon, not a chip. Topic tags are `.tag.topic`, at most two in the summary |
| Card body | `dl.c-fields`, `ol.walk`, `.c-recorded`, `.c-label`, `fieldset.rdecision`, `.c-foot` | Fields become one `dl` (today one `div` per field). "Uses" is a row of that list |
| Premise card | `details.card.premise`, `.p-actions` | Same |
| Options | `label.opt`, `.opt-label`, `.suggested`, `.hint` | See "Decisions in a spec" |

## Respond

| Component | Classes | Markup change from today |
|---|---|---|
| Respond panel | `aside.respond-panel`, `.respond-head`, `.respond-progress`, `.respond-actions`, `pre.live`, `.respond-status`, `.built` | One panel replaces both the floating dialog and the round's side column. It shows the live response on every page type |
| Clear confirmation | `.confirm` | Replaces the "click again to clear" button text |

## Tour

| Component | Classes | Markup change from today |
|---|---|---|
| Step section | `section.sec[data-step]`, `.is-reviewed` | Same. The Reviewed tool gets a check icon |
| Coverage panel | `.coverage`, `.cov-repo`, `.cov-head`, `details.cov-dir`, `table.cov`, `.st-*` | The repository box is removed. The two filter buttons become a segmented control |

## States

Every interactive component has these states in `components.css`:

| Component | Default | Hover | Focus | Active or pressed | Disabled |
|---|---|---|---|---|---|
| `.btn` | Outline | Sunken fill | Signal ring | Darker fill; `aria-pressed` gives an ink fill | Grey text and border |
| `.btn.primary` | Ink fill | Lighter ink | Signal ring | — | — |
| `.tool` | Grey text | Sunken fill, ink text | Same as hover, with ring | `aria-pressed` gives green text | — |
| `.seg button` | Grey text | Sunken fill | Ring inside | Ink fill | — |
| `.doclink`, outline link | Grey text | Sunken fill, ink text | Signal ring | Current: sunken fill, or the signal mark | — |
| `.card > summary` | Plain row | Sunken fill | Signal ring | Open: sunken card, caret turned | — |
| `.opt` | Control border | Ink border | Signal ring on the whole option | Checked: 2px ink border | — |
| Diagram node | Control border | Ink border; outgoing lines turn signal | Signal border | — | — |

## Responsive and other modes

| Mode | Behaviour | Checked |
|---|---|---|
| 1200px and wider | Three columns | Yes, on the built page at 1920px, both themes |
| 860–1199px | The outline column hides; Contents menu appears; Respond opens as an overlay panel, on demand also on a round | Yes, in a 1000px iframe, including the Respond overlay |
| Below 860px | The document list moves into the Contents menu; card summaries wrap; tables scroll inside their block | Yes, in a 390px iframe on all five fixture documents; no page-level horizontal scroll |
| Dark theme | Composed tokens | Yes, on the built page |
| Print | Chrome hidden, everything expanded, code wraps | Not tested in a real print preview (the browser tool cannot print). Checked as screen rules plus the `beforeprint` handler: chrome hidden, collapsed sections, filtered cards and closed `details` open, code wraps, light scheme with `data-theme="dark"` |
| Reduced motion | No transitions | Not tested in the real mode (the tool cannot set it). Checked as a screen rule: transition duration `0s` on `.btn`, the caret and a flashed card |
| Forced colours | Borders on tags, cards, options and code | Not tested in the real mode (the tool cannot set it). Checked as a screen rule: 1px borders on tag, card, option, code block and note; the current outline link is underlined |
| More contrast | Stronger greys and borders (in `tokens.css`) | Not tested in the real mode (the tool cannot set it). Checked as a screen rule: `--ink-2`, `--ink-3`, `--rule` and `--border-control` take the stronger values |

## One-of-each check

| Item | Result |
|---|---|
| Button shapes | One (36px, 6px radius); a tool is text only |
| Tag shapes | One |
| Card recipes | One |
| Dividers | One (1px `--rule`) |
| Link looks | One, with a dotted variant for IDs |
| Surface depth | Two at most. A code block or a "Recorded" block inside an open card uses the page colour, so it is not a third level |
| Accent uses | Position, change, focus, link underline, the Respond count |

## Decided points

Decided by the owner on 2026-11-15, at the start of the implementation round.

| Point | Decision |
|---|---|
| Respond on a decision round | Always open on a round at 1200px and wider (the reader is there to answer), on demand on other pages. Below 1200px the panel is an overlay that would cover the cards, so on a round it also opens on demand and has a close button. `page.html` has a switch that shows both |
| "Show N more" on rounds | Show all cards. The limit of 12 and the "Show N more" button are removed: a closed card is one row, and find-in-page and "Next unanswered" then need no special case |
| Bulk accept | It still applies at once, and the Respond status line gets an "Undo" |
| Copy response | A secondary button. Respond in the top bar is the only primary button (decided after the task review) |

## Not in this library

- The library and `page.html` show the look and the states. The behaviour (scroll tracking, filtering,
  answering, the Respond text, the theme switch, the Contents menu, the popover timing) is in
  `skills/render-view/assets/view.js`.
- `skills/render-view/assets/view.css` is the live stylesheet: `design-system/tokens.css` followed by
  `components.css`, with a few rules added while applying the design. `components.css` stays here as the design
  record.
- No full test page for a tour or a plain spec; their parts are in the library page. The synthetic fixture in
  `../fixture/` builds all three page types.
- The fonts, licence texts and the measured contrast are in `../design-system/`.
