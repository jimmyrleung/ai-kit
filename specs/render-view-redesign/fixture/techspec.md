> Notes: synthetic sample for the render-view redesign checks. Nothing here describes a real system.

# Techspec — Invoice reminders

An overdue invoice gets one reminder email on day 7 and an overdue notice on day 14. A daily job at 09:00 UTC
reads the unpaid invoices, re-reads each status, and sends. This sample covers the requirements `R1`–`R3` and
the decisions `D1`–`D3`.

Mode: **Greenfield**

Design approach: **Daily batch job**

## Context

The billing service stores invoices with a status. Customers pay by card or bank transfer, so an invoice can
change status while the job runs. The job must never email a customer who has paid.

### Requirements

| ID | Requirement | Status |
|---|---|---|
| R1 | A customer with an unpaid invoice gets an email on day 7 and day 14. | Done |
| R2 | A paid or void invoice never gets a reminder. | In progress |
| R3 | A bounced email is logged as failed and retried once. | Not started |
| R4 | Reminders use the customer's locale, else English. | Blocked |
| R5 | A failed run alerts the owner. | Partial |
| R6 | Reminders stop after the overdue notice. | Rejected |

### Constraints

- The job runs once a day at **09:00 UTC**.
- It sends at most *one* email per invoice per day.
- A send takes about 300 ms; a run of 5,000 invoices takes under 30 minutes.

> A run that starts late still sends the same day's emails. It does not skip a day.

---

#### Open questions

1. Does a credit note count as payment?
2. Which timezone shows in the email?

## Design

### Data flow

The job reads a batch, then re-reads each invoice before it sends. The re-read is the key step (`D1`).

```text
Scheduler ──> ReminderJob ──> InvoiceStore
                  │
                  ├──> Mailer
                  └──> reminder_log
```

| Step | Count | Duration (ms) | Share |
|---|---:|---:|---:|
| Read batch | 5,000 | 420 | 12% |
| Re-read status | 5,000 | 1,260 | 36% |
| Send email | 4,100 | 1,230 | 35% |
| Write log | 4,100 | 590 | 17% |

### Key decisions

| ID | Decision | Status |
|---|---|---|
| D1 | Read the status again just before each send. | Keep |
| D2 | Retry a bounced email once, one hour later. | Open |
| D3 | Store the send result in `reminder_log`. | Deferred |

The retry in `D2` adds one job path. The log in `D3` is read by `R3` only.

```ts
export function shouldRemind(invoice: Invoice, today: Date): boolean {
  if (invoice.status === "Paid" || invoice.status === "Void") {
    return false;
  }
  const age = daysBetween(invoice.sentAt, today);
  return age === 7 || age === 14;
}
```

```ts
// before
send(email)
// after
await send(email)
if (bounced) retryOnce(email)
```

## Implementation map

### InvoiceStore — Modify

`InvoiceStore.dueForReminder()` returns the batch; a new `statusOf()` reads one row. The pattern follows the
existing store helper in `skills/render-view/scripts/render_view.py:86`.

### ReminderJob — Create

A new job class holds the loop. See `D1` and `R2`.

## Confidence

| Factor | Weight | Score | Evidence | Total |
|---|---:|---:|---|---:|
| Requirements are clear | 30% | 28 | Three requirements, all testable | |
| Similar patterns found | 25% | 22 | A nightly job exists | |
| Data flow understood | 20% | 18 | One writer per table | |
| Total | 100% | 91 | | 91% |
