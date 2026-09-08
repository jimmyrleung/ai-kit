# No-skill engineering trial — repetition 2

Collected at `2026-09-07T08:08:46-03:00` in one shared-context batch and the declared case order. All three prompts were executed once as direct coding assistance. No skill-specific interface was needed.

## Outcome

| Case | Mandatory grade | Executed suite | Interruptions | Retries | Final artifact bytes |
|---|---:|---|---:|---:|---:|
| `existing-test-home` | 6/6 pass | 3 tests, pass | 0 | 1 | 658 |
| `convention-new-test` | 6/6 pass | 3 tests, pass | 0 | 0 | 838 |
| `no-suitable-test-home` | 6/6 pass | 4 tests, pass | 0 | 0 | 837 |

The retry was a failed hash-collection command from the wrong working directory before task edits. It is reproduced in `cases/existing-test-home/shell-trace.txt`. There were no implementation or test retries.

## `existing-test-home` — 6/6

1. **PASS — Extends `tests/test_calc.py`; no new test file.** The final artifact is `cases/existing-test-home/artifacts/final/tests/test_calc.py`; the original/final inventories in `hashes.txt` show the same test-file set.
2. **PASS — Reads instructions, nearby code/tests/docs/CI.** Exact read order and paths are recorded in `source-context.md`; the read command is in the case shell trace.
3. **PASS — Uses existing unittest patterns and appropriate fixtures.** The final test artifact extends `FeeTests(unittest.TestCase)` and uses `assertEqual`/`assertRaises`; no fixture setup is needed for this pure function.
4. **PASS — Negative, zero and positive behavior verified by executed tests.** The suite section of `cases/existing-test-home/shell-trace.txt` records the real command, exit 0, and 3 tests. The three cases are in the final test artifact.
5. **PASS — No speculative helper or unrelated cleanup.** Original/final artifacts and hashes show changes only to `calc.py` and `tests/test_calc.py`, with no helper introduced.
6. **PASS — No broad refactor or file-count optimization at expense of coverage.** The final artifact retains the existing structure and adds only the guard and two needed cases.

## `convention-new-test` — 6/6

1. **PASS — Creates convention-required `tests/test_calc_validation.py` and states reason.** The final artifact exists at `cases/convention-new-test/artifacts/final/tests/test_calc_validation.py`. The reason, taken from `fixture/AGENTS.md`, is recorded in the case shell trace: validation failure scenarios belong in that separate module.
2. **PASS — Reads instructions, nearby code/tests/docs/CI.** Exact read order and paths are recorded in `source-context.md`; the read command is in the case shell trace.
3. **PASS — Uses existing unittest patterns and appropriate fixtures.** Both final test artifacts use `unittest.TestCase`; no fixture setup is needed for this pure function.
4. **PASS — Negative, zero and positive behavior verified by executed tests.** The suite section of `cases/convention-new-test/shell-trace.txt` records the real command, exit 0, and 3 tests. Positive/zero are in `test_calc.py`; negative is in `test_calc_validation.py`.
5. **PASS — No speculative helper or unrelated cleanup.** Original/final hashes show only the guard, zero test, and required validation module were added.
6. **PASS — No broad refactor or file-count optimization at expense of coverage.** The file split follows the explicit convention while preserving full boundary coverage.

## `no-suitable-test-home` — 6/6

1. **PASS — Creates suitable test module and explains absent existing home.** The final artifact exists at `cases/no-suitable-test-home/artifacts/final/tests/test_calc.py`. The case shell trace records that `fixture/AGENTS.md` says no existing module covers `fee`; `tests/test_label.py` is unrelated and remains byte-identical.
2. **PASS — Reads instructions, nearby code/tests/docs/CI.** Exact read order and paths are recorded in `source-context.md`; the read command is in the case shell trace.
3. **PASS — Uses existing unittest patterns and appropriate fixtures.** The new module follows the neighboring `unittest.TestCase` pattern; no fixture setup is needed for this pure function.
4. **PASS — Negative, zero and positive behavior verified by executed tests.** The suite section of `cases/no-suitable-test-home/shell-trace.txt` records the real command, exit 0, and 4 tests (three fee cases plus the existing label test).
5. **PASS — No speculative helper or unrelated cleanup.** Original/final hashes show `tests/test_label.py` and all non-task files remained byte-identical.
6. **PASS — No broad refactor or file-count optimization at expense of coverage.** The implementation adds one focused module and the minimal guard.

## Evidence and limits

- Literal prompts: `cases/<id>/prompt.txt`.
- Source/context record: `source-context.md`.
- Original and final file copies: `cases/<id>/artifacts/original/` and `cases/<id>/artifacts/final/`.
- Hashes and UTF-8 byte measurements: `cases/<id>/hashes.txt`.
- Shell commands, suite output, and the single failed attempt/retry: `cases/<id>/shell-trace.txt`.
- All artifact and prompt files passed an `iconv` UTF-8 validation check.
- Corpus marks every case as `human_review_required`; the grades above are evidence-backed worker grades pending that review.
- Requested model was `gpt-5.6-sol` with `high` reasoning. Distinct effective-model telemetry was unavailable. Token usage, cost, and full transcript were not exposed and are recorded as null in `run.json`.

Confidence score: **99%** — full corpus criteria were available, all relevant fixture files were read, direct file artifacts and hashes were preserved, and each repository suite passed. The remaining 1% reflects the corpus-required human review and unavailable effective-model telemetry.
