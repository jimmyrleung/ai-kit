# Candidate engineering trial — repeat 1

Completed all 15 selected cases in the required order as one shared-context supplied-body batch. Fixtures were independent, but case-level context independence is not claimed. All 78 corpus mandatory checks passed against the preserved outputs/traces; the 10 predeclared analyze-work comparison checks also passed. Human owner review remains pending.

Requested selection: `gpt-5.6-sol`, reasoning `high`. The host did not expose the effective runtime selection, token use, cost, host version, or a complete exportable assistant/tool transcript. Exact frozen bodies, per-case prompts/manifests, all available command transcripts, failed attempts, outputs, and artifact hashes are preserved.

| Case | Mandatory result | Primary evidence |
|---|---:|---|
| dirty-review | 4/4 pass | `cases/dirty-review/output.md; trace-committed.txt; trace-staged.txt; trace-unstaged.txt; trace-untracked.txt; trace-layer-hashes.txt` |
| unborn-short-history | 3/3 pass | `cases/unborn-short-history/output.md; trace-unborn-head-probe.txt; trace-unborn-scope.txt; trace-single-scope.txt` |
| review-invalidation | 6/6 pass | `cases/review-invalidation/output.md; trace-variant-identities.txt` |
| task-reverification | 6/6 pass | `cases/task-reverification/output.md; trace-input-resolution.txt; trace-produced-verification.txt; fixtures/task-reverification/tasks.md` |
| consumer-closure | 4/4 pass | `cases/consumer-closure/output.md; trace-inspection.txt; trace-direct-test.txt` |
| completion-resources | 6/6 pass | `cases/completion-resources/artifacts/executable-task-graph.md; output.md` |
| existing-test-home | 6/6 pass | `cases/existing-test-home/trace-context-before.txt; trace-tests.txt; trace-after.txt; output.md` |
| convention-new-test | 6/6 pass | `cases/convention-new-test/trace-context-before.txt; trace-tests.txt; trace-after.txt; output.md` |
| no-suitable-test-home | 6/6 pass | `cases/no-suitable-test-home/trace-context-before.txt; trace-tests.txt; trace-after.txt; output.md` |
| unneeded-helper | 3/3 pass | `cases/unneeded-helper/trace-inspection.txt; artifacts/review.md; output.md` |
| authorization-cadence | 4/4 pass | `cases/authorization-cadence/trace-a-b-diff.txt; trace-poststate.txt; output.md; fixtures/authorization-cadence/variants/*` |
| review-depth-severity | 6/6 pass | `cases/review-depth-severity/trace-inspection-and-probes.txt; artifacts/review-coverage.md; output.md` |
| check-reuse | 6/6 pass | `cases/check-reuse/artifacts/initial-check-record.json; trace-initial-*.txt; trace-variant-identities.txt; trace-subset-run.txt; trace-missing-prod-key-exit-aware.txt; output.md` |
| intent-routing | 6/6 pass | `cases/intent-routing/trace-inspection.txt; artifacts/routes.md; output.md` |
| incident-causality | 6/6 pass | `cases/incident-causality/trace-variant-a.txt; trace-variant-b.txt; trace-variant-c.txt; artifacts/*_investigation.md; output.md` |

Additional predeclared analysis comparison:

| Input | Result | Artifact bytes | Evidence |
|---|---:|---:|---|
| consumer-closure-complex | 5/5 pass | 3750 | `additional-analysis/consumer-closure-complex/artifacts/fetch_result_analysis.md` |
| existing-test-home-small | 5/5 pass | 2228 | `additional-analysis/existing-test-home-small/artifacts/negative_fee_validation_analysis.md` |

The complex analysis enumerates both executable consumers, assigns the unchanged worker and existing worker test to the contract boundary, and retains compatibility/rollback/test constraints. The small analysis reuses the existing unittest home and records the narrow rollback and behavior-preservation constraints. Artifact length was measured, not treated as a benefit.

Recorded execution exceptions: one unavailable-pytest fallback, two transcript path corrections, one exit-propagation correction, and one reporting measurement correction. All are listed in `run.json`; no case was silently rerun until green. Browser evidence, integration environment, provider usage/cost, and owner judgments remain unavailable or pending where stated in the case outputs.

Confidence score: 97% — outputs, byte identities, and command results support every graded check. 3% uncertainty remains because the host-level transcript/provider telemetry are unavailable and judgment-heavy grading still requires parent and human-owner review.
