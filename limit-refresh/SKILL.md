---
name: limit-refresh
description: A modifier for the [[work-until-limit]] skill — it does NOT work on its own. When added to a work-until-limit run, it lets the run bridge an imminent usage-limit reset ONCE instead of stopping: if the binding daily/session or weekly limit is about to refresh (e.g. usage is at 87% against a 90% ceiling but the limit resets in a minute), it waits for that reset and keeps working afterwards, always leaving a couple of percent of headroom. It is single-use — after one bridge it turns off, because the following reset is hours/days away. Use whenever the user includes "limit-refresh" alongside a work-until-limit invocation, or asks to "keep going across the limit reset / when the limit refreshes". On its own it has nothing to do — tell the user to pair it with work-until-limit.
---

# Limit Refresh (modifier for work-until-limit)

This is not a standalone action — it's an option that changes how [[work-until-limit]] behaves. **Alone it does nothing.** If the user invokes `/limit-refresh` by itself, don't try to run anything: explain that it's a modifier for `work-until-limit` and show them how to use it, e.g. `work-until-limit 90 limit-refresh` or `work-until-limit 90 weekly 90 limit-refresh`. Then, if they want that, proceed via the work-until-limit skill with the flag enabled.

## What it does when paired

Normally work-until-limit stops as it approaches the ceiling. But a usage limit that's about to reset isn't a real wall — once it resets, usage drops back near zero and there's plenty of budget again. `limit-refresh` uses that:

- When a bounded limit (session/daily **or** weekly) would trigger the stop, it checks how long until that limit resets (the monitor reports `SESSION_RESET_MIN` / `WEEK_RESET_MIN`).
- If the reset is **imminent** (within a short refresh window, ~10 minutes), it **doesn't stop** — it pauses, waits out the reset, confirms usage dropped, then resumes working.
- If the reset is **far off** (e.g. the weekly limit days away), the reset can't help, so it **stops as normal**.

It works for both the daily/session limit and the weekly limit — whichever one is binding and about to refresh.

## One-time use (important)

Bridging fires **at most once per run.** After the single bridge, `limit-refresh` is spent and turns off for the rest of the session. The reason is timing: limits reset on long cycles — the session/daily limit only every few hours, the weekly limit once a week — so the *next* reset after the one you just rode through is ~4 hours (or days) away. Waiting for that would stall the run for hours, which is never worth it. So: bridge once, then the next time a ceiling is hit, stop normally.

## The guardrails (these matter)

- **Always keep a couple of percent of headroom.** Decide based on the predictive reading with its safety margin; never run the meter right to the exact ceiling gambling on the reset — a small buffer absorbs an inaccurate reset estimate or one last in-flight chunk.
- **Bridge only the limit that's actually resetting.** If the session is about to reset but the weekly limit is the real wall and isn't resetting soon, stop — working past the session reset still spends weekly quota.
- **Pause while waiting.** Don't keep firing off heavy chunks in the final minute before a reset; wait it out so you don't push further over.
- **Sanity-check the countdown before committing to a wait.** The reset time is parsed from `/usage` text and could be misread. Before you sit idle waiting for a reset, take one extra fresh reading to confirm the countdown is small and consistent (roughly matches the previous read minus elapsed time). If the two readings disagree wildly, don't trust it — treat the reset as unknown and stop normally rather than waiting on a bad estimate.

All of the concrete logic (windows, the wait, re-reading to confirm the drop) lives in the [[work-until-limit]] skill under "If `limit-refresh` is enabled". This skill just carries the intent and the rule that it's pair-only.
