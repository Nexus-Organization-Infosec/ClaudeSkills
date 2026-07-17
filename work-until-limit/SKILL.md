---
name: work-until-limit
description: Work continuously until the account's usage quota reaches a set ceiling — a session ceiling, a weekly ceiling, or both — and DO NOT stop before it for any other reason (not "task done", not "exhausted findings", not "good enough", not "nothing left worth doing" — switch to other useful work instead). Shows a live percentage bar during the run, then stops cleanly at the ceiling. Invoked as "work-until-limit [<sessionPct>] [weekly <weeklyPct>] [limit-refresh] [shutdownwhendone]" — e.g. "work-until-limit 80" (stop at 80% session), "work-until-limit 90 weekly 90" (stop when session OR week hits 90%), "work-until-limit weekly 90" (weekly only), add "limit-refresh" to bridge an imminent limit reset and keep going, and "shutdownwhendone" to power off when it stops. Use whenever the user asks to keep working/improving until near the usage or weekly limit, run an autonomous session bounded by quota, or "go until I'm about to run out". Active ONLY for the message that explicitly invokes it — a new user message that does not re-invoke it ends the mode, so never carry it over from earlier messages or keep working toward a ceiling the user did not just ask for. Compatible with and hands off to the [[shutdown-when-done]] skill.
---

# Work Until Limit

Keep doing useful work until the usage quota hits a ceiling the user sets, showing them where the meter is along the way, then stop gracefully — or shut the machine down if they asked for that too.

## CRITICAL: this is active ONLY when the user just asked for it — it never carries over

This mode applies **only to the single user message that explicitly invoked it.** It is NOT a standing mode that persists across messages. Get this wrong and you burn the user's quota against their will.

- **A new user message ends it.** The autonomous chunk-loop continues across *your own* steps within one run — that's fine, it's the run they started. But the moment the **user** sends a new prompt, the run is over. If that new prompt does **not** itself invoke work-until-limit, do NOT resume the loop, do NOT keep working toward a ceiling, and do NOT reason "I was in work-until-limit, so I'll carry on." Just answer the new message as an ordinary, single request and stop.
- **This is exactly what happens when the user interrupts.** If the user hit stop/escape and typed something new, they are done with the limit run. Treat their new message at face value. Never treat the earlier `work-until-limit` as still in force.
- **Past messages do not count.** The only thing that activates this skill is the user asking for it in their *current* message. Never infer it from earlier in the conversation, from a checkpoint, or from the fact that a ceiling was mentioned before.
- **Never start it on your own.** Don't decide to "keep working until the limit" unless the user, in this message, told you to.

In short: no explicit request in the latest user message means no work-until-limit. When in doubt, do the one thing they asked and stop.

## Compatibility

This works WITH `/shutdown-when-done` (it is not one of the mutually-exclusive pairs). If the invocation includes the `shutdownwhendone` token, the shutdown is the finale that runs once the limit is reached.

## Step 1: Parse the invocation

There are two usage limits — the **session** limit (the shorter rolling window) and the **weekly** limit — and you can bound either or both. The grammar:

`work-until-limit [<sessionPct>] [weekly <weeklyPct>] [limit-refresh] [shutdownwhendone]`

- **`<sessionPct>`** — the leading number is the SESSION ceiling (1–99).
- **`weekly <weeklyPct>`** — sets the WEEKLY ceiling (1–99).
- **`limit-refresh`** (optional token) — instead of stopping when a limit is about to be hit, *bridge* an imminent reset: if the binding limit resets very soon, wait it out and keep working afterwards (see [[limit-refresh]] and Step 3). Only meaningful together with a ceiling — it's a modifier, not a standalone.
- **`shutdownwhendone`** (optional token) — run the [[shutdown-when-done]] finale when work stops.

