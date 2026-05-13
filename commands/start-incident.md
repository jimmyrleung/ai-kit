---
description: Initialize a new incident directory and create the incident report from the template.
argument-hint: Short incident descriptor (e.g. orders_api_outage, database_deadlock — underscores, no date).
---

# Start Incident

Initialize a new incident directory and create the incident report from the template.

## Usage

```
/start-incident <incident-descriptor>
```

- `incident-descriptor`: short description for the incident, underscores not spaces (e.g. `orders_api_outage`, `database_deadlock`). Don't include the date — it's added automatically.

## What this command does

1. Generates today's date in `YYYY-MM-DD` format.
2. Creates the incident directory: `incidents/inc_<date>_<descriptor>/`.
3. Copies the template `agent-workflows/incident-response/templates/incident-report.md` into the directory as `incident_report.md`.
4. Creates a `logs/` subdirectory for log files.
5. Displays the path to the new incident report and guidance on next steps.

## Example

```
/start-incident orders_api_outage
```

creates:

```
incidents/inc_2026-05-12_orders_api_outage/
├── incident_report.md
└── logs/
```

## Next steps

1. Fill out `incident_report.md` with all available information.
2. Copy relevant log/trace files into the `logs/` directory if available.
3. Run `/diagnose` to start the diagnosis phase. (Or, for the full severity-routed workflow, `/full-incident-response <severity> incidents/inc_<date>_<descriptor>/incident_report.md`.)

## Notes

- The descriptor should use underscores, not spaces; keep it short but meaningful.
- The date is added automatically — don't include it in the descriptor.
