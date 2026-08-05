---
description: Start the full bug fix workflow to help a developer investigate, fix, and validate a bug (intended for small to medium bugs).
argument-hint: File with the bug report description.
---

# Goal

- Thoroughly investigate the bug and identify the root cause.
- Review the investigation for accuracy.
- Analyze the impact of the proposed fix.
- Guide implementation with proper testing.
- Create a regression test plan for validation.

Intended for **small-to-medium** bugs — large/extra-large work routes to the detailed per-command workflow.

This command is a thin orchestrator: each phase invokes a skill that owns the methodology, output contract, and confidence gate. The orchestrator owns only the glue — the complexity classifier and the L/XL bail-out, the review hand-off, the manual-implementation phase, the phase wiring, the quality-gate table, and the output manifest.

## Process

Create a todo list with all phases, then go through them in order.

### Phase 1 — Investigation

1. Read the bug report in `$ARGUMENTS` and classify its complexity:
   - **S** (small) — single file, obvious cause
   - **M** (medium) — multiple files, moderate complexity
   - **L** (large) — system-wide, complex root cause
   - **XL** (extra large) — architectural issue, high risk
2. If **L or XL**: recommend the detailed per-command workflow instead — `/investigate-bug` → `/review-investigation` → `/analyze-impact` → `/implement-bug-fix` → `/bug-regression-test` (which run the full multi-agent passes per phase) — and stop here.
3. Otherwise, use the `bug-investigation` skill with:
   - the bug report (`$ARGUMENTS`) as the input,
   - `{bug_id}` derived from the bug report's filename,
   - the complexity (S vs M) as a hint for breadth (S: do it on the main thread; M: the skill may launch 1–3 `bug-investigation-agent` sub-agents).

   The skill handles the clarification questions, codebase exploration and execution-path tracing, consolidation (consensus on root cause / disagreement / confidence-weighted findings), the ≥ 90% confidence gate, and writing `{bug_id}_investigation.md`.

When the skill hands back, proceed to [Phase 2].

### Phase 2 — Review Investigation

Use the `review-artifact` skill with:

- `artifact_path`: `{bug_id}_investigation.md`
- `artifact_label`: `investigation`
- `reviewer_agent`: `bug-investigation-reviewer-agent`
- `creator_agent`: `bug-investigation-agent`
- `support_docs`: the bug report (`$ARGUMENTS`)
- `next_step`: `Phase 3 — Impact Analysis`

When the skill hands back, proceed to [Phase 3].

### Phase 3 — Impact Analysis

Use the `impact-analysis` skill with:

- the bug report (`$ARGUMENTS`) and the reviewed `{bug_id}_investigation.md` from Phase 2 as inputs,
- `{bug_id}` as before,
- the complexity (S vs M) as a hint for breadth (S: main thread; M: the skill may launch 1–3 `impact-analysis-agent` sub-agents).

The skill handles dependency mapping (direct + indirect), test-coverage assessment, risk-level scoring (Low / Medium / High / Critical), the rollback strategy, the SAFE-TO-IMPLEMENT / WITH-CAUTION / REQUIRES-ADDITIONAL-REVIEW recommendation, the user-approval gate, and writing `{bug_id}_impact_analysis.md`.

When the skill hands back, proceed to [Phase 4].

### Phase 4 — Implementation (Manual)

This phase is executed manually by the developer (or via `/implement-bug-fix`). Provide guidance:

1. Present implementation guidance based on the reviewed investigation and the impact analysis:
   - Files to modify (with line numbers)
   - Proposed solution approach
   - Test requirements
   - Rollback plan
2. Implementation checklist:
   - [ ] Code implements the proposed solution
   - [ ] Code follows project standards
   - [ ] Unit tests added for the bug scenario
   - [ ] Unit tests added for edge cases
   - [ ] All existing tests pass
   - [ ] No unintended changes
3. If during implementation a critical issue surfaces that needs refactoring, STOP — document it and get explicit approval before proceeding. Do not mix bug fixes with refactoring.
4. Ask the user to confirm when implementation is complete before proceeding to [Phase 5].

### Phase 5 — Regression Testing

Use the `regression-test-plan` skill with:

- the bug report (`$ARGUMENTS`), the reviewed `{bug_id}_investigation.md`, and `{bug_id}_impact_analysis.md` as inputs,
- `{bug_id}` as before,
- whether test tooling (Playwright / Selenium / the project's suite) is available — if so, the skill executes the tests; if not, it produces detailed manual steps.

The skill writes `{bug_id}_regression_test_plan.md` (bug-fix verification · related-functionality · integration · performance tests) and provides the final checklist. When it hands back, this command is complete.

## Output Documents

At the end of this workflow you should have created (alongside the bug report):

1. `{bug_id}_investigation.md` — root cause analysis with evidence (reviewed; carries a `## Review` section)
2. `{bug_id}_impact_analysis.md` — risk assessment and rollback strategy
3. `{bug_id}_regression_test_plan.md` — test plan for validation

## Quality Gates

- Phase 1 → Phase 2: investigation confidence ≥ 90%
- Phase 2 → Phase 3: review confidence ≥ 90% (review-artifact)
- Phase 3 → Phase 4: user approval of the risk level
- Phase 4 → Phase 5: user confirms implementation complete
- Phase 5 → Done: all tests pass
