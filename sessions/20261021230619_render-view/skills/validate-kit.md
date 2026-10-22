---
name: validate-kit
description: "Runs ai-kit's portability checks locally before a commit: live skill names and frontmatter, INVENTORY/README counts, local Markdown links, Python syntax, and a sync dry run. Use when adding, renaming or editing a skill, or before committing changes to README.md, INVENTORY.md or skills/."
---

# validate-kit (draft)

Goal: get the same verdict as the GitHub Actions portability job without pushing.

## Steps

1. Find a Python 3.12+ interpreter (`python3`, `py -3`, or `uv run --no-project python`).
2. Extract and run the workflow's validation block, so the check never drifts from CI:

   ```bash
   awk '/name: Validate live skill format and links/{f=1;next} f&&/run: \|/{r=1;next} r&&/- name: Check Python syntax/{exit} r{sub(/^          /,""); print}' \
     .github/workflows/portability.yml > "$TMP/ci_validate.py"
   python "$TMP/ci_validate.py"
   ```

3. Run the workflow's `py_compile` line with `-B` (no `__pycache__` in skill folders).
4. Run `sync-skills.py --dry-run`; report new `create` entries for added skills.
5. Report pass/fail per check. Do not commit or sync for real.

## Notes

- Write the extracted script to a scratch folder, not the repo.
- The skill count must match in three places: the live directories, `INVENTORY.md` ("contains N skills" plus one row each), and `README.md` ("N live skills").
