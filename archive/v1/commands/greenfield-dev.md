---
description: Start a new greenfield project. Mode-aware iterative slicing workflow.
argument-hint: Optional path to product requirement file with mode hint, or describe the project inline.
---

# Goal

Build a new feature / product / experiment using **vertical slices**. Avoid horizontal scaffolding. Validate the path early.

## What this workflow is for

Four discovery modes, all supported:

- **One-off / quick experiment** — single throwaway script or test
- **MVP to validate an idea** — small slicing (~3–5 slices), demoable fast
- **New full product** — full roadmap with master spec
- **Exploratory in existing repo** — prototype something without established patterns; lives in the host repo's structure

For execution-mode work in an existing repo (patterns are clear, you're "fitting" something in), use **`/integration-feature-dev`** instead.

## Process

### Phase 0 — Mode + light architecture chat

1. Create todo list.
2. Read $ARGUMENTS if a file path is given; otherwise prompt the user to describe the project.
3. **Ask the user explicitly which mode this is:**
   - One-off / quick experiment
   - MVP to validate an idea
   - New full product
   - Exploratory in existing repo
4. Capture the mode in conversation. If a product requirement file exists, suggest the user adds the mode hint to the file.
5. **For new-product mode:** brief architecture chat — major shape decisions (tech stack, monorepo, deployment shape, frontend/backend split). Capture conclusions; they flow into the master roadmap §4 (principles) and §N+3 (carried-forward).
6. **For exploratory mode:** brief location chat — *"Where does this fit in the existing repo? What existing pieces are we anchoring to vs. deliberately leaving alone?"* The host repo IS the foundation; don't propose new architecture.
7. **For one-off / MVP modes:** skip the architecture chat. Go straight to Phase 1 with whatever's most expedient.

### Phase 1 — Master roadmap (skip for one-off)

8. Run **`/create-roadmap`** with the product requirement file (or the captured Phase 0 conversation if no file).
9. The roadmap doc is mode-aware — minimal Part I for MVP / exploratory, full Part I for new-product.
10. Confirm the slice list with the user before proceeding. **Slice 1 MUST ship user-observable behavior.**

### Phase 2–5 — Per-slice loop

For each slice the user picks up (lowest-numbered incomplete first):

11. **`/create-prd <slice>`** — slice's PRD. Just-in-time, not pre-written.
12. **`/create-techspec <slice>`** — slice's techspec.
13. **`/review-techspec <slice>`** — optional; skip for small slices with high-confidence techspecs.
14. **`/create-tasks <slice>`** — slice's tasks (vertically ordered).
15. **`/gf-implement-task slice=<slice> task=<N>`** per task — implement, test, review, mark done.
16. **Slice close** — verify the slice PRD's Done-when checklist passes. "While we're here" additions go to the **next slice's backlog**, not the current slice.

### Phase 6 — QA scenarios

17. **`/create-qa-scenarios <slice>`** — invoke per slice on slice close, OR
18. **`/create-qa-scenarios project`** at major project milestones for cross-cutting flows.

---

## Mode-specific behavior at a glance

| Mode         | Phase 0           | Roadmap (Phase 1)             | Slices       | Notes                                                                                   |
| ------------ | ----------------- | ----------------------------- | ------------ | --------------------------------------------------------------------------------------- |
| One-off      | skip              | skip                          | 0 (just code) | Drop straight to writing code. Optionally `/create-prd` for a minimal slice PRD if you want any structure. |
| MVP          | skip              | minimal Part I + 3–5 slices   | 3–5          | Demoable fast. Done-when is loose.                                                      |
| New product  | architecture chat | full Part I + Part II         | 8–20         | Trip_planner shape — full master spec.                                                  |
| Exploratory  | "where does this fit?" chat | minimal Part I + slice list | 2–10        | Slices live in host repo's spec convention. §N+3 = the existing repo.                   |

---

## Anti-pattern guards (this workflow exists to avoid these)

- **Reject "Phase 1: Foundation / Phase 2: Core / Phase 3: Integration / Phase 4: Polish" task ordering.** Vertical only.
- **Reject one big upfront PRD/techspec/task list for the whole project.** PRD per slice, techspec per slice, tasks per slice. Just-in-time.
- **Reject infrastructure-only first slices.** Slice 1 must ship user-observable behavior.
- **Reject "while we're here" scope creep.** Scope-creep additions go to the next slice's backlog, never the current slice.
- **Reject premature commitments** in techspecs — Performance / Security / Monitoring / Deployment sections are escape hatches, not defaults.

## Output documents (across the full workflow)

- `specs/00-roadmap.md` — master roadmap (skip for one-off)
- `specs/slices/slice-NN-<name>/PRD.md` — per slice
- `specs/slices/slice-NN-<name>/techspec.md` — per slice
- `specs/slices/slice-NN-<name>/tasks.md` — per slice
- `specs/slices/slice-NN-<name>/qa_scenarios.md` — per slice (optional)
- `specs/qa_scenarios.md` — project-level (optional, at milestones)

For exploratory mode, paths follow the host repo's existing convention.
