# Engineering supplied-body trial — current repeat 2

- Status: **completed with one unavailable mandatory check**
- Reviewed source base: `aeec06bfa0a6b97402b17824d957f29635f40ba7`; all 11 supplied skill-body hashes match that base
- Execution: supplied-body procedure, not native discovery
- Batch: shared context in declared order; fresh filesystem fixtures, weaker case-level context independence
- Provider/model request: OpenAI, gpt-5.6-sol/high requested; effective host version/model/reasoning/settings unavailable
- Mandatory grades: 77 pass, 0 fail, 1 unavailable
- Measurements: 16529 artifact bytes; 72844 total output bytes under the recorded definitions. These are completeness measurements, not a savings claim.

| Order | Case | Status | Mandatory checks | Output |
|---:|---|---|---|---|
| 1 | `dirty-review` | completed | 4 pass / 0 fail / 0 unavailable | `cases/01-dirty-review/output.md` |
| 2 | `unborn-short-history` | completed | 3 pass / 0 fail / 0 unavailable | `cases/02-unborn-short-history/output.md` |
| 3 | `review-invalidation` | completed | 6 pass / 0 fail / 0 unavailable | `cases/03-review-invalidation/output.md` |
| 4 | `task-reverification` | completed | 6 pass / 0 fail / 0 unavailable | `cases/04-task-reverification/output.md` |
| 5 | `consumer-closure` | completed | 4 pass / 0 fail / 0 unavailable | `cases/05-consumer-closure/output.md` |
| 6 | `completion-resources` | completed | 6 pass / 0 fail / 0 unavailable | `cases/06-completion-resources/output.md` |
| 7 | `existing-test-home` | completed | 6 pass / 0 fail / 0 unavailable | `cases/07-existing-test-home/output.md` |
| 8 | `convention-new-test` | completed | 6 pass / 0 fail / 0 unavailable | `cases/08-convention-new-test/output.md` |
| 9 | `no-suitable-test-home` | completed | 6 pass / 0 fail / 0 unavailable | `cases/09-no-suitable-test-home/output.md` |
| 10 | `unneeded-helper` | completed | 3 pass / 0 fail / 0 unavailable | `cases/10-unneeded-helper/output.md` |
| 11 | `authorization-cadence` | completed | 4 pass / 0 fail / 0 unavailable | `cases/11-authorization-cadence/output.md` |
| 12 | `review-depth-severity` | completed | 6 pass / 0 fail / 0 unavailable | `cases/12-review-depth-severity/output.md` |
| 13 | `check-reuse` | completed_with_unavailable | 5 pass / 0 fail / 1 unavailable | `cases/13-check-reuse/output.md` |
| 14 | `intent-routing` | completed | 6 pass / 0 fail / 0 unavailable | `cases/14-intent-routing/output.md` |
| 15 | `incident-causality` | completed | 6 pass / 0 fail / 0 unavailable | `cases/15-incident-causality/output.md` |

## Extra predeclared analysis prompts

1. `Analyze rejecting negative amounts; produce a reference map, no implementation recipe` — completed from a fresh initial `existing-test-home` fixture.
2. `Analyze the fetch return-contract change; produce a reference map, no implementation recipe.` — completed from a fresh initial `consumer-closure` fixture.

Both exact prompt byte comparisons pass. The artifacts remain reference maps and do not contain implementation recipes.

## Failures, pending questions, and unavailable evidence

- `xxd` was unavailable during a validation check; `od` succeeded as the fallback. This did not affect a trial case.
- `authorization-cadence` variant C remains pending on the unspecified retention rule. Variant D remains pending on the user's disposition of item 1; item 2 was not presented.
- `check-reuse` has no supplied browser screenshot/output. Its browser-dependent mandatory check is unavailable; subjective wording approval remains human-owned.
- Native skill discovery, the full host transcript, tokens, cost, and effective model/settings identity are unavailable.
- Human owner review remains pending for judgment-heavy grades.

## Confidence & unverified

Confidence score: 97% — exact inputs and skill bodies are hashed, stateful claims have tool traces, tests/reproduction actually ran, and all mandatory checks have locators.

3% uncertainty — one browser-dependent check lacks evidence; shared context weakens case-level independence; the human owner and parent grounding are pending.