Read it like this:
- `work-until-limit 80` → stop when **session ≥ 80%** (weekly not bounded).
- `work-until-limit 90 weekly 90` → stop when **session ≥ 90% OR week ≥ 90%** (whichever comes first).
- `work-until-limit weekly 90` → stop when **week ≥ 90%** only (session not bounded).
- `work-until-limit 90 limit-refresh` → work toward session 90%, but if the session limit is about to reset, ride through the reset and keep going.
- `work-until-limit 90 weekly 90 shutdownwhendone` → same as the two-ceiling case, then shut down.

At least one ceiling must be set. If the user gave neither a number nor `weekly N`, ask or default to session 80. A ceiling that isn't set is passed as `0` to the monitor (meaning "don't bound this limit").

**Safe ceilings differ by limit** (because they move at different speeds — see the Reality check): the **weekly** limit moves very slowly, so a high weekly ceiling like **99% is fine**. The **session/daily** limit moves fast, so keep headroom there — **don't set a session ceiling near 99%** (≈90% is a sensible max) or a single heavy chunk can overshoot into the real limit.

**Pin the exact ceilings to a file so they can't drift.** This run can be long (many chunks, possibly a context compaction in between), and a ceiling held only in your memory is exactly what drifts — a `99` silently becoming `96`. So record the numbers the user gave *right now* and read them back on every check instead of recalling them:

```bash
printf 'SESSION=%s\nWEEKLY=%s\n' <sessionPct-or-0> <weeklyPct-or-0> > .claude/wul-config
printf 'SESSION=0\nWEEKLY=0\n' > .claude/wul-banked   # progress banked from resets, starts at 0
```

The `wul-banked` file matters for resets — see "Resets bank your progress" in Step 3. It starts at 0 for a fresh run.

The ceiling is **exactly** the number the user gave — never round it, approximate it, or substitute a remembered value. If you are ever unsure what it was, `cat .claude/wul-config`; do not guess. If the user said weekly 99, every check uses 99 — not 96, not "about 95."

Also determine **what to work on**. Usually it's the task already in play (keep building/improving/validating it). If there's no obvious task, ask the user what to work on before starting — "work until the limit" needs something to work on.

## Step 2: Take a baseline reading

Before the first chunk, take one fresh reading so you know the starting point. Run the monitor in single-reading mode (`-Once`), **sourcing the pinned ceilings from `.claude/wul-config`** so the exact numbers are used every time (never typed from memory). Do it as one command so the sourced values are in scope:

```bash
. .claude/wul-config; powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:/Users/flori/.claude/skills/work-until-limit/scripts/usage_monitor.ps1 -Once -Threshold ${SESSION:-0} -WeeklyThreshold ${WEEKLY:-0} -StatusFile .claude/usage-status.txt
```

Because the monitor writes `THRESHOLD`/`WEEKLYTHRESHOLD` and the `STOP` flag into the status file from exactly these pinned values, **your stop decision reads from the file, not from memory** — which is what keeps the ceiling from drifting mid-run.

This runs `claude -p "/usage"` **inside PowerShell** (critical — Git Bash mangles the `/usage` argument into a file path, PowerShell does not), parses the two limit lines ("Current session: N% used", "Current week: N% used"), and writes `.claude/usage-status.txt` with `STATUS`, `SESSION`, `WEEK`, `PERCENT` (the higher of the two, for the bar), `THRESHOLD`, `WEEKLYTHRESHOLD`, `STOP`, and a `BAR`. It ignores the breakdown stats like "96% of your usage was at >150k context".

Confirm `STATUS=OK` with a sensible `PERCENT`. `STATUS=UNKNOWN`/`TIMEOUT` is a genuine fault — show the user the raw output and ask whether to stop or fall back to a fixed work budget. Never treat an unreadable meter as "0% — keep going forever."

## Step 3: Work in bounded chunks, checking on-demand — and stop *predictively*

The danger this design guards against: on high-context work a single chunk can move the meter several percent, so a stale reading can let you sail past the ceiling. Two rules defeat that — **fresh readings** and **stopping early enough to absorb one more jump.**

