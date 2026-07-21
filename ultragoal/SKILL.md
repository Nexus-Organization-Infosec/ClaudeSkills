---
name: ultragoal
description: The intensified version of a goal — don't just reach the requirement, then push far past it. First work relentlessly until the stated requirement is genuinely met and verified, then run up to 10 rounds of improvement (code changes, refactors, deeper analysis, backtests, optimizations — whatever makes it measurably better), keeping only changes that actually improve things. Use whenever the user invokes /ultragoal or says "take it to the next level", "reach X then make it as good as possible", "don't just hit the goal, perfect it", or wants maximum-effort iteration beyond the minimum. Designed to be compatible with and hand off to the [[shutdown-when-done]] skill when both are requested.
---

# Ultragoal

Two phases, in order: **reach the requirement, then relentlessly improve past it.** This is "goal" turned up — the requirement is the floor, not the finish line.

## Compatibility — this WORKS WITH `/shutdown-when-done`

Unlike the mutually-exclusive skill pairs, `/ultragoal` is *designed* to combine with `/shutdown-when-done`. If the user invoked both (e.g. "ultragoal X, then shut down"), treat ultragoal as the work and the shutdown as the finale: complete all of ultragoal (Phase 1 + the improvement rounds, or an early stop), write the final summary, and only then run the shutdown-when-done sequence as the very last action. Never shut down before the rounds are done unless the user set an explicit early-stop condition.

## Phase 1: Reach the requirement — don't stop short

1. **Pin down the requirement precisely — to a file, not just your memory.** What, concretely, does "done" mean here? What's the measurable bar — tests passing, a metric hit, a feature working end-to-end? Write it to `.claude/ultragoal-goal.md` at the very start. This run can be long (many rounds, possibly a context compaction in between), and a requirement held only in your head drifts — you end up declaring a *different, easier* bar "met." Re-read the pinned goal before you claim it's reached, and judge against exactly that, not a fuzzy recollection of it.
2. **Work until it's genuinely met**, not until it looks plausible. Push through obstacles rather than declaring victory early. Verify the requirement is actually satisfied — run it, test it, measure it. "I think it works" is not met; "I ran it and confirmed X" is.
3. **If the requirement is truly blocked or unreachable** (missing access, contradictory constraints, a real dead end), stop and say so honestly rather than looping forever or faking success. Persistence is the goal; delusion is not.

Do not begin improvement rounds until the requirement is verified met.

**A large requirement is worked in continuous installments, never one-batch-then-handback.** If Phase 1 is a big multi-item program (e.g. "implement these 80 things"), break it into tested batches — good — but then execute batch after batch **without stopping between them**. "This is far more than one turn can complete well, so I did batch A and it's structured so `/continue` resumes here" is an early hand-back wearing a planning costume, and it does not count as reaching the requirement. The requirement is met only when **all** of it is built and verified. Waiting on a test suite mid-run is fine; the moment it's green, start the next batch — don't end your turn to wait for `/continue`. Turn length is the harness's concern, not a stop condition. (If `/dont-stop-till-complete` is also active, this is doubly binding — see that skill.)

## Phase 2: Up to 10 improvement rounds

Now make it better — as much as 10 focused rounds of improvement. This is where ultragoal earns its name. Each round:

1. **Pick the single highest-value improvement available** right now — the change most likely to make the result better. Rotate across kinds of improvement so you don't just polish one corner: correctness, performance, robustness, readability, deeper analysis, additional tests, and (where the project calls for it) backtests / empirical validation.
2. **Make the change.**
3. **Prove it's actually better — measure, don't assume.** Run the relevant test/benchmark/backtest and compare against the state before the round. This project's own hard-won rule applies: gains that only look good on a shallow check often vanish under real validation, so verify the way the project really validates.
4. **Keep it only if it genuinely improves things; revert it if it doesn't** (neutral or worse). A round that makes things worse and gets reverted still counts as a round — you learned the change doesn't help.
5. **Log the round** (see below) before starting the next.

After 10 rounds — or earlier if you run out of improvements genuinely worth making (don't invent churn just to hit 10, and don't degrade a good result with pointless changes) — stop and move to the finish.

## Track progress every round — survive interruption

After **each** round, update `.claude/ultragoal-progress.md` in the project so nothing is lost if the session is cut off (e.g. the usage limit is hit mid-run — see the note below). Keep it simple:

```markdown
# Ultragoal progress
Requirement: <the bar> — MET on <when/how verified>

## Rounds
1. [x] <what changed> → <measured result> → KEPT / REVERTED (why)
2. [x] ...
3. [ ] <next planned>
```

This doubles as the record you'll summarize at the end, and lets a later `/continue` pick up mid-improvement if needed.

## About the usage limit — what's real and what isn't

The user may want improvement rounds to stop before burning too much of their usage limit. Be honest about the mechanics:

- **You cannot read a live usage-limit percentage.** The rolling account limits are enforced server-side; there is no tool or local file that reliably tells you "you're at 90%." A real limit hit shows up as the session simply being cut off, not as a number you can check.
- **So the round cap IS the budget control.** Ten rounds is a bounded, predictable amount of work — that's the guardrail. If the user wants a tighter budget, honor a smaller number they give ("just 3 rounds") or an explicit stop condition.
- **Because a cutoff can strike between rounds**, the per-round progress file above is what makes this safe: if the session dies mid-run, `.claude/ultragoal-progress.md` preserves everything done so far, and the user can resume with `/continue`.
- If the harness ever does surface a genuine remaining-usage signal to you, then act on it: when it's low, stop early, report what improved and that the limit is the reason — and if `/shutdown-when-done` is armed, run its shutdown sequence instead of just stopping. But don't pretend to observe a number you can't.

## Finish

Summarize clearly:
- **Requirement:** met (how it was verified).
- **Rounds:** what each round tried, what was measured, what was kept vs reverted, and the net improvement from floor to final.
- **Stopped because:** 10 rounds done / ran out of worthwhile improvements / early-stop condition / interruption.

Then: if `/shutdown-when-done` was requested alongside this, run its finale now (notification + scheduled shutdown) as the very last action. Otherwise, hand the finished, improved result back to the user.
