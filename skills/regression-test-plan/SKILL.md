---
name: regression-test-plan
description: Create a comprehensive regression test plan for a bug fix — bug-fix verification, related-functionality, integration, and performance tests, driven by the impact analysis. Produces {bug_id}_regression_test_plan.md. Use ad-hoc, or as Phase 5 of /full-bug-fix-workflow and the body of /bug-regression-test.
---

# Regression Test Plan Skill

You take a bug fix (the reviewed investigation + impact analysis) and produce a concrete, repeatable regression test plan: verify the bug is actually fixed, exercise everything the impact analysis flagged, cover the integration paths, and check for performance regressions. Tests must be specific and actionable — not "test the save flow" but the exact steps, inputs, expected result, and pass/fail criteria.

This is a single-approach skill — there's no 3-way exploration and no sub-agent fan-out; one person produces one plan.

## When to use

- **Ad-hoc**: a fix has been (or is about to be) implemented and you want the validation plan.
- **Orchestrated**: Phase 5 of `/full-bug-fix-workflow`, or the body of `/bug-regression-test`.

## When NOT to use

- The fix isn't designed yet — you need the reviewed investigation and impact analysis first.
- You want the *implementation* checklist (that lives in the implementation phase / `/implement-bug-fix`), not a test plan.

## Input contract

- **Bug report** (`{bug_id}.md`), **reviewed investigation** (`{bug_id}_investigation.md`), **impact analysis** (`{bug_id}_impact_analysis.md`) — the impact analysis is the primary driver of *what* to test. If the impact analysis doesn't exist (ad-hoc, fix already made), reconstruct the affected-area list from the diff and the investigation, and say so.
- **`{bug_id}` base name** — derive from the input filenames.
- **Test tooling** — note whether Playwright / Selenium / other test runners are available (via MCP or the project's own suite). If they are, *execute* the tests programmatically, report results, capture failures. If not, produce detailed manual steps.

## Process

1. **Pull the affected surface** from the impact analysis: direct dependencies, indirect dependencies, shared state, related features, the test gaps it identified.
2. **Bug-fix verification tests** — the original bug scenario no longer reproduces; bug-related edge cases are handled; error conditions are handled correctly.
3. **Related-functionality tests** — for each item in the impact analysis: direct dependencies still work, indirect dependencies are unaffected, shared state behaves, side effects function as expected.
4. **Integration tests** — workflows that involve the changed code: end-to-end scenarios complete, data flows correctly through the system, external systems integrate properly.
5. **Performance tests (if applicable)** — response times within range, no increase in DB queries, stable memory, cache performance maintained. Use the impact analysis's baseline figures if it has them; otherwise note the threshold and leave the baseline to be filled.
6. **Make each test concrete** — description, numbered steps, inputs/test data, expected result, an `Actual Result` placeholder, and a `[ ] Pass / [ ] Fail` status. Cover happy path *and* error scenarios. Note test-data and environment requirements.
7. **Execute if you can** — if a test runner is available, run the suite (or the subset that applies), fill in actual results, capture screenshots/logs of failures, and surface anything broken before handing back.
8. **Write the plan** to `{bug_id}_regression_test_plan.md` using the structure in `templates/regression-test-plan-template.md`, then present the test plan to the user (verification tests · related-functionality tests · integration tests · performance tests) and provide the final checklist (bug fix verified · related features tested · no regressions found · ready for deployment).

## Output file

Write the plan to `{bug_id}_regression_test_plan.md`, alongside the bug report and the other bug artifacts. Scaffold: `templates/regression-test-plan-template.md` in this skill's directory.
