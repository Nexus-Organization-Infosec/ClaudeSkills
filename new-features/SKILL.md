---
name: new-features
description: Build new features into the project, as many as asked for. Invoked as "new-features" for one, or "new-features N" for N of them (e.g. "new-features 10" builds ten). Each one is picked to genuinely fit the project, built complete and working (never a stub), verified, and checked against breaking what already exists. Use whenever the user invokes /new-features (or /new-feautures), or says "add some features", "build N new things", "what else could this app do", or "add more functionality". The feature building counterpart to [[improve]], which polishes what already exists.
---

# New Features

Add real, working features to the project. `/improve` makes existing things better; this makes new things exist. The bar is the same though: **a feature counts only when it actually works end to end.** Ten half built features are worth less than three real ones.

## How many

- **`new-features`** (no number) → **one** feature.
- **`new-features N`** → **N** features (e.g. `new-features 10` → ten).

If there is no project in play, ask what to build for first.

## Step 1: Gather candidates

Do not invent features in a vacuum. Look at what the project actually is and where its gaps are:

- **The backlog first.** If `LATER_IDEAS.md` exists (from [[later-ideas]]), read it. Ideas whose "ready when" is now met are the best candidates, because the user already wanted them.
- **Obvious missing basics.** What would a user of this app immediately expect that is not there? Missing basics beat clever extras every time.
- **TODOs and comments** in the code that describe intended-but-unbuilt behavior.
- **Pain points.** Anything clunky that a feature would smooth out.
- **The domain.** What comparable apps have that this lacks and would fit here.

## Step 2: Pick the N, and say what they are

Choose the N highest value ones that genuinely **fit this project**, ordered best first. State the list up front, one short line each, so the user can see where you are going and redirect you cheaply if a pick is wrong.

Do not block waiting for approval on a normal run, just proceed after stating them. Exception: if a feature would be destructive, irreversible, or needs a product decision only the user can make (pricing, data retention, a policy choice), flag that one and ask instead of guessing.

## Step 3: Build each one, properly

For every feature, in order:

1. **Design it briefly.** What it does, where it hooks in, what the user sees. A few sentences, not a document.
2. **Build it completely.** Real working code, wired into the app. **No stubs, no TODOs, no "simulated for now", no dead code nobody calls.** If it has UI, the UI works. If it needs persistence, it persists. A feature that only half exists is a bug you added on purpose (see [[placeholder-replacer]]).
3. **Match the project.** Follow the existing patterns, naming, style, and architecture. A feature that looks foreign is a maintenance problem.
4. **Verify it works.** Actually exercise it, do not assume. Run the app or the path, or add a test that covers it.
5. **Do not break what exists.** Run the test suite after each feature and confirm still green before starting the next. Fix a regression immediately, do not stack it.
6. **Log it** in one line (what you built, that it is verified) so the trail is visible.

Keep the project in a working, runnable state between features. If a feature turns out much bigger than expected, say so rather than shipping a rushed shell of it.

## Step 4: Report

List what shipped, one line each, with a note that each is verified working. Then state honestly:
- anything you flagged instead of building, and why (needs a decision, too big, risky),
- anything that turned out shallower than intended.

## Deliver N — refusing is almost always under-looking

`new-features N` means **build N features.** The default, overwhelmingly, is that you deliver N. On any real app there is a deep well of features that genuinely fit — look at the domain, at what comparable apps have, at what users expect, at the [[later-ideas]] backlog, at the obvious missing basics. A chat app alone has dozens of natural features. If you think there aren't N worth building, you almost certainly didn't look hard enough. Look again before concluding otherwise.

**This is NOT `/improve`, and the "no manufactured churn" rule does not govern it.** That rule is about not making pointless *edits* to hit a round count. Here the user asked for *features*, and the bar is simply "does it fit the app and does it work" — not "is it a huge improvement." Do not cite churn-avoidance as a reason to build fewer than N. Finding features that fit is the job, and it's almost always doable.

**Bug fixes, refactors, and reliability work are NOT features.** A feature is new user-facing functionality that wasn't there before. Fixing an offline banner, a lockout, or a flaky check is valuable, but it does **not** count toward `new-features N`. If the user asked for 5 features, doing 5 bug fixes and reporting "done" is not delivering what they asked. Those belong to [[fix]] or [[bug-hunt]]; build the actual features here.

### The quality bar (once you're building the right things)

- **Complete beats numerous.** Hitting N with junk is failure. A "feature" that is a settings toggle wired to nothing is not a feature.
- **Fits beats clever.** Don't bolt genuinely unrelated things on to pad the count. A note-taking app does not need a crypto ticker. But "it must *fit*" is a filter on *which* features, not an excuse to build none — there are always fitting ones.
- **Working beats demoed.** If you cannot exercise it, you are not done.

### The one honest exception

If, after looking hard, you truly believe fewer than N features genuinely fit, do NOT silently build fewer and move on. Instead: build the ones you're confident in, then **list concrete candidate features for the rest and ask the user which they want** (or propose your best picks). Hand the decision back with real options, rather than deciding for them that the app is "done enough." Declining to build without offering alternatives is the failure this note exists to prevent.

## Notes

Pairs with [[map]] (track the N as a checklist), [[later-ideas]] (source of pre-vetted ideas), [[improve]] (polish afterwards), [[control]] (STOP button on a long build), and [[work-until-limit]]. Under `work-until-limit`, building features is exactly the kind of real work to switch to when other activities run dry.
