# Task 1 - Synthetic fixture and baseline

## Description

Create a small spec folder with made-up content that produces all three page types (spec view, decision
round, tour) and every component the redesign touches. Build it with today's script to prove it works before
any change.

- Status: Done
- Complexity: M
- Estimated time: 2–3h
- Depends on: —
- Can run in parallel with: —

## AI guidance

- `render-view` skill: `skills/render-view/SKILL.md` and its three references define what the script reads.
  Follow them; do not invent formats.
- `AGENTS.md`: the repository is public. Use the "invoice reminders" sample from the references. No client
  names, no real paths.
- Global rules: no commits, no comments in code, ask before `rm`-type commands.

## Requirements

- Content is synthetic and small: the whole fixture builds in a few seconds.
- The exhibit files are kept outside `.views/` (that folder ignores itself in git) and copied in for a build.
- The tour's change set uses this repository with two fixed commits, so the diff never changes.
- Every `code` exhibit has `"ref": "a3ed724"`. Without a ref it reads the working tree, and later tasks
  change files in it, so the exhibit would go stale and `render_view.py check` would stop saying "Fresh".
- No change to `skills/render-view/`.

## Files involved

All new, under `specs/render-view-redesign/fixture/`:

| File | Content |
|---|---|
| `techspec.md` | A quote block before the first section (notes), an intro paragraph, `Mode: **…**`, level 2 and 3 sections, a level 4 heading, lists, a blockquote, a rule, a table with a Status column (one value per status class), a right-aligned number column, a confidence table (Weight, Score, Evidence, Total), a `ts` code block, a `// before` … `// after` block, a text diagram block, two implementation headings (`— Create`, `— Modify`), ID definitions (`R1`, `D1`, …) that other docs link to, a `` `path:line` `` code reference into this repository |
| `tasks.md`, `task_01.md` | Short. `tasks.md` has an `**Overall Progress**:` line |
| `decisions_walkthrough.md` | One `## Walkthrough — 2026-11-14 (round 1)` with: 2 premises (one confirmed), 14 items (more than the old limit of 12) with a Source column, mixed open / decided / deferred, and `### Dispositions` entries |
| `tour_2026-11-15.md` | `## Change set` with one row: Prefix `kit:`, Repo `.`, Base `f174a75`, Head `a3ed724`; a roadmap; steps `S1`–`S3` that cite `` `kit:path:line` ``; `## Not toured` |
| `exhibits/*.json` | One of each type: `claims` (at `top`), `flow`, `tree`, `states`, `graph` (with `new`, `changed`, `shared`, `removed` marks), `sequence` (with a `new` message, a `note`, a `divider`, a `fail`), `walk`, `timeline`, `code` (with `"ref": "a3ed724"`, `highlight` and one pin per tone), `diff` from text, `diff` from git on a tour step, `decisions`; for the round: one diagram per premise, a `decision` exhibit for 4 open items (two with `needs: true`, two shared `tags`, `uses`, a `walk`), and one item left without options |
| `README.md` | Six lines: what the fixture is, and the build commands from `../tasks.md` |

## Implementation steps

1. Run `git log --oneline -3` and confirm `f174a75` and `a3ed724` exist. If not, pick two commits on `main`
   whose diff has 3–10 files and use them in the tour.
2. Write the docs. Take the item table, premises and exhibit examples from
   `skills/render-view/references/rounds.md`, `tours.md` and `exhibits.md`, and extend them.
3. Write the exhibit files without `stamp`.
4. Build once (creates `.views/`), copy the exhibits in, build again with `--repo .`.
5. Fix the fixture until the build reports no invalid or orphan exhibit and no unresolved ref.
6. Open the page (see "How to check a task" in `tasks.md`) and look at each page type once.

## Acceptance Criteria

- `render_view.py plan specs/render-view-redesign/fixture --all` lists the round (2 premises, 14 items), the
  tour (3 steps, the changed files) and every exhibit as `fresh` (run it after the build, which stamps
  them).
- The build output line reports 5 docs and prints no `invalid`, `orphan` or "Unresolved refs" entry.
- In the browser: no console error; the round shows 12 cards and a "Show 2 more" button (today's behaviour);
  the tour's coverage panel lists the files of `git diff --name-status --no-renames f174a75 a3ed724` (the
  script splits a rename into a delete and an add).
- `render_view.py check specs/render-view-redesign/fixture` prints "Fresh".
- `git status --short` shows new files only under `specs/render-view-redesign/fixture/`, and nothing under
  `fixture/.views/`.
- `grep -ri` for a home path or a client name in the fixture returns nothing.

## Testing

No automated test (decision 5 in `tasks.md`). The acceptance criteria above are the test. Later tasks use
this fixture for their own checks.

## Additional relevant files

- `sessions/20261022101915_render-view-rounds-tours/skills/check-view-page.md` — the browser check steps.
- `components/page.html` — the same "invoice reminders" sample, useful for wording.
