---
name: loop
description: Turn a skill OR a plain-language activity into a continuous loop that repeats until YOU quit — no round count, no ceiling, it just keeps going. Pair it with a skill ("/loop /improve", "/improve /improvement-ideas /loop") or just name an activity ("/loop skill creation", "/loop strategy creation", "/loop write tests") and it produces one new complete unit of that each iteration, over and over. Automatically launches the [[control]] STOP button at the start so you can end it gracefully anytime. Use whenever the user invokes /loop alongside a skill or an activity, or says "keep creating X until I stop", "loop this on repeat", or "run this continuously until I quit". The only thing that ends it is the user (STOP button, or a new message) or a genuine blocker.
---

# Loop

Take whatever skill(s) the user paired with `/loop` and run them **repeatedly, indefinitely, until the user quits.** It's an unbounded repeat wrapper: no round number, no usage ceiling — the loop's only exit is the user stopping it. Think of it as [[work-until-limit]] bounded by *"until you say stop"* instead of by a quota.

## Step 1: Always launch the STOP button first

Because this runs forever until the user intervenes, the user **must** have a graceful off-switch. So on the first thing you do, launch [[control]] — the red STOP button — exactly as that skill describes (start `control_panel.py` as a background task, tell the user it's up). This is not optional; a loop with no STOP button is a trap. If the button is already up this session, reuse it.

## Step 2: Identify what to loop

`/loop` takes **either a skill or a plain-language activity** — whatever follows it is what repeats.

**A) Paired with a skill:**
- **`/loop /improve`** → run improvement rounds forever (one `/improve` round per iteration).
- **`/loop /improvement-ideas`** → keep generating and refreshing ideas.
- **`/improve /improvement-ideas /loop`** → alternate: generate/refresh ideas, then act on the top ones with improvement rounds, then regenerate ideas against the new state, and repeat. A self-feeding cycle.
- **`/loop /bug-hunt`**, `/loop /new-features`, etc. → repeat that skill's unit of work each iteration.

**B) Paired with a plain-language activity (no skill needed):**
Whatever you name in words becomes the repeating task — you don't have to invoke a formal skill. Examples:
- **`/loop skill creation`** → each iteration, invent and build **one new skill** (design it, write its `SKILL.md`, any scripts, test it), then start the next. Keep producing new, distinct skills until stopped.
- **`/loop strategy creation`** → each iteration, create and validate **one new trading strategy** (design it, implement, backtest/judge it, keep or discard with the result), then the next. New distinct strategies, round after round.
- **`/loop <anything>`** → repeat that activity's natural unit: "write tests" → a test module per iteration; "harden security" → one hardening pass; "add levels to the game" → one level; etc.

**Define one iteration = one complete, real unit of that activity**, and keep it consistent: for "skill creation" that's one finished, tested skill (not a half-written stub); for "strategy creation" that's one designed-and-measured strategy. Each unit must be genuine and distinct from the last — no near-duplicates to pad the count (same spirit as the anti-churn rules). If the activity is vague, state the unit you chose in one line, then go.

If both a skill and a plain activity are given, or it's ambiguous, pick the natural unit and keep it consistent across iterations.

## Step 3: Run the loop

Each iteration:
1. **Check the STOP flag** at the boundary (never mid-action), per [[control]]:
   ```bash
   [ -f .claude/stop ]&&echo STOP||echo go
   ```
   `STOP` → finish the current unit cleanly, then go to Step 4. `go` → continue.
2. **Do one unit of the paired skill(s)** — a real, complete, verified piece of work (an actual improvement round with a measured result, an idea genuinely acted on, etc.). Apply that skill's full discipline; don't cut it short because you're "in a loop."
3. **Log it briefly** and go straight into the next iteration. Do not stop, do not ask "want me to keep going?", do not hand back — that's what the STOP button is for.

### Inherit work-until-limit's anti-stop discipline

The loop's failure mode is identical to work-until-limit's: the model inventing a reason to quit early. **The same bans apply here.** None of these end the loop — only the user does:
- "Ran out of high-value work / the vein is thin / diminishing returns" → rotate to a different kind of work and keep looping (see [[improve]] and [[work-until-limit]]).
- "Everything's complete / this is a good stopping point / it needs your decision now" → park what needs a decision, keep looping on what doesn't.
- "A background job is running, I'll wait" → keep doing other iterations while it runs; never idle-wait.
- "That's enough iterations" → there is no iteration count; the user quits, not you.

The loop continues across background jobs, thin veins, and "feels done" — always. If you catch yourself about to end the turn for any reason other than the STOP flag or a real blocker, don't: start the next iteration.

## Step 4: When the user stops it

The loop ends **only** when:
- **The STOP button is pressed** (`.claude/stop` exists) — finish the current unit, clear the flag (`rm -f .claude/stop`), report what the loop accomplished (iterations done, net result), and hand back. Per [[control]], the button window self-closes.
- **The user sends a new message** — a new prompt ends the loop the same way any run ends; respond to the new request (don't silently keep looping).
- **A genuine blocker or the hard safety line** — something only the user can resolve, or a destructive/irreversible action needing confirmation. Surface it, then continue once cleared.

Nothing else stops it. Not a round count (there isn't one), not "done", not a quiet moment.

## Notes

- Pairs by design with [[improve]], [[improvement-ideas]], [[bug-hunt]], [[new-features]], and always launches [[control]]. Composes with [[work-until-limit]] too — if both are set, whichever limit trips first ends it (the ceiling OR the user), and the STOP button covers the manual case.
- If the user also set [[shutdown-when-done]], run the shutdown finale when the loop actually ends (on STOP), not between iterations.
- Respects [[no-talk]] (loop quietly, log each iteration in a line, report on stop).
- Distinct from the built-in interval runner: this loops as fast as it can do real units of work, gated by the STOP button, not on a timer.
