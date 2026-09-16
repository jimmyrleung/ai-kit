# Bug/Incident investigation - [meaningful name]

## Executive summary

[1–2 sentences: what's broken, why, how to fix.]

## Effective policy

[severity/state, depth, threshold, causal requirements, action boundary.]

## Confidence score

[Detailed breakdown of the confidence score]

## Bug understanding

[reported issue, expected vs actual behavior, reproduction steps.]

## Entry point

[Map the entrypoint(s), including `file:line`]

## Execution path trace

[the call chain from entry to failure, with the variable state at each step, each hop distinguishing `SOURCE`, `OBSERVED`, and `INFERRED`, with provenance, causal limits, and next probes.]

## Root cause

[with category (Logic Error / State Management / Data Validation / Integration / Configuration), plus a **Falsifier** line: the concrete observation that would disprove this diagnosis.]

## Evidence

[logs, code references, variable states that support the diagnosis.]

## Proposed solution or next probe

[confirmed remediation, reversible mitigation, or unconfirmed candidate clearly distinguished; specific `file:line` references, the minimal change described (not coded), why it fixes the root cause.]

## Alternative approaches considered

[if any, including rejected ones.]

## Impact assessment preview

[files affected, tests needed, potential side effects.]

## Incident additions

[When it is an incident, add this section with the following items:

- **Incident timeline** — the correlated event sequence with timestamps (error onset vs deploys, config changes, traffic shifts — the correlation evidence the lens gathered, laid out for the `post-mortem` skill to build on)
- **Scope of impact** — affected users / services / data and duration, derived from the evidence, not estimated
- **Hypotheses ruled out** — each with the evidence that ruled it out (this list is what stops a war room re-litigating dead ends).]
