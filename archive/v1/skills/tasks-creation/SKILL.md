---
name: tasks-creation
description: Decompose a slice's techspec into vertically-ordered tasks. Anti-horizontal-scaffolding by design.
---

# Tasks Creation Skill

You decompose a single slice's techspec into ordered, actionable tasks. **Vertical ordering, not horizontal phasing.**

---

## Scope rules

- Tasks are for **one slice**. The slice already has a Done-when list in its PRD; tasks are the concrete steps to make those checkboxes pass.
- Don't pull in tasks for future slices. If a setup-shaped item belongs to a later slice, leave it there.
- A task is 2–8 hours. Larger → split. Smaller → merge with a neighbor.

---

## Ordering principle: vertical, not horizontal

> **Order tasks so each one moves the slice's user-observable behavior closer to "demoable." Don't order as setup → core → polish.**

The classic anti-pattern (which previous versions of this skill encouraged):

```
Phase 1: Foundation
Phase 2: Core Features
Phase 3: Integration
Phase 4: Polish & Testing
```

Tasks 1–N ship no user-observable behavior. By task 7 you're still in Phase 1. **Reject this shape.**

The right shape:

```
Task 1: Smallest possible end-to-end touch — one happy path, hardcoded values, no error handling
Task 2: Add the second behavior the slice's PRD lists — still happy path
Task 3: Wire the first error case from the PRD
...
```

Each task has a **"Why this task is on the list"** line that names the user-observable behavior moving forward. If you can't write that line for a task, the task is wrong.

### When infrastructure tasks are unavoidable

Sometimes you genuinely need a setup task before any user-observable work happens (e.g., "scaffold the Next.js app"). When this happens:

- **Make it the smallest infrastructure that supports the next user-observable task.** Don't add scaffolding "we'll need later."
- **Bundle it with the first user-observable task** if possible. "Task 1: Scaffold Next.js + render hello-world page" beats "Task 1: Scaffold Next.js" + "Task 2: Render hello-world page."
- **Time-box.** If setup is taking > 25% of the slice's total estimate, the slice is too ambitious — split it.

---

## Process

1. Read the slice PRD and techspec.
2. List every Done-when checkbox in the PRD.
3. For each, identify the smallest task or merged-task that makes the box pass.
4. Order tasks vertically — each task moves a Done-when box closer to ✓.
5. Identify dependencies (Task N must come after Task M because…).
6. Identify parallelism (Tasks A, B can be done concurrently if a second pair of hands is available).
7. Cross-check: if Tasks 1–3 ship no user-observable behavior, restructure.

---

## Each task includes

- **Title** — action-oriented, imperative ("Add", "Wire", "Implement"), not vague ("Frontend stuff", "Make it work")
- **Description** — what needs to be done
- **Why this task is on the list** — what user-observable behavior moves forward (this is the anti-horizontal-scaffolding test)
- **Files affected** — concrete paths
- **Acceptance criteria** — testable checkboxes
- **Depends on** — task IDs or "None"
- **Complexity** — S / M / L (split if XL)
- **Status** — Not started / In progress / Done
- **Size budgets (when a file is size-sensitive):** distinguish a **hard cap** ("must stay ≤ N lines" — an AC, gate-enforced) from a **`~` forecast** ("~N lines" — planning data; variance is recorded, never failed). For a **shared cumulative file** that several tasks grow (a stylesheet, a page file), state each task's expected **delta** and the **final-slice ceiling** — a one-task estimate against a cumulative file misclassifies healthy growth as overrun.

Drop the heavy fields from the old template (assigned-to, retrospective, blockers placeholder, actual-complexity, implementation notes). Add them only if you actually need them in practice.

---

## Anti-pattern guards (reject these)

- **Reject Phase 1 / Phase 2 / Phase 3 / Phase 4 ordering.** Vertical only.
- **Reject "Setup" / "Foundation" tasks that don't bundle a user-observable touch.**
- **Reject testing-only tasks at the end.** Tests live with the task that creates the behavior. (Exception: end-to-end smoke test as the final slice-close task.)
- **Reject documentation tasks** unless the slice's PRD specifically requires docs.
- **Reject "polish" tasks at the end.** If something is needed for done-when, it's not polish — it's part of the relevant task.

---

## Output

Write to `specs/slices/slice-NN-<name>/tasks.md` (or host repo's existing convention).

Use `templates/tasks_template.md` as the structural base.

Output the tasks-overview table, then the task list, then the slice-close cross-check (do all Done-when checkboxes from the slice PRD have a corresponding task that makes them pass?).

## Communication style

- Action-oriented imperative for task titles
- Specific acceptance criteria (testable checkboxes, not "Component works")
- Concise — drop the boilerplate fields the old template asked for unless they earn their place
