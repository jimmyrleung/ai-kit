---
name: bug-investigation
description: "Diagnoses a reported bug, error, crash, regression, or unexpected behavior from source and runtime evidence, with a minimal-fix proposal or next probe. Use to investigate, debug, or root-cause a failure, including a production incident or outage. Accepts a bug report, issue link, or inline reproduction; Produces `investigations/[slug]/investigation.md`."
---

# Bug investigation

## Goal

From a bug or incident report:

- Gather context from the relevant sources
- Trace through the code to identify the cause supported by the available evidence, or the precise next probe.

Then:

1. When it is a code issue, propose a **minimal** fix with specific `file:line` references.

2. When the issue is caused by an external element, provide a detailed summary with hypothesis

**IMPORTANT**: In both scenarios, separate source facts, runtime observations, and hypotheses; code alone does not establish that a branch caused a particular incident.

> **Litmus test:** if you're proposing a refactor or writing implementation pseudocode, you've gone too far. Your output diagnoses _why_ it breaks and points at the minimal change — the implementation phase writes the code.

## Approach

**The approach should follow each subsection below sequentially.**

### Initial context

Ensure you have enough information to get started on the investigation. It is expected that the user shares one of the following:

- An inline prompt with enough details on the bug or incident.
- An input file with enough details on the bug or incident, like an initial investigation or similar.
- A folder containing a set of relevant files that provide relevant context

> If not provided, or it is too vague, pause and ask the user what's the initial context.

Inspect the input(s) end-to-end and confirm its understanding.

### Investigate

Execute the following steps sequentially accounting for the [Incident lens], [Absence-claim guidance], and [Subagents guidance] protocols:

1. **Inspect the bug report.** Extract: what's broken, how to reproduce, expected vs actual behavior, affected components. Note any suspected files the reporter named.

2. **Map relevant info and artifacts.** Read the AGENTS.md file(s) and any referenced documents (especially rules) to gather context from each project involved, and map any relevant info to account for during the investigation, or any useful skills for the investigation.

3. **Locate the relevant code.** Search the codebase for: entry points (API endpoints, UI handlers, jobs), the core business logic related to the bug, data-access layers, error-handling code.

4. **Inspect and query relevant sources.** When applicable and available, inspect and query relevant sources, like live resources (application logs, config resources, etc.), monitoring and logging tools available, database, etc.

5. **Trace the execution path.** Record each hop and variable state with evidence type:

- **SOURCE** = inspected code/config proves a possible mechanism;
- **OBSERVED** = executed reproduction, logs, debugger, trace or DB probe shows behavior with inputs, build/config, time/environment and result;
- **INFERRED** = causal hypothesis, with its next confirming probe and falsifier. Separate these within a hop when necessary.

Do not call a source-read configuration/race branch the incident cause without evidence that it executed and explains the symptom in that incident. A deterministic reproduction can establish a reproducible defect; claiming it explains a production incident still needs incident linkage.

6. **Analyze the root cause.** Determine _why_ it fails and categorize:

- Logic Error (wrong condition / bad calculation)
- State Management (race condition / stale data)
- Data Validation (missing check / wrong type)
- Integration (API change / dependency problem)
- Configuration (environment-specific).

Check git history if relevant (when was the buggy code introduced?). If you find multiple plausible causes, investigate the most likely first.

This step is complete when you can determine the root cause.

#### Incident lens

When it is a production incident, outage, or live severity:

- **Evidence widens beyond code:** error patterns and frequencies in logs, trace timings and timeouts, metric spikes — each with timestamps, **correlated against the incident timeline** (deploys, config changes, traffic shifts). Every quantitative claim (counts, rates, durations) cites the query or log excerpt that produced it.

- **5-Whys depth:** "the pool was exhausted" is the symptom — keep asking why until you reach the change or design that caused it, tagging each why SOURCE / OBSERVED / INFERRED like any other hop.

#### Absence-claim guidance

Before asserting "no event / no error / not used / nobody sets this":

- **Positive control first:** prove the probe can see data of the target class at all (query a known-to-exist event in-window) before interpreting an empty result as absence.
- **Right channel / full enumeration:** enumerate which log channels/stores are actually enabled (platform operational channels, not just the default) and paginate to completion — page 1 of a filtered read is not the population.
- **Sample the identifier format:** pull one known instance of the target class and copy its exact identifier encoding before sweeping (a GUID sweep missed base64-encoded protobuf ids).
- **History before blame:** search the repo's artifacts for the suspect symbol before root-causing it as a mistake — a recorded decision was called a copy-paste error at 95% confidence. For authz bugs, enumerate scheme → handler → claims issued before reasoning from an endpoint's policy attribute.

#### Subagents guidance

1. When available and applicable, use subagents for doing evidence-based exploration for distinct areas. Launch it with proper instructions according to this bug-investigation flow. Ensure each subagent:

- Do not make assumptions: they should trace through the code and logs systematically.
- Return clarification questions instead of guessing, for anything they can't establish reproduction steps, execution path, and/or the root cause.
- Support each claim with logs, traces, or code references.

2. Each subagent should be doing one focused exploration for reduced degradation.

3. Each subagent should report a confidence score according to the [Confidence score] guidance described on the [Consolidate] step.

### Consolidate

1. Consolidate the investigation with one or more minimal solution proposals with causal evidence.

2. Calculate the confidence score, according to the following guidance:

- Use an explicit 0–100% assessment for the scoped conclusion or next workflow step.
  This is a structured judgment of evidence and remaining uncertainty, not a calibrated
  probability of correctness, success, or safety. A score never supplies facts, turns
  worker agreement into proof, passes an unrun/failed check, or grants authorization.

- Factors and weights:
  - Causal clarity and evidence 40%
  - Codebase/execution-path understanding 30%
  - Proposed solution or next-probe simplicity and fit 15%
  - Similar-pattern coverage 15%
  - State whether the subject is a confirmed diagnosis, candidate hypothesis, or mitigation.

3. Display to the user a concise summary, including:

- Key insights and relevant details for the investigation
- Key events timeline when there is an incident associated with the investigation
- Solution proposals with your recommendation
- Summary of the confidence score in the following format:

  ```
  Confidence: X% - {justification}
  Remaining uncertainty: {justification}
  ```

So the user can make a decision: choose one of the proposals or iterate on the investigation.

### Write investigation document

Once the user decides on a given solution, write the final investigation document:

- Read `./references/TEMPLATE.md` thoroughly - this is the final investigation document template
- Write the investigation document following the template structure on `specs/[slug]/investigation.md`
