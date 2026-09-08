# Engineering no-skill trial — repetition 1

## Run conditions

- Condition: direct coding assistance, no skill body supplied or read.
- Ordered cases: `existing-test-home`, `convention-new-test`, `no-suitable-test-home`.
- Corpus source: `<user-home>/ai-kit/tests/skill-outcomes/cases.json`, limited to those three selectors.
- Prompt execution: once per case, with actual fixture edits and the repository test command.
- Requested worker profile: `gpt-5.6-sol`, reasoning `high`. Distinct effective model/reasoning telemetry was unavailable.
- Token count, cost, and full transcript: unavailable (`null` in `run.json`).
- Host disclosure: the inherited context exposed skill catalog names and descriptions. No skill body or other condition/trial result was read or used.
- Skill-specific interfaces: intentionally unavailable in this no-skill condition; native editing and shell test execution were used.
- User interruptions: 0. Implementation retries: 0. Test retries: 0.
- Administrative trace: the first final-artifact copy retained an absolute parent hierarchy under `output/final/tmp/...`; one additional canonical copy was made under `output/final/artifacts/`. Both are outside fixtures. This did not re-execute any prompt or test.

## Results

| Case | Mandatory checks | Test result | Original bytes | Final bytes | Delta |
|---|---:|---|---:|---:|---:|
| existing-test-home | 6/6 | PASS, 3 tests | 427 | 658 | +231 |
| convention-new-test | 6/6 | PASS, 3 tests | 523 | 837 | +314 |
| no-suitable-test-home | 6/6 | PASS, 4 tests | 464 | 836 | +372 |
| Total | 18/18 | PASS | 1,414 | 2,331 | +917 |

All byte counts are UTF-8 file byte measurements. The fixtures contain ASCII-only content, so these are also the serialized UTF-8 sizes. Each literal prompt is 237 bytes, has no trailing newline, and has SHA-256 `0851f04370df4b4e1af4f40740efc10a7d6f070248e82e7c8cbad9fb5cbd19fa`, matching `jq -j` extraction from the corpus.

## existing-test-home grading

1. **PASS — Extends `tests/test_calc.py`; no new test file.** Negative and zero cases are in `cases/existing-test-home/output/final/artifacts/tests/test_calc.py:4` and `:8`; the positive case remains at `:11`. The final artifact inventory and hashes are in `cases/existing-test-home/output/traces/hashes.tsv`.
2. **PASS — Reads instructions, nearby code/tests/docs/CI.** The pre-edit read list is in `cases/existing-test-home/output/traces/context-read.txt`; it includes `AGENTS.md`, `calc.py`, `tests/test_calc.py`, `README.md`, and `.github/workflows/test.yml`.
3. **PASS — Uses existing unittest patterns and appropriate fixtures.** The existing `unittest.TestCase` module was extended directly at `cases/existing-test-home/output/final/artifacts/tests/test_calc.py:3`; a pure function requires no fixture setup.
4. **PASS — Negative, zero and positive behavior verified by executed tests.** Assertions are at `tests/test_calc.py:4`, `:8`, and `:11`; the actual 3-test passing run is recorded in `cases/existing-test-home/output/traces/test.txt`.
5. **PASS — No speculative helper or unrelated cleanup.** Changed content is limited to the guard in `calc.py:2` and the two requested behavior tests in `tests/test_calc.py`; unchanged artifact hashes are recorded in `hashes.tsv`.
6. **PASS — No broad refactor or file-count optimization at expense of coverage.** No production helper or new test module was added, and all three behavior classes are executed.

## convention-new-test grading

1. **PASS — Creates convention-required `tests/test_calc_validation.py` and states reason.** `AGENTS.md:1` requires validation failures in that file; negative coverage is at `cases/convention-new-test/output/final/artifacts/tests/test_calc_validation.py:5`. The direct response records the reason in `cases/convention-new-test/output/response.md`.
2. **PASS — Reads instructions, nearby code/tests/docs/CI.** The pre-edit read list is in `cases/convention-new-test/output/traces/context-read.txt`.
3. **PASS — Uses existing unittest patterns and appropriate fixtures.** Both test modules use the observed `unittest.TestCase` pattern; the pure function needs no setup fixture.
4. **PASS — Negative, zero and positive behavior verified by executed tests.** Negative is at `tests/test_calc_validation.py:6`; zero and positive are at `tests/test_calc.py:4` and `:7`. The actual 3-test passing run is in `cases/convention-new-test/output/traces/test.txt`.
5. **PASS — No speculative helper or unrelated cleanup.** The only production change is the direct guard at `calc.py:2`; existing instructions, README, and CI hashes remain unchanged.
6. **PASS — No broad refactor or file-count optimization at expense of coverage.** The one new module is explicitly required by repository convention, and normal-calculation coverage stays in its existing home.

## no-suitable-test-home grading

1. **PASS — Creates suitable test module and explains absent existing home.** The existing `tests/test_label.py` covers labels only; focused fee coverage is in `cases/no-suitable-test-home/output/final/artifacts/tests/test_calc.py:5`. The direct response explains the choice in `cases/no-suitable-test-home/output/response.md`.
2. **PASS — Reads instructions, nearby code/tests/docs/CI.** The pre-edit read list is in `cases/no-suitable-test-home/output/traces/context-read.txt`, including the unrelated nearby test.
3. **PASS — Uses existing unittest patterns and appropriate fixtures.** The new test follows the observed `unittest.TestCase` pattern; the pure function needs no setup fixture.
4. **PASS — Negative, zero and positive behavior verified by executed tests.** The assertions are at `tests/test_calc.py:6`, `:10`, and `:13`; the actual 4-test passing run is in `cases/no-suitable-test-home/output/traces/test.txt`.
5. **PASS — No speculative helper or unrelated cleanup.** The only production change is the direct guard at `calc.py:2`; `tests/test_label.py` and all supporting files retain their original hashes.
6. **PASS — No broad refactor or file-count optimization at expense of coverage.** One focused test module was added as instructed and all relevant behavior was covered.

## Confidence

Confidence score: 99%. The grading is grounded in preserved original and final files, SHA-256 hashes, explicit pre-edit read traces, and actual passing test output. The remaining 1% is the mandatory human-review judgment and the lack of full harness telemetry/transcript.
