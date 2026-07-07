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
| integration-feature-dev | `{feature_name}` | analysis | `{feature_name}_integration.md` |
| integration-feature-dev | `{feature_name}` | techspec | `{feature_name}_techspec.md` |
| integration-feature-dev | `{feature_name}` | tasks | `{feature_name}_tasks.md` |
| full-bug-fix-workflow | `{bug_id}` | investigation | `{bug_id}_investigation.md` |
| full-bug-fix-workflow | `{bug_id}` | impact | `{bug_id}_impact_analysis.md` |
| full-bug-fix-workflow | `{bug_id}` | regression | `{bug_id}_regression_test_plan.md` |
| refactor-techdebt-dev | `{refactor_name}` | audit | `{refactor_name}_audit.md` |
| refactor-techdebt-dev | `{refactor_name}` | plan | `{refactor_name}_plan.md` |
| refactor-techdebt-dev | `{refactor_name}` | tasks | `{refactor_name}_tasks.md` |
| full-incident-response | (none — bare, in the incident dir) | diagnosis | `diagnosis.md` |
| full-incident-response | (none) | hotfix | `remediation_plan.md` |
| full-incident-response | (none) | postmortem | `postmortem.md` |

## Known residual drift — none

Normalized 2026-07-07 (audit proposal 02): the remaining `{feature}` spots — 3 integration-family
skill descriptions + `balanced-tasks-creation`'s companion-docs example block (×3, incl. the
`_description.md` input line, normalized to avoid a mixed-token block) — now read `{feature_name}`.
Check 11 verified zero drift at 2026-07-07. Expected non-drift hits for future runs: `{prefix}` in
`qa-gates` / `verify-task` (those skills' own argument name); audit-skills Check 11's own example
text; `{feature}_description.md` in `integration-analysis`'s input contract (an *input* file — this
contract governs phase *output* docs only, and that skill's output line is already canonical).

## When you add a new workflow family

Add its row(s) here first, pick one token, and reference this table from both the orchestrator and the
standalone command bodies. Do not invent a parallel filename in the orchestrator.
