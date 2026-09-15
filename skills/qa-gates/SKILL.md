---
name: qa-gates
description: "Do a final verification for a completed, reviewed, and QAed implementation against its spec. Confirms build/tests were run and passes, QA report is present, ensure acceptance criteria and invariants are met, ensure docs consistency, and provide a final go/no-go. Use to verify, validate, or QA a completed feature/refactor or all repository tasks for a prefix. Accepts a prefix, doc path, or short description. Code-quality review belongs to review-implementation; detailed QA execution belongs to qa-execution."
---

# QA Gates — implementation verification

Do a final, thorough verification for a given implementation, executing each gate sequentially, providing a final GO/NO-GO.

You do not review code and do not perform a detailed QA execution with live validation - these are expected to be done before with `review-implementation` and `qa-execution` when applicable.

## Input

Accept a loose target, including:

- feature implementation folder containing relevant files, like investigation/requirements/techspec/tasks/QA docs
- a single implementation plan with evidence that it was reviewed and verified/QAed
- An inline prompt with detailed description that helps you nail down the target implementation to verify

**IMPORTANT**:

- If you can't lock the target implementation, go back to the user asking more details.
- It is mandatory that the target implementation has been reviewed and verified or QAed - if there is no evidence, go back to the user suggesting `review-implementation` or `qa-execution` accordingly.

## Output

If there is an existing QA document, like a `qa.md` generated on `qa-execution`, append a new section `## QA gates`, and add the evidence within (one subsection per gate)

If there isn't a QA document, create a new `qa-gates.md` document and add the evidence there in the following structure:

```markdown
# QA Gates - [meaningful name]

[summary]

### Gate 0 - Initial context

[gate 0 details]

### Gate 1 - Rules and general guidance

[gate 1 details]

[...and so on]
```

## Approach

### Gate 0 - Initial context

Inspect every artifact from the input and extract:

- implementation context and proposal
- the acceptance criteria list
- the files the implementation was supposed to touch
- implementation review evidence
- testing scenario implementation and execution evidence
- Live validation evidence

Gate 0 passes when you complete the initial inspection and you can extract each item of the list above (regardless if it is complete or no, this will be verified in further gates).

> **Note:** Missing live validation evidence is acceptable with proper justification as there are scenarios where live validation might not be possible.

### Gate 1 - Rules and general guidance

Confirm the implementation's adherence to the codebase's documented and observed patterns, including `AGENTS.md` and referenced rules.

### Gate 2 - Specs adherence

Confirm the implementation's adherence to what was proposed on the specs / implementation plan, including:

- Architecture implemented as specified
- Components, interfaces, and contracts implemented as defined
- Data models implemented as documented
- Endpoints/APIs and integrations, when applicable, implemented as specified

### Gate 3 - Tasks

For each task marked as complete, ensure:

- there is an associated implementation
- there is one or more acceptance criteria tracked
- there are tests implemented and executed for that given task

### Gate 4 - Build & test

Re-run build and tests to confirm they are all green.

Document the result accordingly:

```
- [x] Gate 1 — build/test: pass (commands: `…`; run: <ID>; executed here | reused with matching identities)   ← command actually ran with exit 0
```

or FAIL (executed, non-zero):

```
- [ ] Gate 1 — build/test: FAIL
  - command: `…`
  - output: <2-3 line digest of the failure>
  - resolution: <"address before re-running" / "accepted: <reason>">
```

or BLOCKED (could not execute — sandbox/permission/headless denial, missing toolchain):

```
- [ ] Gate 1 — build/test: BLOCKED
  - command: `…`
  - reason: <why it couldn't run — e.g. "sandbox denies `dotnet test`; not in the cc-loop allow-list">
  - resolution: <"run before merge" / "re-run with the allow-list added via `cc-loop init`">
```

### Gate 5 - Acceptance Criteria

For each AC item, ensure:

- It is a **Testable AC item**, pointing at the test that proves it; pass = test exists and passed in Gate 1.
- There's evidence that confirms that AC item at **Code-level** - record file:line evidence.
- When applicable, there's evidence that confirms the **Observable UI AC item** (prefer screenshots).
- **Subjective/manual owner for AC item** - ask the user and record their actual confirmation.

Record one line per AC:

```
- [x] AC #1 — "logout button visible on /account" — pass (test: tests/account.test.ts:42)
- [ ] AC #4 — "techspec total ≤ 150 lines" — FAIL: actual 164 (file:line)
```

### Gate 6 - Release checklist and readiness

Build a checklist of everything that should be done and/or should be in place for the implementation to be released, and verify if each item checks.

Record one line per item, and it should either be checked or has a justification, like: "user needs to do XYZ manually", "this can't be verified from here", etc.

### Gate 7 - Docs consistency

Ensure the implementation and the docs are consistent and aligned.

- did the implementation reveal a gap the doc should record?
- are file paths / function names / API signatures in the doc consistent with what shipped?
- are there stale docs with stale decisions?

### Gate 8 - Final decision

1. Ensure this whole process is documented on the existing `qa.md` file or, when not present, in the new `qa-gates.md` file

2. Provide a concise summary of this whole process for the user

3. If all gates passes, ask for a final GO/NO-GO. Else, final decision should be NO-GO with the reason why.
