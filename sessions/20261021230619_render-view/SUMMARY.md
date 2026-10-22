# Session summary — render-view

## What happened

- Read three posts on making model output easier to understand: Karpathy (writing → diagrams → HTML → video explainers), omarsar0 (artifacts as a two-way interface), and Thariq's `html-plan` plugin (a claim tree with exhibits, decision forms, Respond, and a linter).
- Assessed which kit skills benefit: techspec + tasks-breakdown (high), walkthrough decision rounds (high, after evidence from a 49-decision round), walkthrough-implementation (high, conversation stays in chat), define-reqs (lower).
- Laid out three build options on a design canvas: A Compile (script only), B Assemble (script + cached model exhibits), C Author (model writes the whole page). The owner chose B.
- Built `skills/render-view/`, tested it on a real ~1,000-line spec set and a fictional fixture, compared it side by side with an html-plan engine, then extended the Python version with SVG diagrams, repo code excerpts, git diffs and automatic before/after diffs. Removed the html-plan engine.
- Committed `f34fa0d` on branch `render-view`; synced (24 skills, 48 links).

## Decisions

1. Generated HTML views are build output; the markdown stays the source of truth. Agents read markdown best and two sources drift. See [decision](decisions/generated-html-views-option-b.md).
2. Option B: the script parses markdown and lays out the page; the model writes only exhibits (JSON) stamped by section hash and, for code, by code hash. Cheap rebuilds, fault isolation, stale detection.
3. Standard-library Python, no html-plan runtime or node, no mingrammer `diagrams`. See [decision](decisions/python-stdlib-over-html-plan.md).
4. Views stay local and git-ignored (`.views/.gitignore` holds `*`); client views are never hosted. No bundled web fonts, so pages make no network requests.
5. Diagrams use author-supplied grids (as html-plan does) instead of a layout engine.

## Learnings

- X/Twitter returns HTTP 402 to WebFetch; the Chrome extension reads it.
- The Chrome extension cannot open `file://` pages; a static server bound to `127.0.0.1` works (stop it after).
- html-plan's runtime takes over the whole page (global CSS, injected contents rail, comment buttons on every element), so its blocks cannot be embedded in another page cleanly.
- Code excerpts and git diffs surfaced real spec-to-code drift in the test spec, which is a feature: label it.
- Naive ID linking resolves ambiguous IDs (for example a review finding "R1" vs requirement "R1") to the first definition.
- `python`/`python3` may be Store stubs on Windows; `uv run --no-project python` works.
- No git identity was configured on the machine; earlier commits came from another tool.
- Skill examples drifted toward the real test data (client paths, a commit hash) and had to be scrubbed before committing.

## Open

See [`LOGS.md`](LOGS.md) for the next actions. Also untested: the Respond loop with an owning skill applying a pasted response. Leftovers to delete: html-plan comparison files in the test spec's `.views/`. `specs/html-output/` in ai-kit is untracked and was not created this session.

## References

- https://x.com/karpathy/status/2105819303471976479
- https://x.com/omarsar0/status/2106801689495826520
- https://x.com/trq212/status/2107192901537329354
- https://github.com/anthropics/claude-plugins-community/tree/main/html-plan

## Files touched

Commit `f34fa0d`: `skills/render-view/` (SKILL.md, references/exhibits.md, scripts/render_view.py, assets/view.css, assets/view.js), `README.md`, `INVENTORY.md`, `.github/workflows/portability.yml`.
