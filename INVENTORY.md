# ai-kit Inventory (v2)

One row per live skill (30 total), grouped by family, plus the reference docs. Keep open during day-to-day use.

Not in this repo: the **loop variants** (`tasks-loop`, `qa-loop`, `review-checkpoint`, …) live in the cc-looper repo's `claude-config/` tree; native loop primitives (`/goal`, `/loop`, `/schedule`) are documented only in [`docs/loop-recipes.md`](docs/loop-recipes.md). The v1 inventory (commands, agents, templates) is archived under [`archive/v1/INVENTORY/`](archive/v1/INVENTORY/).

## Skills

### Discovery & routing (pre-workflow)

| Skill | Role |
| --- | --- |
| `triage` | Route a free-text request to the right entry skill / chain / loop primitive, or "just do it directly". Mid-flight detection first; ≤2 questions; one-line recommendation, never auto-executes. |
| `lay-of-the-land` | Pre-workflow recon: sourced current-state map of an unfamiliar area; every finding cited + confidence-scored, assumptions escalated as open questions. Produces `{topic}_lay-of-the-land.md`. |

### Analysis & design

| Skill | Role |
| --- | --- |
| `analyze-work` | Unified reference map of upcoming work; detects mode (integration / greenfield / refactor) and applies its lens. Produces `{work_name}_analysis.md`. |
| `bug-investigation` | Trace the path from entry point to failure; evidence-based root cause (VERIFIED/ASSUMED hops), minimal-fix proposal. Incident lens for production failures (log/trace/metric evidence, severity-aware gate). Produces `{bug_id}_investigation.md`. |
| `techspec` | Unified committed design blueprint; detects mode (integration / greenfield / refactor / fix + hotfix variant) with an orthogonal risk lens; single-approach pragmatic by default, 3-way escalation; post-write QA-scenario pass. Produces `{work_name}_techspec.md`. |
| `tasks-breakdown` | Unified implementation-tasks decomposition; detects mode; balanced sizing by default with 3-way escalation; spec-carrying mode when the techspec is deliberately skipped. Produces `{work_name}_tasks.md`. |
| `review-artifact` | Adversarial review of an analysis / investigation / techspec / tasks doc before the next stage builds on it — generic reviewer fan-out, re-grounding, doc-type lens, in-place `## Review` block. |

### Implementation

| Skill | Role |
| --- | --- |
| `implement-task` | Implement one task (or a reviewed bug fix — fix lens) end-to-end from a loose target; runs the `verify-task` gates before Done; review is batched per prefix via `review-implementation`. |

### Quality assurance

| Skill | Role |
| --- | --- |
| `verify-task` | Per-task closeout: composes `qa-gates` with per-task inputs — gates 1+2+3 only. Runs inside `implement-task`. |
| `review-implementation` | Batched post-implementation code review for a prefix: 3 parallel generic reviewers, findings verified against source, sha-stamped `## Review` block for `qa-gates`. |
| `qa-gates` | Prefix-level verification: 5 pass/fail gates (build/test, AC checklist, cross-cutting invariants, docs consistency, human go/no-go). Each gate passes with evidence or fails with a recorded reason. |

### Incident response

Diagnosis rides inside `bug-investigation` (incident lens); hotfix planning inside `techspec` fix mode. Only the closeout is a dedicated skill.

| Skill | Role |
| --- | --- |
| `post-mortem` | Blameless post-mortem after a resolved incident — impact, timeline + response metrics, root cause, owned/dated action items. Produces `{incident_id}_postmortem.md`. |

### Documentation

| Skill | Role |
| --- | --- |
| `document-workflow` | Deep-dive doc of one workflow operation (endpoint / consumer / job): trace hop-by-hop through real source → canonical doc under `workflows/`. Backend mode default, full-stack opt-in. |
| `update-workflow-docs` | Refresh existing workflow docs after the code moved on — per-doc commit-diff staleness detection, drift buckets, targeted in-place updates. |
| `docs-tasks-creator` | Scan a codebase, emit a tasks doc with one `document-workflow` task per detected route / handler / job + a `project-overview.md`. Monorepo-aware. |
| `document-terraform` | Document a Terraform codebase: per-environment resolved-resource inventory with module-provenance chains, architectural-role narratives, confidence-scored gaps. |

