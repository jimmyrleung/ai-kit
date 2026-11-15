# Decisions walkthrough — Invoice reminders

Decisions made while building tasks `T1` to `T3` that the techspec did not cover.

## Walkthrough — 2026-11-13 (round 0)

| # | Source | Decision as built | Disposition |
|---|---|---|---|
| D4 | T2-1 | The job logs every skipped invoice. | **Keep** (2026-11-13) |

## Walkthrough — 2026-11-14 (round 1)

| # | Source | Decision as built | Disposition |
|---|---|---|---|
| D4 | T2-1 | The job reads the batch at 09:00 and sends later, without re-reading the status. | |
| D5 | T2-2 | A voided invoice keeps its queued reminders until the next run. | |
| D6 | T2-3 | Reminders use the customer's locale, else English. | **Keep** (2026-11-14) |
| D7 | T2-4 | The email shows the due date in UTC. | |
| D8 | T2-5 | The job sends at most 50 emails per second. | **Keep** (2026-11-14) |
| D9 | T2-6 | A run that fails halfway restarts from the first invoice. | |
| D10 | T3-1 | A bounced email is retried once, after one hour. | **Change** (2026-11-14) |
| D11 | T3-2 | The retry uses the same subject line. | Defer to round 2 |
| D12 | T3-3 | The log keeps results for 90 days. | **Keep** (2026-11-14) |
| D13 | T3-4 | The overdue notice has no unsubscribe link. | Defer to round 2 |
| D14 | T1-1 | `statusOf()` reads from the primary database. | **Keep** (2026-11-14) |
| D15 | T1-2 | The batch read is limited to 5,000 invoices. | **Keep** (2026-11-14) |
| D16 | T1-3 | A credit note does not count as payment. | Defer to round 2 |
| D17 | T2-7 | The run time is written to the log. | |

### Premises

- **P1 — Invoice lifecycle.** Paid and Void are final; Void is allowed from Draft or Sent. ([techspec.md § Context](techspec.md#context))
- **P2 — Reminder timeline.** Daily run at 09:00 UTC; reminder on day 7, overdue notice on day 14.
  - **Confirmed** (owner, 2026-11-14)

### Dispositions

- **D6 — Keep (owner, 2026-11-14).** Why: the locale is already on the customer record.
- **D8 — Keep (owner, 2026-11-14).** Why: the mail provider allows 100 per second.
- **D10 — Change (owner, 2026-11-14).** Why: one hour is too short for a mailbox that is full.
- **D12 — Keep (owner, 2026-11-14).** Why: 90 days covers the dispute window.
- **D14 — Keep (owner, 2026-11-14).** Why: the replica can lag behind a payment.
- **D15 — Keep (owner, 2026-11-14).** Why: the batch fits in one run.
