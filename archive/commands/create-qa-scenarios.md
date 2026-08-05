---
description: Generate QA test scenarios for a slice (or end-of-project).
argument-hint: Slice number, slice folder name, or "project" for end-of-project scenarios.
---

# Goal

Generate QA test scenarios proportional to scope.

## Process

1. Create todo list.
2. Determine scope from $ARGUMENTS:
   - **Slice scope** (default): read the slice's PRD, techspec, and tasks. Generate scenarios for the slice's Done-when checklist + edge cases the techspec called out.
   - **Project scope** ("project"): read the master roadmap §8 (success criteria). Generate scenarios for the cross-cutting flows.
3. Identify scenarios for:
   - Happy path
   - Error conditions
   - Edge cases (from the techspec's open questions or noted edge cases)
   - Integration points (if cross-slice or external systems)
4. Prioritize each scenario (High / Medium / Low).
5. Flag which scenarios can be automated.
6. Write to:
   - Slice scope: `specs/slices/slice-NN-<name>/qa_scenarios.md`
   - Project scope: `specs/qa_scenarios.md`

## Output requirements

- Every Done-when box (slice scope) or success-criterion (project scope) maps to at least one scenario.
- Each scenario has steps + expected result + priority.
- Heavyweight sections (full browser/device matrix, accessibility full sweep, security audit) included ONLY when the scope demands them. For most slices, a tight functional scenario list is enough.
