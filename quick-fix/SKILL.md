---
name: quick-fix
description: Fix a known, well-understood bug fast — go straight to the patch, minimal talk. Use whenever the user invokes /quick-fix or says "just fix this quickly", "quick patch", or points at a specific obvious bug they want gone. The fast counterpart to [[fix]]: skip the reproduce-and-investigate ceremony because the cause is already clear. Part of the /quick family — do the work, keep the chatter to a minimum.
---

# Quick Fix

Patch a known bug fast. The user already knows what's wrong (or it's obvious) and wants it fixed, not investigated. So: minimal talk, make the fix, a fast sanity check, done.

## How to work

1. **Go straight to the fix.** The cause is understood — apply the correct change directly. No elaborate reproduction, no root-cause write-up unless something surprises you.
2. **Fast sanity check.** Confirm the change is right with a quick check — run the relevant test or the affected code path, or a targeted lint/compile. Quick, not a full ceremony, but never zero: don't hand back an unverified "fix."
3. **Report in a line or two.** What you changed, and that the quick check passed. That's it — no essay.

## Keep it quick, but not reckless

- **If the bug turns out not to be well-understood** — you can't see the cause fast, or the "obvious" fix doesn't hold up — stop quick-fixing and switch to [[fix]] (reproduce, root-cause, test). Quick-fix is for known bugs; don't paper over a mystery.
- **Don't skip the sanity check** to be faster — a wrong fix shipped silently is worse than a slow one.
- **Auto-escalate if it grows.** If the "quick" patch starts spanning more than a few edits or several files, or the change keeps rippling outward, that's no longer a quick fix — stop, say so, and switch to [[fix]] (reproduce → root-cause → test). Don't let a quick patch quietly balloon into an unverified sprawling change.
- Still confirm before anything destructive or irreversible; "quick" trims talk and investigation, not safety.
