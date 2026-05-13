# Tasks — Slice [NN] — _[Slice name]_

|                  |                  |
| ---------------- | ---------------- |
| **Slice**        | NN               |
| **PRD**          | [`./PRD.md`]     |
| **Techspec**     | [`./techspec.md`] |
| **Total tasks**  | [N]              |
| **Total est.**   | [hours / days]   |
| **Created**      | YYYY-MM-DD       |

---

## Ordering principle

> **Vertical slicing inside the slice.** Each task moves the user-observable behavior closer to "shippable." **Do NOT order as setup → core → polish.** A task that only sets up infrastructure without moving demoable behavior forward is a code smell — bundle it with the task that actually needs it, or split the slice.

## Tasks overview

| #   | Title           | Complexity | Est. | Status      |
| --- | --------------- | ---------- | ---- | ----------- |
| 1   | [Title]         | S          | 1h   | Not started |
| 2   | [Title]         | M          | 3h   | Not started |
| ... | ...             | ...        | ...  | ...         |

**Progress:** 0/N (0%)

---

## Task list

### Task 1: [Action-oriented title]

**Description.** [What needs to be done. Be specific.]

**Why this task is on the list.** [What user-observable behavior moves forward when this is done. If you can't answer this, the task is wrong.]

**Files affected.**

- `path/to/file.ext` — [Action: create / modify / delete]

**Acceptance criteria.**

- [ ] [Testable]
- [ ] [Tests pass, if applicable]

**Depends on.** None / Task [ID]

**Complexity.** S | M | L (split if XL)

**Status.** Not started

---

### Task 2: [Title]

[same shape]

---

## Slice-close cross-check

When all tasks above are done, verify:

- [ ] Every Done-when checkbox in [`./PRD.md`] passes
- [ ] No "while we're here" additions snuck in (those go to the next slice's backlog)
- [ ] Manual smoke test from the techspec passes

## Insights captured during the slice

<!-- Filled during/after implementation -->

- **What surprised me:** [...]
- **PRD/techspec gaps surfaced:** [...]
- **Technical debt knowingly taken:** [...]
