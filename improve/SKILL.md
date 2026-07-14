---
name: improve
description: Run improvement rounds on the current project/work — each round finds the single highest-value change, makes it, proves it's actually better by measuring, and keeps it only if it genuinely improves things (reverting regressions). Invoked as "improve" for one round, or "improve N" for N rounds (e.g. "improve 10" runs ten). Use whenever the user invokes /improve, or asks to "make this better", "do an improvement pass", "run a few improvement rounds", or "polish/optimize what we have". This is the same measured improvement loop [[ultragoal]] uses, on its own and count-controlled.
---

# Improve

Make the current work meaningfully better, one disciplined round at a time. The discipline is the point: an "improvement" only counts if you can *show* it helped. Changes that merely feel better — or that look great on a shallow check but don't hold up — are how a codebase drifts worse while everyone believes it's improving. Measure, keep what wins, revert what doesn't.

## How many rounds

Parse the count from the invocation:
- **`improve`** (no number) → **one** round.
- **`improve N`** → **N** rounds (e.g. `improve 10` → ten).

If there's no obvious thing to improve (no current project/task in play), ask the user what to improve before starting — "improve" needs a target.

**Pin a baseline before round 1.** Capture the key metric(s) that define "better" for this work *up front* — test count/pass rate, the benchmark or backtest number, lint-clean status, whatever applies — and note them. You'll compare every round against this fixed starting point and report the final delta, so "net improvement" is a concrete number (e.g. "net +14.2% on the 2y backtest, 512→534 tests") rather than a vibe. Without a pinned baseline, a long run's real value is unprovable.

## What one round is

1. **Pick the single highest-value improvement available right now** — the change most likely to make the result better. Rotate across *kinds* of improvement across rounds so you don't just polish one corner: correctness, performance, robustness/error-handling, readability/structure, test coverage, deeper analysis, and (where the project calls for it) empirical validation / backtests.
2. **Make the change** — one focused, self-contained change, not a sprawling rewrite.
3. **Prove it's actually better — measure, don't assume.** Run the relevant test, benchmark, or backtest and compare against the state *before* this round. This project's hard-won rule applies: gains that only look good on a shallow or short check often vanish under real validation, so verify the way the project actually validates (for this repo, that means validating at the real timeframe/panel, not a flattering proxy).
4. **Keep it only if it genuinely improves things; revert it if it's neutral or worse.** A change you make and then revert because it didn't help still counts as a completed round — you learned it doesn't work, which is real progress and stops it being tried again.
5. **Log the round** briefly (what you tried → what you measured → kept or reverted, and why) so the trail is visible and a later round doesn't repeat it.

## Running N rounds

Repeat the round above N times, each time re-picking the now-highest-value improvement given everything done so far. Between rounds, keep the work in a consistent, runnable state.

**Don't manufacture churn to hit the number.** If you genuinely run out of improvements worth making before reaching N, stop and say so — pointless edits that don't improve anything (or that risk degrading a good result) are worse than stopping early. Quality of the rounds beats quantity every time.

**Exception — this does NOT apply when you're inside `/work-until-limit`.** `/improve N` is bounded by a round *count*, so "out of worthwhile rounds → stop" is right here. `/work-until-limit` is bounded by a *quota ceiling*, and there the ceiling wins: running out of improvements to make is not a reason to stop the run, it's a reason to switch to a different kind of useful work (tests, bug hunt, security pass, docs, a real feature) and keep going. Do not use "no manufactured churn" as an excuse to stop a work-until-limit run early — that's a specific trap [[work-until-limit]] calls out.

If N is large and the run is long, this composes with the tools that manage long autonomous work: pair with **`/control`** for a STOP button, **`/work-until-limit`** to bound it by quota, and **`/shutdown-when-done`** to power off at the end. It is not mutually exclusive with any of them.

## Finish

Summarize across the rounds: what each round tried, what was measured, what was kept versus reverted, and the **net improvement from start to finish**. Be honest — if only 3 of 10 rounds produced a real gain, say that; it's more useful than a list of ten changes with no evidence any of them helped.
