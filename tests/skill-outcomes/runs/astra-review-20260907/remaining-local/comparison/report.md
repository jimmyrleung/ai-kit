# Existing engineering comparison

**Decision: no attributable savings or broad simplification adoption is supported.** This report satisfies bounded comparison/reporting for B21.AC2/AC3, B23.AC3 and B24.AC3 using preserved evidence. It does not claim a positive benefit or universal quality; human judgment remains pending.

## Per-condition and repeat measurements

| Condition/repeat | Primary worker grades P/F/U | Reported unnecessary approvals | Reported required clarifications | Requested discussion turns | Retry counter | Artifact bytes, original | Batch seconds | Cost |
|---|---|---:|---:|---:|---|---:|---:|---|
| current/1 | 77/0/1 | 0 | 3 | 1 | 1 reported | 29923 | 1590 | unavailable |
| current/2 | 77/0/1 | 0 | 1 | 1 | 0 reported | 16529 | 906.501 | unavailable |
| candidate/1 | 78/0/0 | 0 | 2 | 1 | 5 command fallbacks/corrections | 21982 | 1429 | unavailable |
| candidate/2 | 78/0/0 | 0 | — (case sum 2) | — (case sum 1) | 0 whole-case | 31245 | 1453 | unavailable |

These are original reported measurements, not a matched effect estimate. Current/1 reports artifact-plus-trace output; candidate/1 excludes traces from its total-output definition; current/2 uses a different preserved-output set; candidate/2 has total-output null. All tokens and costs are null. Current/2 reports zero retries yet separately records an xxd→od tooling fallback. Candidate/2 reports zero whole-case retries while preserving prompt/rename setup corrections. Per-case counters absent in a run remain null in comparison.json.

## Per-case comparison

P/F/U below are worker grades only. Bytes are remeasured over the same explicit rule: eligible declared result/artifact files, excluding traces; actual file inventories are in comparison.json. Different declared populations remain a limitation. No missed-defect or false-positive census was supplied: those fields are null rather than inferred zero.

| Case | Current/1 P/F/U; bytes | Candidate/1 P/F/U; bytes | Current/2 P/F/U; bytes | Candidate/2 P/F/U; bytes |
|---|---|---|---|---|
| dirty-review | 4/0/0; 1722 | 4/0/0; 2431 | 4/0/0; 2406 | 4/0/0; 1773 |
| unborn-short-history | 3/0/0; 906 | 3/0/0; 1589 | 3/0/0; 957 | 3/0/0; 1001 |
| review-invalidation | 6/0/0; 1435 | 6/0/0; 1785 | 6/0/0; 4717 | 6/0/0; 1357 |
| task-reverification | 6/0/0; 2338 | 6/0/0; 2122 | 6/0/0; 2595 | 6/0/0; 3231 |
| consumer-closure | 4/0/0; 1294 | 4/0/0; 1821 | 4/0/0; 1283 | 4/0/0; 1175 |
| completion-resources | 6/0/0; 2027 | 6/0/0; 3066 | 6/0/0; 2364 | 6/0/0; 2134 |
| existing-test-home | 6/0/0; 538 | 6/0/0; 1057 | 6/0/0; 1599 | 6/0/0; 696 |
| convention-new-test | 6/0/0; 605 | 6/0/0; 980 | 6/0/0; 1819 | 6/0/0; 708 |
| no-suitable-test-home | 6/0/0; 653 | 6/0/0; 975 | 6/0/0; 1794 | 6/0/0; 718 |
| unneeded-helper | 3/0/0; 960 | 3/0/0; 1993 | 3/0/0; 1189 | 3/0/0; 1079 |
| authorization-cadence | 4/0/0; 2506 | 4/0/0; 2134 | 4/0/0; 1267 | 4/0/0; 4031 |
| review-depth-severity | 6/0/0; 1598 | 6/0/0; 3150 | 6/0/0; 2025 | 6/0/0; 2094 |
| check-reuse | 5/0/1; 1500 | 6/0/0; 3838 | 5/0/1; 6442 | 6/0/0; 1715 |
| intent-routing | 6/0/0; 1108 | 6/0/0; 2214 | 6/0/0; 1465 | 6/0/0; 1448 |
| incident-causality | 6/0/0; 3706 | 6/0/0; 6981 | 6/0/0; 3118 | 6/0/0; 3291 |

The apparent candidate advantage on check-reuse is a grading-definition difference: all four outputs lack browser evidence. Current grades that check unavailable; candidate grades its handling pass. This does not prove extra observable UI coverage. Candidate/2 also records three unasked required command-approval questions and a changed shell order; its all-pass worker criteria do not erase those missed protocol obligations.

## Approval, clarification and user cadence

