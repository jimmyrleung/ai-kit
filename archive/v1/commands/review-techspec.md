---
description: Review a slice's techspec to catch issues before tasks/implementation.
argument-hint: Slice number or slice folder name.
---

# Review Techspec Command

Review a slice's techspec for accuracy, scope adherence (no over-spec, no premature commitments), and alignment with host-repo conventions / earlier-slice precedents.

## When to skip

Skip this command entirely if ALL are true:

- slice is small (≤ 1 day)
- all techspec agents agreed on the approach
- confidence ≥ 95% on the techspec
- no flagged risks

(The `review-artifact` skill applies the same skip-check internally.)

## Process

Use the `review-artifact` skill with:

- `artifact_path`: the slice's techspec file (updated **in place**)
- `artifact_label`: `techspec`
- `reviewer_agent`: the `techspec-creation` skill in **review mode** — review the existing techspec, don't author a new one
- `creator_agent`: the `techspec-creation` skill (regenerate the techspec only if > 30% needs change)
- `support_docs`: the slice PRD; the master roadmap (Part I + this slice's entry, for context)
- `next_step`: end of command — no further phase

### Greenfield-specific review focus

When categorizing issues, look for:

- **Out-of-scope content** — sections present that this slice doesn't demand (Performance, Security, Monitoring without justification)
- **Missing decisions** — a key decision deferred without reason
- **Wrong patterns** — techspec contradicts host-repo conventions or earlier-slice precedents
- **Over-spec** — committing to file structure / components that won't be consumed for several slices
- **Under-spec** — slice demands something the techspec doesn't address

Output a numbered list of issues, each with category + severity + suggested fix. Default to in-place edits; only escalate to a rewrite if review found > 30% of the techspec needs change. Confidence in the techspec post-review must be ≥ 90%.
