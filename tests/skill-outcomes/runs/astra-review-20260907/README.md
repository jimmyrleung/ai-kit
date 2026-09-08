# Astra review outcome evidence — 2026-09-07

## Current owner dispositions — 2026-09-07

Source review is complete with documented limits; owner review is next and can start now. The original independent engineering, domain and tooling reviews remain preserved. The later LICENSE/README attribution amendment was checked separately by the parent.

- **B33:** resolved as `Copyright (c) 2026 Jimmy Leung` in LICENSE and README.
- **B17:** Claude deferred at owner direction. Cursor retry stopped before model execution because the added isolated test root requires trust; this does not contradict the reported ai-kit repository trust. Provider evidence remains partial.
- **B32:** hosted CI deferred until committed changes are available; not a blocker to owner review. Local checks pass; hosted platforms are not marked PASS.
- **B23:** owner review is the next step; final GO remains pending.
- **B24:** documented comparison limitations accepted by the owner. Missing measurements remain unknown, and no efficiency benefit is claimed.

The current ledger has 108 observed-bounded, four partial and one not-adopted AC. Partial evidence is separate from accepted limitations and deferred work. [Decision record and preserved prior state](owner-dispositions/evidence.zip) · [Cursor retry](owner-dispositions/cursor-retry/report.md).

Confidence: 95%; remaining uncertainty is unavailable provider/platform execution and pending owner judgment.

## Earlier evidence snapshots — superseded where stated above

Status: review packet assembled; QA and owner acceptance remain open. The authoritative acceptance record is
[the execution report](../../../../20260906_astra_review_execution.md). Worker grades below
are submitted claims; they are not automatic parent or owner approval.

Each completed run has its original `report.md`, `run.json`, a ZIP of available inputs,
supplied bodies, fixture setup, command traces and artifacts, and an archive manifest.
The manifest records original and archived SHA-256 values and any path redactions.
Git internals, dependency installations and bytecode caches are excluded; fixture setup
recipes and recorded Git-layer evidence are retained. This is evidence packaging, not a
generic model runner. Full host transcripts and provider accounting were unavailable
unless a specific run explicitly records them.

| Run | Evidence | Parent review |
| --- | --- | --- |
| Engineering candidate, repeat 1 | [Submitted report](engineering-candidate-1/report.md), [record](engineering-candidate-1/run.json), [archive](engineering-candidate-1/evidence.zip), [identities](engineering-candidate-1/archive-manifest.json) | Bounded artifacts and actual fixture tests checked; original source/version limits retained |
| Engineering current, repeat 1 | [Submitted report](engineering-current-1/report.md), [record](engineering-current-1/run.json), [archive](engineering-current-1/evidence.zip), [identities](engineering-current-1/archive-manifest.json) | Bounded artifacts and actual fixture tests checked; original source/version limits retained |
| Engineering candidate, repeat 2 | [Submitted report](engineering-candidate-2/report.md), [record](engineering-candidate-2/run.json), [archive](engineering-candidate-2/evidence.zip), [identities](engineering-candidate-2/archive-manifest.json) | Pairwise small-prompt mismatch and probe-order deviation; supplied procedure evidence only |
| Engineering current, repeat 2 | [Submitted report](engineering-current-2/report.md), [record](engineering-current-2/run.json), [archive](engineering-current-2/evidence.zip), [identities](engineering-current-2/archive-manifest.json) | Shared case materialization in some subvariants; browser evidence unavailable |
| Domain candidate, original repeat 1 | [Submitted report](domain-candidate-original-1/report.md), [record](domain-candidate-original-1/run.json), [archive](domain-candidate-original-1/evidence.zip), [identities](domain-candidate-original-1/archive-manifest.json) | Bounded artifacts checked; incomplete supplied references and informed no-op remain limitations |
| Engineering no-skill, repeat 1 | [Report](engineering-no-skill-1/report.md), [record](engineering-no-skill-1/run.json), [archive](engineering-no-skill-1/evidence.zip), [identities](engineering-no-skill-1/archive-manifest.json) | All three actual test-placement fixtures checked; unavoidable skill catalog exposure disclosed |
| Engineering no-skill, repeat 2 | [Report](engineering-no-skill-2/report.md), [record](engineering-no-skill-2/run.json), [archive](engineering-no-skill-2/evidence.zip), [identities](engineering-no-skill-2/archive-manifest.json) | All three actual test-placement fixtures checked; setup retry preserved |
| Final focused, one noncomparative run | [Report](final-focused-1/report.md), [record](final-focused-1/run.json), [archive](final-focused-1/evidence.zip), [identities](final-focused-1/archive-manifest.json) | Ten groups; submitted 46 pass, one workflow-format fail, two unavailable; bounded artifacts re-grounded |
| Parent and source-review checks | [Archive](parent-verification/evidence.zip), [identities](parent-verification/archive-manifest.json) | Central local suite, source reviews, byte-preserving fixture tests, browser export, native discovery and real runner serializer with synthetic input |

