# Decision: remove the v2 evaluation tooling

- **Status:** Accepted in session; pending repository commit
- **Date:** 2026-09-27

## Context

The v2 work introduced `tests/`, multiple repository checker/generator scripts, Node package
metadata, and a large skill-outcome evidence corpus. The evaluation work was not part of an
approved specification, and its stale assumptions caused the portability workflow to fail after
the v3 skill review.

## Decision

Remove:

- `tests/`, including the historical skill-outcome corpus
- `scripts/bundle-skill-references.mjs`
- `scripts/check-mechanics-mirror.py`
- `scripts/check-skill-portability.mjs`
- `package.json` and `package-lock.json`

Do not replace these with a new evaluation framework during this cleanup.

## Rationale

Removing the unsolicited design restores a neutral starting point for a deliberately planned
evaluation system. Git history retains the removed evidence if it is later useful for research.

## Consequences

- Repository portability no longer depends on npm or the v2 fixtures.
- Future evaluations require their own requirements and design.
- Historical specifications may still mention the removed paths; they remain unchanged as
  historical records.
