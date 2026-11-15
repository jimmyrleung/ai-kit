# Skill draft — check page behaviour a browser tool cannot switch

Draft from the 2026-11-15 session. For the owner to review; not a live skill. Extends `check-view-page`.

**Use when:** a page has print, reduced-motion, forced-colours or more-contrast rules and the browser tool
cannot set those modes.

## Steps

1. Read the rules of one mode from `document.styleSheets` (`CSSMediaRule` with the matching `conditionText`)
   and inject their `cssText` in a `<style id="emu">` as plain rules. Remove it after the check.
2. Read computed styles for each acceptance point (display of hidden chrome, transition duration `0s`,
   border widths, custom-property values, `color-scheme`).
3. For print, dispatch `beforeprint` and `afterprint` on `window` to test handlers that open `details`.
4. Report the mode as "Not tested in the real mode", with what was checked as a screen rule. Never "Yes".

## Gotchas

- Background tabs throttle timers and media-query change events. Take a screenshot to force a render.
- Compare the Respond text of two builds by SHA-256 of the text (with the build time removed), not by eye.
- Do not call `navigator.clipboard.readText()`; it hangs the page tool. Stub `writeText` to test copy logic.
