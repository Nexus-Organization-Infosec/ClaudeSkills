---
name: work-till-message
description: Work continuously on useful work and DO NOT end your turn for any reason until the USER sends a new message — the only thing that stops you is the user interrupting. Not "task done", not "exhausted findings", not "good enough", not "nothing left worth doing", not "waiting for a background job" — when one thread of work runs out, switch to another and keep going. The user coming back is the stop signal; nothing else is. Invoked as "work-till-message" (keep working until I message you), optionally with what to work on. Use whenever the user invokes /work-till-message or says "keep working until I get back", "don't stop until I message you", "work until I say stop", "just keep going until I interrupt", "I'll be away, keep improving things till I return", or "work continuously until my next message". Active ONLY for the message that explicitly invokes it — a new user message ends the mode by definition (it's the stop condition), so never carry it over. The time-open sibling of [[work-until-limit]] (quota-bounded) and [[work-until-time]] (clock-bounded); shares their anti-early-stop discipline. Compatible with [[shutdown-when-done]] only if the user pairs them, but note the natural end here is the user's message, not a task finishing.
---

# Work Till Message

Keep doing genuinely useful work, without ever ending your turn, until the **user sends their next message.** That message — and only that message — ends the run. There is no quota to watch and no clock to hit: the single stop condition is the human coming back.

This is the loophole-hardened sibling of [[work-until-limit]]. It has the same failure mode — a model that rationalizes an early stop — and the same answer: **only the named stop condition ends the run, and here that condition is "the user messaged," which is not something you can observe mid-turn.** So in practice, *you never voluntarily stop.* You keep working until the turn is interrupted from outside.

## The one stop condition — and why you can't reach it yourself

**The run ends when, and only when, the USER sends a new message.**

That is an *external* event. It interrupts your turn; you do not detect it and decide to stop. Which means: **from inside your turn, there is no legitimate reason to end.** Every sentence you might write that concludes your turn is, by definition, a voluntary early stop — and there are no voluntary stops in this mode.

- You do **not** stop because the task is done. Task done → start the next useful task.
- You do **not** stop because you "ran out of things to do." On a real project you never do; re-scan and find the next thing (see the rotation below).
- You do **not** stop to ask "should I keep going?" — the user already answered that by invoking this. Asking is itself a stop, and it strands the run because they're away.
- You do **not** stop to wait for a background job. It runs on its own; you work on something else meanwhile.
- You do **not** end your turn with a summary and a hand-back. Ending the turn *is* the stop you're forbidden from making.

The only thing that ends this is the user typing again. Until that happens, produce real work.

## CRITICAL: active ONLY for the message that invoked it

Like [[work-until-limit]], this applies **only to the single user message that turned it on** — and the way it ends is even more direct: the user's *next* message is literally the stop condition.

- **The user's new message ends the run, full stop.** When they message again, this mode is over. Read that new message at face value and just answer it — do not resume "work till message," do not keep grinding toward a nonexistent ceiling, unless the new message itself re-invokes the skill.
- **Never carry it over.** Past invocation ≠ current permission. Only an explicit invocation *in the latest user message* turns it on.
- **Never start it on your own.** Don't decide to "just keep working until they come back" unless they told you to in this message.

## What "keep working" means — the anti-early-stop discipline

Everything [[work-until-limit]] says about not stopping applies here verbatim, minus the meter. The short version, because these are the exact rationalizations to refuse:

### Only the user's message stops you — everything else is a switch, not a stop
When a thread of work ends, that is a signal to **change activity**, never to end the turn. Rotate through the deep well of real work any live project has:

security audit → bug hunt → test coverage & edge cases → live testing (actually run it, see [[test-live]]) → performance profiling & optimization → error-handling & resilience hardening → refactoring for clarity → docs/comments → dependency & config review → input validation → logging/observability → design/UX polish → the next feature → deeper validation.

"I can't think of anything worth doing" almost always means "I didn't look hard enough." Re-scan and pick the next real improvement.

### If you can name work you could do, you have NOT run out of work — go do it
The universal tell: you stop, then in the same breath list things you "could" do next. Naming that work proves it exists. **Do it, don't offer it.** Offering a menu of next steps and ending the turn is a hand-back dressed as helpfulness — and doubly broken here because the user is away and can't pick.

### Background tasks running is NEVER idle time
Kicking off a long job (build, download, test capture, backtest) does not end your turn. It runs by itself; you fill the time with *other* real work. Banned as turn-enders, verbatim: "everything that can run without me is running, nudge me when it's done", "awaiting the capture/build/results", "I'll report each as it lands." Background the job, then immediately start the next piece of work in the same turn. Pick up the job's result when it lands, in a later step of the same run.

### Saying you'll continue is not continuing
The camouflage failure: reciting "the run continues, I'll keep working" and then ending the turn anyway. The test is behavioral, not verbal — the *very next thing* after any such sentence must be a real action (an edit, a test run, a fix, the next item), not a status summary and a stop. Words like "continuing" are made true by the tool calls that follow them in the same turn, or they're a lie.

### Every one of these is FORBIDDEN as a reason to end the turn
- "The task is complete / everything requested is done." → Start the next task.
- "This is a natural stopping point / I've done enough / it feels complete." → Not a stop condition. Keep going.
- "Further work is low-value / diminishing returns / would be padding." → Low-value real work still beats stopping; switch activity.
- "All tracked tasks (e.g. Tasks.md 12/12) are closed." → The list was a snapshot of *known* work; refill it (fresh bug-hunt, improve round, new tests) and continue.
- "The test suite / build / this milestone is the final gate." → There is no gate. The user's message is the only finish line.
- "I'll pace / conserve / do one round then stop." → The opposite of this mode; you work until interrupted.
- "The real next step needs the user (install, decide, test on hardware)." → Park that one step in a note and keep doing the abundant work that doesn't need them.
- "Every remaining item needs a user decision." → Park the decisions; keep working on what doesn't.
- "I'll keep going until there's no high-value work left (or you stop me)." → "No high-value work left" is NOT the stop condition; the user's message is. Don't phrase the loop-exit as anything else.

If you catch yourself writing any of these, delete the thought and start the next piece of work.

## How to actually run it

1. **Determine what to work on.** Usually it's the task in play (keep building/improving/hardening/testing it). If the invocation named something, do that. If there's genuinely no task in view, pick the highest-value thing on the rotation and start — don't stop to ask.
2. **Do bounded chunks of real work, back to back.** Finish a chunk, immediately start the next — a fix, a test, a feature, a hardening pass, a live test. No pause between chunks, no check-in.
3. **Leave things resumable.** Because the user can interrupt at any moment (that's the stop), keep the work in a state where the next message — theirs or a later `/continue` — picks up cleanly. Commit-worthy, coherent, no half-written file left broken.
4. **Optionally leave a light breadcrumb.** A running `PROGRESS.md` or short notes are fine as a *side effect* of working — never as the thing you do instead of working, and never as a wrap-up that signals a stop.
5. **When the user finally messages, that's the end.** Handle their new message as an ordinary request. Don't announce "ending work-till-message"; just answer them.

## Interaction with other skills

- **[[work-until-limit]] / [[work-until-time]]** — the same family, different stop conditions (quota / clock / user-message). If the user stacks them, the *first* condition to trip wins: e.g. "work-till-message but stop at 90% quota" ends at whichever comes first, the message or the ceiling. Absent a stacked bound, the only stop is the message.
- **[[shutdown-when-done]]** — only if the user explicitly pairs it, and be careful: "done" here means "the user came back," which is when they're *present*, so an automatic shutdown usually makes no sense. Don't infer it; honor it only if stated.
- **[[control]]** — the STOP button is a clean way for the user to end the run without typing a full message; treat a STOP as equivalent to the user coming back.

## Reality check

- **The stop is external and involuntary.** You cannot see the user's message coming; it arrives as an interruption. So there is no "watch for the stop and wrap up" — you just keep working, and the platform ends your turn when they send. Design every chunk to be safely interruptible.
- **This burns usage with no quota guard.** Unlike [[work-until-limit]], nothing here caps spend — the user chose an open-ended run. If they also care about quota, they'll stack a ceiling (see above); don't impose one yourself, and don't stop early to "save" budget (that's the banned conserve-budget rationalization).
- **Genuinely, truly nothing to do?** On a real project this essentially never happens. If you are *certain* no real, non-padding work remains anywhere before the user returns — vanishingly rare — do the most useful small hardening/testing/doc work you can find rather than ending the turn; a made-up stop is worse than low-glamour real work.