One worker per condition/repetition shares context across ordered cases; case-level
independence is not claimed. Supplied-body procedure results are separate from native
discovery, actual implementation, browser execution and human judgment. Keep failed,
unavailable, contaminated or mismatched trials visible when comparing conditions.

The repeat-1 extra analyzer prompts were not identical across conditions, and their order
differed. Their artifacts remain useful diagnostics, but their size difference cannot be
attributed to the skill bodies alone. Repeat 2 also differs in the small prompt's final
period and the candidate's shell-probe order. It does not repair repeat 1.
The short-core pilot is **not adopted**: the
predeclared two-repeat comparison requirement was not met. The original analyzer structure
is retained with the required engineering and authorization repairs. No cost saving is claimed.


## Review navigation

- [Exact acceptance ledger](acceptance.md) and [machine-readable evidence](acceptance.json): every backlog AC, current source support and remaining outcome limits.
- [Consolidated source review](source-review.json): current scoped identities, review lanes and the superseded tooling dependency record.
- [Archive verification](package-verification.json): content hashes and targeted privacy-pattern findings. Original/archived hashes differ only for recorded path redactions.
- [Documentation consistency](docs-consistency.json): original historical title/body preservation and input checkbox census.

Artifact and trace paths inside submitted reports resolve inside their ZIP, whose entries preserve the run layout. Absolute scratch locators are provenance, not durable filesystem links; the archive manifest maps their run-relative suffixes. One intentionally permission-denied Terraform fixture cannot be read into the final archive and is listed under `unreadable`; its setup and actual denied-read result remain preserved. Git history internals are excluded, so use recorded setup recipes and layer traces for reproduction.

The parent-verification archive contains `final-validation/run.json` and logs, `final-review/<lane>/report.md` and reviewed identities, `parent-placement-test-check-final.json`, `native-probe/discovery-*`, `browser-probe/domain-parent/`, and `runner-probe/`. Native discovery used an existing authenticated Codex host and earlier candidate body; it does not prove final-body behavior or fresh-user authentication. Runner serialization used actual external code with synthetic input, not a live headless workflow.

The original final focused results preserve their failed workflow format, unavailable strict standalone-root fixture and unavailable configured conversion secret scanner. The later informed corrections separately complete all three documentation layouts; they do not regrade that original trial. Synthetic access, control-plane and incident evidence remains labeled. No full host trace, effective model proof, monetary saving, universal reliability or owner GO is claimed.

## Local completion supplement

The [supplement archive](remaining-local/evidence.zip) and [manifest](remaining-local/archive-manifest.json) contain corrective work and additional coverage after the original runs. Read the [current acceptance summary](acceptance-review-report.md); the [previous summary](before-local-completion/acceptance-review-report.md) and ledger remain preserved.

- [Documentation correction](remaining-local/w1-correction/report.md) and [remaining layouts](remaining-local/w1-correction-layouts/report.md): full required outputs and actual refresh across separate, co-located and multi-workspace roots; original trial bytes unchanged.
- [Missing documentation fixtures](remaining-local/docs-coverage/report.md): non-ancestor/legacy evidence, mounted detectors, Terraform destinations and cross-file grouping, including recorded corrections/checker limits.
- [Descriptive comparisons](remaining-local/comparison/report.md): recorded grades, interruptions, retries, bytes and time; absent cost/defect censuses remain null, no attributable savings.
- [Fresh-home bootstrap](remaining-local/fresh-bootstrap/report.md): installation, native discovery of all canonical skills, and actual workflow/provider attempts that stop at missing authentication.
- [Independent fixture review](remaining-local/browser-reuse/independent-review/report.md): one native reviewer, matched browser-result reuse, repository-only completion and owner GO pending.

`mechanics/result.json`, `browser-reuse/prefix-result.json` and `parent-verification.json` inside this archive retain actual checker outcomes, the repository-only QA path, and parent hash/Git checks. Reports' artifact links resolve within their respective archived directories. These are informed repairs/coverage, not new independent comparison trials.

## Existing authenticated provider follow-up

The [report](existing-provider-stores/report.md), [verification](existing-provider-stores/verification.json), [archive](existing-provider-stores/evidence.zip) and [manifest](existing-provider-stores/archive-manifest.json) separate existing authentication from actual recording. Codex completed one disposable Claude-layout recording slice with an honest enabled missing-record failure. Claude was service-denied; Cursor could not establish workspace trust under the protected host-write boundary. B17.AC3 remains partial. The original fresh-home failures and Cursor setup correction remain visible. Parent independently checked artifacts, native traces and source identities; no source edits or live private-store writes were part of this follow-up.

## Comparison adjudication — 2026-09-07

The [source-grounded audit](comparison-adjudication/report.md) adds bounded proposal-scope and decision-obligation counts from saved artifacts. It preserves candidate/2's omitted baseline guard observation and the missing patch-scope/authorization ground truth. This is post-hoc adjudication, with no new model trial or source change. B23.AC3 and B24.AC3 remain partial; human review and true patch-defect totals are not replaced by artifact counts.
