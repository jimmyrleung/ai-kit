---
name: prd-creation
description: Create a self-contained per-slice PRD. Just-in-time at slice pickup. Anti-horizontal-scaffolding by design.
---

# PRD Creation Skill

You produce a self-contained PRD for a single slice. **Just-in-time** — invoked when the user is about to start that slice, not all upfront.

For the master roadmap (run once at project start), use the `roadmap-creation` skill instead.

## Goal

Produce a self-contained PRD for the named slice. Modeled after `templates/prd_template.md`.

## Process

1. Read the master roadmap if present, focusing on:
   - Part I §4 (principles), §5 (domain model) — for context
   - Part II §N+3 (carried-forward) — for foundation references
   - Part II §N+4 — the slice's own row
2. Read prior-slice PRDs/techspecs (especially the most recent one — patterns established there often carry forward).
3. Identify what user-observable behavior this slice ships.
4. Identify what this slice is NOT going to do (out-of-scope) — and which later slice owns each deferred item.
5. Identify "Building on" — concrete file paths for code this slice consumes.
6. Identify "Deferred to techspec" — decisions to make at techspec time, with a recommendation if you have one.
7. Ask clarifying questions if needed (max 2 rounds — slice PRDs are lighter than master roadmaps).
8. Generate the PRD.

## Refresh mode (slice PRD already exists)

If the target slice folder already has a PRD, run a REFRESH, not a creation: audit every
section against current code/roadmap; list the stale premises found (with file evidence)
**before** editing; carry unaffected sections; stamp the header
`> refreshed YYYY-MM-DD against <short-sha>` so the next refresh can diff the range.
The JIT-refresh discipline has caught wrong core premises three times (a never-shipped
mechanism across 5 sections; 5 stale premises + a new SDK capability that changed the central
mechanism) — fund it, don't skip it.

## Slice PRD requirements

- **§1 Summary** names the demoable behavior in user-observable terms.
- **Goals are user-observable.** "Component X exists" is not a goal; "User can do Y" is.
- **Non-goals point to which later slice owns the deferred item.**
- **Done-when is concrete checkboxes** — every box should be testable by opening the product or running a single command.
- **Building on lists actual file paths,** not abstract systems.
- **Deferred-to-techspec items have a recommendation** when there's a clear prior.

## Anti-pattern guards (reject these)

- **Reject "set up X" as a goal.** Goals are user-observable.
- **Reject Performance / Security / Monitoring / Deployment / Approval sections** in slice PRDs unless the slice specifically demands them.
- **Reject success metrics with baselines** (those belong in the master roadmap, not per slice).
- **Reject change logs and approval signature blocks** — overkill for slice scope.

## Confidence

Score 0–100%. Target ≥ 90%. Below 90%, ask clarifying questions.

## Output

Write to the path the orchestrator specifies:

- `specs/slices/slice-NN-<name>/PRD.md` (or host repo's existing convention for exploratory mode)

Confirm the path with the user before writing.

## Communication style

- Concise, decisive
- Include the slice name in headers (improves grep-ability across slices)
- Reference the master roadmap by section number (`§4 principle 8`, `§7 S6`)
- Don't include planning material the reader doesn't need — write the PRD, not a meta-document
