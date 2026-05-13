# Agents Inventory

Subagents invoked by skills/commands. Each row: file → registered `name` (used in `subagent_type`), model pin, role.

> Reviewer agents (`*-reviewer-agent` / `*-review-agent`) are invoked by the `review-artifact` skill, which references them by name. The producer agents are increasingly thin pointers to skills — see `docs/model-assignments.md` for the migration status.

## Bug fix family

| File                                  | Name                               | Model  | Role                                                                        |
| ------------------------------------- | ---------------------------------- | ------ | --------------------------------------------------------------------------- |
| `bug-investigation-agent.md`          | `bug-investigation-agent`          | opus   | Investigate a bug, trace execution path, identify evidence-based root cause |
| `bug-investigation-reviewer-agent.md` | `bug-investigation-reviewer-agent` | sonnet | QA the investigation before remediation                                     |
| `impact-analysis-agent.md`            | `impact-analysis-agent`            | sonnet | Assess blast radius and risks of a proposed fix                             |

## Feature integration family

| File                                     | Name                                 | Model  | Role                                                            |
| ---------------------------------------- | ------------------------------------ | ------ | --------------------------------------------------------------- |
| `integration-analysis-agent.md`          | `integration-analysis-agent`         | opus   | Map how a new requirement integrates into the existing codebase |
| `integration-analysis-review-agent.md`   | `integration-review-agent`           | sonnet | Review the integration analysis                                 |
| `integration-techspec-creator-agent.md`  | `integration-techspec-creator-agent` | opus   | Produce a lightweight techspec                                  |
| `integration-tasks-creator-agent.md`     | `integration-tasks-creator-agent`    | sonnet | Break techspec into ordered tasks                               |
| `feature-integration-validator-agent.md` | `integration-validator-agent`        | sonnet | Verify feature is implemented, tested, ready to ship            |

## Refactor / tech-debt family

| File                                 | Name                              | Model  | Role                                     |
| ------------------------------------ | --------------------------------- | ------ | ---------------------------------------- |
| `audit-agent.md`                     | `audit-agent`                     | opus   | Audit codebase to scope the refactor     |
| `audit-reviewer-agent.md`            | `audit-reviewer-agent`            | sonnet | Second-pass review of the audit          |
| `refactoring-planner-agent.md`       | `refactoring-planner-agent`       | opus   | Produce phased plan with rollback points |
| `refactoring-tasks-creator-agent.md` | `refactoring-tasks-creator-agent` | sonnet | Break plan into implementation tasks     |

## Incident response family

| File                          | Name                       | Model  | Role                                                       |
| ----------------------------- | -------------------------- | ------ | ---------------------------------------------------------- |
| `diagnosis-agent.md`          | `diagnosis-agent`          | opus   | Diagnose the incident, find root cause (5 Whys + evidence) |
| `diagnosis-reviewer-agent.md` | `diagnosis-reviewer-agent` | sonnet | Senior-SRE review of the diagnosis                         |
| `hotfix-planner-agent.md`     | `hotfix-planner-agent`     | opus   | Plan immediate remediation steps with rollback             |
| `post-mortem-agent.md`        | `post-mortem-agent`        | opus   | Write blameless post-mortem, action items                  |

## Cross-cutting

| File                     | Name              | Model  | Role                                                      |
| ------------------------ | ----------------- | ------ | --------------------------------------------------------- |
| `discovery-agent.md`     | `discovery-agent` | sonnet | Build codebase understanding before a workflow starts     |
| `code-reviewer-agent.md` | `code-reviewer`   | sonnet | Confidence-filtered code review (bugs, security, quality) |
