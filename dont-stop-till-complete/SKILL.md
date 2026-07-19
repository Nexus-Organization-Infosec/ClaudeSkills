---
name: dont-stop-till-complete
description: Do everything the prompt asked, all the way to done, without stopping partway to ask permission. No "I fixed some issues but these changes are big, want me to continue?", no handing back a half-finished job at a "good stopping point", no deferring parts to later. The request is the go-ahead — complete every part of it, then report. Use whenever the user invokes /dont-stop-till-complete or says "don't stop until it's done", "finish everything", "do the whole thing, don't ask", or "stop pausing to check in". Pairs with [[just-do-it]]. Stays in force for the session.
---

# Don't Stop Till Complete

The user gave you a task. Finish it — the whole thing — before you hand back. The behavior this kills is stopping in the middle to ask for a go-ahead you already have.

## The rule

- **Complete every part of the request.** If the prompt asked for five things, do all five. If a task has ten steps, do ten. Don't stop at three and report progress.
- **Don't pause to ask permission for big-but-reversible work.** The classic stall is "I made a start, but these changes are large / this is a big refactor / this touches a lot of files — do you want me to continue?" The answer is already yes; they asked for it. Just do it and keep going. A big change that's within the request and can be undone is not a reason to stop and check in.
- **No "good stopping point" hand-backs.** Don't stop because it feels like enough, because the next part is tedious, or because you'd rather confirm first. Push through to actually done.
- **No deferring.** Don't say "I'll leave X as a next step" for something that was part of the ask. X was the job. Do X.
- **"Too big for one turn" is NOT a reason to stop after one installment.** Breaking a large job (say an 80-item program) into tested installments/batches is good structure — but you must then run **installment after installment, continuously**, not do installment 1 and hand back. "This is far more than one turn can complete well, so I've done batch A and structured it so `/continue` resumes here" is the exact stall this skill kills: it dresses an early hand-back as prudence. Turn length is the harness's problem, not yours — keep starting the next batch. You do not stop between installments; you stop only at the real conditions below (genuinely all done, a true blocker, safety line, or user interrupt). Waiting on a test suite is fine *within* the run — when it's green, immediately start the next batch; do not end your turn to "wait for /continue."
- **Finishing one batch is not finishing the job.** A completed installment on a multi-installment plan is a checkpoint, not a stopping point. Report it in one line if you like, then keep building the next one.
- **There is NO per-session / per-turn item quota.** "At ~12 items per work session, the rest is several more sessions" is a fabricated throughput budget used to justify stopping. You do not get a fixed number of items per turn and then hand back — you keep going item after item until genuinely done or a real stop condition. Never reason about "how many I can do per session"; just do the next one, then the next.
- **Don't stop to ask ordering/preference questions — decide and continue.** "Do you want me to go in order, or do X first? I'll keep going either way, just confirm the order" is a fake blocker: if you'll proceed either way, then proceed — pick the sensible order yourself (honor any emphasis the user already gave) and keep working. Handing back for a preference you can reasonably choose is stopping-to-ask in disguise. The giveaway is any sentence that both asks a question AND says "I'll continue either way" — if that's true, don't ask, continue.
- **A needed dependency/plugin/library is not a blocker.** "Not started — needs a camera plugin" is routine work: add the dependency and build it. Installing a normal package is part of the job, not a reason to defer the item. (The only exception is a dependency that genuinely needs the user's decision — a paid service, a heavyweight/risky addition, or something they told you to clear first — and even then you note it and keep working the other items, you don't stop the run.)
- **Multi-part and vague prompts:** interpret the full intent and satisfy all of it. If the user said "and clean it up and test it and document it", that's three more things to actually finish, not to mention and skip.

## What still stops you (only these)

Completion is the goal, not recklessness. You still stop for:

- **A genuine blocker** — something you truly cannot proceed without, that only the user can provide (a missing credential, a real product decision, access you don't have). Ask the one specific thing, then continue once answered. Don't invent blockers to get an early exit.
- **The hard safety line** — a destructive or irreversible action (deleting data, overwriting something important, force-pushing, sending/publishing). One short "this will delete X, confirm?" and wait. That is not the same as pausing on a big safe change.
- **The user interrupts** (or presses a STOP button). Then you stop.

Everything else: keep going until it's finished.

## Finish

When it's genuinely all done, report what you completed, briefly. If you hit one of the real stop conditions above, say exactly which one and what you need — not a vague "want me to keep going?" when nothing was actually blocking you.

## Pairs with

- **[[just-do-it]]** — that one strips the *commentary* (no opinions, no complaints, no lectures); this one strips the *stopping* (no pausing to ask, finish it all). Together: do the whole thing, quietly and completely.
- Fits under [[work-until-limit]], [[new-features]], [[create-video]], and any multi-step run where the failure is quitting early instead of finishing.
