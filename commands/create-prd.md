---
description: Create a per-slice PRD. Run once per slice as you pick them up (just-in-time).
argument-hint: Slice number, slice folder name, or "next" for the next incomplete slice.
---

# Goal

Create a self-contained PRD for one slice. **Just-in-time** — invoke when you're about to start the slice, not all upfront.

For the master roadmap (one-time per project), use `/create-roadmap` instead.

## Process

1. Create todo list.
2. Read the master roadmap if present (typically `specs/00-roadmap.md`).
3. Identify the slice from $ARGUMENTS — number, name, or "next" for the next incomplete slice in §N+4.
4. Read prior slice PRDs/techspecs for context (especially the most recent — patterns there often carry forward).
5. Launch 1 @prd-creation skill agent. Provide:
   - The roadmap (if present)
   - The slice's row from §N+4
   - Prior-slice context as relevant
   - The slice number + name
6. Ask clarifying questions if needed (max 2 rounds — slice PRDs are lighter than master roadmaps).
7. Confirm with user.
8. Write to `specs/slices/slice-NN-<name>/PRD.md` (or host repo's convention).

## Quality gates

- §1 Summary names the **demoable behavior** in user-observable terms.
- Out-of-scope items each point to **which later slice** owns the deferred item.
- Done-when is concrete checkboxes — every box testable by opening the product or running a single command.
- No "set up X" goals; no Performance / Security / Monitoring / Deployment sections unless this slice demands them.
- Confidence ≥ 90%.

## When the master roadmap is missing (one-off mode or skipped roadmap)

If there's no master roadmap, the slice PRD is still valid — it just stands alone instead of referencing a roadmap. Trim §10 References to whatever exists. The §1 Summary's demoable-behavior requirement still applies.
