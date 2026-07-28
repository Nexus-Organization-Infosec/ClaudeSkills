---
name: no-waiting
description: Never burn time blocking on a wait. Forbids foreground `sleep`/idle-polling to wait for a long job (a download, fetch, build, backtest, deploy) — instead run that job in the BACKGROUND and keep doing other useful work while it runs, checking on it with a quick non-blocking peek only at task boundaries. Use whenever the user invokes /no-waiting or says "don't just sit there waiting", "run it in the background and keep working", "stop sleeping/blocking", "don't waste time waiting for X", or when you're about to `sleep N` to wait for something. Waiting is not work; overlap it with real work.
---

# No Waiting

Blocking to wait for something is wasted time. If a job takes minutes (a data fetch, a download, a build, a backtest, a long test suite, a deploy), you do **not** sit there — you put the job in the background, go do other real work, and glance at the job only when you pass a natural checkpoint. The wait overlaps with work instead of replacing it.

## The banned move: `sleep` to wait

**Never run a foreground `sleep N` (or a blocking poll loop) to wait for a background job.** Commands like:

```bash
sleep 590; grep -c cached .claude/fetch1m.txt      # BANNED — 10 dead minutes
```

are pure dead time — you've frozen yourself for ten minutes doing nothing while the fetch you're waiting on was already running on its own. (In this harness a foreground `sleep` is blocked outright anyway.) There is essentially always other useful work you could have done in those ten minutes.

## What to do instead

1. **Launch the long job in the background.** Use the Bash tool's `run_in_background` option (it runs detached and notifies you when it finishes), or start it as a detached process that writes progress/results to a file. Kick it off, note where its output lands, and move on **in the same turn.**
2. **Go do other real work while it runs.** This is the whole point. Pick the next independent task — another feature, a fix, tests, a refactor, docs, a different module, analysis that doesn't need the job's output — and actually do it. The background job needs none of your attention to run.
3. **Check on it with ONE quick non-blocking command at a boundary.** When you reach a natural stopping point in the other work (or when the harness notifies you the job finished), take a single instant peek — not a sleep-then-check:
   ```bash
   grep -c cached .claude/fetch1m.txt; tail -1 .claude/fetch1m.txt   # instant, no sleep
   ```
   If it's done, use the result. If not, go back to step 2 and do more work; check again later. Never precede the check with a `sleep`.
4. **Only block if you truly cannot proceed on anything else** — which, on a real project with a backlog, almost never happens. If you genuinely must wait on a condition, use a non-blocking waiter (e.g. the Monitor tool with an until-condition) rather than a fixed `sleep`, and still prefer interleaving real work.

## The rule of thumb

**Waiting is not work.** A turn that consists of "start job → sleep → read result" did almost nothing; a turn that consists of "start job in background → build the next thing → peek at the job → keep building" did a full unit of work *and* advanced the job. Always the second shape.

- If you catch yourself typing `sleep` before a check command, stop — that's the anti-pattern. Background the job and go work.
- "I'll wait for X to finish and then continue" is the same idle-wait: X finishes on its own; you continue *now* on something else.
- Time spent blocked is time the user paid for and got nothing back. Treat every minute of blocking as a bug.

## Notes

- This is the general-purpose version of the rule [[work-until-limit]] enforces during a bounded run ("background tasks running is never idle time"); `/no-waiting` applies it everywhere, any time, not just inside a quota run.
- Pairs with everything, especially long autonomous work — [[work-until-limit]], [[loop]], [[ultragoal]], [[dont-stop-till-complete]] — where a single blocking wait can waste a big share of the session.
- Respects [[no-talk]] (just background it and keep working, no narration).
