# Decision — impeccable as the design reference, as reading material only

**Date:** 2026-11-15. **Status:** accepted by the owner (through the approved research and design system).

## Context

The `ui-process` skill recommends one of two public skills in steps 4 and 5 to avoid generic AI-looking
design: `taste-skill` and `impeccable`. A research agent read both repositories on 2026-11-15.

## Decision

Use `impeccable`, and only read it. Do not install or run its engine, hooks, live mode or network catalog.

## Why

- `impeccable` has a "Read" mode for documents and guides, is stack-neutral, and gives a design-document
  format (`DESIGN.md` with token frontmatter and eight fixed sections) that the design system here follows.
- `taste-skill` on `main` was rebuilt on 2026-11-05 into a kit for company marketing sites: one section per
  screen, required motion, Google Fonts, no accordions, nothing on tables, code or print. Its "dials" exist
  only in the older `taste-skill-classics` repository.
- Both skills tell an agent to run binaries or hooks. None of that is needed to use their rules.

## Consequences

- Rules taken from `impeccable`: no label above a heading, no nested cards, mono only for code, roles for
  colours, motion only for state, every component with all its states.
- Rules deliberately not followed: tables turned into cards on phones, the push to a more distinctive
  frame, the ban on section numbers that carry meaning.
- One idea taken from `taste-skill`: the "one of each" check (one button shape, one card recipe, two
  surfaces deep at most).
- The `ui-process` skill's "Skill references" section still presents both as equal choices.
