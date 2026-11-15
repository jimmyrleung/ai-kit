# Task 1 — Store reads

## Description

Add `statusOf()` to the invoice store so the job can re-read one invoice (`D1`).

- Status: Done
- Depends on: —

## Acceptance Criteria

- `statusOf(id)` returns the current status of one invoice.
- The batch read still returns only unpaid invoices (`R2`).
