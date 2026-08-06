---
description: Check the current status of an incident (which artifacts exist, which phase you're in) and get guidance on the next step.
argument-hint: (run from inside the incident directory).
---

# Incident Status

Check the current status of an incident and get guidance on what to do next.

## Usage

```
/incident-status
```

## What This Command Does

1. Checks which incident files exist in the current directory
2. Determines the current phase of the incident response
3. Provides guidance on the next steps
4. Validates file completeness

## Steps

When you run this command, I will:

1. **Check current location**: Verify we're in an incident directory
2. **Scan for files** (and inspect `diagnosis.md` for a `## Review` section — that's the signal the diagnosis-review phase ran, since `/review-diagnosis` updates `diagnosis.md` in place rather than producing a separate file):
   - `incident_report.md`
   - `diagnosis.md` — and whether it has a `## Review` section (post-review confidence + recommendation)
   - `remediation_plan.md`
   - `postmortem.md`
3. **Analyze workflow state**: Determine current phase
4. **Provide guidance**: Suggest next command to run

## Output Format

```
📊 INCIDENT STATUS
==================

Incident: inc_2025-10-13_orders_api_outage
Location: /path/to/incidents/inc_2025-10-13_orders_api_outage

Files Present:
✅ incident_report.md (completed)
✅ diagnosis.md (completed, reviewed — APPROVED)
❌ remediation_plan.md (not started)
❌ postmortem.md (not started)

Current Phase: Diagnosis Complete ✅
Next Step: Run /plan-hotfix

Progress: ████████░░░░ 60%

Workflow Status:
✅ Phase 1: Incident Report (complete)
✅ Phase 2: Diagnosis (complete)
✅ Phase 3: Diagnosis Review (APPROVED)
⏳ Phase 4: Hotfix Planning (next)
⬜ Phase 5: Post-Mortem (pending)
```

## Workflow Phases

### Phase 1: Incident Report

**File**: `incident_report.md`

- ✅ Complete: Move to diagnosis
- ❌ Missing: Run `/start-incident`

### Phase 2: Diagnosis

**File**: `diagnosis.md`

- ✅ Complete: Move to review
- ❌ Missing: Run `/diagnose`

### Phase 3: Diagnosis Review

**Signal**: a `## Review` section in `diagnosis.md` (post-review confidence + recommendation). `/review-diagnosis` updates `diagnosis.md` in place — there is no separate `diagnosis_reviewed.md`.

- ✅ APPROVED: Move to hotfix planning
- ⚠️ APPROVED WITH NOTES: Address notes, then move to hotfix planning
- 🔄 NEEDS REVISION: Fix issues and re-run `/review-diagnosis`
- ❌ REJECTED: Return to `/diagnose`
- ❌ No `## Review` section in `diagnosis.md`: Run `/review-diagnosis`

### Phase 4: Hotfix Planning

**File**: `remediation_plan.md`

- ✅ Complete: Execute the remediation
- ❌ Missing: Run `/plan-hotfix`

### Phase 5: Post-Mortem

**File**: `postmortem.md`

- ✅ Complete: Distribute and track action items
- ❌ Missing: Run `/create-post-mortem` (after incident is resolved)

## Validation Checks

In addition to checking for files, I will:

### Check File Completeness

- Is `incident_report.md` filled out?
- Does `diagnosis.md` have a root cause?
- Does `diagnosis.md`'s `## Review` section have a recommendation (APPROVED / APPROVED WITH NOTES / NEEDS REVISION / REJECTED)?
- Does remediation plan have steps?
- Does post-mortem have action items?

### Flag Issues

```
⚠️ WARNINGS:
- incident_report.md appears incomplete (missing affected systems)
- No log files found in logs/ directory
- diagnosis.md is missing confidence level
```

## Use Cases

### 1. New to an Incident

Run `/incident-status` to understand:

- What's been done so far
- Where the team left off
- What needs to happen next

### 2. After a Break

Run `/incident-status` to refresh:

- Current workflow phase
- Last completed step
- Next action to take

### 3. Before Sharing

Run `/incident-status` to verify:

- All phases complete
- No missing files
- Ready for distribution

### 4. Multi-Person Response

Run `/incident-status` when:

- Taking over from another team member
- Coordinating parallel work
- Checking team progress

## Example Scenarios

### Scenario 1: Just Started

```
/incident-status

Files Present:
✅ incident_report.md (completed)
❌ diagnosis.md (not started)

Next Step: Run /diagnose
```

### Scenario 2: Diagnosis Needs Revision

```
/incident-status

Files Present:
✅ incident_report.md
✅ diagnosis.md (reviewed — NEEDS REVISION)

⚠️ Review Status: NEEDS REVISION
Issues to Address:
- Insufficient evidence for root cause claim
- Alternative hypotheses not considered

Next Step: Address the issues in diagnosis.md and run /review-diagnosis again
```

### Scenario 3: Ready for Post-Mortem

```
/incident-status

Files Present:
✅ incident_report.md
✅ diagnosis.md (reviewed — APPROVED)
✅ remediation_plan.md (executed ✓)
❌ postmortem.md

Next Step: Run /create-post-mortem
Note: Recommended to wait 24-48 hours after resolution
```

### Scenario 4: All Complete

```
/incident-status

Files Present:
✅ incident_report.md
✅ diagnosis.md (reviewed — APPROVED)
✅ remediation_plan.md (executed ✓)
✅ postmortem.md (complete)

✨ All phases complete!

Next Steps:
- Create tickets for action items
- Distribute post-mortem to team
- Archive incident documentation
```

## Progress Bar Guide

```
Progress: ░░░░░░░░░░░░ 0%   - Not started
Progress: ████░░░░░░░░ 20%  - Incident report complete
Progress: ████████░░░░ 40%  - Diagnosis complete
Progress: ████████░░░░ 60%  - Diagnosis reviewed
Progress: ██████████░░ 80%  - Remediation planned
Progress: ████████████ 100% - Post-mortem complete
```

## Quick Commands Reference

Based on status, you'll see suggestions like:

```
Available Commands:
/start-incident <descriptor>  - Start a new incident
/diagnose                    - Run diagnosis analysis
/review-diagnosis            - Validate diagnosis
/plan-hotfix                 - Create remediation plan
/create-post-mortem           - Generate post-mortem
/incident-status                      - Check current status (this command)
```

## Notes

- Run `/incident-status` anytime to check progress
- Status is determined by files present, not file content
- Warnings are suggestions, not blockers
- Use this to coordinate with team members
