# Long-term memory candidates

Drafts for the owner to review. Nothing here is in `AGENTS.md` or `rules/` yet.

## 1. Checking a local HTML page in the browser

The Chrome extension cannot open `file://` pages. To look at a generated page, serve its folder with a
static server bound to `127.0.0.1`, open it by `http://127.0.0.1:<port>/`, and stop the server afterwards.
Resizing the window may not change the viewport; to test a narrow layout, load the page in an iframe of
that width.

**Why:** two attempts to open `file://` failed, and a window resize left the viewport at full width.
**Where it could go:** `AGENTS.md`, or the `render-view` skill's "Look at it" step, which names `file://`
first.

## 2. Fan-out agents write their own report

When a fan-out must keep each agent's report on disk, tell each agent to write its report file and return
only a short summary and the path. Do not rely on the background transcript file.

**Why:** the transcript files were empty, so five reports of 200–300 lines were retyped by hand.
**Where it could go:** the `orchestrate` skill's Collect step.

## 3. Source of truth for the render-view page design

The design of the generated page is `specs/render-view-redesign/`: `design-system/DESIGN.md` and
`tokens.css` for the rules and values, `components/COMPONENTS.md` and `components.css` for the parts.
A change to the page's look starts there, then goes to `skills/render-view/assets/`.

**Why:** without this, a later change to `view.css` would drift from the approved system.
**Where it could go:** a line in the `render-view` row of `INVENTORY.md`, or in the skill's `SKILL.md`, once
the design is applied.
