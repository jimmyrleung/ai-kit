# ai-kit Inventory (v3)

The live catalog contains 27 skills, with one row per tracked `skills/<name>/SKILL.md`
file. The live directory tree is the source of truth. Historical material is preserved under
[`archive/v1/`](archive/v1/) and [`archive/v2/`](archive/v2/).

`Explicit only` means the skill sets `disable-model-invocation: true`; invoke it by name rather than expecting automatic selection.

## Skills

### Discovery, requirements, and design

| Skill | Invocation | Current role |
| --- | --- | --- |
| `lay-of-the-land` | Normal | Maps the sourced current state of an unfamiliar code area before requirements or change design. |
| `define-reqs` | Normal | Maps scope, entry points, existing patterns, risks, and acceptance context for feature, greenfield, or refactor work. Produces `specs/<slug>/requirements.md`. |
| `bug-investigation` | Normal | Diagnoses a bug or incident from source and runtime evidence, then records the chosen minimal fix or next probe in `investigations/<slug>/investigation.md`. |
| `techspec` | Normal | Designs the implementation blueprint for feature, greenfield, refactor, bug-fix, hotfix, or incident-remediation work. Produces `specs/<slug>/techspec.md`. |
| `tasks-breakdown` | Normal | Converts an approved spec or plan into ordered `tasks.md` and `task_NN.md` files with dependencies, tests, and acceptance criteria. |

### Implementation, review, and QA

| Skill | Invocation | Current role |
| --- | --- | --- |
| `implement-task` | Normal | Resolves and implements one ad-hoc or documented task end to end, runs relevant verification, and records completion evidence. |
| `review-implementation` | Normal | Reviews a completed task or task set for correctness, repository fit, simplicity, and regressions before QA execution. |
| `qa-execution` | Normal | Executes acceptance checks, automated tests, and live validation; records evidence in `specs/<slug>/qa.md` and fixes verified defects within the approved design. |
| `qa-gates` | Normal | Runs the final readiness gates over a reviewed and QA-tested implementation, records evidence, and produces the GO/NO-GO decision path. |

### Repository and workflow documentation

| Skill | Invocation | Current role |
| --- | --- | --- |
| `guides-and-sensors` | Normal | Scans a repository and proposes project guides, feedback sensors, rules, and local skills for later user review and authoring. |
| `docs-tasks-creator` | Normal | Inventories supported HTTP, message, GRPC, function, and background-job entry points; creates or refreshes `_docs-tasks.md`, `project-overview.md`, and a `workflows/` scaffold. |
| `document-workflow` | Normal | Traces one backend or explicitly full-stack operation through real source and writes its canonical workflow document. |
| `update-workflow-docs` | Normal | Classifies existing workflow docs as Current, Stale, or Unverifiable and updates only stale sections in place. |
| `document-terraform` | Normal | Documents Terraform roots and environments, resolved resources, module provenance, permission evidence, and external or cross-stack dependencies. |

### Learning

| Skill | Invocation | Current role |
| --- | --- | --- |
| `triage-learning-content` | Normal | Recommends `TTS`, `TTS_PLUS_REVIEW`, or `READ` for supplied learning content, with scores, review targets, and a 1× listening estimate. |
| `teach` | Explicit only | Maintains a multi-session teaching workspace with a mission, resources, HTML lessons, reusable assets, glossary, and learning records. |
| `breakout-session` | Normal | Runs a short Socratic checkpoint in which the user demonstrates previously studied material and receives a scoped go/no-go assessment. |

### Guided decisions and architecture

| Skill | Invocation | Current role |
| --- | --- | --- |
| `walkthrough` | Normal | Takes an existing list of questions or findings, presents one item per turn by default, and records each disposition in the owning artifact. |
| `walkthrough-implementation` | Normal | Explains recently completed owned work in dependency order, including code, rationale, and verification, before commit or shipping. |
| `grill-me` | Explicit only | Thin wrapper that forwards to a companion `grilling` skill for a rigorous plan/design interview. |
| `grill-with-docs` | Explicit only | Thin wrapper that combines companion `grilling` and `domain-modeling` skills so the interview also maintains ADR/domain artifacts. |
| `improve-codebase-architecture` | Explicit only | Scans architecture for module-deepening opportunities, renders a visual HTML report, then uses companion design/grilling skills to explore the selected candidate. |

### Orchestration, lifecycle, and skill ecosystem

| Skill | Invocation | Current role |
| --- | --- | --- |
| `orchestrate` | Normal | Coordinates an ad-hoc multi-agent fan-out, persists worker outputs as they arrive, and consolidates an evidence-backed result. |
| `close` | Normal | Distills a session into continuation state plus optional durable decisions, learnings, observations, and skill candidates; asks before commits or pushes. |
| `improve` | Normal | Reviews recorded workflow friction and the improvement backlog, then stages supported proposals for owner disposition instead of directly editing live skills. |
| `write-skills` | Normal | Authors a focused global or repository-local skill, or refactors a skill that does not trigger reliably. |
| `find-skills` | Normal | Searches for installable third-party skills, inspects candidates before recommending them, and installs only with authorized scope and destination. |

## Bundled support files

The live tree also includes the support material consumed by individual skills:

- Output templates for investigations, requirements, workflow docs, QA reports, technical specs, and task sets.
- Detector rules for `docs-tasks-creator` and Terraform resolution heuristics for `document-terraform`.
- Skill-local evidence, authorization, feedback, and provider-capability references where required; each copy is maintained with its consuming skill.
- Teaching workspace formats plus provider metadata under `skills/teach/`.

## External and retired dependencies

- `grill-me` expects a companion `grilling` skill that is not bundled in this repository.
- `grill-with-docs` expects companion `grilling` and `domain-modeling` skills that are not bundled here.
- `improve-codebase-architecture` expects `codebase-design`, `grilling`, and `domain-modeling`; its referenced `HTML-REPORT.md` scaffold is also not present in the live folder.
- `document-workflow` names `document-workflow-loop` as a cc-looper-owned external fork.
- Some live handoffs still name retired or absent skills: `triage`, `compile-kb`,
  `onboard-me`, `audit-skills`, and `implement-fix`. These names are not live skills and are
  not included in the count above.
