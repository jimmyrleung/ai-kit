# Slice [NN] — _[Slice name]_

> [One sentence — the demoable behavior at slice close.]

|                  |                                                |
| ---------------- | ---------------------------------------------- |
| **Slice**        | NN                                             |
| **Theme**        | [What this slice is fundamentally about]       |
| **Size (rough)** | 1–3 days                                       |
| **Depends on**   | [Previous slice(s) or carried-forward foundation] |
| **Blocks**       | [Slice(s) that need this one]                  |
| **Status**       | Not started / In progress / Done               |
| **Roadmap**      | [`../../00-roadmap.md`] §N+4 Slice NN          |
| **Created**      | YYYY-MM-DD                                     |

---

## 1. Summary

[Plain prose, two paragraphs at most. First paragraph: what this slice ships in user-observable terms. Second paragraph: why this slice exists vs. doing it later or doing it differently.]

## 2. Goals & non-goals

### Goals

- [User-observable behavior 1]
- [User-observable behavior 2]

### Non-goals

- [What this slice deliberately does not ship — every non-goal points to a later slice that owns it, e.g., "Authentication → slice 3"]

## 3. Scenarios & acceptance criteria

### S1 — [Scenario name]

> **As a [user type], I want** [observable behavior].

**Acceptance criteria:**

- [Concrete, testable, end-user-observable]
- [Another criterion]

## 4. UX decisions

<!-- Only if this slice ships UI. Each decision: Choice / Rationale / Alternatives rejected. Skip the section entirely if not applicable. -->

### 4.1 [Decision name]

- **Choice.** [What we're going with]
- **Rationale.** [Why]
- **Alternatives rejected.** (a) [X — rejected because Y]. (b) [Z — rejected because W].

## 5. Done-when

- [ ] [Concrete checkbox — testable by opening the product or running a single command]
- [ ] [Another criterion]

## 6. Out of scope (explicitly rejected for this slice)

- **[Capability]** → slice [NN] (where it's owned)
- **[Capability]** → deferred until [trigger condition]

## 7. Building on (existing code this slice consumes)

<!-- Concrete file paths, not abstract systems. Pulled from the roadmap §N+3 carried-forward + prior-slice outputs. -->

- [`path/to/file.ext`] — [what we use from it]

## 8. Deferred to techspec

<!-- Decisions the upcoming techspec must make. Recommendation included where I have a clear prior. -->

- **[Decision name].** [Recommendation pending techspec; my prior is X.]

## 9. Open questions (non-blocking)

- [Question — won't block techspec authoring but worth flagging]

## 10. References

- **Roadmap** — [`../../00-roadmap.md`]
- **Master PRD** — [link or inline reference]
- [Other docs / external references]
