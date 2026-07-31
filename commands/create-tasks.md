---
description: Break the slice's techspec into vertically-ordered tasks. Anti-horizontal-scaffolding.
argument-hint: Slice number or slice folder name.
---

# Goal

Decompose a single slice's techspec into ordered, actionable tasks.

## Process

1. Create todo list (if a todo tool is available in this harness; otherwise track inline).
2. Read the slice PRD and techspec.
3. Launch @tasks-creation skill agents:
   - **1 agent** for small slices
   - **2 agents** for typical/complex slices (different priors — granular vs. balanced)

   If subagents are unavailable in this harness, run the skill body inline per draft — note
   the substitution.
4. Compare outputs. Surface ordering disagreements (esp. whether tasks 1–3 ship user-observable behavior).
   Also diff the drafts' factual corrections separately from their ordering — port every
   verified correction from the losing draft (a rejected draft supplied both corrections in a
   lived run). When any task renames a symbol, grep repo-wide and assign every call site to
   that task (a 3-of-4 coverage left tasks 3–6 red).
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
