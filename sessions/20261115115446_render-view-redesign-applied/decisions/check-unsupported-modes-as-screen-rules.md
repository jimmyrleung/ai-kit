# Check unsupported browser modes as screen rules, and report them as not tested

- Date: 2026-11-15
- Status: accepted by the owner (the T9 results and the modes table in `COMPONENTS.md`)
- Scope: render-view page checks (print, reduced motion, forced colours, more contrast)

## Context

Task 9 asked for each mode to be tested or reported as "not tested". The browser tool cannot set print media,
`prefers-reduced-motion`, `forced-colors` or `prefers-contrast`.

## Decision

Apply the mode's `@media` rules as plain screen rules in a scratch `<style>` and read the computed values.
Fire `beforeprint` for the handler that opens closed `details`. Write "Not tested in the real mode" in the
modes table, with what was checked.

## Why

- Reading the CSS alone does not show that the selectors win the cascade (an earlier review found that
  `:root[data-theme="dark"]` beat `@media print { :root }`).
- The screen-rule check finds cascade and handler problems; it does not prove the real mode.

## Consequences

- A real print preview and a Windows contrast theme are still open for the owner.
- A print bug was found this way: closed `details` do not print open, so `view.js` now opens them on `beforeprint`.
