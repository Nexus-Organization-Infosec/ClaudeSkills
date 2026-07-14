---
name: quick-cleanup
description: Quick, safe tidy of the code — remove dead code, unused imports, stray debug prints, and minor mess, fast and with minimal talk. Does NOT move files or restructure folders (that's the risky part). Use whenever the user invokes /quick-cleanup or says "quick tidy", "clean this up a bit", or "remove the obvious junk". The lightweight counterpart to [[cleanup]] — for the full revamp (folder restructure, moving files, production pass), use that instead. Part of the /quick family — do the work, keep the chatter to a minimum.
---

# Quick Cleanup

Tidy the obvious, safe stuff quickly — no big revamp, no file moves, minimal talk. This is the light version of [[cleanup]]: it deliberately skips the dangerous parts (reorganizing folders, moving files and rewiring imports) and just clears the easy mess in place.

## What to do (safe, in-place only)

- Remove **unused imports**, **dead/unreachable code**, **commented-out blocks**, and **stray debug prints**.
- Small readability tidies: clearer local names, obvious duplication collapsed, tighten a messy line.
- **Prove "unused" before deleting** — a quick grep for references (code can be reached dynamically); if unsure, leave it. This check stays even in quick mode.

## What NOT to do here

- **Don't move or rename files, or restructure folders** — that breaks imports and is exactly what the full [[cleanup]] handles with verification. If the code really needs reorganizing, say so and point to `/cleanup`.
- Don't reformat the whole file or churn broadly; keep changes small and obviously safe.

## Keep the scope small

Default to a **bounded** target — the files in the current change, the file(s) the user named, or the module you're already in — not a whole-project sweep. "Quick" means a small, contained tidy; if you find yourself wanting to scan and clean the entire codebase, that's `/cleanup`, not this. Staying scoped is what keeps it quick and low-risk.

## Finish

Quick sanity check — a fast compile/lint or the relevant test to confirm nothing broke — then report in a line or two what you removed/tidied. No essay.
