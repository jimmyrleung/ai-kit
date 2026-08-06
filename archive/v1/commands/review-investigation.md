---
description: Review a bug investigation for accuracy and completeness before remediation.
argument-hint: <bug_file> <investigation_file> <bug_id>
arguments: bug_file investigation_file bug_id
---

# Review Investigation Command

Use the `review-artifact` skill with:

- `artifact_path`: `$investigation_file` (the existing investigation document, e.g. `${bug_id}_investigation.md` — updated **in place**; do not create a separate `*_reviewed.md`)
- `artifact_label`: `investigation`
- `reviewer_agent`: `bug-investigation-reviewer-agent`
- `creator_agent`: `bug-investigation-agent`
- `support_docs`: `$bug_file` (the bug report)
- `next_step`: end of command — no further phase

When the skill hands back, give a clear recommendation on whether to:

- ✅ Proceed to Impact Analysis
- ⚠️ Proceed with noted concerns
- ❌ Require reinvestigation
