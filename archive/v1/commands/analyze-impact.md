---
description: Analyze the impact of a proposed bug fix.
argument-hint: <bug_file> <reviewed_investigation_file> <bug_id>
arguments: bug_file reviewed_investigation_file bug_id
---

# Analyze Impact Command

This command is a thin shim: the `impact-analysis` skill owns the methodology and output contract.

1. Create a todo list with the steps for this command.
2. Use the `impact-analysis` skill with:
   - `$bug_file` as the bug report,
   - `$reviewed_investigation_file` as the reviewed investigation,
   - output file `${bug_id}_impact_analysis.md` (alongside the bug report).

   The skill handles dependency mapping (direct + indirect), test-coverage assessment, risk-level scoring (Low / Medium / High / Critical), the rollback strategy, the SAFE-TO-IMPLEMENT / WITH-CAUTION / REQUIRES-ADDITIONAL-REVIEW recommendation, the user-approval gate, and writing the file — launching 1–3 `impact-analysis-agent` sub-agents for breadth where useful.

When the skill hands back, this command is complete.
