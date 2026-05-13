# Templates Inventory

Document templates copied/filled at the start of a workflow. One folder per workflow family. See the sibling `templates-*.md` files for file-by-file detail of each subfolder.

| Folder                   | Purpose                                                       | Used by                                                    |
| ------------------------ | ------------------------------------------------------------- | ---------------------------------------------------------- |
| `bugfix/`                | Bug report template (the input to investigation)              | `/full-bug-fix-workflow`, `/investigate-bug`               |
| `feature-addition/`      | Feature definition template + per-type variants (API, DB, UI) | `/integration-feature-dev`, `/integration-analyze-feature` |
| `greenfield-dev/`        | Product requirement template (mode-aware)                     | `/greenfield-dev`, `/create-prd`                           |
| `incident-response/`     | Incident report template                                      | `/start-incident`, `/full-incident-response`               |
| `refactoring-tech-debt/` | Refactor proposal template                                    | `/refactor-techdebt-dev`, `/audit-refactor-techdebt`       |

> Skill-level templates (the _outputs_ of phases — e.g., techspec / tasks / roadmap document shells) live inside the skill folder under `skills/<skill>/templates/`, not here.
