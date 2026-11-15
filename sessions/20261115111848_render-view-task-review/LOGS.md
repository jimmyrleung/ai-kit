## [2026-11-15] — render-view redesign: tasks reviewed, decisions taken, ready to implement

**Summary:** The adversarial review of the ten tasks found 2 blockers and 10 should-fix items; the owner
decided them and the open points, and the tasks and design docs were updated. No code changed.
**Next:** The owner creates the branch, or a git worktree if other sessions must keep the old render-view page
until T9 (the installed skill is a junction to this working tree). Then run `implement-task` on
`../../specs/render-view-redesign/task_01.md`.
**Blockers:** none.
**Didn't work:** —
**Artifacts:** `../../specs/render-view-redesign/tasks.md` (decisions 1–9, confirmed choices a–d, order
diagram, how to check a task), `../../specs/render-view-redesign/task_01.md` to `task_10.md`,
`../../specs/render-view-redesign/design-system/DESIGN.md` ("Decided points"), `SUMMARY.md`,
`decisions/respond-panel-on-narrow-rounds.md`, `decisions/keep-66ch-measure.md`.

**Replaces** the "Do not sync the skill" line in `../20261115104823_render-view-redesign-tasks/LOGS.md`:
syncing changes nothing, because edits are live at once (see `tasks.md`, "Implementation order").

**Before committing:** `design-system/directions/a-paper-and-ink.html` and `b-swiss-ledger.html` embed font
subsets without licence texts. Remove them or add the licences.
