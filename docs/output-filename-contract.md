# Output-doc filename contract

Single source of truth for the output-document filename each workflow phase produces. Orchestrators
(`integration-feature-dev`, `full-bug-fix-workflow`, `refactor-techdebt-dev`, `full-incident-response`)
and their standalone per-phase commands MUST agree with this table — cite it rather than restating a
filename inline. Drift between an orchestrator's restatement and the standalone command's actual output
recurred across three families during skill-ification (see `~/.claude/observations/2026-05-12-skillify-*`);
this table + `audit-skills` Check 11 exist to prevent it.

## Rule

**One placeholder token per family.** The suffix is fixed per phase. Never mix `{feature}` / `{prefix}`
with `{feature_name}` within the integration family, etc.

| Family | Token | Phase | Output filename |
|---|---|---|---|
| analyze (skill-centric) | `{work_name}` | analysis | `{work_name}_analysis.md` |
| bug-investigation (skill-centric) | `{bug_id}` | investigation | `{bug_id}_investigation.md` |
| techspec (skill-centric) | `{work_name}` | techspec (all modes, refactor included) | `{work_name}_techspec.md` |
| integration-feature-dev *(archived)* | `{feature_name}` | analysis | `{feature_name}_integration.md` |
| integration-feature-dev *(archived)* | `{feature_name}` | techspec | `{feature_name}_techspec.md` |
| integration-feature-dev *(archived)* | `{feature_name}` | tasks | `{feature_name}_tasks.md` |
| full-bug-fix-workflow *(archived)* | `{bug_id}` | impact | `{bug_id}_impact_analysis.md` |
| full-bug-fix-workflow *(archived)* | `{bug_id}` | regression | `{bug_id}_regression_test_plan.md` |
| refactor-techdebt-dev *(archived)* | `{refactor_name}` | audit | `{refactor_name}_audit.md` |
| refactor-techdebt-dev *(archived)* | `{refactor_name}` | plan | `{refactor_name}_plan.md` |
| refactor-techdebt-dev *(archived)* | `{refactor_name}` | tasks | `{refactor_name}_tasks.md` |
| full-incident-response *(archived)* | (none — bare, in the incident dir) | diagnosis | `diagnosis.md` |
| full-incident-response *(archived)* | (none) | hotfix | `remediation_plan.md` |
| full-incident-response *(archived)* | (none) | postmortem | `postmortem.md` |

> **Kit-refactor note (2026-08-05):** the skill-centric `analyze` family supersedes the analysis
> phases of the archived `integration-feature-dev` / `refactor-techdebt-dev` families (one unified
> `{work_name}_analysis.md` for integration, greenfield, and refactor modes), and the skill-centric
> `techspec` supersedes their design phases plus the bug family's impact phase (one unified
> `{work_name}_techspec.md`; the refactor `_plan.md` and `{bug_id}_impact_analysis.md` suffixes are
> retired — impact now rides inside the fix-mode techspec). `bug-investigation` keeps its
> `{bug_id}_investigation.md` contract, now as a standalone skill. Archived rows are kept for
> reading archived docs; do not emit those filenames from new work. `review-artifact` (was
> `review-analysis`) updates the reviewed artifact in place (a `## Review` section) and produces
> no file of its own.

## Known residual drift — none

Normalized 2026-07-07 (audit proposal 02): the remaining `{feature}` spots — 3 integration-family
skill descriptions + `balanced-tasks-creation`'s companion-docs example block (×3, incl. the
`_description.md` input line, normalized to avoid a mixed-token block) — now read `{feature_name}`.
Check 11 verified zero drift at 2026-07-07 and 2026-07-19. Expected non-drift hits for future runs: `{prefix}` in
`qa-gates` / `verify-task` / `qa-loop` / `qa-loop-docs` (those skills' own argument name; the loop pair are
qa-gates' headless forks, canonical in cc-looper); audit-skills Check 11's own example
text; `{feature}_description.md` in `integration-analysis`'s input contract (an *input* file — this
contract governs phase *output* docs only, and that skill's output line is already canonical).

## When you add a new workflow family

Add its row(s) here first, pick one token, and reference this table from both the orchestrator and the
standalone command bodies. Do not invent a parallel filename in the orchestrator.
