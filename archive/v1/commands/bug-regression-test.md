---
description: Create a comprehensive regression test plan for a bug fix.
argument-hint: <bug_file> <impact_analysis_file> <bug_id>
arguments: bug_file impact_analysis_file bug_id
---

# Regression Test Command

This command is a thin shim: the `regression-test-plan` skill owns the methodology, the output structure, and the template.

1. Create a todo list with the steps for this command.
2. Use the `regression-test-plan` skill with:
   - `$bug_file` as the bug report,
   - `$impact_analysis_file` as the impact analysis (the primary driver of what to test),
   - the reviewed `${bug_id}_investigation.md` if available,
   - output file `${bug_id}_regression_test_plan.md` (alongside the bug report).

   The skill builds the bug-fix-verification / related-functionality / integration / performance tests, makes each test concrete (steps, inputs, expected result, pass/fail), executes them if a test runner is available (otherwise produces detailed manual steps), and writes the file using its `templates/regression-test-plan-template.md`.

When the skill hands back, this command is complete.
