# Collected — B · Document layouts and editorial inspiration (Q2, Q8)

Agent output, verbatim. Collected 2026-11-15. Model: Opus 5.5. One closing line about the research
tool's account credits (with a billing link) is left out; it is not research content.

---

I studied 20 doc sites and 16 editorial sites, mostly from their real CSS and from 1440×900 screenshots I took. Dribbble, Pinterest and SiteInspire blocked me.

**Short answer:**
- **Shell:** the best doc sites use one plain page surface and a prose column of about 40–48rem. Documents go on the left and the in-page outline on the right. Wide items get a wider column of their own.
- **Section tools and metadata:** section tools are hidden until hover. Page metadata is one line of plain text, not chips.
- **Respond:** none of the sites adds a third content column for an action panel. They use a popover, a drawer that replaces a column, or a bar that floats at the bottom.

## Q2 findings

Widths come from each site's CSS unless I write "est." (estimated from the screenshot at 1440px).

**Stripe docs**
- **Shell:** two-row top bar (search row, then product tabs; ~112px). Left nav ~280px, content ~815px, right "ON THIS PAGE" ~230px (est.).
- **Under the title:** a row of small text actions ("Ask about this page · Copy for LLM · View as Markdown") with thin dividers and a hairline below. These are links, not buttons.
- **Callout:** a grey left rule with a small bold title and no fill.
- **Long outline labels:** they wrap. The active item is blue text, and child items sit beside a hairline.

**Linear docs**
- **Shell:** 64px top bar with breadcrumb, a sun-icon theme toggle at the top right and a "Copy page" split button. Left nav ~280px, content ~650px (est.).
- **Outline:** at least 250px wide and hidden at ≤1024px. It has a thin left line, and the active item gets brighter text and a bright segment on that line.

**Linear changelog**
- The date and a timeline dot sit in a left column, and the title and body sit in the main column. There are no cards; a hairline separates the header from the content.

