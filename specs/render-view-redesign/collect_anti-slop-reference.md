# Collected — E · Anti-slop reference: taste-skill and impeccable (Q9)

Agent output, verbatim. Collected 2026-11-15. Model: Opus 5.5.

---

## taste-skill

**Main finding:** on `main` today, taste-skill is a kit for building company marketing websites. It is not a general design reference, and the "dials" your process may mention are no longer in this repo.

**1. What it is**
- One skill, install name `design-taste-frontend`, version "tasteskill 2.5.1". It is a full rebuild released 2026-11-05 (2.5.0), with a fix release on 2026-11-07. A `v2.5.2` branch already exists.
- Files: `skills/taste-skill/SKILL.md` (31 KB), 22 reference docs in `references/` (about 430 KB), about 20 Node scripts in `scripts/` (one checker, `consistency.mjs`, is about 1 MB), and a large `assets/` kit. The kit holds a starter page, `system.css`, 11 hero layouts, about 19 UI fragments, diagram, shader, motion, "moments", scenes, 3D objects, and photo and icon libraries. There are also `library/type.json` (49 Google font families) and `library/palettes.json`.
- Repo: about 102 MB, 1,811 files (1,126 of them images). MIT licence. About 115.8k stars and 7.8k forks. Last push 2026-11-08. Very active, and it changes a lot.
- Install: `npx skills add … --skill "design-taste-frontend"`, or as a Claude Code plugin, a Codex plugin, or with `install.sh`. It needs Node 22+ and Chrome/Edge/Chromium. It targets Claude Code and Codex, and says it works with any agent through `npx skills`.
- The older skills (soft, minimalist, brutalist, gpt-taste, Stitch, v1, v2-experimental) moved to `Leonxlnx/taste-skill-classics`. The **DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY dials (1–10)** exist only in `taste-skill-v1` there. That version is React/Next-only, Tailwind, Framer Motion and Phosphor icons.
- **Instructions it gives to agents (I did not follow any of them):** the SKILL.md frontmatter registers a Claude Code **Stop hook** that runs `node gate.mjs`. The skill tells the agent to copy `assets/`, run deal scripts (including a `node -e` random picker), and run headless Chrome checks.

**2. Core content**
- **Principles.** Build "the website a good company would ship", with figma.com and x.ai as the bar. Nine "house rules" win over everything else:
  - no captions under images;
  - every visual must render;
  - one section per screen;
  - equal left and right edges;
  - hover micro-animations are required;
  - more real photos;
  - real full-colour brand icons;
  - shader and scene effects only on tech pages;
  - address rules.
- **Workflow.** Classify the business kind (software, gaming, tech, product, service or place). Then "deal, never choose by taste": scripts pick the palette, font pairing, hero layout, nav, footer, buttons and moments. Write the copy first, plan screen by screen, build from `starter.html`, then run copy-lint, the checker at 1440/1024/820/768/390, layout check, perf and screenshots. A finish gate allows up to 3 rounds.
- **Typography** (`layout-v4.md`, `system.md`):
  - one family, or a display face plus a text face; never three, at most four font files;
  - **banned:** Inter, Roboto, Open Sans, Lato, Montserrat, Poppins, Space Grotesk, Plus Jakarta Sans and "the system look";
  - weights 400/500 only, never 700/800;
  - fixed size scale (h1 72/38, h2 48/30, body 16/26, small 14, labels 13/500), each step at least 1.3x the next;
  - nothing under 13px, lines at most 62 characters;
  - sentence case, never tracked capitals or small caps;
  - fonts load from Google Fonts with `display=swap`.
