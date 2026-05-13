---
description: Review an incident diagnosis for accuracy and completeness before remediation.
argument-hint: Incident directory (must contain incident_report.md and diagnosis.md).
---

# Review Diagnosis Command

Independent review of an incident diagnosis — a quality gate before hotfix planning. Not a rubber stamp.

## Prerequisites

- You are in an incident directory.
- `incident_report.md` exists.
- `diagnosis.md` exists (created by `/diagnose`).
- You have read the diagnosis yourself first.

## Process

Use the `review-artifact` skill with:

- `artifact_path`: `diagnosis.md` (updated **in place** — no separate `diagnosis_reviewed.md`)
- `artifact_label`: `diagnosis`
- `reviewer_agent`: `diagnosis-reviewer-agent`
- `creator_agent`: `diagnosis-agent`
- `support_docs`: `incident_report.md`
- `mode`: `full` (for a live P1 where speed beats thoroughness, pass `abbreviated` instead)
- `next_step`: end of command — no further phase

The reviewer should validate evidence independently, check the 5-Whys reaches a true root cause (not a symptom), confirm alternatives were considered, and look for ignored contradictory evidence or timeline gaps.

## When the skill hands back — recommendation

- ✅ **Approved** — evidence supports all claims, root cause is specific → proceed to hotfix planning (`/plan-hotfix`).
- ⚠️ **Approved with notes** — minor non-blocking issues noted → address them, then proceed to hotfix planning.
- 🔄 **Needs revision** — significant gaps in evidence or logic → fix `diagnosis.md` (gather more data if needed) and re-run this command.
- ❌ **Rejected** — fundamental errors / insufficient evidence → return to `/diagnose` with the reviewer's guidance.
