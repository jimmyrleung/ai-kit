# Commands Inventory

> **Kit-refactor (2026-08-05): all commands except `/tasks-loop` are archived** (`archive/commands/`).
> Skills are invoked directly (`/analyze`, `/bug-investigation`, `/techspec`, `/review-artifact`,
> `/implement-task`, …) — no command wrappers. The tables below describe the archived population
> and are kept for reading archived docs.

Slash commands users invoke from Claude Code. Grouped by workflow family. Orchestrators run the full multi-phase flow; per-phase commands run a single skill standalone.

## Discovery (pre-workflow)

| Command            | Role                                                                                                                       |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| `/lay-of-the-land` | Pre-workflow recon: sourced current-state map of an unfamiliar area, no-assumptions / every finding cited. Feeds the workflow you run next. (was `/trigger-discovery-phase`) |

## Greenfield / new project (mode-aware iterative slicing)

| Command                    | Role                                                    |
| -------------------------- | ------------------------------------------------------- |
| `/greenfield-dev`          | **Orchestrator.** Start a new greenfield project.       |
| `/create-roadmap`          | Master roadmap + slice list (run once at project start) |
| `/create-prd`              | Per-slice PRD (just-in-time, as slices are picked up)   |
| `/create-techspec`         | Slice-scoped technical spec                             |
| `/review-techspec`         | Catch techspec issues before tasks                      |
| `/create-tasks`            | Decompose techspec into vertically-ordered tasks        |
| `/gf-implement-task`       | Implement one task (runs `verify-task` at end)          |
| `/create-qa-scenarios`     | QA scenarios for a slice (or end-of-project)            |

## Feature integration into an existing codebase

| Command                           | Role                                                       |
| --------------------------------- | ---------------------------------------------------------- |
| `/integration-feature-dev`        | **Orchestrator.** Small/medium feature into existing code. |
| `/integration-analyze-feature`    | Phase 1 standalone — integration analysis                  |
| `/integration-create-techspec`    | 3-way techspec exploration                                 |
| `/integration-pragmatic-techspec` | Single-approach pragmatic techspec                         |
| `/integration-create-tasks`       | 3-way task sizing exploration                              |
| `/integration-balanced-tasks`     | Single-approach balanced tasks                             |
| `/implement-task`                 | **Converted to a skill** (`skills/implement-task`, 2026-08-05); command file deleted |

## Bug fix

| Command                  | Role                                                       |
| ------------------------ | ---------------------------------------------------------- |
| `/full-bug-fix-workflow` | **Orchestrator.** Investigate → impact → fix → regression. |
| `/investigate-bug`       | Phase 1 standalone — produce evidence-based investigation  |
| `/review-investigation`  | QA the investigation before fixing                         |
| `/analyze-impact`        | Phase 3 standalone — blast-radius analysis                 |
| `/implement-bug-fix`     | Apply the fix (runs `verify-task` at end)                  |
| `/bug-regression-test`   | Regression test plan                                       |

## Refactor / tech-debt

| Command                    | Role                                                      |
| -------------------------- | --------------------------------------------------------- |
| `/refactor-techdebt-dev`   | **Orchestrator.** Small/medium refactor in existing code. |
| `/audit-refactor-techdebt` | Phase 1 standalone — audit + review pass only             |

## Incident response

| Command                   | Role                                                 |
| ------------------------- | ---------------------------------------------------- |
| `/full-incident-response` | **Orchestrator.** P1 streamlined / P2+ full process. |
| `/start-incident`         | Initialize incident directory + report from template |
| `/incident-status`        | Where you are, what's missing, what's next           |
| `/diagnose`               | Phase 2 standalone — root-cause diagnosis            |
| `/review-diagnosis`       | QA the diagnosis before remediation                  |
| `/plan-hotfix`            | Phase 4 standalone — executable remediation plan     |
| `/create-post-mortem`     | Phase 5 standalone — blameless post-mortem           |

## Quality assurance

| Command                             | Role                                                          |
| ----------------------------------- | ------------------------------------------------------------- |
| `/qa-gates`                         | Verify implementation against spec (5 gates). Use `prefix=…`. |
| `/implementation-quality-assurance` | Back-compat alias for `/qa-gates`                             |

## Meta

| Command              | Role                                                      |
| -------------------- | --------------------------------------------------------- |
| `/document-workflow` | Deep-dive documentation for a specific workflow operation |
