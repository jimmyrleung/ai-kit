---
description: Design the technical approach for a single slice. Run after the slice's PRD is approved.
argument-hint: Slice number or slice folder name.
---

# Goal

Create a slice-scoped technical specification. **Slice-scoped, not project-wide.**

## Process

1. Create todo list.
2. Read the slice PRD (`specs/slices/slice-NN-<name>/PRD.md` or host repo convention).
3. Read the master roadmap §N+3 (carried-forward) and prior-slice techspecs (patterns established).
4. Read the **actual code** referenced in the slice PRD's "Building on" section — don't trust descriptions; read the files.
5. For exploratory-in-existing-repo mode: read host repo conventions (folder layout, idioms, test patterns). Anchor to those.
6. Launch @techspec-creation skill agents in parallel:
   - **1 agent** for small slices (size = 1 day or simple)
   - **2 agents** for typical slices (different priors — e.g., favor simplicity vs. favor reuse of existing patterns)
   - **3 agents** only for genuinely complex slices
7. Compare outputs. Surface disagreements (esp. around key decisions).
8. Form your opinion. Recommend one to the user with reasoning.
9. User picks. Write to `specs/slices/slice-NN-<name>/techspec.md`.

## Quality gates

- **Default sections only:** Summary / Approach / Key Decisions / File Changes / Test Approach / Open Questions / Confidence.
- **Escape-hatch sections** (Performance / Security / Monitoring / Deployment / Migration / Documentation) — include ONLY if this slice demands them. Reject by default.
- File changes are concrete paths for THIS slice — no speculative future structure.
- Confidence ≥ 90%.
