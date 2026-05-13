---
description: Investigate a bug and produce an evidence-based investigation document.
argument-hint: <bug_file> <bug_id>
arguments: bug_file bug_id
---

# Investigate Bug Command

This command is a thin shim: the `bug-investigation` skill owns the methodology and output contract.

1. Create a todo list with the steps for this command.
2. Use the `bug-investigation` skill with:
   - `$bug_file` as the bug report,
   - output file `${bug_id}_investigation.md` (alongside the bug report).

   The skill handles the clarification questions, codebase exploration and execution-path tracing, consolidation (consensus on root cause / disagreement / confidence-weighted findings — launching 1–3 `bug-investigation-agent` sub-agents for breadth where useful), the ≥ 90% confidence gate, and writing the file.

When the skill hands back, this command is complete — the investigation is ready for `/review-investigation`.
