---
name: quick-improve
description: Make a few quick, tiny, low-risk improvements — small readability, clarity, or obvious-win cleanups — fast and with minimal talk. Use whenever the user invokes /quick-improve or asks to "tidy this up a bit", "small improvements", or "make a couple quick tweaks". The lightweight counterpart to [[improve]]: no measured rounds, no benchmarks — just small safe wins. Part of the /quick family — do the work, keep the chatter to a minimum.
---

# Quick Improve

Make small, safe, obvious improvements quickly. This is the light version of [[improve]] — no measured rounds, no benchmarking, no big refactors. Just tidy the easy wins and move on, with minimal talk.

## What counts as a quick improvement

Small and low-risk, the kind of thing that's clearly better and can't plausibly break behavior:
- Clearer names, a confusing line simplified, dead code or a stray debug print removed.
- A missing small guard, a tidier structure, a helpful short comment where intent was murky.
- Obvious micro-cleanups you'd fix in passing.

## How to work

1. **Make the small wins directly — cap it at about five.** Pick a handful (≤~5) of tiny, self-contained improvements and list them in a line first, so the change stays bounded and reviewable rather than sprawling. Preserve behavior; these should be safe by nature. If there's clearly much more worth doing, that's a sign to use [[improve]] (measured rounds), not to keep piling on here.
2. **Quick sanity check** — a fast compile/lint or the relevant test to confirm nothing broke. Quick, but not skipped.
3. **Report in a line or two** — what you tidied. No essay.

## Stay in scope

- **If an "improvement" turns out to be non-trivial** — it needs measuring, a real refactor, or could change behavior — don't force it here. Flag it, and use [[improve]] (measured rounds) or the appropriate skill instead. Quick-improve is only for genuinely small, safe wins.
- Don't reformat or churn broadly just to look busy; keep changes minimal and obviously beneficial.
