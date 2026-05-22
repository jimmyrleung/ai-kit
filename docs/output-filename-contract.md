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

## Known residual drift (not yet normalized — flagged by audit-skills Check 11)

As of 2026-05-22 a few spots still use `{feature}` / `{prefix}` instead of `{feature_name}` for the
integration family (`_techspec.md` ×2, `_integration.md` ×2, `_tasks.md` ×2). Left intentionally
un-normalized; Check 11 will surface them for a future cleanup decision.

## When you add a new workflow family

Add its row(s) here first, pick one token, and reference this table from both the orchestrator and the
standalone command bodies. Do not invent a parallel filename in the orchestrator.
