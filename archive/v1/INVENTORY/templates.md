# Templates Inventory

Document templates copied/filled at the start of a workflow. One folder per workflow family. See the sibling `templates-*.md` files for file-by-file detail of each subfolder.

| Folder                   | Purpose                                                       | Used by                                                    |
| ------------------------ | ------------------------------------------------------------- | ---------------------------------------------------------- |
| `bugfix/`                | Bug report template (the input to investigation)              | `/bug-investigation`                                       |
| `feature-addition/`      | Feature definition template + per-type variants (API, DB, UI) | `/analyze` (integration mode)                              |
| `greenfield-dev/`        | Product requirement template (mode-aware)                     | `/analyze` (greenfield mode)                               |
| `incident-response/`     | Incident report template                                      | archived incident-response commands                        |
| `refactoring-tech-debt/` | Refactor proposal template                                    | `/analyze` (refactor mode)                                 |

> Skill-level templates (the _outputs_ of phases — e.g., techspec / tasks / roadmap document shells) live inside the skill folder under `skills/<skill>/templates/`, not here.
