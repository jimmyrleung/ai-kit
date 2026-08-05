# Incident Report: [Brief Title]

**Incident ID:** inc*[YYYY-MM-DD]*[short-descriptor]  
**Reported By:** [Your Name]  
**Date/Time Detected:** [YYYY-MM-DD HH:MM UTC]  
**Severity:** [P0 - Critical | P1 - High | P2 - Medium | P3 - Low]  
**Status:** [Investigating | Diagnosed | Remediating | Resolved]

---

## Incident Summary

<!-- Provide a 2-3 sentence overview of what happened -->

**Affected Systems:**

- [ ] Orders API
- [ ] Payment Service
- [ ] User Authentication
- [ ] Database
- [ ] Other: ******\_\_\_******

**Customer Impact:**

- **Scope:** [% of users affected / specific regions / all users]
- **Duration:** [How long has this been happening?]
- **Symptoms:** [What are users experiencing?]

---

## Timeline

| Time (UTC) | Event                     |
| ---------- | ------------------------- |
| HH:MM      | [First alert/user report] |
| HH:MM      | [Investigation started]   |
| HH:MM      | [Key discovery/action]    |

---

## Technical Details

### Symptoms Observed

<!-- What errors, alerts, or anomalies were detected? -->

### Error Messages

```
[Paste relevant error messages here]
```

### Related Alerts/Monitoring

- **Alert Name:** [e.g., "High API Error Rate"]
- **Dashboard Link:** [URL to monitoring dashboard]
- **Metrics Affected:** [e.g., "Error rate 15% → 45%"]

### Log Files

<!-- Reference log files that should be analyzed -->

**Location:** `logs/[path/to/logs]`
**Time Range:** [Start] to [End]
**Key Files:**

- `application.log`
- `error.log`
- `database-slow-queries.log`

### Trace Files

<!-- Reference distributed trace files if available -->

**Location:** `traces/[path/to/traces]`
**Trace IDs:** [Comma-separated list of relevant trace IDs]

---

## Initial Hypothesis

<!-- Optional: Your initial thoughts on what might be causing this -->

---

## Context & Recent Changes

### Deployments

- **Last Deployment:** [Date/Time - Service Name - Version]
- **Related PRs:** [Links to recent PRs if relevant]

### Infrastructure Changes

- [ ] No recent infrastructure changes
- [ ] [Describe any recent changes to servers, databases, networking, etc.]

### Traffic Patterns

- [ ] Normal traffic patterns
- [ ] Traffic spike detected
- [ ] Unusual request patterns

### Dependencies

- [ ] All external dependencies healthy
- [ ] [List any degraded third-party services]

---

## Communication

**Internal Stakeholders Notified:**

- [ ] Engineering Team
- [ ] DevOps/SRE
- [ ] Product Management
- [ ] Customer Support

**External Communication:**

- [ ] Status page updated
- [ ] Customer emails sent
- [ ] N/A - No customer communication needed

**Slack Channel:** #incident-[incident-id]

---

## Notes

<!-- Any additional context, observations, or information -->
