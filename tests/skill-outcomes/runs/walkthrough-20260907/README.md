# WB01–WB03 evidence — 2026-09-07

This package supports the [walkthrough execution record](../../../../20260907_astra_review_walkthrough_execution.md).
It covers the incremental walkthrough follow-ups, not the earlier Astra implementation or
unexecuted provider/platform work. No source changes were staged, committed or published.

The fresh review correction is in [review-correction.zip](review-correction.zip), with its
[manifest](review-correction-manifest.json). It contains the original fresh review, targeted
correction report, parser/test before-and-after bytes, regression probes and current checks.
The correction record explains the original multiline fixture's trailing-period mistake.
Routing dispatch metadata is a labeled reconstruction from the parent conversation, not raw
runtime receipts or independent proof of hidden context. No native trial was rerun.

Download the unchanged pre-correction [evidence.zip](evidence.zip); verify its identity with [manifest.json](manifest.json).
The archive contains 377 entries, including its per-entry hash manifest. `source/final/`
contains exact source bytes reviewed/tested before the fresh review correction, and
`source/baseline/` the captured pre-WB files. Use the supplement for current parser/test bytes.
The owner's `SESSION_LOG.md` content is excluded; its unchanged identity was checked locally.
Other evidence text masks local user/run paths and email-shaped strings. Each entry records
both captured and stored hashes so redaction is not mistaken for identical raw output.

| Archive location | Evidence |
|---|---|
| `reports/consolidation-verification.json` | Current review identities, unchanged original AC sections, check inputs, HEAD and unstaged-work boundary |
| `reports/packaging-review.json` / `reports/semantics-review.json` | Independent lanes, original findings, corrected verdicts, targeted follow-ups and inspected hashes |
| `reports/packaging-probes*.json` | Original and corrected reference-style dependency reproductions, output-link and ownership probes |
| `descriptions/` | Proposals, preservation evidence, measurements, two catalogs, 100 blind cases, prewritten key and actual baseline/candidate selections |
| `reports/final-measurements.json` | Separate description/frontmatter/body and generated-reference size measurements |
| `confidence/` | Accepted contract draft, narrow replacements and integration evidence; later arithmetic correction is in final source and review follow-up |
| `native/` | Public copied procedures, fixtures, exact prompts, actual traces and artifacts, including blocked attempts and the failed arithmetic output |
| `reports/native-verification.json` | Parent artifact/trace/arithmetic checks and exact distinctions between procedure versions |
| `reports/native-arithmetic-failure.json` | Original task output reported 98.05 while its contributions total 99.05; preserved as FAIL |
| `final-checks/` | Executed command/exit/output records and environment identity; final affected checks are runs 12–17 |
| `reports/check-input-manifest*.json` | Actual source/configuration dependencies for each recorded validation phase |

Observed results:

- Descriptions: 16,694 → 10,733 characters; frontmatter: 18,232 → 12,287. No measured token/cost claim.
- Blind roster simulation: baseline 99/100; candidate 100/100. This is not native discovery.
- Three completed document outputs provide explicit scoped scoring. The original tasks output
  failed arithmetic; a fresh full tasks trial using final procedure bytes executed arithmetic
  and produced a correct total. Analysis/design and policy-boundary outputs predate that narrow
  refinement and are preserved with their actual procedure identities.
- Three bounded policy slices preserve the stricter 98 threshold, mandatory integration
  evidence despite prior score 97, and active-P1 depth without causal or action permission.
- Repository Node checks and Python sync suite pass on Linux. The latter ran 41 tests with
  one Windows-only test skipped. The final isolated-home check resolves 62 links for 31 skills.

The three initial mount-fixture trials stopped at process-launch EACCES before skill reads.
The successful retries retained the native workspace-write sandbox, disabled project instruction
loading and used explicit local procedure copies. Their traces did not access the source checkout;
they do not establish physical source absence. Detached file-resolution probes separately verify
that required targets stay inside the copied skill folders.

Native CLI requested `gpt-5.6-sol`; resolved provider identity was not independently exposed.
These small explicit-invocation fixtures do not establish universal model reliability, native
discovery, full pipeline behavior, or Claude/Cursor/Windows/macOS parity. Existing hosted CI and
provider limitations remain as recorded in the execution document. Human GO and any commit are pending.