- **Colour:**
  - the interface stays 90–95% neutral, with a near-black ink (never #000) and at most one accent;
  - reading text at **7:1 or more**; muted text (4.5:1 or more) only for labels and meta;
  - "highlight by contrast, never by colour";
  - violet and lavender are banned (OKLCH hue 270–330 gets moved);
  - dark pages and dark heroes are "tech only".
- **Spacing and layout:**
  - spacing scale 4, 8, 12, 16, 24, 32, 48, 64, 96, 128; 12-column grid with 24px gaps; `.wrap` 1280 wide;
  - every section is exactly 100svh or 200svh;
  - sections separate by a full-width ground change or space only, with no rules inside sections (a list may close each row with a 1px rule);
  - "one strict system per page" (one button shape, one radius family, one card recipe, one hairline, one link look);
  - "two boxes deep at most"; "never text in a box in a box".
- **Motion** (`motion.md`): required on every page. A hero entrance on load, one or two "dealt moments", cards lift 2px on hover, photos zoom 1.02–1.03. No scroll reveals, no parallax on text, no scroll-jacking. Reduced motion shows the finished state.
- **UX writing** (`copy*.md`, plus the `copy-lint.mjs` script): a strong list of AI copy tells:
  - banned words (delve, seamless, robust, elevate…) and stock lines;
  - "invented specifics", stat strips, "X. Y." headings, em-dash overuse.
  - It is tuned for sales copy: the h1 names the category, buttons are a verb and an object.
- **Accessibility:** visible labels, alt text, headings one level at a time, focus ring 2px at 3:1 that never animates, skip link, 44px tap targets, `aria-expanded` on the menu.
- **Anti-patterns** (SKILL.md "Never", and `cards.md` "Never"): fade-in on scroll, parallax, scroll-jacking, stock photos passed off as the client's, drawn look-alike logos, invented reviews, violet, three levels of boxes, an accent on every chip, loops over 5 s without a pause button.
- **Tunable parameters:** no dials in 2.5. Values are "dealt" by script: page kind, trade palette, pairing, radius `sharp|soft|round`, button look, nav and footer types, ground `sand|sky|sage`.

**3. Assumptions and bias**
- **Stack:** plain static HTML and CSS by default, or the project's own React/Vue/Svelte/Astro/Tailwind. Next.js builds as a static export. Its tooling needs Node and Chrome, and fonts, photos and icons come from the network.
- **Product kind:** marketing and company sites only. Docs, document pages and dashboards are not covered.
- **Default look:** premium SaaS (x.ai, Figma), lit feature-card panels, product UI fragments, photographs, required motion.
- **Conflicts with your constraints:** Google Fonts links (CDN); 100svh sections; a fixed nav and a hero; required hover lift, hero entrance and moments; "FAQs open in full… no accordion", which conflicts with your collapsible decision cards; dark mode limited to tech pages; no print guidance; no guidance for tables or code blocks. Its rule 1 (no captions under images) also clashes with the figure captions a spec needs (my inference).

**4. Useful for your topics**
- **Long-form reading:** the 16px floor, line height 1.5–1.8, the 7:1 ink rule and the 62-character measure (`system.md`). There is nothing on long documents as such.
- **Tables, code blocks, print:** nothing. The `code`, `doc` and `diff-review` items in `assets/ui` are fragments for marketing mockups.
- **Cards:** "the card is barely there" (one step off the page plus a hairline). No blurred shadow at rest. No three-level boxes (`cards.md`).
- **Accordions:** it rejects them.
- **Status chips:** chips are ink tints; the accent appears once per fragment; "never a row of green dots" (`cards.md`).
- **Colour tokens and dark mode:** `--g-main/--g-alt/--g-dark`, `--action`. Dark is tech-only.
- **SVG diagrams:** `diagrams.md` covers node-and-line marketing visuals from presets (hub, lanes, timeline). It is not for spec figures.
- **Boxes inside boxes:** clear, useful rules ("two boxes deep at most").
- **Fonts:** see the ban list above. `type.json` does include Literata, Newsreader, Source Serif 4, IBM Plex and JetBrains Mono.

## impeccable

**1. What it is**
- One skill, `impeccable` (SKILL.md version 4.9.1, engine 0.1.24). It has 24 commands, 47 reference docs (about 440 KB) and 5 subagents (asset-producer, documenter, finish-reviewer, manual-edit-applier, motion-reviewer).
- It ships a Rust engine (`crates/`), with a detector of **62 deterministic rules** (`crates/live/assets/antipatterns.json`), a CLI, a Chrome extension and a VS Code extension. Source is in `skill/`; built copies sit in about 20 tool folders (`.claude/`, `.cursor/`, `.agents/`, `plugin/`…).
- Repo: about 888 MB, 5,417 files (2,519 are tests). **Apache-2.0** licence. Based on Anthropic's `frontend-design` skill; the iOS/Android references come from an MIT project. About 110.4k stars. Commits landed today, 2026-11-15.
- **Branch note:** the latest commit message says work now lands on a `next` branch and `main` ships only at a release.
- Install: `npx impeccable install` (detects the tool and offers a design hook), Claude Code `/plugin`, a git submodule, or a manual copy of the folder. Run `/impeccable init`, which writes `PRODUCT.md`. Then `/impeccable <command> <target>`. It targets Claude Code, Cursor, Codex, Copilot, Gemini CLI and about 15 other agents.
- **Instructions it gives to agents (I did not follow any of them):**
  - SKILL.md tells the agent to run the `scripts/impeccable context` binary every session. The binary downloads once.
  - The README says hooks "run outside model approval".
  - Live mode can launch `codex` or `claude` with approvals and sandbox bypassed.
  - A new design fetches visual directions from impeccable.style, with optional telemetry.

**2. Core content**
- **Principles.** "The brief wins"; refinement keeps the current design, redesign replaces it.
- **Four modes** (SKILL.md):
  - Persuade: landing and marketing pages;
  - Operate: apps and dashboards;
  - **Read: docs, articles, guides, changelogs;**
  - Experience: portfolios and showcases.
  - On Operate and Read, "ambition shows as precision and restraint".
- **Read mode** (`mode-read.md`):
  - the page "is first a document of its kind";
  - the visual direction owns the frame (masthead, rail, title, section openers, how code, tables and callouts are set);
  - the reading column stays calm (reading face, real contrast, 60–75 characters, body near 16px);
  - mono only for code, parameters and small labels;
  - code, tables, notes and figures "in the standard forms readers already know";
  - one signature move, "never a frame repeated around every element".
- **Typography** (`typeset.md`, `operate.md`, `craft-floor.md`):
  - for Read, one well-tuned family and a fixed rem scale, ratio 1.125–1.2, not fluid;
  - body at least 16px, measure 45–75ch, leading tuned to the measure;
  - light text on dark gets more leading, a little more tracking and one more weight step;
  - `text-wrap: balance` on headings and `pretty` on body;
  - paragraph spacing **or** indent, not both;
  - tabular numbers and code features where they help;
  - load only the weights you use, with metric-compatible fallbacks, and self-host fonts.
- **Colour** (`colorize.md`, `new-work.md` §4):
  - roles, not swatches: canvas and raised surfaces, two text levels, action/focus/selection, borders, success/warning/error/info, data scales;
  - OKLCH for new palettes, with lower chroma near white and black;
  - strategies are Restrained, Committed, Full or Drenched; Restrained is the base for Read and Operate;
  - dark mode is "composed, not mechanically inverted"; themes remap semantic tokens;
  - prefer explicit colours over chains of transparent overlays;
  - WCAG AA table: text 4.5:1, large text 3:1, controls/icons/focus 3:1;
  - never colour alone.
- **Spacing and layout** (`layout.md`):
  - group by proximity before you add containers;
  - rhythm comes from tight against generous spacing;
  - a 4-unit base scale;
  - more space above a heading than below;
  - for Read, "predictable structure… navigable linearity".
- **Motion** (`animate.md`, `operate.md`):
  - for Read, feedback and state only;
  - 100–150 ms for feedback, 150–300 ms for routine changes;
  - no page-load choreography, exits faster than entrances, no bounce;
  - hover never moves neighbours;
  - a deliberate reduced-motion version that keeps state changes.
- **Interaction:** every component has default, hover, focus, active and disabled states, plus loading and error where they apply. Theme the "browser surfaces": selection, caret, scrollbars, focus ring, underline offset, tabular numbers (`craft-floor.md`).
- **UX writing** (`clarify.md`): one fact, then the next action, then context; say each idea once; the same noun and verb for the same concept; errors say what failed, why, and how to recover.
- **Responsive and print** (`adapt.md`): a print section (page breaks, hide nav and controls, expand hidden content and URLs, black-and-white friendly, metadata).
- **Accessibility:** `audit.md` scores accessibility, performance, theming, responsiveness and implementation integrity from 0 to 4, with P0–P3 findings.
- **Anti-patterns.** `craft-floor.md` has a "Refuse" list, a few absolute bans, and the 62 detector rules. Examples:
  - kicker or eyebrow above a heading (**ban**), nested cards, coloured `border-left` over 1px on cards or callouts;
  - gradient text, glow halos, hard offset shadows, monospace as a costume;
  - cream palette, italic serif display, overused fonts (Inter, Roboto, Fraunces, Geist, Plus Jakarta, Space Grotesk);
  - icon tile above a heading, numbered section labels, decorative grid backgrounds;
  - monotonous spacing, flat type hierarchy, heading rhythm, line length over about 80ch, tight leading, justified text, skipped headings, low contrast.
- **Workflow and parameters:**
  - context first (`init` writes PRODUCT.md, `document` writes DESIGN.md, `shape` plans);
  - steer commands (`quieter`, `distill`, `typeset`, `layout`, `colorize`…), review (`critique` uses Nielsen's 10 heuristics on a 0–4 scale; `audit`), finish (`polish`, `harden`, `adapt`);
  - live-mode sliders: scale 0.85–1.3, density 0.6–1.4, colour amount 0–1.

**3. Assumptions and bias**
- **Stack:** neutral. Plain HTML/CSS works, including the detector and live mode.
- **Product kind:** covers all four modes, but much of the depth (new-work, comps, `bolder`, `overdrive`) is aimed at Persuade pages.
- **Default push:** commit to a distinct visual direction. Its self-check asks "could this be any other product's documentation?", and craft-floor says "when torn between refined and committed, commit".
- **Conflicts with your constraints:**
  - the heavy tool chain (engine binary, hooks, network catalog, subagent-only critique, image comps);
  - "tables → cards on mobile" (`adapt.md`);
  - the new-work direction roll, which you do not need because the direction is already chosen.
- **A direct warning for your direction:** `new-work.md` lists "broadsheet-editorial hairlines, italic display serif, and small tracked mono labels" as one of the looks AI output clusters around.

**4. Useful for your topics**
- **Reading typography:** strong (`typeset.md`, `mode-read.md`).
- **Tables:** "tables at 120ch+ are fine", density is allowed in Operate/Read, tabular numbers.
- **Code blocks:** mono only for code; set in the standard form.
- **Cards and accordions:** "cards are the lazy container", no nested cards; `<details>` for progressive disclosure.
- **Status chips:** chip is a standard DESIGN.md component; semantic colours plus a non-colour cue; no pulsing dots.
- **Colour tokens and dark mode:** strong (see Colour above).
- **SVG figures:** only "figures in standard forms" plus a ban on shape-assembled illustration at hero size. Thin.
- **Boxes inside boxes:** strong (nested-cards rule, proximity first).
- **Fonts:** for Read, "system stacks and workhorse UI faces" are fine. The "training-data defaults" list (Fraunces, Playfair, Cormorant, Lora, Crimson, Newsreader, Syne, Space Grotesk/Mono, IBM Plex, DM Sans/Serif, Outfit, Plus Jakarta, Instrument Sans) applies to Persuade and Experience pages.
- **Design-system document:** `document.md` gives a ready DESIGN.md format: YAML token frontmatter, 8 fixed sections, "Named Rules", and component snippets with their states.

## Comparison

| Criterion | taste-skill | impeccable |
|---|---|---|
| Fit to a document/reading page | Poor. Only company sites; no docs mode | Good. Explicit Read mode with column, frame and wayfinding rules |
| Stack neutrality | Static HTML kit, but needs Node, Chrome, Google Fonts and network photos | Neutral HTML/CSS. Optional engine binary |
| Depth of typography guidance | Fixed marketing scale, ban list, good numeric floors | Deep: roles, measure, leading, wrapping, optical alignment, delivery, dark-text compensation |
| Colour/theming guidance | Neutral-first plus one accent, 7:1 ink; dark is tech-only | Role-based tokens, OKLCH, composed dark mode, AA table, colour-blindness checks |
| Anti-pattern list quality | Very good for copy; visual list is marketing-specific | 62 coded rules plus the craft-floor list; generic and checkable |
| Use for step 4 (design system) | Low. Values are dealt by script for sales pages | High. DESIGN.md template, colour roles, type system steps |
| Use for step 5 (components library) | Low. Its components are hero layouts, effects and moments | Medium-high. State checklist, DESIGN.md component snippets, no-nesting rules. No specific table or code components |
| Audit/critique support | Automated gate, but checks marketing rules (100svh sections, hover lift) | `critique` (Nielsen, personas), `audit` (P0–P3), detector by CLI, hook or extension |
| Risk of a marketing/"premium SaaS" look | Very high. That is its stated goal | Low on Read; medium if you follow its "commit to the direction" push |
| Maintenance/activity | Very active, but rebuilt 10 days ago; high churn | Very active (commits today); release flow just moved to `next` |
| Licence | MIT | Apache-2.0 (with NOTICE) |

## Recommendation

**Use impeccable as the main reference for steps 4 and 5.** It is the only one of the two with a mode for reading surfaces, and its guidance does not depend on a stack. Its typography, colour-role and anti-nesting rules fit a calm, dense document page. Its `document.md` format is close to a ready template for the design-system step. taste-skill's current `main` is built for something else: one-screen marketing sections, required motion, Google Fonts and photos. Its tables, code, print and accordion guidance is missing or goes against your page. Use impeccable as **reading material**. Do not run its engine, hooks, live mode or new-work direction roll.

**The 15 rules that matter most for your page**
1. Treat the page as a Read surface. It is a document first; the direction shows in the frame (masthead, rail, headings, how code and tables are set), and the reading column stays calm. (`SKILL.md` Modes; `reference/mode-read.md`)
2. Code, tables, notes and figures use forms readers already know, in the system's type and palette. Use one signature move only where it earns its place, never a frame around every element. (`mode-read.md`)
3. Use mono only for code, parameters, IDs and data, never for running text, headings or a "technical" look. (`mode-read.md`, `craft-floor.md`)
4. Use one well-tuned family, or very few, with a fixed rem scale and ratio about 1.125–1.2. Keep at least one clear step between heading and body. (`operate.md`, `typeset.md`; detector `flat-type-hierarchy`)
5. Body at least 16px, prose measure 45–75ch, leading tuned to the measure, `balance` on headings and `pretty` on body, paragraph spacing or indent but not both. (`typeset.md`, `craft-floor.md`)
6. Use tabular numbers and code font features. Theme selection, caret, scrollbars, focus ring and underline offset from the palette. (`typeset.md`, `craft-floor.md`)
7. Self-host only the faces and weights you use, with metric-compatible fallbacks. (`typeset.md`, `craft-floor.md`)
8. Build colour as roles: surfaces, two text levels, action/focus/selection, borders, success/warning/error/info. Use OKLCH and a Restrained strategy. (`colorize.md`, `new-work.md` §4, `operate.md`)
9. Compose dark mode on its own; never invert. A theme switch remaps the semantic tokens. Prefer explicit colours over stacked transparency. (`colorize.md`)
10. Meet AA in both themes and every state: text 4.5:1, large text 3:1, controls/icons/focus 3:1. Never use colour as the only cue. (`colorize.md`)
11. Group by proximity before containers. No nested cards. Rhythm from tight against generous spacing, a 4-unit scale, more space above a heading than below. (`layout.md`, `distill.md`; detectors `nested-cards`, `heading-rhythm`, `monotonous-spacing`)
12. Refuse: kickers above headings, gradient text, coloured side borders over 1px on cards or callouts, decorative glass and glow, hard offset shadows, pulsing dots, decorative grid backgrounds. (`craft-floor.md`, `antipatterns.json`)
13. Motion only for feedback and state, 100–300 ms, no load choreography, exits faster, no bounce, a deliberate reduced-motion version. Hover never moves neighbours. (`operate.md`, `animate.md`)
14. Every interactive component defines default, hover, focus, active and disabled states, plus loading, error and empty where they apply. (`operate.md`, `polish.md`)
15. Write the design system as DESIGN.md: token frontmatter, the 8 fixed sections, Named Rules, component snippets with `:hover` and `:focus-visible`. Add print rules from `adapt.md`: logical page breaks, hide controls, expand hidden content. (`document.md`, `adapt.md`)

**Rules from impeccable you should deliberately NOT follow**
- **The new-work flow:** the concept-seed direction roll, the catalog fetch from impeccable.style (network and telemetry), image comps, decision pages. Your direction is chosen, and Read pages are "code-led" anyway. (`new-work.md`, `new-work-world.md`)
- **The push to "commit":** "Push the frame further… could this be any other product's documentation?" and "when torn… commit". For an internal spec viewer, take one quiet signature (for example the ID and numbering system) and stop there. This is my inference. (`mode-read.md`, `craft-floor.md`)
- **Tables to cards on mobile:** this breaks comparison in dense tables. Keep real tables in a scroll wrapper. (`adapt.md`)
- **Section numbers:** do not apply `numbered-section-labels` or the section-numbers refusal. Your numbers carry real meaning, which is the exception craft-floor allows.
- **Side-border ban on diffs:** do not apply the `side-tab` ban to diff gutters. A coloured diff gutter is a git convention; follow the ban for callouts and cards. This is my inference.
- **Tooling:** the critique rule "two isolated sub-agents required" with stored snapshots, live mode, hooks and the engine. Use the rubric and audit tables by hand. Running `npx impeccable detect page.html` is an optional choice to evaluate, not a requirement.
- **Fonts:** treat `overused-font` as advice, not a ban. Legibility and licence come first on a Read page.

**One idea to borrow from taste-skill:** its "one strict system per page" inventory as a checklist for step 5. One button shape, one radius family, one card recipe, one hairline, one link look, and "two boxes deep at most" (`references/system.md`, SKILL.md §5). A close second is its contrast tiering: reading text at 7:1, muted grey only for labels and meta.

## What this means for render-view

- Write the step-4 design-system document in impeccable's DESIGN.md format (`document.md`). Use OKLCH role tokens with a separately composed dark theme.
- Set the page as Read mode: a calm column at about 65–75ch, 16px+ body, a fixed rem scale. Put the personality in the frame (outline rail, headings, ID chips, how tables and code are set).
- The editorial direction is at risk of the "AI cluster" impeccable names: hairlines, italic display serif, small tracked mono labels, cream ground. Avoid tracked-caps kickers and a cream background. Use roman headings.
- Decision cards should be full-width `<details>` with no card inside a card. Use spacing and one hairline, not nested boxes. This fits your existing collapsible-card rule.
- Use mono only for code, IDs and diffs. Use tabular numbers in tables. Keep tables as tables, with horizontal scroll at narrow widths.
- Status chips: semantic colour plus a text label, low saturation, no pulse, one shape.
- Motion: only `<details>` open/close and hover/focus feedback, 150–250 ms, plus a reduced-motion rule. No entrance animations.
- Components library (step 5): for each component show default, hover, focus-visible, active and disabled states, both themes and a print view. Check it against the "one strict system" list above.
- Use impeccable's `audit.md` (P0–P3, five dimensions) and the critique heuristics as manual review checklists. Do not install its hooks or engine for this work.
- If your process doc mentions taste-skill "dials", update it. They now live only in `taste-skill-classics/taste-skill-v1`, which is React/Tailwind/Framer Motion.

## Sources

All checked 2026-11-15. Files were read at pinned commits: taste-skill `main` @ `f6b76575` (2026-11-07) and impeccable `main` @ `2b86d9c0` (2026-11-15).
- **GitHub API:** `api.github.com/repos/Leonxlnx/taste-skill` and `/pbakaus/impeccable` (repo metadata, `git/trees/HEAD?recursive=1`, commits, branches). The releases call failed with a rate limit.
- **taste-skill raw files** (`raw.githubusercontent.com/Leonxlnx/taste-skill/f6b76575…/`):
  - read in full: README.md, `skills/taste-skill/SKILL.md`, `references/system.md`, `references/layout-v4.md`;
  - read in part: CHANGELOG.md (2.5.x), `references/cards.md`, `copy-tells.md`, `copy.md`, `motion.md`, `diagrams.md`, `gate.md`, `library/type.json`, `library/palettes.json`;
  - downloaded and searched by keyword, not read in full: the other 13 reference docs (backgrounds, copy-moves, copy-registers, copy-voice, effects-creative, effects-objects, effects-usage, icons, moments, perf, photos, scenes, sections, sections-library).
- **taste-skill-classics:** tree listing; `skills/taste-skill-v1/SKILL.md` (searched for the dials); `skills/minimalist-skill/SKILL.md` (read).
- **impeccable raw files** (`raw.githubusercontent.com/pbakaus/impeccable/2b86d9c0…/`):
  - read in full: README.md, `plugin/skills/impeccable/SKILL.md`, and these references: mode-read, operate, craft-floor, typeset, colorize, layout, quieter, distill, polish, audit, document, extract, clarify;
  - read in part: animate, adapt, critique, critique-rubric, harden, new-work, component-review, NOTICE.md, DESIGN.md (head), `crates/live/assets/antipatterns.json` (all 62 rules);
  - searched by keyword or headings only: init, shape, routing, hooks, live, live-setup, new-work-world, new-work-comp, visualize, generate, region-map, doctor, foundations, bolder, delight, overdrive, onboard, optimize, ios, android, the native variants, and the 5 agent files.
- **Not read:** any script, CSS or JS code (by design); impeccable `PRODUCT.md`, `AGENTS.md`/`CLAUDE.md` (contributor files), `docs/`, the Rust crates other than the rule list; the impeccable.style and tasteskill.dev websites.

## Confidence

- **Confidence score: 90%.** Both skills' main files and every reference that drives the recommendation were read in full, and the result is clear-cut. taste-skill's own description targets company websites; impeccable has an explicit Read mode.
- **10% uncertainty:**
  - About half of each repo's reference docs were searched by keyword only, not read in full (listed above). A detail on tables, code or print could be in them, but I think a change to the recommendation is unlikely.
  - **Branch ambiguity, impeccable:** its latest commit moves work to a `next` branch; I read `main`. Rules may change soon.
  - **Branch ambiguity, taste-skill:** 2.5 is 10 days old and a `v2.5.2` branch exists; details may change.
  - Star counts and versions are as of today and change fast.
  - Some points are my inference, not stated in the repos: the diff-gutter exception to `side-tab`, the "one quiet signature" advice, the clash with figure captions, and how the editorial cluster warning applies to your page.
  - I could not check the releases endpoint (rate limit). I did not run either detector, so I describe rule behaviour from its text only.
