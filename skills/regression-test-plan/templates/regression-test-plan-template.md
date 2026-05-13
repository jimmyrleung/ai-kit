# Regression Test Plan Template

Copy this structure into `{bug_id}_regression_test_plan.md`. Repeat the numbered `Test N.M` blocks as needed; drop the Performance section if it doesn't apply.

---

# Regression Test Plan: {bug_id}

## Test Execution Summary

- [ ] All tests defined
- [ ] All tests executed
- [ ] All tests passed

## 1. Bug Fix Verification

### Test 1.1: Original Bug Scenario

**Description:** [Describe the test — the exact scenario from the bug report]
**Steps:**
1. [Step 1]
2. [Step 2]

**Expected Result:** [What should happen now that it's fixed]
**Actual Result:** [Fill in after testing]
**Status:** [ ] Pass / [ ] Fail

### Test 1.2: Edge Case — [Description]

[Same format as Test 1.1]

## 2. Related Functionality Tests

> One block per item the impact analysis flagged (direct deps, indirect deps, shared state, side effects).

### Test 2.1: [Feature / Dependency Name]

[Same format as above]

## 3. Integration Tests

### Test 3.1: [Workflow Name]

[Same format as above]

## 4. Performance Tests

> Drop this section if not applicable.

### Test 4.1: [Performance Metric]

**Metric:** [e.g., response time for preferences save]
**Baseline:** [from the impact analysis, if available — else "TBD"]
**After Fix:** [Fill in after testing]
**Threshold:** [e.g., < 500ms]
**Status:** [ ] Pass / [ ] Fail

## Test Environment

- **Environment:** [Staging / Local / etc.]
- **Database:** [Clean state / Seeded / etc.]
- **Test Data:** [Description of test data used]
- **Browser/Client:** [If applicable]

## Issues Found

[Document any issues discovered during testing]

## Sign-Off

- [ ] All critical tests passed
- [ ] All medium-priority tests passed
- [ ] Performance within acceptable range
- [ ] No new issues introduced
- [ ] Ready for deployment

**Tested By:** [Name]
**Date:** [Date]