Loop:
1. **Do ONE bounded chunk of useful work** — a single improvement, fix, analysis, or backtest. Keep chunks modest on purpose: the smaller the chunk, the smaller the worst-case jump between readings. If the next step is known to be heavy (a long backtest, a huge file read), treat that as its own chunk and check *before* launching it.
2. **Take a fresh reading** with the same `-Once` command as Step 2. Do not rely on a timer or an old value — read the meter *now*.
3. **Append the reading to a run-log, then compute the jump.** Log each reading so the deltas come from real history and overshoot is auditable afterward — not just held in your head across a long run:
   ```bash
   printf '%s SESSION=%s WEEK=%s\n' "$(date '+%H:%M:%S')" "$SESSION" "$WEEK" >> .claude/wul-log
   ```
   Then compute the jump for each bounded limit from the previous logged reading: `session_delta = SESSION_now − SESSION_prev`, `week_delta = WEEK_now − WEEK_prev`. These estimate how much the next comparable chunk will add. Keep a running `max` of each from the log (default to a safety floor of ~4% for session until you've observed real jumps, since high-context turns are large; weekly moves slower, so a smaller floor like ~1% is fine). Reading the max jump from the logged history — rather than just the last two points — makes the predictive stop more robust to one unusually small gap.

   **Bank progress across resets, and work with EFFECTIVE progress from here on.** The ceiling is the *total* budget for the whole run, not a fresh allowance each time a limit resets. So detect a reset: if a reading *dropped* sharply from the previous one (e.g. session 61 → 2 — normal work only pushes usage *up*, so a big drop means the limit rolled over). On a reset, add the pre-reset value (the peak just before the drop) into `.claude/wul-banked` for that limit:
   ```bash
   # session reset detected; PREV_SESSION was the peak just before the drop:
   b=$(grep '^SESSION=' .claude/wul-banked | cut -d= -f2); nb=$((b + PREV_SESSION))
   sed -i "s/^SESSION=.*/SESSION=$nb/" .claude/wul-banked
   ```
   Your **effective progress** toward each ceiling is `banked + current`: `eff_session = banked_session + SESSION`, `eff_week = banked_week + WEEK`. From here on the ceiling is compared against *effective* progress, not the raw meter. (Before any reset, banked is 0, so effective equals the raw reading and nothing changes.)

   **CRITICAL — bank the WHOLE pre-reset reading, never a "run-delta".** The number you bank is the raw meter value right before the drop (e.g. 87), *not* the amount this run supposedly added on top of some earlier baseline. Do NOT reason "the meter was already at 82 before I started, so I'll only bank my ~5% and keep the pre-existing 82 out of it" — that is wrong and it is banned. The ceiling is an **absolute cumulative meter target**: all usage on the meter counts, whether this run caused it or not. If you bank only a run-delta, the reset hands you a near-full fresh session (you'd grind the new meter up to ~ceiling again), which is exactly what banking exists to prevent. Concretely: baseline 82, run pushes it to 87, ceiling 95, reset hits → bank **87**, then stop when the fresh meter reaches **8** (87 + 8 = 95). That is ~8% more work, NOT ~90% more. When in doubt, bank the higher number.
4. **Show the user the bar with the trend**, and show effective vs raw when a reset has banked anything, e.g.:
   `Usage: session 22% + 20% banked = 42% of 40 ceiling` — otherwise just `session [##############------] 72% (+4%) · ceiling 90`.
5. **Decide — using EFFECTIVE progress.** The base rule is simple — **reaching the ceiling is the goal**, so stop when `eff_session >= sessionCeiling` (or `eff_week >= weeklyCeiling`). The predictive headroom is an *extra* early-stop that applies **only when the ceiling is near the real hard limit**, because that's the only time overshoot actually costs you (lockout).
   - `STATUS=UNKNOWN`/`TIMEOUT` → follow the fallback agreed in Step 2.
   - **Is the ceiling near the real limit?** Danger zone ≈ **session ceiling ≥ 90%** or **weekly ceiling ≥ 95%**. Overshooting a ceiling *in* the danger zone risks crossing 100% → days of lockout; overshooting a ceiling *below* it (e.g. a 10% session target) is harmless — you're nowhere near the real limit. (The danger check uses the *raw* current meter, since lockout is about the real 100% wall; the soft target check uses effective progress.)
   - **Ceiling in the danger zone → apply predictive headroom** (stop a chunk early): `eff_session + max_session_delta >= sessionCeiling` → stop; likewise for week. Better to stop a hair short than get locked out.
   - **Ceiling below the danger zone → do NOT stop early.** Just stop when effective progress actually reaches it (`eff_session >= sessionCeiling`). A single in-flight chunk nudging slightly past a low soft target does no harm, whereas stopping 3% short throws away budget the user allowed.
   - When you stop, tell the user *which* ceiling triggered it and whether it was a reach or a predictive stop, and note any banked amount. **If `limit-refresh` is enabled, first check whether that limit is about to reset — see below before actually stopping.**
   - otherwise → continue with the next chunk.

So for a **danger-zone ceiling** the effective stop lands *at or just under* it (protecting against lockout); for a **soft ceiling below the danger zone** you run all the way to it and may drift a hair past — which is fine and is what "use the whole budget" means. The predictive headroom is lockout insurance, not a reason to leave a low target's budget unspent.

### Resets bank your progress — the ceiling is a cumulative budget

This is the key rule for resets: **the ceiling counts total work across the whole run, so a reset does not hand you a fresh full budget.** What you already spent before the reset is banked and subtracted from what's left.

- **Worked example (the user's):** ceiling **40**, you work up to **20%**, then the session limit resets to 0. Bank the 20. Keep working after the reset, and stop when the *new* meter reaches **20%** — because banked 20 + current 20 = **40**. Total spent across the reset is the 40 they asked for, not 60.
- **Bank the raw pre-reset reading, not a "run-delta".** If the meter was already at some baseline when you started (say 82) and your run pushed it to 87 before a reset, you bank **87**, not the 5 you think you "added". Never keep pre-existing usage out of the banked figure — the meter number is the meter number. Banking only your delta would let the reset restart you at a near-full fresh session, defeating the whole cumulative-budget idea.
- Each limit banks separately (`SESSION` and `WEEK` in `wul-banked`). Session/daily resets every few hours, so it's the usual case; weekly rarely resets mid-run, but the same rule applies if it does.
- **This survives interruptions.** `wul-banked`, `wul-config`, and `wul-log` are on disk, so if the session is cut off (or `/usage` goes briefly self-inconsistent, like the 0/0 you saw), a later `/continue` reads them back and resumes toward the *remaining* budget, not the full ceiling again.
- It composes with `limit-refresh`: bridging waits out an imminent reset; banking then makes sure the post-reset work only fills the remainder, not a whole second ceiling.

### If `limit-refresh` is enabled: bridge an imminent reset instead of stopping

The status file reports how long until each limit resets: `SESSION_RESET_MIN` and `WEEK_RESET_MIN` (minutes; `-1` = unknown). A limit that's about to reset isn't really a wall — cross the reset and it drops back near 0.

**Bridging is ONE-TIME USE per run.** The first time you bridge a reset, `limit-refresh` is spent — turn it off for the rest of the session. Limits only reset on long cycles (the session/daily limit every few hours, the weekly limit once a week), so the *next* reset after the one you just rode through is hours or days away. Waiting for that one would stall the run for ~4 hours, which is never worth it. After the single bridge, any further ceiling hit just **stops normally.** Note the "already bridged" state so it survives across chunks.

So when a bounded limit *L* would trigger the stop (and you haven't already bridged this run):

1. **Look at `L`'s reset countdown.** If it's within the **refresh window** (default ~10 minutes; keep it short — you're going to wait it out) and ≥ 0:
   - **Don't stop. Bridge it:** pause work (start no new chunk — you don't want to push *further* over while waiting), then wait until about 1–2 minutes past the reset. A blocking wait is fine because the window is short by design, e.g.:
     `powershell.exe -NoProfile -Command "Start-Sleep -Seconds <(reset_min+2)*60>"`
   - After waiting, take a fresh `-Once` reading and **confirm the limit actually dropped** (the printed reset time is an estimate; if it hasn't reset yet, wait another minute and re-check). Once it's low again, **mark bridging as used** and resume the loop.
   - Tell the user you're bridging, e.g. "session at 88% but it resets in 3 min — waiting for the reset, then continuing (this is my one bridge)."
2. **If `L`'s reset is NOT within the window** (e.g. the weekly limit is days away), the reset can't save you — **stop as normal.**
3. **Guard the other limit.** Only bridge if the *other* bounded limit still has room. If session is about to reset but the weekly ceiling is also essentially hit (and weekly isn't resetting soon), stop anyway — bridging the session does nothing when weekly is the real wall, and work after the session reset still spends weekly quota.

**Always keep a couple of percent of headroom.** Bridge based on the predictive reading with its safety margin, don't try to run the meter to the exact ceiling before the reset — a small buffer absorbs an inaccurate reset estimate or one last in-flight chunk. `limit-refresh` extends the run across reset boundaries; it never justifies knowingly blowing through a limit that isn't about to reset.

### Only THREE things may stop this run — check this every time you consider stopping

**(1) a bounded limit reaches its ceiling, (2) the meter is unreadable (Step 2 fault), or (3) the user interrupts. Nothing else — full stop.**

Before you stop for *any* reason, name which of those three it is. If your reason isn't literally one of them, it is not a valid stop — resume working. Every one of these is FORBIDDEN as a stop reason:
- "I've exhausted the findings / covered every high-risk file / the audit is done."
- "The project is already past half done" / "it's in good shape now."
- "Further work seems useless / low-value / diminishing returns."
- "This is a natural stopping point" / "I've done enough" / "it feels complete."
- "Every requested item is done and verified, so continuing would be padding."
- **"Per the `/improve` discipline, padding to the ceiling would be manufactured churn, so I'm stopping honestly."** This one is a trap and it is wrong here — see below.
- **"I've covered the high-value surface; continuing would be lower-value review of solid code."** BANNED. "Lower-value" is not "no value" and is not a stop condition — the ceiling does not care about a value gradient. Low-value real work still beats stopping. And if the code is solid, stop *reviewing* and go *build*: add tests, harden an edge, write the next feature. Value dropping is a signal to **switch activity**, never to stop.
- **"I was confirming robustness rather than finding defects, so there's little left to do."** BANNED. Running out of one lens (defect-hunting) is not running out of work — pivot to a different activity (tests, features, perf, docs, hardening) and keep going. See "Running out of one activity."
- **"If you want me to keep going to the ceiling, just say the word."** BANNED as a closing line. Writing this to a user who already invoked `work-until-limit` is stopping-and-asking — they already said the word when they invoked it. Do not offer to continue; **continue.**
- **"I'll pace / conserve budget / run one round, not endless rounds, then stop."** BANNED. Conserving budget is the *opposite* of this mode — the user asked you to *spend* it up to the ceiling. "Pacing" is only ever about leaving a small headroom for the final verification/shutdown to fit *under* the ceiling; it never means stopping at 25% of a 50% run. If a swarm or any expensive activity makes each unit of work cost more, that is a reason to pick **cheaper effort so the budget lasts longer and you do MORE**, never a reason to do one round and coast to a stop. Stopping far below the ceiling to "save" budget is the early-stop this skill exists to prevent.

### If you can name work you could do, you have NOT run out of work — go do it

The recurring tell in every one of these failures: the model stops, then in the same breath lists concrete things it *could* do next ("I could dig into the server routers, the panic/wipe module, deeper web testing…"). **Naming that work is proof the work exists.** Offering it to the user instead of doing it is the violation, full stop. If a candidate task comes to mind, that is your next task — start it, don't surface it as a question. You are only allowed to claim "no work left" if you can name *nothing*, which on a real app essentially never happens.

These are all your *opinion that the work is finished*. The user has already overruled that opinion by telling you to work until the limit. That instruction **is** the decision — so don't re-make it each chunk and don't dress it up as a finding ("I stopped because I genuinely ran out of things to do, not because of the limit" is precisely the sentence this rule exists to prevent).

### The `/improve` "no manufactured churn" rule does NOT authorize stopping here

`/improve` says: don't make pointless marginal edits just to hit a round count. That is true, and it stays true. But it is being misused as a stop excuse, so be exact about what it means when `work-until-limit` is active:

- "No manufactured churn" means **don't pad *one activity* (e.g. improving the same file) with junk edits.** It does **not** mean "stop the run." Those are different. The honest alternative to churning one thing is **switching to a different, genuinely useful kind of work** — not ending the session.
- `/improve N` is bounded by a *round count*, so "out of worthwhile rounds → stop" is correct there. `work-until-limit` is bounded by the *quota ceiling*, not by whether improvements remain. When the two are combined, the ceiling wins. Running out of improvements to X means go do Y (tests, bug hunt, security audit, docs, a real feature), not stop.
- "Stopping honestly" is not honest when the user told you to reach 75% and you stopped at 62% because you didn't want to look for more real work. The honest move is to keep finding legitimate work until the ceiling. There is essentially always real, non-churn work on a live app: more tests, edge cases, hardening, a security pass, performance, documentation, the next feature. Go find it.

If you genuinely believe there is *no* real, non-churn work left anywhere in the project before the ceiling — which on a real app is almost never true — then say that explicitly to the user and ask **while you keep working**. Asking is not a stop condition (see the three), and it never licenses ending the run.

### "Stopping to ask" is just stopping. Naming work you could do proves you have work to do.

The escape hatch above gets abused, so it is fenced hard:

- **If you can name a concrete thing you could build or fix, you have NOT run out of work — go do that thing.** Writing "if you'd rather I keep going, I could add QR verification or chat export, just say so" is a confession that real work existed and you chose not to do it. That is a violation, not a courtesy. Name it and *build* it; don't offer it and quit.
- **Unattended runs cannot stop-and-ask.** If the user is away (they invoked `shutdownwhendone`, said goodnight, went to bed, or simply is not answering), there is nobody to answer the question, so "asking" guarantees the run dies right there while the budget sits unspent — the exact outcome this mode exists to prevent. When unattended, do not ask: pick the next item off the rotation and keep working to the ceiling.
- **"Too risky to build unsupervised" is not a stop reason.** It is a reason to pick *different* work. Skip the risky item (new deps, hardware, anything you can't verify) and take safe, verifiable work instead: tests, edge cases, hardening, profiling, docs, refactors, smaller features. There is always safe work.
- **The `/full-speed` "no padding / no make-work" rule does NOT authorize stopping here either.** Same trap as `/improve`, same answer: it bans *manufactured* work inside an activity; it never bans *continuing the run*. Under `work-until-limit`, work up to the ceiling is **required work**, not padding — the user asked for it, so it is by definition not waste. Reaching for `/full-speed`, `/improve`, or any "don't do useless work" instruction as grounds to end the run early is misreading all of them, and it is banned.
- The floor the user set is a **commitment, not a target you may negotiate down.** Stopping at 28% of a 45% run is a 38% shortfall on what they asked for, delivered while they slept and could not correct you.

### Running out of one activity is NOT running out of work

The single most common trap: you finish a *task or activity* (no more audit findings, no more bugs, no more placeholders) and mistake it for the *run* being done. It isn't. This mode is bounded by the **limit**, never by any one task or activity reaching "complete." When an activity is exhausted, **switch to the next one and keep going.** There is a deep well of genuinely useful work on any real project — rotate through it:

security audit → bug hunt → test coverage (raise it, add edge cases) → performance profiling & optimization → error-handling & resilience hardening → refactoring for clarity → docs/comments → dependency & config review → input validation → logging/observability → small feature or UX improvements → deeper validation/backtests.

"I can't think of anything worth doing" almost always means "I didn't look hard enough." Re-scan the project and pick the next real improvement. The whole purpose of this mode is to spend the budget **right up to the ceiling** — stopping early because it *feels* like enough is the exact thing this skill exists to prevent, and it wastes the budget the user explicitly asked you to use (and, with `shutdownwhendone`, shuts the machine down before the work you owed them is done).

### Don't fill the run with verification theater

A chunk is supposed to be **work**. Running the test suite, reading the meter, and writing status updates are **overhead** — necessary, but they are not progress. Burning the budget on overhead while the real task goes untouched is a failure mode that *looks* productive (everything's green!) and delivers almost nothing.

- **Verify proportionately.** After a one-line change, run the affected tests, not the whole suite. Save the full suite for a substantive change or once at the end. A full suite after every micro-edit is expensive and tells you nothing new.
- **"Final verification" happens once.** If you run a "final" full suite and then keep working, it wasn't final. Announcing final verification repeatedly is a reliable tell that you're padding the run with safe busywork.
- **Read the meter between real chunks**, not after every micro-step. A chunk is a unit of *work*, not a unit of testing.
- **Never let overhead crowd out the actual task.** This is the important one: **if you can name a substantial remaining task and there is budget left, start it.** Do not spend the run on tests and re-verification and then hand back saying "the natural next task is X" — X was the work you were supposed to be doing. Naming it at the end while having chosen testing instead is not a handoff, it's an admission you avoided the hard part.
- If a known task genuinely doesn't fit the remaining budget, **say that explicitly and say why** ("media locking needs the delivery-ack reordered, that's ~2 hours of work and I have 3% left"), rather than quietly filling the time with suite runs. The user can then decide.

Bias toward the substantive and the risky over the safe and the green. Tests and verification serve the work; they are not a substitute for it.

## Step 4: Stop cleanly

When the loop ends:
1. **Summarize**: what you accomplished this session, and the final usage reading (with the bar), noting you stopped with headroom if the predictive rule triggered.
2. **If `shutdownwhendone` was in the invocation**, run the `/shutdown-when-done` finale now (Claude-branded notification + scheduled shutdown) as the very last action. Otherwise hand the work back to the user.

## Reality check to keep in mind

- **The stop is cooperative.** Nothing can interrupt your turn from outside — the ceiling is honored only because you take a fresh reading and decide *between* chunks. So keep chunks bounded and check every single time; a giant unbroken chunk is where overshoot hides.
- **Fresh-per-chunk beats any timer.** That's why this uses on-demand `-Once` readings rather than a background poller: the number you act on is current at the moment of decision, not minutes old.
- **Cadence and headroom scale with how fast the limit moves, not with raw proximity.** The only real danger is a chunk jumping usage *past the ceiling between checks* — and how likely that is depends entirely on how much a single chunk moves that particular limit:
  - **Weekly limit — moves very slowly.** A single chunk barely nudges the weekly meter, so overshoot risk is tiny. A **high weekly ceiling (up to 99%) is safe**, and spacing checks out is fine even when close to it — don't waste `-Once` reads hovering over a slow-moving weekly number.
  - **Session/daily limit — moves fast.** A heavy chunk can jump the session meter several percent, so **don't push a session ceiling near 99%** — keep real headroom (e.g. stop around ~90%) so one more jump can't blow the actual limit. Near the session ceiling, check **every chunk** and keep chunks small.
  The predictive rule already tracks each limit's per-chunk delta, so trust it: weekly's tiny delta lets you ride right up to the line, while session's larger delta makes it stop earlier on its own. When in doubt on the *session* limit near its ceiling, check; on weekly, relax.
- **A hard server-side limit hit can still cut the session off** between chunks regardless of your ceiling — that's the involuntary case `/continue` recovers from, so each chunk should leave things in a resumable state.
- **Optional passive monitor:** if you also want a continuously-updating readout, the `work_until_limit.bat <percent> <statusfile> <interval>` launcher runs the loop in the background — but the per-chunk `-Once` reading is what the stop decision must rely on.
