# Techspec — Slice [NN] — _[Slice name]_

|                |                       |
| -------------- | --------------------- |
| **Slice**      | NN                    |
| **PRD**        | [`./PRD.md`]          |
| **Status**     | Draft / Approved      |
| **Confidence** | [X]%                  |
| **Created**    | YYYY-MM-DD            |

---

## 1. Summary

[2–3 sentences. What approach are we taking? What's the shape of the change?]

## 2. Approach

[High-level shape. How does this slice extend or build on what exists? Diagrams or descriptions only when they add clarity — skip if obvious.]

## 3. Key decisions

<!-- Only decisions that matter for THIS slice. Don't pre-decide for future slices. -->

### 3.1 [Decision name]

- **Choice.** [What we're going with]
- **Rationale.** [Why]
- **Alternatives.** (a) [X — rejected because Y]. (b) [Z — rejected because W].

## 4. File changes

| File                   | Action          | Purpose                |
| ---------------------- | --------------- | ---------------------- |
| `path/to/file.ext`     | Create / Modify | [What it does]         |

## 5. Critical logic / non-obvious algorithms

<!-- Only if the slice has any. Pseudocode or prose. Skip the whole section if not applicable. -->

## 6. Test approach

<!-- Proportional to slice scope. Don't write coverage targets — write specific tests to add. -->

- **Manual smoke test** — [list the prompts/actions to verify by hand]
- **Automated tests** — [what to write, if any. May be "none for this slice; first tests land in slice X" if appropriate]

## 7. Open questions

<!-- Resolved during this techspec or deferred to implementation. Don't pretend to resolve them all. -->

- [Question]

## 8. Confidence

**Confidence: [X]%** — [reason]

**Uncertainty:**

- [Specific concern]

---

## Escape-hatch sections (include ONLY when this slice demands them)

> Don't include these by default. Add a section back ONLY when the slice has a real reason — production-bound, high-traffic, security-sensitive, deployment-critical, etc. Otherwise these belong in a later slice.
>
> - **Performance considerations** — caching, optimization, scaling
> - **Security considerations** — authn/authz, data handling, OWASP
> - **Migration steps** — DB schema changes, data backfills
> - **Monitoring & observability** — metrics, logging, alerts
> - **Deployment** — env vars, rollback plan, feature flags
> - **Documentation needs** — API docs, READMEs (rare for slice-level)
