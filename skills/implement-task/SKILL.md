---
name: implement-task
description: "Implements and verifies a given task. Use to implement, work on, or pick up a task from where it was left. Accepts a prefix, tasks-doc path, a specs folder/doc, task number, task ID, or short description. Batched code review belongs to review-implementation."
---

# implement-task

## Goal

Implement a specific task end-to-end ans verify its implementation.

## Approach

**The approach should follow each subsection below sequentially.**

### Resolve the target

The first thing to do is to resolve the target task first.

Accept whatever the invocation provides and understand what type of task are you going to work:

- An ad-hoc implementation, like a straightforward implementation from a plan, investigation, or even inline prompt
- A specific task from a tasks document, and it could be:
  - A single tasks document - in that case, identify what is the next task to be implemented
  - If it is a task from a tasks document created with the `tasks-breakdown` skill, resolve both the `tasks.md` and the specific `task_[num].md` you are going to work next

If you can't resolve the target, ask rather than guess.

### Initial context

With the target resolved, gather additional context for its execution.

1. Read the target task thoroughly and referenced documents

2. Read the AGENTS.md file(s) and any referenced documents in it (especially rules) to gather context from each project involved.

3. If not done on step 1, read any relevant sibling documents that can provide additional context (requirements, techspec, past tasks, etc.)

4. Do a web search (web search tool, firecrawl, etc. according to what's available) on any relevant framework, lib, docs, or any other thing that is relevant for the task and is not necessarily present in it or its files

> If running on a loop like `/goal` or similar, you don't have to re-read any documents that didn't have had any changes

### Pre-implementation checklist

With the initial context resolved, ensure all items from the following list are checked

- [ ] I have read the whole target task document and its referenced documents
- [ ] I have read the AGENTS.md file(s) and any referenced documents in it or there isn't an AGENTS.md file to read
- [ ] I have read any relevant sibling documents or there are no relevant sibling documents
- [ ] I did search for anything relevant or there isn't anything relevant to search
- [ ] Task dependencies and lifecycle prerequisites are met; write/resource conflicts are
      serialized or have explicit isolation and reconciliation
- [ ] I understand the acceptance criteria (for a fix: the investigation's expected
      behavior plus the ACs)
- [ ] For greenfield tasks: I understand the user-observable behavior
      this task moves forward

### Implement

1. Create a step-by-step implementation plan for the specific task. It must be aligned with the [Initial context], especially on:

- Completing it means progress on completing the requirements/techspec (when they are present) or progress on completing part of a given implementation plan
- Accounting for key information that relevant references and search results provide
- Following the chosen approach and architecture
- Following the repo's coding standards and rules

2. Calculate the confidence score for the plan with the following guidance, factors, and weights.

- Confidence score guidance: use an explicit 0–100% assessment for the scoped conclusion or next workflow step. This is a structured judgment of evidence and remaining uncertainty, not a calibrated probability of correctness, success, or safety. A score never supplies facts, turns worker agreement into proof, passes an unrun/failed check, or grants authorization.
- Confidence score factors and weights:
  - Requirement/AC and changed-scope coverage 30%
  - Direct source and executed-check evidence for the claimed stage 35%
  - Data-flow, dependency and environment understanding 20%
  - Risk and regressions 15%.

3. Scope guard: when the implementation surfaces work beyond the task's boundaries:

- **Critical issues** (bugs in surrounding code, architectural problems, code that needs
  refactoring for safety) → STOP, document the issue, propose it separately, and get
  explicit approval before proceeding. Never fold it into the current task — even in
  auto-accept mode.
- **Nice-to-haves** ("while we're here" improvements not required by the task) → capture
  them as named follow-ups in the prefix's reference files; do not implement them now.

3. Execute the implementation plan

### Verify implementation

1. Build with no errors when the repository/change requires a build.

2. Run tests and required checks to confirm nothing is broken.

3. Ensure every item from the task's acceptance criteria is met.

4. Inspect the implementation to confirm it did what it was supposed to do and didn't violate its scope.

5. When applicable, execute a live validation using any tools, skills, and/or AGENTS.md instructions available to confirm the expected behavior is solid.

- **Non-blocker step**: Do not mark the task as blocked or failed if you couldn't run the live validation. Add a note with the reason why it was skipped so the user can review later.

#### Subagent recommendation

For steps 3 to 5, launch a separate agent so the adversarial review is done from a clean perspective.

Model recommendation per harness:

- Claude code: Fable high
- Codex: Astra high
- Cursor: Grok high or Fable high
- Any other harness: ask the user

### Post-implementation

1. Document the task progress and verification in the tasks files and update its status marking as complete. Ensure the the tasks document are consistent with the implementation.

2. When the task is completed and not blocked/interrupted, re-calculate the confidence score using the same guidance, factors, and weights.

- Document it in the task notes comparing with the plan confidence score.
- Once this process is complete, it is expected that you present the confidence summary to the user in the following format:

  ```
  Confidence: X% - {justification}
  Remaining uncertainty: {justification}
  ```

3. Add task notes in a specific task notes section for any implementation gaps or decisions made during the implementation.

4. Gracefully stop running any services or background processes you've launched (only the ones you launched, do not touch processes that belong to other worktrees or the user)

- This should be execute not only when the task is completed successfully, but also when it is blocked or interrupted for some reason.
- Skip condition: if running on a loop like `goal` and you know in subsequent tasks you will still need the services/processes running, you can skip this step

5. Provide a concise and brief final implementation summary for this whole process.

#### Finish boundary

Suggest a prompt for launching an adversarial review using the `review-implementation` skill when:

- This is the last task of a set of implementation tasks
- This is the last task being implemented in a given boundary

Example 1 - given we are implementing a set of 6 tasks, where 4 are backend and 2 are frontend tasks:

- If that's the 4th task (last backend task), suggest `review-implementation` for the whole back-end implementation
- If that's the 6th task (last task implemented), suggest `review-implementation` for either the whole implementation if no review was done, or just for the front-end tasks if the backend tasks were already reviewed.

Example 2 - given we are implementing a set of 10 tasks, where 6 are in repo 1, and 4 in repo 2:

- Suggest `review-implementation` at the right boundaries following [Example 1] for repo 1, and then do the same thing for repo 2.
- Even though the work is cross-repo it is expected that each repo has its own review passes as they are probably going into separate PRs
