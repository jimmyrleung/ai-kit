# Additional guidance for bugfix

Follow these instructions when working on a bugfix.

## Impact awareness

- Design the fix supported by the current reviewed investigation; route new contradictory causal evidence back to investigation and avoid drifting into a refactor plan.
- Emit a designated **Acceptance criteria** section with stable IDs for the fix's observable
  outcomes, mapped to the investigation's expected behavior and §6 test scenarios. This is
  the AC source for a tasks-doc-less implementation/verification handoff; deduplicate repeated
  obligations while preserving their source locators.
- The impact half is required, not optional: **direct dependencies** (who imports / calls / instantiates the changed code — grep, don't assume), **indirect** (shared state, side effects, events, config), **test coverage** of the changed paths and — explicitly — the gaps, plus the risk lens below.
- Keep it proportional: the design half may be short when the fix is small; the blast radius is why this doc exists.

## Design approach

For bugfix, we should consider both **minimal-changes** and **pragmatic-balance** depending on the urgency vs. root-cause fix.

Launch separate subagents to explore the different design approaches when in doubt of which one would be better.
