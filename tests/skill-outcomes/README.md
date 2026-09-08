# Skill outcome corpus

This small corpus evaluates routing, procedure execution, produced artifacts, and final outcomes
separately. It supplements the existing portability/sync tests; passing those tests does not prove
these outcomes. Cases are anonymized reproductions of reviewed contracts, not claims that historical
incidents were replayed. `cases.json` owns the prompts, fixture contents, setup recipes and mandatory
grading criteria. Fixture paths are relative to a new isolated trial root; never materialize them
over the real repository. No generic model runner is required.

## Predeclared comparison and decision rule

Run each selected case twice per condition in fresh independent contexts, preserving unsuccessful
runs. If capacity requires several cases in one worker, treat the worker as one shared-context batch: record
its case order and batch ID, use a separate fresh worker for every condition/repetition, and disclose
possible cross-case learning. Such a batch is not evidence of case-level context independence. Keep the fixture, user prompt, tool access and provider/model/settings the same across a pair.
Vary only the supplied skill instructions. Declare additional repetitions before looking at their
results; never hide a failed trial by rerunning until green.

| Condition | Instructions | What the comparison can establish |
|---|---|---|
| `no-skill` | User prompt + fixture + necessary safety/user instructions; no skill body | Whether the skill adds value beyond direct task assistance; omit with reason when an interface is skill-specific |
| `current` | Bodies and relevant references from reviewed commit `aeec06bfa0a6b97402b17824d957f29635f40ba7` | Reproduces the prior instruction contract; does not replay historical outcomes |
| `candidate` | Exact proposed working-tree bodies/references captured before the run | Whether the repair retains obligations or a proposed simplification earns adoption |

A second simplification candidate must have a distinct condition ID and preserved body. Do not edit
a deployed skill merely to run the experiment. Freeze source snapshots for a comparison batch; later
edits are another batch. Broad simplification is adopted only if all mandatory checks pass across
the repeated selected cases with no missed required obligation or unauthorized action. Lower
interruptions, retries, output size, latency, or cost are secondary benefits; none can compensate for
lost coverage, wrong roots, false evidence, or violated user cadence. If quality is tied and savings
are unmeasured/inconsistent, retain the current default and record the inconclusive result. A
bounded proven defect repair need not wait for unrelated simplification experiments.

## Prepare and dispatch

1. Pick a case and materialize its `files` in a fresh scratch root. Apply its `state.recipe` before
   dispatch, recording setup commands separately from agent work. Preserve input hashes, Git base,
   all dirty layers, and relevant environment identity. Where case variants are independent, use
   separate copies. Do not seed claimed PASS evidence without executing its producer or labeling it
   explicitly as supplied synthetic evidence.
2. Capture the exact user prompt, any conversation responses, loaded instruction bodies/references,
   tool availability, and public-safe source manifest. Hash bytes with SHA-256. For current bodies,
   use `git show <reviewed-revision>:<path>`; for candidates, read the actual working-tree path.
   Missing baseline/externally owned files are `unavailable` with reason, not silently substituted.
3. Dispatch a fresh worker with only that condition's prompt/context. A worker receiving bodies is a
   **supplied-body procedure trial**, not proof of native skill discovery. A description-only roster
   test is a **routing simulation**. Native discovery/invocation is a separate host probe that records
   the actual mechanism and exact literal input; if inaccessible, mark it unavailable.
4. Save the complete worker output and tool trace promptly, plus produced artifact files and their
   hashes. Give interruptions consistent scripted answers when they are part of the fixture; record
   unspecified blocking questions as such. Do not let answer variation masquerade as a skill effect.
5. Grade every mandatory check as pass/fail/unavailable using exact trace/artifact locators. A check
   needing execution/rendering cannot pass by prose assertion. Record scope limitations, unexpected
   behaviors and failures. Parent re-grounding uses source/artifact bytes or reruns the relevant probe.
6. Preserve `run.json` using `run-record.example.json`, the transcript, artifacts, inputs and grading
   under `runs/<batch>/<condition>/<case>/<repeat>/`. If a tool cannot expose full trace, preserve its
   available output and mark the missing trace explicitly. No secrets or private home paths in checked-in
   records. Final owner review remains pending until the user reviews the judgment-heavy grades.

## Measurement rules

- Record exact provider/host, model and reasoning setting only when exposed or explicitly selected;
  unknown fields are `unavailable`, never inferred from output. Inherited settings must say inherited.
- Count actual unnecessary approval interruptions separately from required clarifications and requested
  discussion cadence. Record retries and their reasons, including failed/abandoned trials.
- Measure UTF-8 artifact bytes with a command over produced files, and report both artifact and total
  output size when available. Do not claim savings from squeezed lines or missing required sections.
- Record elapsed time from actual timestamps. Record tokens and monetary cost only from measured
  provider output; otherwise `null` with `unavailable_reason`. Never infer cost from model labels.
- Compare missed obligations, false positives, interruptions and retries per case/condition before
  aggregating. The small personal corpus does not establish universal skill or model rankings.

## Coverage and execution status

The cases include the required dirty-scope, consumer-closure, malformed-tag, completion-dependency,
wrong-root and clean-no-op controls, plus all engineering test-placement alternatives. Additional
cases exercise authorization, review severity/depth, check reuse, intent routing, teaching export and
learning evidence. Each case lists its backlog IDs. September 4 tag/consumer/dependency controls are
regression trials for already-applied improvements, not duplicate missing-feature tickets.

The corpus is an executable evaluation protocol with fixture data; its presence is not a trial pass.
Initial source snapshots and baseline availability are recorded in `source-manifest.json`; refresh
capture at each batch boundary. Native provider discovery, offline browser rendering, human review,
and unrun conditions must remain visibly pending/unavailable. A self-run by the author is allowed
as a fixture smoke check but cannot stand in for fresh independent model trials.
