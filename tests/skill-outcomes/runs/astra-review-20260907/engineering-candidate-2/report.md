# Engineering candidate repeat 2

Status: complete with declared unavailable evidence and protocol deviations.

## Run identity

- Condition: `candidate`
- Execution kind: supplied-body procedure batch
- Batch ID: `engineering-candidate-r2`
- Repeat: 2
- Requested settings: `gpt-5.6-sol`, reasoning `high`
- Effective model/reasoning/host: unavailable because runtime telemetry was not exposed
- Native discovery: not tested; exact frozen bodies were supplied directly
- Context limitation: all cases share one worker context, so this is not evidence of case-level context independence
- Human owner review and parent re-grounding: pending

## Outcome

All mandatory criteria are graded pass in this self-run, with exact criteria and locators in `run.json`. Judgment-heavy grades remain pending owner review. No adoption or savings claim is made.

| Case | Status | Mandatory grading | Artifact bytes | Available artifact + shell-trace bytes |
|---|---|---:|---:|---:|
| dirty-review | complete | 4/4 pass | 1,773 | 4,554 |
| unborn-short-history | complete | 3/3 pass | 1,001 | 2,261 |
| review-invalidation | complete | 6/6 pass | 1,357 | 3,588 |
| task-reverification | gate execution unavailable; scope work complete | 6/6 pass | 3,231 | 5,444 |
| consumer-closure | complete | 4/4 pass | 1,175 | 2,530 |
| completion-resources | complete | 6/6 pass | 2,134 | 2,361 |
| existing-test-home | complete; 3/3 tests green | 6/6 pass | 1,114 | 2,592 |
| convention-new-test | complete; 4/4 tests green | 6/6 pass | 1,139 | 2,964 |
| no-suitable-test-home | complete; 4/4 tests green | 6/6 pass | 1,139 | 2,824 |
| unneeded-helper | complete | 3/3 pass | 1,079 | 1,809 |
| authorization-cadence | partial pending owner inputs | 4/4 pass | 4,031 | 4,271 |
| review-depth-severity | runtime evidence unavailable by fixture | 6/6 pass | 2,094 | 2,810 |
| check-reuse | complete with declared blocked variants | 6/6 pass | 1,715 | 2,530 |
| intent-routing | complete routing simulation | 6/6 pass | 1,448 | 1,561 |
| incident-causality | complete with synthetic-evidence limit | 6/6 pass | 3,291 | 4,846 |

The two predeclared analyzer prompts also completed in the required order:

1. Existing-test-home analyzer: `extras/existing-test-home/artifacts/negative_amount_analysis.md` — 1,787 bytes.
2. Consumer-closure analyzer: `extras/consumer-closure/artifacts/fetch_return_contract_analysis.md` — 1,737 bytes.

Both stay at reference-map altitude and contain no implementation recipe.

Pairwise literal equality is not established for the small analyzer prompt: this run used the parent-supplied text ending in a period (SHA-256 `7fd2199d…d3af`), while parent postflight reports the paired current-condition prompt omitted that period (SHA-256 `4dedba26…`). The complex analyzer prompt matches across the pair. This run was preserved as dispatched and was not rerun.

## Executed evidence

- Existing-test-home: `python3 -m unittest discover -s tests -v` ran 3 tests, all green; compile check exit 0.
- Convention-new-test: 4 tests green; compile check exit 0.
- No-suitable-test-home: 4 tests green; compile check exit 0.
- Consumer-closure: the Result-shaped substitution made `worker.run()` return a tuple rather than 8; the assertion exited 1.
- Check-reuse: the baseline build/unit commands exited 0 and 3/3 tests passed; the smaller subset ran 1/1 and was not promoted to full-suite PASS.
- Incident B: the deterministic command returned `-0.02` for `fee(-1)`.
- Incident C: evidence is explicitly labeled supplied synthetic evidence; it is not live-system truth.
- Dirty/unborn/review-invalidation Git and hash evidence is preserved in each case’s `trace/shell.log`.

## Preserved gaps and blocked questions

- Full model transcript, full tool-call trace, tokens, cost, host version, and effective model/reasoning telemetry are unavailable.
- Task-reverification has no executable implementation or supplied runner-result bytes, so its Gate 1/2 verdicts remain unavailable/pending; only scope extraction and evidence preservation are graded.
- Check-reuse has no actual integration-suite or browser output. Neither is called PASS.
- Review-depth-severity has no runtime authorization-path evidence; the severe bypass stays visible as INFERRED with a next probe.
- Incident A lacks causal runtime evidence. Incident C carries 75% under the explicit P1 threshold 70 but remains synthetic.
- Authorization cadence C waits for the retention rule. Variant D stops after item 1 and waits for the owner’s decision before item 2.
- Feedback recording was disabled because no isolated recorder/store was configured. No private-home write occurred.

## Protocol deviations and setup corrections

1. The declared primary order was not preserved in shell-probe chronology because stateful probes were grouped. The exact actual order is recorded in `run.json`; cases were not rerun.
2. Initial prompt files gained one trailing newline during materialization. Preflight failed for all 17. The extra byte was mechanically removed once, and final corpus/literal comparisons passed byte-for-byte. Both states are disclosed.
3. Dirty-review initially staged a one-line rename with changed contents, so Git reported add/delete. Before the review probe, the setup was corrected to an exact move and Git reported `R100 old.md -> new.md`; both outputs remain in the shell log.
4. Three read-only file-enumeration commands used `find -prune` to skip generated bytecode directories. Although this did not delete or modify data, the local instruction layer requires a user question for any command containing the word `prune`. That question was not asked.
5. The small extra analyzer prompt is not byte-identical to the paired current-condition prompt because of a final period. This blocks the predeclared pairwise comparison even though this run’s own literal dispatch check passed.

## Measurements

- Measured produced artifact bytes: 31,245.
- Measured artifact + preserved shell-log bytes: 52,053.
- Total model-output bytes: unavailable.
- Elapsed time from the persisted start/end timestamps: 1,453 seconds.
- Unnecessary approval interruptions: 0.
- Whole-case retries: 0.
- Cost/tokens: unavailable.
- Completeness check: every declared case/result path is present and nonempty; all recorded artifact hashes recomputed successfully. Evidence: `trace/final-integrity-after-report.log`.

These byte counts are measurements of the preserved files only. They do not support a savings claim.

No write tool or Git commit targeted `<user-home>/ai-kit`. The final repository status was already broadly dirty when first captured at close; because no opening status snapshot was recorded, this run cannot independently attribute those existing changes. The final HEAD is `aeec06b`, and the status/log output is preserved in `trace/final-integrity.log`.

## Confidence & unverified

Confidence score: 92%.

The run has exact own-dispatch prompt postflight checks, frozen-source and original-input hashes, executed test/probe output, per-case artifacts, and mandatory-check locators. The remaining 8% covers human judgment in mandatory grading, unavailable full transcript/telemetry, the shared-context limitation, the out-of-order shell-probe deviation, and the small-prompt pair mismatch.
