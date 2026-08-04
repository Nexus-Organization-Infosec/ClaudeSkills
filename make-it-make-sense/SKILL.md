---
name: make-it-make-sense
description: Take something that's already implemented but done in a strange, awkward, or illogical way — a feature wired up oddly, a chat panel placed in the wrong spot, logic living in the wrong layer, a confusing flow or structure — and rework it so it actually makes sense. Understand the real intent, find what's off, and fix the placement/structure/flow so it's coherent and obvious, without breaking what works. Use whenever the user invokes /make-it-make-sense or says "this is implemented but it's weird", "it works but it's placed wrong", "this doesn't make sense, fix the structure", "why is this here, move it where it belongs", or "clean up how this is wired". Preserves behavior; fixes the sense.
---

# Make It Make Sense

Something is already built and (mostly) works, but it was done in a way that doesn't make sense — a chat panel dropped in the wrong part of the UI, a function living in the wrong module, business logic in the view layer, a flow that zig-zags for no reason, state kept somewhere strange. Your job: figure out what it was *meant* to be, spot what's awkward, and put it right — so the next person (or the user) looks at it and it's obvious, not baffling.

This is **coherence work**, not a rewrite and not a bug fix: the thing functions; it's the *arrangement* that's wrong.

## Step 1: Understand the real intent

Before moving anything, get what this is actually supposed to do and be:
- What is the feature/component for, from the user's point of view? Where would a reasonable person *expect* it to live and behave?
- Read how it's currently wired — where the code sits, what calls what, where state lives, how data flows in and out.
- Separate "works correctly" from "arranged sensibly." You're keeping the first and fixing the second.

## Step 2: Name what doesn't make sense

Be specific about the awkwardness — vague "it's messy" isn't actionable. Common shapes:
- **Wrong placement** — a component/panel/button in a spot that fights the user's mental model (the classic "chat is in the wrong place"); a file in the wrong folder; a route/screen nested oddly.
- **Wrong layer** — logic in the UI that belongs in a service; data access in a view; validation scattered instead of at the boundary.
- **Confusing flow** — steps in an unintuitive order, a round-trip that doesn't need to happen, a state machine that loops back on itself for no reason.
- **Naming/shape that lies** — a thing named for what it *was*, not what it *does*; a component doing three unrelated jobs; related things split apart, unrelated things jammed together.
- **Surprise** — anything where you had to stop and go "wait, why is it done like *that*?" That reaction is the signal.

List the concrete issues, worst-first (the ones that most confuse or most constrain future work).

## Step 3: Rework it into the sensible arrangement

Fix the arrangement so it matches the intent:
- **Move things where they belong** — the panel to where users expect it, the function to the right module, the logic to the right layer, the file to the right folder.
- **Straighten the flow** — remove the pointless round-trip, reorder steps to match how someone actually thinks about the task, collapse the needless indirection.
- **Fix names and boundaries** — rename to what it does now; split a component doing three jobs; group related things together.
- Do it **incrementally and behavior-preserving** — the feature must still work identically after each move. Rework the *arrangement*, not the *behavior* (unless the behavior itself is the thing that doesn't make sense, in which case confirm with the user first).

## Step 4: Verify nothing broke

Sense-making that breaks the feature is a net loss. After each move: run it, run the tests, exercise the real flow. Confirm the thing still does exactly what it did — just from its new, sensible home. If there's UI involved, actually look at it (drive it / screenshot) to confirm the placement is now right, not just different.

## Step 5: Report

Say what didn't make sense, what you moved/restructured and why it's clearer now, and that behavior is unchanged (verified). If you found something that's not just awkward but actually *wrong* (a real bug hiding behind the weirdness), flag it separately rather than silently changing behavior under the banner of "making sense."

## Notes

- Distinct from [[cleanup]] (broad tidy/reorganize of a whole codebase) — this is focused: one thing that's implemented strangely, made coherent. Distinct from [[fix]] (a bug) — here it works, it's just arranged wrong. If the right answer is "rebuild it properly from scratch," hand off to [[build-it-new]].
- Pairs with [[careful]] (minimal, behavior-preserving moves), [[test]] (prove nothing broke), and [[run]]/[[verify]] (confirm UI placement is actually right now).
