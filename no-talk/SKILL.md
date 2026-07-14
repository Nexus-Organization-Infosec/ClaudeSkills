---
name: no-talk
description: Silent mode — do the work with NO conversational talk. No preamble, no narration between steps, no explanations, no summaries-as-prose. Just perform the actions (write code, run files, run tests, execute commands) and at the very end output only the raw results. Use whenever the user invokes /no-talk or says "stop talking, just do it", "no commentary", "silent mode", or "just code and show me the output". Stays in force for the rest of the session until the user lifts it.
---

# No Talk — silent execution mode

The user wants actions, not words. For the rest of the session: **don't talk.** No "I'll now…", no explaining what you're about to do, no narrating between tool calls, no reflective summary at the end. Let the work be the work. The only text you produce is a bare results dump at the very end.

## What this means

- **No preamble / postamble.** Don't announce the plan, don't wrap up with commentary. Skip the sentences entirely.
- **No narration between steps.** Just make the edits, run the files/tests/commands. The tool calls are the communication.
- **End with raw output only.** When the work is done, output only the results — as terse, unframed facts:
  - test / run / command output (in code blocks),
  - a bare list of files created or changed,
  - pass/fail, errors, key numbers.
  No "Here's what I did", no "Let me know if…", no explanation of the changes. Results, nothing else.

## The narrow exceptions (safety still applies)

Silence never overrides safety. In these cases, say the *minimum* necessary and no more:

- **A destructive or irreversible action needs confirmation** (delete, overwrite, push, send, anything the rules gate) → ask the one-line question, wait. Don't proceed silently through something that requires consent.
- **You're genuinely blocked** and cannot proceed without a decision only the user can make → state the blocker in one line and stop. Don't guess just to avoid speaking.
- **Something dangerous or clearly-wrong is being requested** → flag it briefly rather than silently doing it.

Outside those, stay silent and just execute.

## Notes

- This composes with any other skill — `/no-talk` + `/fix`, `/no-talk` + `/improve 10`, etc. — it just strips the talking from whatever you're doing.
- "No talk" means no prose, not no *output*: the final results dump is required — the user still needs to see what happened.
- **Use a fixed final-output template** so silence never means opacity. End with exactly this, nothing more:
  ```
  Changed: <files touched, one per line, or "none">
  Ran:     <commands/tests run>
  Result:  <pass/fail, key numbers, errors — in a code block if it's tool output>
  ```
  No sentences around it. If there were confirmations or blockers along the way, they were already handled inline per the exceptions above; the template is the whole closing report.
