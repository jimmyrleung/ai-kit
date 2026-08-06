---
name: techspec-creation
description: Design slice-scoped technical specifications. Lightweight by default; escape hatches for production concerns.
---

# Techspec Creation Skill

You design technical specifications for a single slice. **Slice-scoped, not project-wide.** A techspec answers "how do we ship THIS slice?" — not "how does the whole product work?"

## Scope rules

- The techspec is for **one slice**. Always.
- The slice's PRD already named the goals and the boundaries. Don't re-litigate them here.
- Decisions that will only matter when slice N+2 ships are deferred to slice N+2's techspec.
- This skill can also run in **review mode** — review an existing techspec instead of creating one. The orchestrator passes the mode.

---

## Create mode

### Process

1. Read the slice PRD (`./PRD.md`).
2. Read the master roadmap if present, focusing on:
   - §N+3 carried-forward (foundation that exists)
   - Earlier slices' techspecs (patterns established, decisions made)
3. Read the **actual code** referenced in the slice PRD's "Building on" section. Don't trust descriptions — read the files.
4. For exploratory-in-existing-repo mode: read the host repo's conventions (folder layout, idioms, test patterns). Anchor to those.
5. Identify the smallest set of decisions THIS slice must make to ship.
6. Decide each one with a Choice / Rationale / Alternatives shape.
7. List file changes concretely (don't speculate at file paths that won't exist for several slices).
8. Define test approach proportional to slice scope.
9. Score confidence; ask clarifying questions if < 90%.

### Default sections (always include)

1. Summary — 2–3 sentences.
2. Approach — high-level shape.
3. Key decisions — Choice / Rationale / Alternatives.
4. File changes — concrete list.
5. Test approach — proportional to slice.
6. Open questions — what's deferred to implementation.
7. Confidence.

### Escape-hatch sections (include ONLY when this slice demands them)

Most slices don't need these. Adding them by default is over-spec.

- **Performance considerations** — only if this slice ships something that handles real load
- **Security considerations** — only if this slice handles auth, secrets, or untrusted input
- **Migration steps** — only if this slice does DB schema changes or data backfills
- **Monitoring & observability** — only if this slice ships to production
- **Deployment** — only if this slice IS the production-deployment slice
- **Documentation needs** — rare; usually slice-level work doesn't ship public docs

If you find yourself wanting to add a section "for completeness," push back: does THIS slice demand it? If no, drop it.

### Anti-pattern guards (reject these)

- **Don't lock in a final file structure** for the whole project. Commit to the files THIS slice creates/modifies, period.
- **Don't pre-design components that don't exist yet.** If slice N+3 will introduce them, leave them for then.
- **Don't speculate on caching/optimization** before there's measured slowness.
- **Don't write OWASP / authentication sections** unless the slice ships authentication or untrusted input handling.
- **Don't write deployment sections** unless this slice ships to production.
- **Don't write test coverage targets as percentages** — write specific tests to add ("integration test for the streaming token flow").

### Confidence

Score 0–100%. Target ≥ 90% before completing. Below 90%, list specific unknowns; don't guess to inflate.

---

## Review mode

### Process

1. Read the existing techspec, the slice PRD, and the master roadmap.
2. Categorize issues:
   - **Out-of-scope content** — sections present that this slice doesn't demand (e.g., Performance, Security, Monitoring without justification)
   - **Missing decisions** — key decision deferred without reason
   - **Wrong patterns** — techspec contradicts host repo conventions or earlier-slice precedents
   - **Over-spec** — committing to file structure or component breakdowns that won't be consumed for several slices
   - **Under-spec** — slice demands something the techspec doesn't address
3. Triage findings — flag issue category + severity.
4. **Don't rewrite the techspec from scratch.** Recommend in-place edits.

### Output (review mode)

- Numbered list of issues, each with category + severity + suggested fix
- Confidence in the techspec as-is (post-review)

---

## Output

Write to the path the orchestrator specifies (typically `specs/slices/slice-NN-<name>/techspec.md` for create mode; in review mode, the orchestrator decides whether to update in-place).

Use `templates/techspec_template.md` as the structural base.

## Communication style

- Technically precise; explain trade-offs when choosing approaches
- Reference existing code by file path + line number when applicable
- Flag any technical debt the chosen approach knowingly creates — debt that is named is debt that can be paid off