All four batches explicitly report zero unnecessary approval interruptions. This does not show an interruption reduction. Current/1 counts application-source questions for A/B plus the retention question (3); current/2 records the retention question (1), while retaining the absent-source gap. Candidate/1 reports 2 clarifications, and candidate/2 has 2 in the case record but no aggregate counter. Their records also count one requested discussion turn, so the clarification categories are not proven disjoint. Do not subtract these numbers as a quality or speed benefit.

Saved artifacts across all four conditions preserve a precise unanswered retention-policy question and stop the walkthrough at item 1, with item 2 queued or undisclosed. These are requested owner decisions, not unnecessary interruptions. No scripted answer, full interaction trace, or completed owner disposition is present. The case-matching recommendation remains a preference awaiting owner judgment. Exact artifact lines are retained in comparison.json/bounded_artifact_observations.

## Review quality and parent evidence

Both conditions retain the severe possible tenant-isolation bypass as suspected/inferred and name a confirming probe. Missing issuer, resource-consumer and runtime evidence prevents a true-positive/false-positive label. Both distinguish the isolated fee change from cross-service authorization risk, accept justified test-file creation, and reject speculative factories, duplicated tests and unrelated formatting in the supplied helper proposal. Independent native-agent effectiveness is not measured: delegation was prohibited and sequential coverage is weaker.

Worker grades stay separate from parent assessment. The supplied parent placement record actually executed the saved test fixtures and recorded passing negative/zero/positive coverage; this synthesis only rechecks its source/test hashes and byte totals. It does not rerun tests or promote those checks into a complete parent review.

| Parent-checked repeat2 case | Current code/test bytes | Candidate code/test bytes | Parent recorded outcome |
|---|---:|---:|---|
| existing-test-home | 419 | 418 | Both exit 0; exact saved hashes match |
| convention-new-test | 568 | 570 | Both exit 0; exact saved hashes match |
| no-suitable-test-home | 563 | 555 | Both exit 0; exact saved hashes match |

The supplied parent file also contains no-skill repeats1/2 passing placement checks; those are retained separately in comparison.json, not promoted into a full no-skill batch comparison. Current/candidate repeat1 placement behavior has worker evidence but no corresponding parent row in this supplied placement file.

## Prompt/order confounds and decision rule

- Repeat1 extra analysis prompts differ in wording and order: current small then complex; candidate complex then small.
- Repeat2 small analysis prompt differs by final period; complex prompt matches. Candidate2 actual shell-probe order differs from declared order.
- Cases share worker context within each batch; no case-level context independence.
- Requested gpt-5.6-sol/high is recorded, effective runtime settings unexposed.
- Candidate2 reports three missed required command-approval pauses, despite unnecessary-interruption count0. Setup repaired17 prompt endings and renamed-file setup; whole-case retry count0 does not count those corrections.
- Original check-reuse grading differs: current marks browser-dependent check unavailable; candidates grade disciplined handling pass while also saying browser unavailable. These are grading semantics, not demonstrated additional browser outcome coverage.
- Original aggregate grade population differs: current1 includes extra-analysis checks; primary15-case counts are recomputed separately.
- Full transcript, per-case latency, token accounting and monetary cost absent.

The corpus rule requires preservation of mandatory coverage, authorization and requested cadence before broad simplification adoption. Smaller artifacts, fewer agents or fewer questions cannot compensate for lost obligations. Retain the current broad default; targeted confirmed defect repairs remain a separate decision. No positive benefit or attributable size/latency/cost improvement is established.

## Evidence and requested AC coverage

- B21.AC2: preserved original run/report paths, exact prompt hashes, artifact manifests, available trace locators, failures and null measurements are indexed in comparison.json. No original input or trial artifact was changed.
- B21.AC3: the existing acceptable-tradeoff rule is applied; missed obligations, interruptions, heterogeneous retries and artifact sizes are compared with limits. No broad simplification is adopted.
- B23.AC3: reported interruption counts and retained missing-fact/owner decisions are compared; the saved one-item walkthrough cadence is preserved. Full interaction-based quantification remains unavailable.
- B24.AC3: suspected issue handling, unknown missed-defect/false-positive totals, batch timing and null measured costs are explicit; preserved parent execution records remain separate from worker self-grades. Human disposition is pending.

[Machine-readable comparison and exact source locators](comparison.json). Primary inputs: [corpus protocol](<user-home>/ai-kit/tests/skill-outcomes/README.md), [parent prompt check](/tmp/astra-backlog-5VdqNm/parent-extra-comparison.json), [parent placement executions](/tmp/astra-backlog-5VdqNm/parent-placement-test-check-final.json).

## Confidence & unverified

Confidence: 95% for this descriptive comparison. Missing full traces, effective settings, per-case latency/cost and complete parent/human defect adjudication prevent causal savings or general quality conclusions. The original trials and grading history remain unchanged.
