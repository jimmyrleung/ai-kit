---
description: Start the feature integration process to help a developer to implement a new feature in an existing codebase (intended for small to medium size features).
argument-hint: File with high-level description of the feature to be built.
---

# Goal

Take a feature description and produce, in order, a reviewed **integration analysis**, a reviewed **techspec**, and a **tasks document** ready for implementation. Intended for **small-to-medium** features — large/extra-large work routes to the detailed per-command workflow.

This command is a thin orchestrator: each phase invokes a skill that owns the methodology, output contract, and confidence gate. The orchestrator owns only the glue — the size classifier, the size→skill routing, the review hand-offs, the phase wiring, and the output manifest.

## Process

Create a todo list with all phases, then go through them in order.

### Phase 1 — Initial Analysis

1. Read the feature described in `$ARGUMENTS` and classify its size: **S** (small) / **M** (medium) / **L** (large) / **XL** (extra large). Keep the chosen size in mind — Phases 3 and 5 route on it.
2. If **L or XL**: recommend the detailed per-command workflow instead — `/integration-analyze-feature` → `/integration-create-techspec` → `/integration-create-tasks` (which run the full multi-agent passes per phase) — and stop here.
3. Otherwise, use the `integration-analysis` skill with:
   - the feature description (`$ARGUMENTS`) as the requirement,
   - output file `{feature_name}_integration.md` (alongside the feature description),
   - the size (S vs M) as a hint for breadth (S: do it on the main thread; M: the skill may launch 2–3 `integration-analysis-agent` sub-agents).

   The skill handles the clarification questions, codebase exploration, consolidation (consensus / disagreement / confidence-weighted integration points), the ≥ 90% confidence gate, and writing the file.

When the skill hands back, proceed to [Phase 2].

### Phase 2 — Review Analysis

Use the `review-artifact` skill with:

- `artifact_path`: `{feature_name}_integration.md`
- `artifact_label`: `integration analysis`
- `reviewer_agent`: `integration-review-agent`
- `creator_agent`: `integration-analysis-agent`
- `support_docs`: the feature description document written by the user
- `next_step`: `Phase 3 — Plan implementation`

When the skill hands back, proceed to [Phase 3].

### Phase 3 — Plan implementation

Pick the techspec skill by the Phase-1 size:

- **S** → use the `pragmatic-techspec` skill (commits directly to the pragmatic approach — no 3-way parade).
- **M** → use the `integration-techspec` skill (explores minimal-changes / clean-architecture / pragmatic-balance in parallel, presents the trade-offs, you pick).

Inputs either way: the reviewed `{feature_name}_integration.md` from Phase 2 and the feature description. Output: `{feature_name}_techspec.md`. The skill handles mapping existing patterns, the ≥ 90% confidence gate, and writing the file.

When the skill hands back, proceed to [Phase 4].

### Phase 4 — Review implementation plan

Use the `review-artifact` skill with:

- `artifact_path`: `{feature_name}_techspec.md`
- `artifact_label`: `techspec`
- `reviewer_agent`: `integration-techspec-creator-agent` (review mode — review the existing techspec, don't author a new one; if the Phase-1 size was **S**, tell it to check against the `pragmatic-techspec` contract, otherwise the `integration-techspec` contract)
- `creator_agent`: `integration-techspec-creator-agent`
- `support_docs`: the feature description document; the integration analysis document
- `next_step`: `Phase 5 — Break down into tasks`

When the skill hands back, proceed to [Phase 5].

### Phase 5 — Break down into tasks

Pick the tasks skill by the Phase-1 size:

- **S** → use the `balanced-tasks-creation` skill (commits directly to balanced sizing).
- **M** → use the `integration-tasks` skill (explores granular / balanced / pragmatic in parallel, presents the trade-offs, you pick).

Inputs either way: the reviewed `{feature_name}_techspec.md` (authoritative), plus `{feature_name}_integration.md` and the feature description. Output: `{feature_name}_tasks.md`. The skill handles inventorying the techspec, ordering by dependencies, proposing an implementation order, the ≥ 90% confidence gate, and writing the file.

When the skill hands back, this command is complete — the tasks document is ready for implementation (`/implement-task` per task).

## Size routing at a glance

| Phase 1 size | Phase 3 (techspec) | Phase 5 (tasks) |
| ------------ | ------------------ | --------------- |
| **S** | `pragmatic-techspec` skill (single approach) | `balanced-tasks-creation` skill (single sizing) |
| **M** | `integration-techspec` skill (3-way explore) | `integration-tasks` skill (3-way explore) |
| **L / XL** | — bail to `/integration-create-techspec` | — bail to `/integration-create-tasks` |

## Output documents

Written alongside the user's feature description, sharing its base name:

- `{feature_name}_integration.md` — integration analysis (reviewed; carries a `## Review` section)
- `{feature_name}_techspec.md` — techspec (reviewed; carries a `## Review` section)
- `{feature_name}_tasks.md` — implementation tasks
