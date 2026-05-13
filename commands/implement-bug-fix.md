---
description: Implement a bug fix based on the reviewed investigation and impact analysis.
argument-hint: <bug_file> <reviewed_investigation_file> <impact_analysis_file>
arguments: bug_file reviewed_investigation_file impact_analysis_file
---

# Implement Bug Fix Command

Implement the bug fix based on the investigation and impact analysis:

**Bug File:** $bug_file

**Reviewed Investigation:** $reviewed_investigation_file

**Impact Analysis:** $impact_analysis_file

## Implementation Requirements

### Follow the Proposed Solution

- Implement the fix exactly as described in the reviewed investigation taking into account the impact analysis
- Reference the specific files and line numbers identified
- Keep changes minimal and focused on the root cause

### Code Quality Standards

- Match existing coding style and conventions
- Follow project's architecture patterns
- Add minimal, necessary comments only
- If you find critical issues during implementation that require refactoring, STOP and document them for explicit approval

### Testing Requirements

- Add unit tests that:
  - Cover the bug scenario that was fixed
  - Test edge cases identified in impact analysis
  - Verify the fix works correctly
- Update existing tests if they're affected by the change
- Ensure all tests pass before completing

### Documentation

- Update inline comments if behavior changed significantly
- Note any deviations from the proposed solution and explain why
- Document any assumptions made during implementation

## Implementation Checklist

Before marking as complete, ensure:

- [ ] Code implements the proposed solution
- [ ] Code follows project standards
- [ ] Unit tests added for bug scenario
- [ ] Unit tests added for edge cases
- [ ] Existing tests updated if needed
- [ ] All tests pass
- [ ] No unintended behavior changes
- [ ] **Verify (use the `verify-task` skill).** Run with:
  - `task_id`: the bug-fix task identifier (usually the `$bug_file`'s bug_id, or the single
    task in the bug's tasks-doc if one exists)
  - `tasks_doc_path`: the bug's tasks-doc — or `$bug_file` if there's no separate tasks-doc
  - `prefix`: `$bug_file` (or the bug's prefix)

  The skill runs gates 1+2+3 (build/test, AC checklist, cross-cutting) against the bug-fix's
  ACs (from the investigation), the files touched, and any line / SDK budgets the impact
  analysis pinned. Records a `## Verify — {date}` block. Halt on any gate fail until resolved.
- [ ] Code is ready for review

## Critical: Refactoring Gate

If during implementation you discover:

- Critical bugs in surrounding code
- Architectural issues that should be addressed
- Code that should be refactored for safety

You MUST:

1. STOP implementation
2. Document the critical issue
3. Propose the refactor separately
4. Get explicit approval before proceeding

Do NOT mix bug fixes with refactoring, even in auto-accept mode.

## Output

After implementation, provide:

1. Summary of changes made
2. Files modified with change descriptions
3. Tests added/modified
4. Any deviations from the plan and rationale
5. Confirmation that all tests pass

## Closeout suggestion

Implementation complete. **Suggest** `/qa-gates prefix=$bug_file` (or the bug's investigation /
impact-analysis prefix — whichever the docs live under) to verify the fix against the
investigation and impact-analysis docs (build/test → AC → cross-cutting → docs → human go/no-go)
before declaring the bug fixed. The user invokes it; this command does not auto-execute.