### Knowledge base

| Skill | Role |
| --- | --- |
| `compile-kb` | Compile a non-Hermes markdown vault: synthesize source notes into a regeneratable `wiki/` tree, adversarially review changed pages, emit a dated compilation digest. Incremental + idempotent. |

### Engineering ownership (retention)

Hand-invoked rituals writing durable artifacts to `~/.claude/ownership/{topic}/`. Slimmed to the two low-friction members in the refactor; the friction-heavy rituals (`predict-first`, `debug-first`, `adr-first`, `challenge-me`) stay archived, individually restorable.

| Skill | Role |
| --- | --- |
| `record-decision` | Cheap mid-work decision capture: full ADR-template record, AI-drafted rationale hard-flagged `UNREVIEWED`; you own the Rationale at review — in-session, or swept later by `/close`. |
| `onboard-me` | Cold-read walkthrough of UNFAMILIAR code by a "staff engineer" — one step per turn, Socratic, assumptions listed every message. |

### Session lifecycle & self-improvement

| Skill | Role |
| --- | --- |
| `close` | End-of-session retrospect → persist to the right layer (repo `docs/rules/`, auto-memory, observations) + slim SESSION_LOG entry + propose a commit. |
| `close-tasks` | End-of-tasks-doc closeout when per-session `/close` didn't run — reconstructs the run from durable artifacts, emits observations + a roll-up SESSION_LOG entry, idempotently. |
| `improve` | Periodic self-improvement review of accumulated observations → STAGED review packet under `~/.claude/improvements/{date}/`; never edits a live file without per-item approval. |
| `audit-skills` | On-demand structural audit of the skill population (strict-YAML, description budget, triggers, redundancy, dead refs); stages proposals, never auto-edits. |
| `write-skills` | Author a new skill — or fix one that won't fire — so it triggers reliably and passes `audit-skills` by construction. |

### Orchestration & walkthroughs

| Skill | Role |
| --- | --- |
| `orchestrate` | Run an ad-hoc multi-agent fan-out well: dispatch contract, persist-on-arrival, verification tiering, cross-agent synthesis, provider-aware model choice. |
| `walkthrough` | Disposition a list of open items one per turn — findings, open questions, decision backlogs — with per-item confidence and dated rounds persisted to the artifact. |
| `walkthrough-implementation` | Dependency-ordered tour of a completed, not-yet-committed implementation — stated rationale as the review mechanism; fixes applied in-turn. |

### Learning & skill discovery

| Skill | Role |
| --- | --- |
| `triage-learning-content` | Content-consumption router: recommend TTS / TTS_PLUS_REVIEW / READ for an article or URL — scores, pre-consumption briefing, addressable review targets, 1× listening estimate, stable JSON for downstream workflows. Chat-only output. |
| `teach` | Stateful teaching workspace: learn a topic over multiple sessions (glossary, learning record, missions). Explicit-only (`/teach`). |
| `find-skills` | Discover and install agent skills when looking for functionality that might exist as an installable skill. |

## Docs

| File | What's in it |
| --- | --- |
| [`docs/output-filename-contract.md`](docs/output-filename-contract.md) | The one artifact-filename contract (`{work_name}_analysis.md`, `{bug_id}_investigation.md`, …) every producing skill follows. |
| [`docs/rules/skill-authoring.md`](docs/rules/skill-authoring.md) | Repo rules — read before editing, validating, enumerating, or converting skills (strict-YAML check, sweep rules, deployment topology, population-sync rule). |
| [`docs/loop-recipes.md`](docs/loop-recipes.md) | Native loop primitives (`/goal`, `/loop`, `/schedule`): frames, rubric, hard constraints, recipes. The only place the primitive names live. |
| [`docs/codex-portability-assessment.md`](docs/codex-portability-assessment.md) | Design + decision record for the Codex adapter. |
| [`docs/cursor-portability-assessment.md`](docs/cursor-portability-assessment.md) | Design + decision record for the Cursor adapter — written for v1; the symlink mechanism survived the 2026-08 v2 reconciliation, the generated surfaces did not (see `adapters/cursor/README.md`). |
| [`docs/model-assignments.md`](docs/model-assignments.md) | **Historical** — per-agent model pins from the v1 kit (banner in the doc). |
