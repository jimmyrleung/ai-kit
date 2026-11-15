# Task 10 - Docs and close-out

## Description

Bring the skill's documentation and the spec folder in line with the page as built, and run the repository's
own checks.

- Status: Done
- Complexity: S
- Estimated time: 1h
- Depends on: T9
- Can run in parallel with: —

## AI guidance

- `write-skills` skill: when editing `SKILL.md`, keep the frontmatter description valid and the file short.
- `sessions/20261021230619_render-view/skills/validate-kit.md`: the local version of the repository's CI
  checks (skill format, inventory counts, links, Python syntax, sync dry run).
- Global rule "Spec & doc updates": when one doc in a folder changes, check its siblings.
- `AGENTS.md`: public repository.

## Requirements

- The references describe what the reader sees now. They do not describe the redesign as a change.
- No change to the exhibit JSON contract or to the Respond format, so those parts of the references stay.
- The spec folder says the design is applied.

## Files involved

| File | Action |
|---|---|
| `skills/render-view/references/rounds.md` | Modify: "Round 0 premise cards" → premise cards; "a Respond column" → the Respond panel (always open on a round at 1200px and wider, on demand below); "the live column or the top-bar button"; add the "Undo" of bulk accept; the page shows all cards |
| `skills/render-view/references/exhibits.md` | Modify: a new sequence message shows a leading "+"; figures get a "Figure N." caption |
| `skills/render-view/references/tours.md` | Read; modify only if a sentence no longer matches the page |
| `skills/render-view/SKILL.md` | Read; modify only if a sentence no longer matches (step 4 "Look at it" can name the theme switch) |
| `INVENTORY.md`, `README.md` | Read; the `render-view` rows mention no layout detail today, so a change is unlikely |
| `specs/render-view-redesign/context.md` | Modify: add a step-log row "Applied to the skill", and rewrite "Next round" as done |
| `specs/render-view-redesign/components/COMPONENTS.md` | Modify: "Not in this library" (the behaviour is now in `view.js`); note that `assets/view.css` is the live stylesheet and `components.css` is the design record |
| `specs/render-view-redesign/tasks.md` | Modify: statuses and progress |

## Implementation steps

1. Read each file in the table end to end, then edit.
2. Run the checks from `validate-kit.md`, including `sync-skills.py --dry-run`. The installed skill is a
   junction to `skills/render-view/`, so the dry run lists one action per skill and the new files need no
   sync. Confirm with `ls skills/render-view/assets` that `fonts.css` and the two licence texts are there.
3. Build the fixture one last time and run `render_view.py check` on it.
4. Report to the owner what is left for them: the branch and commits, and the two files
   `design-system/directions/a-paper-and-ink.html` and `b-swiss-ledger.html` (deleted 2026-11-15), which embedded font subsets
   without licence texts (remove them or add the licences before committing).

## Acceptance Criteria

- `grep -n "Respond column\|Show .* more\|live column\|Round 0" skills/render-view/references/*.md` returns
  nothing.
- Every sentence in `rounds.md`, `tours.md` and `exhibits.md` about the page matches the fixture build (read
  beside the open page).
- The `validate-kit` checks pass; `skills/render-view/assets/` holds `view.css`, `view.js`, `fonts.css`,
  `OFL-Geist.txt` and `OFL-GeistMono.txt`.
- `render_view.py check specs/render-view-redesign/fixture` prints "Fresh".
- `tasks.md` shows 10/10 tasks done.
- `git status --short` shows no staged file.

## Testing

Not applicable: documentation only. The repository checks in step 2 are the verification.

## Additional relevant files

- `.github/workflows/portability.yml` — the CI job that `validate-kit` mirrors.
