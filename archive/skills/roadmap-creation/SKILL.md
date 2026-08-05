---
name: roadmap-creation
description: Create the master roadmap (Part I product spec + Part II slice list) for a project. Mode-aware. Anti-horizontal-scaffolding by design.
---

# Roadmap Creation Skill

You produce the master roadmap document — `00-roadmap.md` — that combines product spec (Part I) and slice list (Part II). Run **once** at project start.

For per-slice PRDs (run as the user picks up each slice), use the `prd-creation` skill instead.

## Goal

Produce a single `00-roadmap.md` that combines product spec (Part I) and slice list (Part II). Mode-aware section weight.

## Process

1. Read the user's product requirement file. Identify the project mode (one-off / mvp / new-product / exploratory).
2. **One-off mode** — output: *"Roadmap not needed for one-off. Either start coding directly, or invoke `/create-prd` for a minimal slice PRD."* and stop.
3. **MVP / new-product / exploratory** — conduct light discovery:
   - **New-product:** capture the major architectural shape decisions discussed with the user (tech stack, monorepo, deployment shape). These flow into Part I §4 (principles) and Part II §N+3 (carried-forward, even if empty).
   - **Exploratory:** capture "where does this fit in the existing repo" and "what existing pieces are we anchoring to vs. deliberately leaving alone." The host repo IS the Part II §N+3.
   - **MVP:** keep Part I minimal; the slice list is the meat.
4. Ask clarifying questions if anything critical is unclear (max 3 rounds).
5. Generate the roadmap using `templates/roadmap_template.md` as the structural base.

## Mode-aware section weight

| Section                              | One-off | MVP        | New product | Exploratory                       |
| ------------------------------------ | ------- | ---------- | ----------- | --------------------------------- |
| Executive summary                    | n/a     | brief      | full        | brief                             |
| Product principles                   | n/a     | optional   | full        | optional                          |
| Domain model                         | n/a     | light      | full        | optional                          |
| User journey                         | n/a     | optional   | full        | optional                          |
| Carried-forward (Part II §N+3)       | n/a     | optional   | "ready-but-idle" foundation | full — repo IS the foundation |
| Slice list                           | n/a     | 3–5 slices | 8–20 slices | 2–10 slices                       |

## Slicing rules (apply to Part II for any non-one-off mode)

1. **Slice 1 must ship user-observable behavior.** Even a stub. No "set up the project" as a slice.
2. **Each slice ships demoable behavior.** The user can open the product and notice something new.
3. **Slice size: 1–3 days.** If larger, split. If a slice estimates >3 days, the slice list is wrong, not the slice.
4. **Scope-creep rejection is a slice-close ceremony.** "While we're here" goes to the next slice's backlog.
5. **Patterns / design systems are pulled in when demanded by a slice, not preemptively.**
6. **PRD per slice is just-in-time at slice pickup.** Don't pre-write slice 13's PRD now.

## Anti-pattern guards (reject these in the slice list)

- **Reject "Phase 1: Foundation" / "Phase 2: Core" / "Phase 3: Integration" / "Phase 4: Polish" structure.** That's horizontal scaffolding.
- **Reject slice 1 = "set up project"** with no UI/output.
- **Reject any slice whose outcome is "infrastructure ready"** without demoable behavior.
- If a slice would naturally start with infrastructure-only work, **invert** — pick the demoable behavior the user would see, then the infrastructure becomes part of that slice's natural scope.

## Confidence

Score 0–100% before completing. Target ≥ 90%. Below 90%, ask clarifying questions and iterate.

## Output

Write to the path the orchestrator specifies:

- New-product / MVP → `specs/00-roadmap.md`
- Exploratory → host repo's existing convention (auto-detect existing `specs/` or `docs/` folders; ask user if unclear)

Confirm the path with the user before writing.

## Communication style

- Concise, decisive
- Reference sections by number (`§4 principle 8`, `§7 S6`) — improves grep-ability
- Don't include planning material the reader doesn't need ("here are the steps I followed to write this") — write the roadmap, not a meta-document
