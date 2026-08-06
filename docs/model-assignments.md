# Model Assignments

> **HISTORICAL (pre-2026-08 kit refactor).** The two agent tables below describe the retired named-agent architecture — all listed agents and most listed skills now live under `archive/`; the live kit uses generic subagents inside skills (see each skill's own subagent section). Kept for provenance. The **Loop-role model floor** section below remains live.

Opus 4.5 (Deep reasoning/creative work)

| Workflow              | Agent / Agent → Skill                                            | Why Opus                  |
| --------------------- | --------------------------------------------------------------- | ------------------------- |
| feature-addition      | integration-analysis-agent → `integration-analysis` skill         | Initial analysis, tracing |
| feature-addition      | integration-techspec-creator-agent → `integration-techspec` skill | Architectural decisions   |
| refactoring-tech-debt | audit-agent → `refactor-audit` skill         | Initial audit             |
| refactoring-tech-debt | refactoring-planner-agent → `refactor-plan` skill | Planning, trade-offs   |
| greenfield-dev        | prd-creator                        | Creative product work     |
| greenfield-dev        | techspec-creator                   | Architecture              |
| bugfix                | bug-investigation-agent → `bug-investigation` skill | Root cause analysis       |
| incident-response     | diagnosis-agent → `incident-diagnosis` skill | Complex root cause        |
| incident-response     | hotfix-planner-agent → `hotfix-plan` skill | Critical safety planning  |
| incident-response     | post-mortem-agent → `post-mortem` skill | Nuanced blameless writing |

Sonnet 4.5 (Structured validation/breakdown)

| Workflow              | Agent / Agent → Skill                                       | Why Sonnet          |
| --------------------- | ---------------------------------------------------------- | ------------------- |
| feature-addition      | integration-review-agent                                    | Validation          |
| feature-addition      | integration-validator-agent                                 | Validation          |
| feature-addition      | integration-tasks-creator-agent → `integration-tasks` skill | Task breakdown      |
| feature-addition      | code-reviewer-agent                                        | Code review         |
| refactoring-tech-debt | audit-reviewer-agent                | Review (review-artifact) |
| refactoring-tech-debt | refactoring-tasks-creator-agent → `refactor-tasks` skill | Task breakdown      |
| greenfield-dev        | tasks-creator                       | Task breakdown      |
| greenfield-dev        | code-reviewer-agent                 | Code review         |
| bugfix                | bug-investigation-reviewer-agent    | Review (review-artifact) |
| bugfix                | impact-analysis-agent → `impact-analysis` skill | Structured analysis |
| incident-response     | diagnosis-reviewer-agent            | Review (review-artifact) |

10 agents on Opus, 11 agents on Sonnet - good balance of quality vs cost/speed.

## Loop-role model floor — structured-output smoke test

Before assigning a cheaper/faster model to any headless loop role (implement-task-loop,
document-workflow-loop, qa-loop, qa-loop-docs, review-checkpoint, map-tasks) or to a workflow-script
fan-out stage that returns pinned-line output, run a ~5-prompt smoke test of the exact contracts the
runner parses by regex:

1. flip a `Status:` line inside a sample tasks-doc section (single Edit, heading untouched);
2. emit `**Recommendation:** go|no-go` + `**Summary:** …` pinned immediately after an H1;
3. emit `**Recommendation:** proceed|fix-then-proceed|abort` (checkpoint variant);
4. return the map-tasks plan.json shape against the schema;
5. write a `## Verify — {date}` gate block with per-gate checkbox lines.

**Any malformed pinned line in the 5 disqualifies the model for loop roles regardless of benchmark
scores** — format adherence is the leading downstream-failure indicator [COMPILOT RQ4], and a
runner regex miss silently strands a run. Passing the floor doesn't assign the model; it makes it
eligible for the cost/quality call (see the `workflow-model-tiering` memory for the
fan-out-vs-synthesis split).
