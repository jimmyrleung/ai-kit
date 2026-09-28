# Decision: preserve synchronization and narrow portability checks

- **Status:** Accepted in session; pending repository commit
- **Date:** 2026-09-27

## Context

The `scripts/` directory mixed obsolete v2 tools with the live synchronization engine used by
both provider adapters. The existing GitHub Actions workflow also mixed repository portability
with stale test and evaluation fixtures.

## Decision

- Move the common engine to the repository root as `sync-skills.py`.
- Keep the Codex and Cursor scripts as thin wrappers around that engine.
- Keep a three-operating-system GitHub Actions workflow.
- Limit the workflow to live skill frontmatter/name rules, inventory consistency, local links,
  Python and adapter syntax, and isolated synchronization dry runs.
- Use Python's standard library; do not add another package manager or checker framework.

## Rationale

Synchronization is an active installation capability and has live callers. Portability checks
are useful, but they should verify repository shape and execution mechanics without defining
skill-quality evaluations.

## Consequences

- Installation behavior remains available after removing `scripts/`.
- The workflow has no npm dependency and no eval corpus.
- The Windows wrappers prefer `py -3` for reliable launcher selection.
- Final cross-platform confirmation depends on the next pushed GitHub Actions run.
