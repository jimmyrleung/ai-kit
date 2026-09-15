---
name: qa-execution
description: "Verifies a finished implementation against its requirements, spec, implementation plan, and/or tasks. Includes build, tests (unit/integration/e2e), and live validation when applicable with available tools. Apply any corrections or improvements found during the process, and provide a final report with evidences. Use when the user asks for executing QA for a given implementation. Task implementation belongs to implement-task; code-quality review to review-implementation."
---

# QA execution

This is a focused QA execution to:

- Confirm a given implementation has the intended behavior with live validation
- Ensure all acceptance criteria are verified and passes
- When available, confirm the goals from the requirements doc are met (usually produced with the `define-reqs` skill)
- Find the root cause of issues that arise during the validation and fix them, hardening the regression tests by adding new test cases to cover them
- Record evidence of the validation

**IMPORTANT**: you should NOT review code, you should verify the outcome.

## Real-world testing

The idea is for that QA execution to be as close as possible to a QA engineer or similar validating a given implementation, so it is expected that you use appropriate tools to simulate that behavior, for instance:

- For UI/front-end, it is expected that you use browser tools like playwright MCP, devtools MCP, agent browsers tools or similar.
- For back-end implementation it is expected that you use appropriate tools to validate the implementation too:
  - For API calls, it is expected that you use tools to perform requests and analyze responses
  - For database it is expected that you use MCPs like toolbox or cli tools (`sqlcmd`, `psql`, etc.) to validate how the data lande
  - For workers, it is expected that you analyze available execution logs
- And so on

## Approach

**The approach should follow each subsection below sequentially.**

### Initial context

1. Read all available references for the implementation you are going to QA: specs (PRD/requirements/techspec/tasks docs/implementation plan/etc.), files, past implementation history, etc.

2. Read the AGENTS.md file(s) and any referenced documents in it (especially rules) to gather context from each project involved in the implementation to be reviewed.

3. Build a list with one verification item per acceptance criteria, and if the implementation includes test scenarios (unit/integration/e2e), associate the verification items with the test scenarios too. This step is completed when each acceptance criteria item have at least one verification item and at least one test scenario (when available) associated.

4. Write the initial QA report following the template `skills\qa-execution\references\TEMPLATE.md` under `./specs/[slug]/qa.md`. It is the final outcome that should have all details of the QA execution. Sections that will still be ran (automated tests, accessibility tests, conclusion, etc. can be blank for now).

### Prepare

1. List everything you need up and running for doing the live validation of the implemented feature, making sure you have everything you need. Go back to the user with anything you need them to launch that you can't do by yourself.

2. Launch everything and confirm it is up and running and healthy. This step is complete when you have evidence that each element you need for the live validation is running as expected.

- For APIs, it can be a successful response on the /health endpoint or similar
- For UI, launch the browser using an available browser tool and confirm you can see the app
- For database (usually running on docker on local), ensure it is listening on the port it should listen and that you can do a no-op query or similar
- etc.

### Execute

Validate each verification item according to their acceptance criteria using the available tools to perform the validation and verify the outcome, including:

- If the application had the intended behavior
- If the application is in the expected state
- If any relevant data is in the expected state (applicable when interacting with data stores)
- If the UI matches the expected design (applicable when interacting with UI/front-end) and responsiveness looks good as well
- etc.

For each verification item:

- Update it in the QA report, marking it as PASS or FAIL and adding any relevant details
- Capture evidences of the QA execution regardless if they passed or failed, and persist to `.specs/[slug]/evidences/`. Link the evidence to the respective verification item in the QA report
  - Example of evidences: logs (application logs, browser logs, etc.), request/response (url, header, payload), screenshots, UI state, detailed description and/or workflow tracing, etc.
- For failed items, add a new bug to the [Bugs found and fixed] section, and reference it in the [Acceptance criteria verified] section

This step is completed when each verification item is marked as PASS or FAIL with their respective evidences collected and referenced.

### Automated tests

1. Verify that each acceptance criteria is covered by automated tests.

2. Execute the existing test suites to confirm everything passes (e2e/integration/unit tests).

3. If the repo has a test coverage target, ensure it is met.

4. Register the verification and execution results in the QA report

This step is completed when all test suites have been executed.

### Accessibility testing

**Only applicable for UI work**: on each screen, use the available browser tool to test keyboard navigation and verify labels and semantics:

- [ ] Keyboard navigation (Tab, Enter, Esc)
- [ ] Interactive elements with descriptive labels
- [ ] Images with appropriate alternative text (`alt`)
- [ ] Adequate color contrast
- [ ] Forms with labels associated with their fields
- [ ] Clear and accessible error messages
- [ ] Appropriately sized fonts

### Fix and revalidate

For each registered bug in the [Bugs found and fixed] section:

- Provide a root cause fix. Do not mask the symptoms
- Add/update a regression test that fails without the fix
- Revalidate to confirm it passes
- When it passes, update the status in both the [Bugs found and fixed] and [Acceptance criteria verified] sections of the QA report and add details for the fix, including new collected evidence to confirm it is working.

**IMPORTANT**: if the fix requires a change in the implementation plan or techspec, pause and request approval for the user providing details (why is it needed, what will be done, etc.)

This step is completed when each failed item of the QA report passes and has associated tests covering it, or when the failed item is explicitly blocked by the user.

### Post-execution

1. Calculate and record the confidence score for the QA execution in the QA report, according to the following guidance:

- Use an explicit 0–100% assessment for the scoped conclusion or next workflow step. This is a structured judgment of evidence and remaining uncertainty, not a calibrated probability of correctness, success, or safety. A score never supplies facts, turns worker agreement into proof, passes an unrun/failed check, or grants authorization.

- Confidence score factors and weights:
  - Requirement/AC and changed-scope coverage 30%
  - Direct source and executed-check evidence for the claimed stage 35%
  - Data-flow, dependency and environment understanding 20%
  - Risk and regressions 15%. 

2. Gracefully stop running any services or background processes you've launched (only the ones you launched, do not touch processes that belong to other worktrees or the user)

3. Provide a concise and brief final review summary for this whole process with a summary of the confidence score at the end. The confidence score you be in the following format:

```
Confidence: X% - {justification}
Remaining uncertainty: {justification}
```
