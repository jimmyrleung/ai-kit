---
description: Create the master roadmap and slice list for a project (run once at project start).
argument-hint: Path to the product requirement file with the mode hint filled in.
---

# Goal

Create the master roadmap document — Part I (product spec, mode-aware weight) and Part II (slice list).

This command runs **once** at project start. After it's done, individual slices use `/create-prd` to write per-slice PRDs at slice pickup time.

## When to use

- Mode = **MVP** / **new-product** / **exploratory**.
- Skip this command entirely for mode = **one-off** — go straight to coding, or invoke `/create-prd` for a minimal slice PRD if you want any structure.

## Process

1. Create todo list.
2. Read the product requirement file from $ARGUMENTS.
3. **Verify the mode hint is filled in.** If missing, ask the user to pick one of: one-off / mvp / new-product / exploratory.
4. If mode = `one-off`, exit with: *"Roadmap not needed for one-off mode. Either start coding directly, or invoke `/create-prd` for a minimal slice PRD."*
5. Conduct light discovery, mode-scaled:
   - **New-product:** brief architecture chat. Major shape decisions (tech stack, monorepo, deployment shape, frontend/backend split). Capture conclusions for Part I §4 (principles) and Part II §N+3 (carried-forward).
   - **MVP:** identify the minimum viable shape. Lighter than new-product. Skip principles unless one is genuinely cross-cutting.
   - **Exploratory:** identify the host repo's spec convention (look for existing `specs/`, `docs/`, `design/`). Identify the existing carried-forward code that's the foundation. Identify the reference being adopted (paper, article, demo). The Part II §N+3 is the existing repo itself.
6. Ask clarifying questions if anything critical is unclear (max 3 rounds).
7. Launch @roadmap-creation skill:
   - 1 agent for one-off / MVP
   - 2–3 agents for new-product / exploratory (different priors — e.g., one favoring fewer larger slices, one favoring more thinner slices)
8. Compare outputs if multiple agents launched. Surface disagreements (esp. around slice list shape).
9. Confirm with user before writing.
10. Write to:
    - **New-product:** `specs/00-roadmap.md`
    - **MVP:** `specs/00-roadmap.md`
    - **Exploratory:** follow host repo's spec convention (auto-detect existing `specs/` or `docs/` folders; ask user if unclear)

## Quality gates

- Slice 1 ships user-observable behavior (not "set up project").
- No "Phase 1: Foundation / Phase 2: Core" structure in the slice list — vertical only.
- Confidence ≥ 90%.

## Output

Path is mode-dependent (see step 10).
