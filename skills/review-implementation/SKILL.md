---
name: review-implementation
description: "Reviews a given implementation, usually a large completed task or a set of completed tasks. Use for specific code review or batched code review before qa execution; Task implementation belongs to implement-task or implement-fix. Complete QA execution happens after this review in a separate session."
---

# review-implementation

## Approach

### Scope

1. Status check: if reviewing a task or set of tasks that have a spec, ensure its implementation is completed. Do not proceed with reviewing a task if it is blocked or interrupted.

2. Identify what's the review scope: a completed task or a set of completed tasks, a specific commit for a given repo, a branch with a given implementation, etc.

- For a small set of changes, evaluate if it large enough so it's worth this whole process. If not, it should be shortened accordingly.
- For a considerable set of changes, execute the whole review approach as described.

### Initial context

1. When available, read any relevant references pointed out in the tasks documents you are going to review

2. Read the AGENTS.md file(s) and any referenced documents in it (especially rules) to gather context from each project involved in the implementation to be reviewed.

3. If not done on step 1, read any relevant sibling documents that provide additional context (requirements, techspec, past tasks, implementation plan, etc.)

4. Double check any searched information for any relevant framework, lib, docs, or any other thing that is relevant for the tasks to be reviewed.

### Diff and compare

Inspect committed, staged, unstaged, and untracked content, and inventory what was implemented and which files were changed.

- There might be unrelated changes that landed before the implementation was done (like user manual changes for a given config, files they don't want to commit, etc.) - you should identify those so you don't point these files as issues.

### Review

General guidance for the review:

1. **Correctness**:

- bugs, missed acceptance criteria, broken invariants
- **marker/alert ownership** — an event name an alert or scheduled query matches must be unique to the
  alert-worthy state (a shared marker could page on healthy work — caught in two runs);
- **mocked-variant reachability** — every mocked result variant a test introduces traces
  to a real production return site (a mocked failure branch proved unreachable: the real
  handler returns true or throws); financial/async ordering (webhook-vs-poller,
  confirm-vs-capture races).

2. **Conventions**:

- adherence to the codebase's documented and observed patterns, including `AGENTS.md` and referenced rules
- lint/format configs
- idioms of the neighboring code the diff touches.

3. **Simplicity + repository fit**: it is mandatory to follow the [Anti-overengineering] guidance described below

4. **Refactors**: unrelated refactor suggestions are opt-in; do not manufacture a mandatory refactor list.

5. **Using subagents**: mandatory to follow the [Subagents guidance] described below to determine whether to dispatch or not subagents for doing the review

#### Subagents guidance

For a small or mid-size set of **low-risk** changes, do not launch subagents, just proceed to execute the review pass according to the general guidance.

For medium or higher risk changes regardless of the size, launch separate review lanes:

- 1 specific lane for tracing the highest-risk boundary end to end
- 1..n to cover remaining distinct risks

> Cross-component/service boundaries, auth/payments, migrations, infrastructure, concurrency, or weak coverage are example of work that require the separate lanes.

#### Anti-overengineering

This is a mandatory guidance that should be followed when reviewing the implementation, regardless if you are doing it or if independent subagents are doing it. In case of launching subagents, the following anti-overengineering guidance should be provided to them verbatim.

Identify the following:

- Overengineering, unnecessary abstractions, and unnecessary complexity
- Excessive validation, safety checks, fallbacks, or defensive branches
- Handling of unrealistic or unsupported edge cases
- Duplicate checks or layers with no clear owner
- Code made harder to understand for minor benefits
- Unrelated cleanup
- Excessive or unjustified test files and tests
- Introducing new patterns/conventions instead of using existing ones
- Variables and methods with names that doesn't follow existing naming conventions or patterns
- Violations to the repo AI-assisted development guidance (AGENTS.md and associated rules)

Once identified, evaluate what's really important and should be kept or not.

- What's really important guidance: anything that **really** prevents performance, scalability, availability, maintainability, or security issues.

When presenting the review result to the user, display the list of overengineering findings with confidence score and severity (critical/high/medium/low) for the user to decide what to keep and what to remove.

### Verify findings

Before a finding is recorded or presented:

- re-verify its `file:line` against current source
- a repro-style finding must be **executed**, not reasoned, to be "confirmed"
- drop stale/refuted findings with a one-line note.
- Distill — every recorded finding carries `file:line` + a one-line expected-vs-actual
- never paste raw build/test/tool output.

### Cofidence score

Calculate the confidence score for the review: one score for each review item and one score for the entire review result, according to the following guidance:

- Use an explicit 0–100% assessment for the scoped conclusion or next workflow step. This is a structured judgment of evidence and remaining uncertainty, not a calibrated probability of correctness, success, or safety. A score never supplies facts, turns worker agreement into proof, passes an unrun/failed check, or grants authorization.

- Confidence score factors and weights:
  - Requirement/AC and changed-scope coverage 30%
  - Direct source and executed-check evidence for the claimed stage 35%
  - Data-flow, dependency and environment understanding 20%
  - Risk and regressions 15%.

### Present results

Present the consolidated findings by severity + the requested refactor suggestions, all of them with a **apply now / apply later / proceed as-is** recommendation., but leaving the final decision to the user.

Gather decision on each item for the user, and once done, record the review results + decision in the associated tasks documents.

> When running on a loop like `/goal` you are allowed to apply any fix or improvements and ready-to-ship refactors associated with the task without the user confirmation to avoid pausing the loop.

### Apply approved review findings

Proceed with applying all review findings and refactors approved by the user.

**IMPORTANT**: You must re-run any checks, build, tests, and live validations recorded on the task to confirm its behavior and document its results, indicating it was done in the review phase.

### Post-review

1. Re-compute the confidence score using the same guidance, weights, and factors of the [Verify findings steps], now with the review findings applied.

2. Update the review results + decisions previously recorded with any relevant information, including marking them as "Applied".

3. Gracefully stop running any services or background processes you've launched (only the ones you launched, do not touch processes that belong to other worktrees or the user)

4. Provide a concise and brief final review summary for this whole process, including the re-calculated confidence score in comparison to the initial one before applying the review findings.
