---
description: Verify an implementation against its spec — runs the qa-gates skill (5 pass/fail gates: build/test, AC, cross-cutting, docs, human go/no-go).
argument-hint: <prefix>
arguments: prefix
---

# Goal

Verify the implementation referenced by `$prefix` passes the standard QA gates.

**Reference files:** `$prefix`

## Pre-work — context + code review

1. **Gather context.** `Read` all relevant files starting with `$prefix` — the techspec, tasks,
   analysis, audit, or investigation document the prefix owns.
2. **Code review (if non-trivial implementation).** Launch 1-3 `@code-reviewer-agent` agents in
   parallel with different focuses: simplicity/DRY/elegance, bugs/functional correctness,
   project conventions/abstractions. Hand them the reference files. Consolidate findings;
   present highest-severity issues to the user; ask: fix now / fix later / proceed as-is.
   Address based on their decision.

## QA gates

3. Use the `qa-gates` skill with:
   - `prefix`: `$prefix`
   - `gates_to_run`: `all`
   - `mode`: `full`  (use `streamlined` only for P1-incident hotfix closeouts)
   - `confidence_gate`: `90`
   - `next_step`: `Declare done — merge / hand back to orchestrator`

When the skill hands back, the `## QA` section in the prefix's review/QA doc is the source of
truth. Done.

## Alias

Also invocable as `/implementation-quality-assurance` — same shim, same skill (back-compat).
