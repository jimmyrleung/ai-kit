# [Project name] — Product & Roadmap

> Master spec **and** vertical-slice implementation roadmap.
>
> - **Part I (§1–§N)** — product context. For new-product mode this is rich. For MVP / exploratory it's deliberately thin.
> - **Part II (§N+1+)** — slice list. Each slice gets a self-contained PRD at `specs/slices/slice-NN-<name>/PRD.md` (or the host repo's existing convention).
>
> **Mode:** [one-off / mvp / new-product / exploratory]
> **Created:** YYYY-MM-DD

---

# Part I — Product

## 1. Executive summary

[2–4 sentences: what is this thing, what problem does it solve, who is the user?]

## 2. Context & motivation

<!-- Light for MVP, full for new product, "what reference are we anchoring to" for exploratory. -->

[Why are we doing this? What's the trigger?]

## 3. Target audience

<!-- Skip for one-off / exploratory if internal-only. -->

[Who uses this?]

## 4. Product principles

<!-- Required for new product, optional for MVP/exploratory. Cross-cutting rules that apply to ALL slices. Any slice that conflicts with a principle must update this list first. -->

1. [Principle]
2. [Principle]

## 5. Domain model

<!-- Required for new product, light for MVP, skip for one-off / exploratory if no new domain. -->

[Core entities and their shape]

## 6. User journey

<!-- Required for new product, optional for MVP, skip for exploratory. -->

[End-to-end narrative of the first full flow a user experiences]

## 7. Scenarios & user stories

<!-- Discrete stories grouped by capability. Each maps to the slice where it's first supported. -->

| ID  | As a user, I want…    | First supported by |
| --- | --------------------- | ------------------ |
| S1  | …                     | Slice NN           |

## 8. Product success criteria

<!-- When is the project "done"? -->

1. [Cross-cutting Done-when criterion]
2. [Another]

## 9. Out of scope

<!-- Cross-cutting deferrals. Things explicitly excluded from the entire project. -->

| Item   | Reason   |
| ------ | -------- |
| [Item] | [Reason] |

## 10. Glossary

<!-- Optional. Terms unique to this project. -->

| Term   | Meaning   |
| ------ | --------- |
| [Term] | [Meaning] |

---

# Part II — Implementation roadmap

## N+1. Why slices

[One paragraph on the no-horizontal-scaffolding principle. The slicing rules in §N+2 are the contract.]

## N+2. Slicing principles

1. **UI / user-observable behavior lives from slice 1.** Even a stub is better than another invisible backend.
2. **Every slice ends at a demoable behavior.** "Infrastructure is ready" is not a slice outcome.
3. **Features can land partially across slices.** Don't pre-build whole subsystems.
4. **Patterns / design systems are ported when demanded, not preemptively.**
5. **Slice size budget: 1–3 days.** If a slice estimates larger, split it.
6. **Scope-creep rejection is a slice-close ceremony.** "While we're here" goes to the next slice's backlog.
7. **PRD up front (per slice), techspec + tasks just-in-time.** Don't pre-plan how slice 13 works until you start it.

## N+3. Where we are today (carried-forward)

<!-- Existing code/infra this project starts from. Required for exploratory mode (the existing repo IS the foundation), required-but-light for new-product mode, skip for one-off. -->

| Carried-forward | First consumed by |
| --------------- | ----------------- |
| [Item]          | Slice NN          |

## N+4. Slice list

| #   | Slice    | Theme   | Size      | Depends on |
| --- | -------- | ------- | --------- | ---------- |
| 1   | [Name]   | [Theme] | 1–3 d     | —          |
| 2   | [Name]   | [Theme] | 1–3 d     | Slice 1    |
| ... | ...      | ...     | ...       | ...        |

[Linked PRDs are created lazily via `/create-prd` at slice pickup, not all upfront.]

## N+5. How to use this doc

Per-slice workflow:

1. **Pick the next slice.** Lowest-numbered incomplete slice in §N+4.
2. **Write the slice's PRD** via `/create-prd <slice>`. Lands at `specs/slices/slice-NN-<name>/PRD.md`.
3. **Create the techspec** via `/create-techspec <slice>`. Lands at `specs/slices/slice-NN-<name>/techspec.md`.
4. **Create the tasks** via `/create-tasks <slice>`. Lands at `specs/slices/slice-NN-<name>/tasks.md`.
5. **Implement the tasks.** Use `/gf-implement-task slice=<slice> task=<N>` per task.
6. **Close the slice.** Verify every Done-when checkbox in the slice PRD passes. "While we're here" additions go to the next slice's backlog.

## N+6. Confidence

**Confidence: [X]%** — [reason]

**Uncertainty:**

- [Specific concern]