**Vercel docs / Geist**
- **Shell:** left nav 300px (active item is a grey filled pill), outline 240px.
- **Long labels:** the outline truncates them with an ellipsis. "Copy page" sits above the content.
- **Boxes:** code blocks and diagrams are boxed, with a filename header on code.
- **Fonts:** Geist Sans and Geist Mono (from Vercel's CSS).

**Tailwind CSS docs**
- **Shell:** 3.5rem header. Left nav 18rem, prose about 42rem, outline 18rem shown only at the xl breakpoint.
- **Labels:** small uppercase, letter-spaced eyebrows ("FLEXBOX & GRID", "ON THIS PAGE").
- **Tables:** bold header, hairline row rules, no zebra, no vertical lines.
- **Outline:** left hairline, and a black bar marks the active item. Decorative hatched gutters mark the column edges.
- **Fonts:** Inter and IBM Plex Mono.

**Tailwind Plus Syntax**
- Light/dark icon at the top right. The left nav has a dot marking the active page, and the right "On this page" uses an accent colour for the active item.

**Tailwind Plus Protocol**
- The active doc in the left nav is a tinted group with a green left bar. Its in-page sections are nested under it, so docs and outline share one column.

**Tailwind Plus Commit**
- A changelog: the date sits on the column edge with a tick mark, and the content is in a single column.

**Tailwind Plus Spotlight**
- An article with one centred ~670px column and no sidebars. The date has a small left rule. Theme toggle is a round button at the top right.

**Starlight**
- **Shell:** nav 3.5–4rem, sidebar 18.75rem, content 45rem, line height 1.75. The right outline appears only at ≥72rem.
- **Narrow screens:** a 3rem "On this page" bar sits under the header, and the sidebar becomes a full-width overlay.
- **Anchor links:** hidden until hover, but only on devices that can hover (`opacity:0` inside `@media (hover:hover)`).
- **Tables:** `display:block; overflow:auto`, so they scroll sideways.
- **Asides:** 0.25rem left border plus a tinted background.
- **Active nav item:** filled with the accent colour and inverted text.
- **Theme:** an "Auto/Light/Dark" select in the header.

**MDN**
- **Shell:** grid with sidebars at least 15rem, 2rem gaps, content 31–48rem. Navigation 2.9–4.1rem plus a 2rem breadcrumb bar, which holds the "Theme" control at the right.
- **Navigation:** the left nav uses `<details>` groups and `overflow-wrap:anywhere`. In the right "In this article", the active item gets a 2px left shadow and a tint.
- **Anchors:** a "#" that shows only on hover or focus.
- **Callouts:** 2px left border, soft background, icon.
- **Tables:** full grid borders, zebra rows.
- **Fonts:** Inter and JetBrains Mono.
- **Footer:** a "last modified" line.

**GitHub Docs**
- **Shell:** header 3.5–4rem, left nav 326px.
- **Grid:** content 500–785px. The "In this article" column (326px) shows only at ≥1400px, or ≥1074px when the left nav is collapsed.
- **Navigation:** the active nav item has a green bar and a grey fill. Long outline labels use `overflow-wrap:anywhere`, the active outline item turns semibold, and an "Up next" link sits under the outline.
- **Tables:** bold header with hairline rows.
- **Copy markdown:** a quiet pill button under the title.

**Primer**
- NavList with group headings. It separates `aria-current="page"` (the current page) from `aria-current="location"` (the current place on a page). That split maps exactly to doc list vs outline.

**Fumadocs**
- The page sits in one rounded panel on a grey canvas; page width 760px and outline 19rem (from Tailwind classes). On mobile the outline becomes a popover bar.

**Mintlify**
- **Shell:** content 40.5rem, sidebar 14–18rem. A green dot marks the active outline item.
- **"Ask a question" bar:** fixed at the bottom centre of the content column.

**Nextra**
- **Headings:** H2s have a bottom border.
- **Under the outline:** "Question? Give us feedback / Edit this page" links.
- **Sidebar foot:** the theme select ("System") and a collapse-sidebar button.
- **Ask AI:** a floating button at the bottom right.

**Tufte CSS**
- **Layout:** body 87.5% wide with 12.5% left padding; prose 55% wide; sidenotes float in the right margin at 50% width.
- **Colours and type:** background `#fffff8` and ET Book serif. Dark mode is automatic only, through `prefers-color-scheme` (`#151515` / `#ddd`), with no toggle.
- **Wide items:** `figure.fullwidth` and `table.fullwidth` take the full width.
- **Narrow screens:** below 760px, sidenotes turn into tap toggles.

**Distill**
- **Width classes:** a ladder of `l-body` → `l-middle` → `l-page` → `l-screen`, each with an "-outset" variant.
- **Byline:** author, date and citation in columns split by vertical hairlines. Large figures break out wider than the text.

**Furo**
- **Shell:** sidebar at least 15em, content 46em including padding, outline 15em. On small screens both become off-canvas drawers.
- **Icons:** view-source, edit and theme icons sit at the top right of the content. The theme toggle cycles Light/Dark/Auto.
- **Admonitions:** coloured left bar, tinted title band, shadow.
- **Tables:** shadow plus header tint.

**Apple developer docs**
- **Shell:** a wide left nav with a filter field at the bottom, and no right outline.
- **Above the title:** a grey "Protocol" eyebrow.
- **Under the title:** availability as one text line split by pipes ("iOS 13.0+ | iPadOS 13.0+ | …"), not chips.
- **Sections:** separated by a hairline and a large heading.

**shadcn docs**
- Sidebar 18rem and header 3.5rem (from classes). I did not analyse it further.

### Recurring patterns
1. **One surface, no section panels.** Sections are separated by space and heading size, sometimes with a hairline (Nextra H2 border, Apple rule). Boxes stay only for code, interactive demos and figures, and some sites (Paco, Tufte) do not even box code.
2. **Measured prose column of ~40–48rem**: Starlight 45, MDN max 48, Furo ~40 of text, Tailwind ~42, Mintlify 40.5, GitHub ≤785px.
3. **Left = documents, right = "On this page".** Each has its own scroll, and the right one is the first thing to hide on narrow screens (≤1024–1400px). It then becomes a top dropdown (Starlight, Fumadocs) or a drawer (Furo).
4. **Active item is quiet:** a 2px left bar, a tint, or bold/brighter text. Only Starlight uses a full accent fill.
5. **Long labels wrap** (`overflow-wrap:anywhere` on MDN, GitHub, Starlight). Vercel truncates instead.
6. **Section actions show on hover/focus only** (Starlight, MDN). Page-level actions ("Copy page") are quiet text or ghost buttons near the title.
7. **Callouts = coloured left rule** (2–4px) with an icon and a faint tint or no fill. Colour stays on the rule and icon.
8. **Tables = horizontal hairlines and a bold header, no zebra** (Tailwind, GitHub). Wide tables scroll inside their own block.

**Where they disagree:**
- **Long labels:** truncate (Vercel) or wrap (most sites).
- **Table style:** full grid and zebra (MDN, Furo) or hairlines only.
- **Doc list and outline:** in separate columns, or the outline nested under the active doc in the left nav (Protocol).
- **Theme control:** in the header (Linear, Starlight, MDN), the sidebar foot (Nextra) or the content corner (Furo).
- **Theme states:** Furo and Starlight offer three (light/dark/auto); Tufte has automatic dark mode only and no toggle.

### Specific answers
- **Where to put "Respond":**
  - *Precedents:*
    - GitHub PR review: comments stay pending and visible only to you. A "Review changes" button above the diff opens a popover with a summary box and Comment / Approve / Request changes, then "Submit review".
    - Google Docs: the comments panel opens from "Show all comments" at the top right and can shrink to margin icons.
    - Notion: comments sit in the right margin, as full comments by default or as icons in "Minimal" mode. A comments pane opens from an icon at the top, with a red dot for unread comments.
    - Linear documents: inline comments, and "Show resolved comments" at the top right.
    - Mintlify and Nextra: an assistant input fixed to the bottom of the content column (Mintlify) or a floating button (Nextra).
  - *My inference:* use a top-bar "Respond (n)" button that opens a right drawer. The drawer takes the outline's column instead of adding a column. When it is open, move the outline into the left nav, nested under the active doc as in Protocol. Below ~1200px the drawer overlays the content.
- **"Generated, do not edit" notice:**
  - Go uses a one-line comment convention: `// Code generated … DO NOT EDIT.`
  - GitHub marks generated files with `linguist-generated` and hides them in diffs by default.
  - Kubernetes puts "Create an issue (auto-generated page)" in its page actions. Its footer says the page is auto-generated and the fix may belong elsewhere.
  - So the convention is quiet text in the footer or margin, not a badge.
- **Collapsing long sections:**
  - On desktop, none of the editorial or doc sites I looked at collapse body sections (my observation). Nav groups collapse everywhere.
  - Precedents for collapsing: Wikipedia mobile, through the MobileFrontend extension, and GitHub's "Viewed", which collapses a reviewed file.
  - GOV.UK says to use accordions only with evidence, and never for content all users need. NN/g says accordions lower visibility and raise interaction cost.
  - So: expanded by default, and collapse is an opt-in tool.

## Q8 findings

**Long-form and editorial sites**
- **Stripe Press:** charcoal `#2f2f2f`, Ivar Display/Text serif, ivory text. A column of small dash ticks on the left edge acts as a minimal section index.
- **Increment:** grey `#f2f2f2` with a coral accent (~`#f5684d`). Issue and date sit in thin ruled boxes; heavy serif headlines and letter-spaced caps for names.
- **Linear Method:** near-black `#08090a`, a big serif display headline over an Inter body, a small caps eyebrow.
- **Linear changelog:** a date column with a timeline dot.
- **Vercel blog:** `#fafafa` background, Geist font. Date, read time and Copy sit as plain text in a right margin column.
- **Anthropic research:**
  - *Colours and fonts:* ivory `#faf9f5`; its own serif for body, sans for headings, a mono face.
  - *Left column:* a numbered outline ("01 Safety first") with hairline rows.
  - *Right column:* metadata as a two-column list with hairlines (Published / Team).
- **Works in Progress:** pink-tinted paper `#fff7f4`, Editor serif body, GT America Mono for all metadata. Hairline rules everywhere, a Swiss-style grid, a big standfirst (intro paragraph).
- **Maggie Appleton:**
  - *Colours and fonts:* `#f6f5f1`, Canela Deck/Text serif with Lato.
  - *Header:* tags as coloured text links (no chips) and "Planted / Last tended" dates on the right, under a hairline.
  - *Outline:* a minimap of dashes in the left margin.
- **iA Writer:** `#f9f9f9`, iA Writer Mono/Sans/Serif families, focus-mode text.
- **Rauno Freiberg:**
  - *Colours and font:* `#fcfcfc`, a custom grotesk (font-face named "X") and JetBrains Mono.
  - *Navigation:* the outline is plain grey text with no rules, section headings are grey at body size, and a segmented scroll indicator at the top marks the current part in yellow `#ffff02`.
- **Paco Coursey:** white, Söhne/Newsreader/Inter. Code is unboxed indented mono; title and date are plain text.
- **Frank Chimero:** split screen with a dark `#3d4340` nav panel and a `#eee` page, monospace body.
- **Fonts only (from CSS, no screenshot):** The Pudding uses Tiempos Text, Atlas Grotesk, Atlas Typewriter and Gooper. The Browser Company uses EB Garamond, Inter, Source Serif Pro, Ivar Text and ABC Diatype Mono. Are.na uses its own sans "areal". Robin Rendle uses "MD UI" / "MD IO".

**Galleries**
- Dribbble returned an empty 202, Pinterest only a JS shell, and SiteInspire a 429 (rate limit), so I got nothing from them.
- Godly and Awwwards loaded, but they list motion-heavy agency sites with little relevance.
- Tailwind showcase lists brands only.

### Proposed visual directions

**A. "Paper & Ink" (scholarly)**
- **Mood:** a printed technical report: warm paper, serif reading text, notes in the margin. Calm and slow-reading.
- **Palette:**
  - *Light:* paper `#faf9f5`, ink `#1f1e1d`, accent oxblood or deep blue.
  - *Dark:* `#262624` / `#2f2f2f` with ivory `#ece9e1` text.
- **Type:** serif body (Charter or Source Serif). Sans for tables, outline and UI. Mono: JetBrains Mono, Cascadia Code or ui-monospace.
- **Sections and figures:** big serif H2 with a number in the margin ("01"), a hairline above, and no panels. Figures are unboxed with a small sans caption and break out to page width. Metadata goes in a right-margin two-column list.
- **Draws on:** Tufte, Anthropic research, Stripe Press, Distill.
- **Risk:** serif next to dense tables and diffs looks mixed, so tables must be sans with tabular numbers. Serif fallbacks on Windows vary, and thin serifs are weak in dark mode.

**B. "Swiss Ledger" (structured)**
- **Mood:** a magazine-grade ledger: neutral paper, one strong accent, mono labels, full-width hairlines. Crisp and orderly.
- **Palette:**
  - *Light:* `#fdfdfc` with near-black ink and a coral or signal accent (~`#f5684d`).
  - *Dark:* `#111` with `#e8e8e6` text and the same accent.
- **Type:** grotesk sans body (Inter or Geist). Mono, uppercase and letter-spaced for eyebrows, IDs, status and dates.
- **Sections and figures:** a hairline across the full width at each H2. A left meta column holds the section number, IDs and status. Tables use hairlines only.
- **Draws on:** Works in Progress, Increment, Linear changelog, Tailwind docs.
- **Risk:** many rules can become "boxes made of lines". Mono labels are harder to read for non-native readers, and the meta column needs a wide screen.

**C. "Quiet Studio" (dark-first, minimal)**
- **Mood:** a precise product-team tool: hierarchy comes only from grey levels and spacing, with almost no lines. Feels fast and modern.
- **Palette:**
  - *Dark:* `#08090a`.
  - *Light:* `#fafafa`.
  - *Both:* a 3-step grey text ramp and one highlight (for example, yellow on the active outline item only).
- **Type:** Geist or Inter for body, Geist Mono for code.
- **Sections and figures:** separated by spacing only. Code is unboxed or on a very slight tint. Navigation is grey text with a brighter active item.
- **Draws on:** Linear docs and Method, Vercel and Geist, Rauno, Paco.
- **Risk:** low-contrast greys tire the eye over 3,000 lines. Long dark tables get muddy, diff colours need care in dark mode, and the look can feel generic.

## What this means for render-view
1. **(1 boxes)** Use one page surface and remove the H2 panels. Separate sections with 3–4rem of space, a stronger H2 and an optional hairline. Keep a tint (no border) only for code and diagrams.
2. **(1 tables)** Tables get a bold header, horizontal hairlines, no zebra and no outer box. Wide tables scroll inside their own block, as in Starlight.
3. **(2 line length)** Set prose to `max-width` 42–46rem (about 70 characters). Give tables, code, diffs and SVG a wider "page" track using a Distill-style width ladder, not the prose width.
4. **(3 top of page)** Use an eyebrow (doc type), the title, a one-line summary, then one muted metadata line (Apple pipes) or a right-margin list (Anthropic, Vercel blog). Remove the chip row.
5. **(3 notes)** Turn the big blue notes callout into a left-rule note (Stripe or MDN style) under the metadata, or a one-line disclosure.
6. **(4 sidebar)** Left = documents only, with `aria-current="page"` and the task group as `<details>`. Right = outline with `aria-current="location"` and scroll-spy, shown only at ≥~1200px. Below that it becomes an "On this page" dropdown under the top bar.
7. **(4 long names)** Wrap file names with `overflow-wrap:anywhere` rather than truncating. Show the doc title first and the file name in muted small text. Keep the illustration dot as a small glyph after the outline label.
8. **(5 top bar)** Keep it 56–64px: doc title or breadcrumb on the left; theme toggle (light/dark/auto) and "Respond (n)" as the only filled button on the right. Move "Collapse all" into the outline header as a text link.
9. **(5 generated notice)** Replace the "DO NOT EDIT" badge with quiet text: "Generated from `<path>` — edit the markdown" in the footer or meta line, as Kubernetes, Go and MDN do.
10. **(6 Respond)** Use no third column. Respond opens as a right drawer that takes the outline's place (outline moves under the active doc in the left nav, as in Protocol), and it overlays below ~1200px. Pending comments work like a GitHub review: collected, then submitted with a summary.
11. **(7 section tools)** Show Comment, Collapse and anchor on heading hover or focus only, and always on touch devices (Starlight's `hover:hover` rule). Place them after the heading text or in the left gutter.
12. **(collapse)** Expand all sections by default. Treat collapse as a reader tool, as in GitHub's "Viewed", not as the default state.

## Sources
All checked 2026-11-15. Screenshots taken at 1440×900. Where a font or width is listed, it comes from that site's CSS.

**Doc sites**
- docs.stripe.com/payments/accept-a-payment
- linear.app/docs/projects
- linear.app/changelog
- linear.app/docs/comment-on-issues
- linear.app/docs/project-documents
- vercel.com/docs/functions
- tailwindcss.com/docs/flex
- syntax.tailwindui.com
- protocol.tailwindui.com
- commit.tailwindui.com
- spotlight.tailwindui.com/articles/crafting-a-design-system-for-a-multiplanetary-future
- starlight.astro.build/getting-started/
- starlight.astro.build/guides/customization/
- developer.mozilla.org/en-US/docs/Web/CSS/grid (redirects to …/Reference/Properties/grid)
- docs.github.com/en/get-started/start-your-journey/about-github-and-git
- docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request
- docs.github.com/en/repositories/working-with-files/managing-files/customizing-how-changed-files-appear-on-github
- primer.style/product/getting-started/
- primer.style/product/components/nav-list/
- primer.style/product/components/banner/
- fumadocs.dev/docs
- mintlify.com/docs/quickstart
- nextra.site/docs
- edwardtufte.github.io/tufte-css/ (and its tufte.css)
- distill.pub/2017/momentum/
- distill.pub/guide/
- pradyunsg.me/furo/reference/admonitions/
- pradyunsg.me/furo/reference/tables/
- pradyunsg.me/furo/customisation/
- developer.apple.com/documentation/swiftui/view
- ui.shadcn.com/docs/components/accordion

**Comment, notice and collapse precedents**
- support.google.com/docs/answer/65129
- notion.com/help/comments-mentions-and-reminders
- design-system.service.gov.uk/components/accordion/
- nngroup.com/articles/accordions-on-desktop/
- pkg.go.dev/cmd/go
- mediawiki.org/wiki/Extension:MobileFrontend
- kubernetes.io/docs/reference/kubectl/generated/kubectl_apply/
- kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/

**Editorial sites**
- press.stripe.com/an-elegant-puzzle
- increment.com/documentation/
- linear.app/method
- vercel.com/blog/death-to-long-lived-static-credentials
- anthropic.com/research/building-strong-safety-evaluations
- worksinprogress.co/issue/advancing-antivenom/
- maggieappleton.com/garden-history
- ia.net/writer
- rauno.me/craft/interaction-design
- paco.me/writing/disable-theme-transitions
- frankchimero.com/blog/2015/the-webs-grain/
- robinrendle.com (fonts only)
- pudding.cool (fonts only)
- thebrowser.company (fonts only)
- are.na/about (fonts only)

**Fetched but little or no usable data**
- tailwindcss.com/showcase: brand list only.
- godly.website and awwwards.com/websites/editorial/: not editorial-specific.
- openai.com/research, craft.do, radix-ui.com: fetched, not analysed.
- notion.com/help/create-a-table-of-contents: 404.

**Not reachable**
- dribbble.com search: empty 202 response.
- pinterest.com search: JS shell, no results.
- siteinspire.com: 429 rate limit.

## Confidence
- **Confidence score: 82%.** Layout numbers, fonts and colour samples come from real CSS, HTML and screenshots, and the patterns repeat across many sites.
- **18% uncertainty:**
  - Widths are CSS values, not measured rendered widths. Stripe, Linear and Apple widths are estimates from one 1440px screenshot.
  - Hover, scroll-spy and mobile behaviour come from CSS rules. I did not see them working; the screenshots are static and desktop-only.
  - Fonts are named from `@font-face` and CSS variables, so a declared face may not be the one shown.
  - The gallery sites (Dribbble, Pinterest, SiteInspire) gave no data, so the Q8 set is curated, not "trending".
  - Notion and Craft page layouts, Read the Docs' classic theme, Diataxis sites and OpenAI were not checked visually.
  - The three directions, the Respond-drawer design and the 1200px breakpoint are my design suggestions, not observed facts.
