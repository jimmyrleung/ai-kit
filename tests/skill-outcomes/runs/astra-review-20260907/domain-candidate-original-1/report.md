# Candidate domain trial — repeat 1

Status: complete, pending owner review. Shared-context batch `domain-candidate-r1`; case order was documentation W1/W2/W3/T1, feedback T1–T6, B12 T1–T5, then the six corpus cases. Cases use independent fixture copies but not independent model contexts, so cross-case learning is possible.

The run executed 21 case groups and graded 65 mandatory checks: 63 pass and 2 unavailable. No mandatory check is recorded as PASS from procedure prose alone. The unavailable checks are:

1. Documentation T1's changed-readable-sibling probe: the fixture supplied no readable sibling module body. Remote module sources remain separately Unverifiable in the generated v4 artifacts.
2. Feedback T3's same-session new-decision receipt: the fixture asserted new work but did not supply the decision content. The log was preserved without inventing a decision or receipt.

The frozen snapshot omitted detector recipes, the canonical workflow output template, Terraform heuristics, and the close tag-checker script. No live or installed copy was substituted. The bodies, contracts, fixture source, and expected fixture contracts were sufficient for the other recorded checks; the omissions remain a setup limitation in `source-manifest.json`.

The clean-no-op corpus result is informed diagnostic evidence only because the parent disclosed a suspected ordering defect before execution. The explicit prompt authorization was honored, the real ownership checker ran, Git stayed clean, and no generic approval interruption or output write occurred.

Key review artifacts:

- Documentation: `cases/documentation-w1`, `documentation-w2`, `documentation-w3`, and `documentation-t1`.
- Feedback: `cases/feedback-t1` through `feedback-t6`; the SQLite ADR is `feedback-t6/repo/decisions/0004-use-sqlite.md`.
- B12 resolved comparison input: `cases/b12-resolved-base/` with original placeholders, exact bytes, resolved manifest, and limitation note.
- Teaching export: `cases/teaching-export/export/idempotency-offline.html`; identical relocated copy, inspected screenshot, and interaction trace are under `relocated/` and `render/`.
- Learning visual: `cases/learning-visuals/ordering.png` plus both interactive and structured results.

Evidence files: `run.json` contains every mandatory status and locator; `source-manifest.json` binds all loaded frozen bytes; `artifact-manifest.sha256` hashes 260 case files; `setup-commands.md` and `tool-trace.md` preserve setup and available command evidence. Case artifacts total 284,867 bytes. Tokens, cost, response bytes, and per-case aggregate timing are null because the host did not expose measured values.

No ai-kit file was written, staged, or committed. Existing ai-kit worktree changes were observed only by read-only `git status`.

- Confidence score: 92% — direct artifact inspection, byte hashing, Git checks, and browser rendering cover the recorded outcomes.
- 8% uncertainty — four referenced frozen resources were absent, two checks were unavailable, final judgment-heavy owner review is pending, and the shared worker context prevents case-level independence.
