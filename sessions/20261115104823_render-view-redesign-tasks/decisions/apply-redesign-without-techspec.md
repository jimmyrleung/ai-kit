# Apply the render-view redesign from the design docs, with a committed fixture and no automated tests

- Date: 2026-11-15
- Status: accepted by the owner
- Scope: `skills/render-view/` (`scripts/render_view.py`, `assets/view.css`, `assets/view.js`)

## Context

The `ui-process` produced an approved design system and components library for the page that `render-view`
generates. `COMPONENTS.md` already lists, per component, what the build script must write differently. The
skill has no automated tests. The three real views used to judge the old page are private and cannot be
stored in this public repository.

## Decision

1. Break the work into tasks straight from `DESIGN.md` and `COMPONENTS.md`. Write no techspec. The tasks
   carry the build decisions (`tasks.md`, "Decisions these tasks carry").
2. Commit a small synthetic fixture in `specs/render-view-redesign/fixture/` that produces a spec view, a
   decision round and a tour. Its exhibit files sit beside the docs and are copied into `.views/exhibits/`
   for a build.
3. Add no automated tests. Each task is checked by building the fixture and driving the page in a browser.
   The Respond text is compared with a build of the old script taken from `main`.

## Why

- A techspec would restate the "Markup change from today" tables.
- A fixture in a scratch folder is lost between sessions, and ten tasks need the same one.
- Tests for generated HTML would be a second copy of the markup to maintain; the risk is visual and is seen
  in a browser.

## Consequences

- Design gaps found during the breakdown became choices in the tasks (a–d) that the owner still reviews.
- Print, forced colours and "more contrast" may need the owner's eyes; task 9 reports "not tested" if the
  browser tool cannot emulate them.
- The comparison with the old build works only while `main` holds the old version.

## Alternatives not taken

| Alternative | Why not |
|---|---|
| Techspec first | Little to add to the approved design docs |
| Fixture in a scratch folder | Lost between sessions |
| A unit-test suite for the renderer | Maintenance cost above the risk it covers |
