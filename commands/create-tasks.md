---
description: Break the slice's techspec into vertically-ordered tasks. Anti-horizontal-scaffolding.
argument-hint: Slice number or slice folder name.
---

# Goal

Decompose a single slice's techspec into ordered, actionable tasks.

## Process

1. Create todo list.
2. Read the slice PRD and techspec.
3. Launch @tasks-creation skill agents:
   - **1 agent** for small slices
   - **2 agents** for typical/complex slices (different priors — granular vs. balanced)
4. Compare outputs. Surface ordering disagreements (esp. whether tasks 1–3 ship user-observable behavior).
5. Recommend one. User picks.
6. Write to `specs/slices/slice-NN-<name>/tasks.md`.

## Quality gates

- **Anti-horizontal-scaffolding check:** read tasks 1–3. Do they ship any user-observable behavior, or are they pure infrastructure? If the latter, restructure before writing.
- Each task has a **"Why this task is on the list"** line naming the user-observable behavior it moves forward.
- Tasks are 2–8 hours. Larger → split. Smaller → merge.
- Every Done-when checkbox in the slice PRD has at least one task that makes it pass (slice-close cross-check).

## Anti-patterns to reject

- "Phase 1: Foundation / Phase 2: Core / Phase 3: Polish" ordering
- Setup tasks that don't bundle a user-observable touch
- Testing-only tasks at the end (tests live with the task that creates the behavior)
- "Polish" tasks at the end (if it's needed for done-when, it's not polish)
