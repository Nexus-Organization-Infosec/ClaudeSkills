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

## The quality bar

- **Complete beats numerous.** Hitting N with junk is failure. A "feature" that is a settings toggle wired to nothing is not a feature.
- **Fits beats clever.** Do not bolt unrelated things onto the app to pad the count. A note taking app does not need a crypto ticker.
- **Working beats demoed.** If you cannot exercise it, you are not done.
- If you genuinely cannot find N features worth building for this project, build the good ones and say plainly how many were real, rather than inventing filler. On most real apps there is plenty left, so look properly before concluding that.

## Notes

Pairs with [[map]] (track the N as a checklist), [[later-ideas]] (source of pre-vetted ideas), [[improve]] (polish afterwards), [[control]] (STOP button on a long build), and [[work-until-limit]]. Under `work-until-limit`, building features is exactly the kind of real work to switch to when other activities run dry.
