## [2026-11-15] — render-view redesign: decisions taken, ten tasks written, implementation not started

**Summary:** The owner decided the three open points and `tasks-breakdown` produced ten ordered tasks for
applying the approved design to `skills/render-view/`; no code changed.
**Next:** Run the adversarial review of the tasks in a separate session (the prompt is below). Then the owner
creates the branch, and `implement-task` starts with `../../specs/render-view-redesign/task_01.md`.
**Blockers:** Four breakdown choices wait for the owner (a–d in `tasks.md`, "Choices made in the
breakdown"); choice b (state and topic filters combine) changes behaviour. The branch is the owner's to
create.
**Didn't work:** —
**Artifacts:** `../../specs/render-view-redesign/tasks.md`, `../../specs/render-view-redesign/task_01.md` to
`task_10.md`, `../../specs/render-view-redesign/components/COMPONENTS.md`,
`../../specs/render-view-redesign/design-system/DESIGN.md`, `SUMMARY.md`,
`decisions/apply-redesign-without-techspec.md`.

**Before committing:** `design-system/directions/a-paper-and-ink.html` and `b-swiss-ledger.html` embed font
subsets without licence texts. Remove them or add the licences.
**Do not sync the skill** (`sync-skills.py`) between task 2 and task 9: the page is half-styled in between.

**Review prompt:**

```text
Review the task breakdown in specs/render-view-redesign/ (tasks.md, task_01.md–task_10.md) as an adversary.
Do not implement anything and do not edit files; report findings only.

Inputs to read end to end first: specs/render-view-redesign/context.md, design-system/DESIGN.md,
design-system/tokens.css, components/COMPONENTS.md, components/components.css, components/page.html, and
the target files skills/render-view/scripts/render_view.py, assets/view.css, assets/view.js, plus
skills/render-view/references/*.md.

Check and report, with file and line for each finding:
1. Coverage: every row of every "Markup change from today" table in COMPONENTS.md, every rule in DESIGN.md
   "Components", and every item under "Not done here" in context.md has an owning task. List what has none.
2. Fidelity: any task step that contradicts the approved design or the seven decisions in tasks.md, and any
   place where a task re-designs instead of translating (see choices a–d).
3. Dependencies and order: a task that needs something a later task delivers; hidden coupling between
   render_view.py markup and view.js selectors or data-* attributes that a task breaks without saying so.
4. Contracts: any step that would change the Respond block format or the exhibit JSON contract.
5. Acceptance criteria: criteria that only restate a step, cannot be observed, or cite the spec as their
   only proof; function, class or line references that do not exist in the code.
6. Sizing: tasks too large to finish in one session or too small to be a checkpoint.
7. Over-engineering: steps, checks or files the work does not need.

Give each finding a severity (blocker, should fix, minor), then a verdict: ready to implement or not, with a
confidence score and what keeps it from 100%.
```
