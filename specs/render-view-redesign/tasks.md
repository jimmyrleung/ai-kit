# Tasks summary — apply the render-view redesign to the skill

Source of the design (there is no separate techspec; these are the specs):
[context.md](context.md), [design-system/DESIGN.md](design-system/DESIGN.md),
[design-system/tokens.css](design-system/tokens.css), [components/COMPONENTS.md](components/COMPONENTS.md),
[components/components.css](components/components.css), [components/page.html](components/page.html).

Target files, all in `skills/render-view/`: `scripts/render_view.py`, `assets/view.css`, `assets/view.js`.

## Tasks overview

| Task | Title | Complexity | Est. Time | Depends On | Status |
| ---- | ----- | ---------- | --------- | ---------- | ------ |
| #1 | [Synthetic fixture and baseline](task_01.md) | M | 2–3h | — | Done |
| #2 | [Stylesheet, fonts and theme](task_02.md) | M | 2–3h | T1 | Done |
| #3 | [Page shell](task_03.md) | M | 3–4h | T2 | Done |
| #4 | [Respond panel](task_04.md) | M | 3–4h | T3 | Done |
| #5 | [Document, tables, code and popover](task_05.md) | M | 3–4h | T4 | Done |
| #6 | [Exhibits and diagrams](task_06.md) | M | 3–4h | T4 | Done |
| #7 | [Decision round](task_07.md) | L | 5–6h | T4, T5, T6 | Done |
| #8 | [Tour](task_08.md) | S | 1–2h | T7 | Done |
| #9 | [Modes, scale and final checks](task_09.md) | M | 2–3h | T7, T8 | Done |
| #10 | [Docs and close-out](task_10.md) | S | 1h | T9 | Done |

**Overall Progress**: 10/10 tasks completed (100%)

**Last Updated**: 2026-11-15

## Implementation order

Fixture first, then the stylesheet, then the shell, then the parts of the page, then the checks and the docs.
All tasks change the same three files, so they run one after the other. T5 and T6 do not depend on each
other, but do them in this order. Both need T4, because their checks read the live Respond text. T8 needs
T7, because it uses T7's check icon. T7 is L and stays one task: the card markup, the filters and the answer
logic in `view.js` change together and cannot be checked apart.

```text
T1 ─> T2 ─> T3 ─> T4 ─┬─> T5 ─┬─> T7 ─> T8 ─> T9 ─> T10
                      └─> T6 ─┘
```

After T2 the page uses the new stylesheet with old markup. Rounds and tours look half-styled until T7 and
T8. The installed skill (`~/.claude/skills/render-view`, `~/.agents/skills/render-view`) is a junction to
`skills/render-view/` in this working tree, so every edit is live in all sessions at once, and
`sync-skills.py` changes nothing. To keep other sessions on the old page until T9 is done, do T2–T9 in a
separate git worktree (the owner creates it). Otherwise, expect half-styled views from other sessions.

## Decisions these tasks carry

Owner decisions, 2026-11-15:

| # | Decision |
|---|---|
| 1 | The Respond panel is always open on a decision round at 1200px and wider. Below 1200px (an overlay) and on other pages it opens on demand and has a close button |
| 2 | A round shows all its cards. The limit of 12 and "Show N more" are removed |
| 3 | Bulk accept applies at once and gets an "Undo" in the Respond status line. One level: it restores the answers from before the last bulk accept and goes away at the next answer |
| 4 | The fixture is committed in `specs/render-view-redesign/fixture/`, with synthetic content |
| 5 | No automated tests are added. Each task is checked on the fixture in a browser |
| 6 | Assets: one `assets/view.css` (tokens, then components), one `assets/fonts.css`, and the two OFL licence texts in `assets/` |
| 7 | The outline and the document list are written twice in the HTML: once in their column, once in the Contents menu |
| 8 | The prose measure stays `66ch`: 700px in Geist at 16px, about 90–95 characters |
| 9 | "Copy response" is a secondary button; Respond in the top bar stays the only primary button |

Choices made in the breakdown, confirmed by the owner on 2026-11-15:

| # | Choice | Task | Why |
|---|---|---|---|
| a | The Contents menu also holds "Collapse all" | T3 | Below 1200px the outline column is hidden, so the button would be out of reach |
| b | On a round, the state filter and one topic filter combine (state AND topic) | T7 | The library shows them as two separate controls; today one filter replaces the other |
| c | "Built from" in the Respond panel lists every document of the view and the repository heads | T4 | The panel is page-level now; today the list is per round |
| d | `decisions` exhibits in a spec keep the suggested option preselected | T6 | COMPONENTS.md says "Same"; the Respond text ("not touched; default kept") depends on it |

## How to check a task

Python is not on PATH on the owner's machine; use `uv run --no-project python -B`.

```bash
cp specs/render-view-redesign/fixture/exhibits/*.json specs/render-view-redesign/fixture/.views/exhibits/
uv run --no-project python -B skills/render-view/scripts/render_view.py build specs/render-view-redesign/fixture --repo .
uv run --no-project python -B -m py_compile skills/render-view/scripts/render_view.py
```

Run the build from the repository root (the fixture's tour names its repository as `.`). The first build
creates `.views/`; run the build once before the `cp` on a fresh clone. Then follow the browser steps in
`sessions/20261022101915_render-view-rounds-tours/skills/check-view-page.md`: serve the fixture folder on
`127.0.0.1`, open `/.views/view.html`, read the console, drive the page with page scripts, check both
themes, stop the server. The Chrome extension cannot open `file://` pages.

To compare with the page before the redesign, write the old files to a scratch folder with
`git show main:skills/render-view/<path>` (keep the `scripts/` and `assets/` layout) and build the fixture
with that copy and `--out <scratch>/old.html`. Both builds use the same storage key, and the Confirm and
Reviewed buttons toggle. Before you drive a build, clear `localStorage` in the page (or serve each build on
its own port), or the second run undoes the first.

To see a stale exhibit, edit a fixture section and rebuild without the `cp` step: `cp` copies the unstamped
files back, so the build stamps them again and nothing shows as stale. Restore the section afterwards.

## Rules for every task

- The owner creates the branch and commits. Leave all changes unstaged.
- Add no comments to the code. Keep the existing comments of code that stays.
- Ask the owner before any command that contains `rm`, `del`, `reset`, `remove` or `prune`.
- The repository is public: synthetic content only, no client names, `~/`-style paths.
- Keep the Respond block format and the exhibit JSON contract unchanged.
- After a task, set its status here and update the progress line.

## Confidence

```
Confidence: 92% - the design is approved and specific, the owner confirmed the open points, and each
"Markup change" row maps to a function that was read in full.
Remaining uncertainty: 8% - checks are manual browser checks; T7 can grow because the Respond text reads
the card markup; print, forced colours and "more contrast" may need the owner's eyes if the browser tool
cannot emulate them.
```

| Factor | Weight | Score | Note |
|---|---|---|---|
| Fidelity to the approved design and the locked decisions, requirement coverage | 35% | 33 | Every row of COMPONENTS.md has an owning task; choices a–d go beyond the letter of the spec |
| Dependency, lifecycle and resource closure | 25% | 23 | One file set, strict sequence; the page is half-styled between T2 and T8 |
| Test and acceptance ownership, checks that can run | 25% | 22 | No automated tests by decision; T9 owns the untested modes |
| Task boundaries, sizing and path grounding | 15% | 14 | T7 is L with a stated reason |
