---
name: smoothener
description: Make a UI feel smooth and alive by adding tasteful animations, transitions, micro interactions, and visual polish. Covers timing and easing, press feedback, loading skeletons, screen and list transitions, plus the performance and reduced motion rules that keep it from backfiring. Use whenever the user invokes /smoothener or says "add animations", "make it feel smoother", "polish the UI", "it feels static or cheap", "add transitions", or "make it look nicer". Motion that communicates, never decoration for its own sake.
---

# Smoothener

Make the interface feel smooth, responsive, and alive. The difference between an app that feels cheap and one that feels premium is mostly motion and consistency, not new features.

## The principle: motion has a job

Every animation should answer one question: **what is this telling the user?** Where something came from, that a tap registered, that state changed, that content is loading, that two screens are related. Motion that only decorates is noise, it ages badly, and it slows people down. If you cannot say what an animation communicates, do not add it.

## Timing and easing

Get these two right and it already feels good, before anything clever:

- **Duration.** Small and local (a button, a toggle, a fade): 150 to 200ms. Medium (a card, a sheet, expand and collapse): 250 to 300ms. Large (page transitions): 300 to 400ms. Past roughly 400ms it stops feeling responsive and starts feeling sluggish. When unsure, go shorter.
- **Never linear.** Real things accelerate and settle. Use ease out for things entering (fast in, gentle settle), ease in for things leaving, ease in out for things moving between two points. Material 3 emphasized curves are good for hero moments.
- **Be consistent.** Define your durations and curves once as tokens and reuse them everywhere. Ad hoc numbers scattered across widgets is exactly why an app feels incoherent even when each screen looks fine.

## Where motion actually pays off

Highest value first:

- **Press feedback.** Ripple, or a small scale down on tap. Instant, so the tap feels registered. This one matters most and costs the least.
- **State and content changes.** Cross fade instead of a hard swap (`AnimatedSwitcher`). Values that change should tween, not jump.
- **Loading.** A skeleton or shimmer beats a bare spinner, and keeps layout stable so nothing jumps when content lands. Layout jump is the cheapest thing to fix and the most jarring to leave.
- **Screen transitions.** `Hero` for a shared element between screens, so the user tracks the object instead of getting teleported. One consistent page transition everywhere.
- **Lists.** A subtle staggered entrance on first load. Do not re animate on every scroll, that is nausea.
- **Expand and collapse.** `AnimatedSize` / `AnimatedContainer` so the layout grows rather than snapping.
- **Empty and error states.** A gentle entrance makes them feel intentional rather than broken.

## Smooth means 60fps, or it is not smooth

A janky animation is worse than no animation. It reads as broken.

- **The budget is ~16ms per frame** (about 8ms at 120Hz). Blow it and the user sees stutter.
- **Animate cheap properties:** opacity and transform/scale. Avoid animating things that force layout or rebuild a big tree every frame.
- **Flutter specifics:** reach for implicit animations first (`AnimatedContainer`, `AnimatedOpacity`, `AnimatedSwitcher`, `AnimatedAlign`) since they are cheap to write and hard to get wrong. For explicit control use `AnimationController` with `AnimatedBuilder` and a narrow `child`, so you rebuild only the animated part. Wrap expensive animated subtrees in `RepaintBoundary`. Never `setState` a whole page per frame.
- **Verify in profile mode, not debug** (debug is misleadingly slow). See [[improve-performance]] for the profiling flow.

## Reduced motion is not optional

Some people disable animations because motion makes them physically ill (vestibular disorders). Honor the OS setting:

- **Flutter:** check `MediaQuery.of(context).disableAnimations` (and `accessibleNavigation`) and fall back to instant or a minimal fade.
- **Web:** `@media (prefers-reduced-motion: reduce)`.

Never ship motion that ignores this. It is a real accessibility requirement, not a nicety.

## Restraint

- **Not everything needs to animate.** If everything moves, nothing stands out and the app feels busy.
- **Go easy on bounce and overshoot.** Fun for one demo, tiring by day two.
- **Motion must never delay the user.** If an animation stands between someone and their action, it is too long or should not exist.

## The visual polish part

Beyond motion, "feels designed" usually comes from consistency, not decoration:

- Spacing on one grid (8dp), consistent corner radii, elevation and shadow from the theme rather than hand picked per widget.
- Animate theme and selection color changes too, so switching modes glides instead of blinking.
- Keep it inside the design system. For Flutter Material 3 specifically, see [[flutter-design]].

## Verify

Motion is judged by eye. Run the app and watch it, in both light and dark, and check the frame chart in profile mode for jank. If you cannot see it running, you cannot claim it is smooth.
