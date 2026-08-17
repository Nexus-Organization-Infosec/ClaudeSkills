---
name: improve-design
description: Smooth down the visual design and motion of an existing UI — refine the animations, transitions, easing, timing, spacing, alignment, color, typography, elevation, and micro-interactions so the whole thing feels polished, fluid, and calm instead of janky, abrupt, or default. Works on what already exists: it does not redesign from scratch, it takes the current UI and makes it feel better. Covers HTML/CSS/JS web UI, Flutter (Android/iOS/desktop), Python GUIs (Tkinter/CustomTkinter, PyQt/PySide, Kivy), C++ UI (Qt/QML, Dear ImGui, JUCE, native), and React/React Native/other component UI. Invoked as "improve-design" for one polish round, or "improve-design N" (e.g. "improve-design 10") for N rounds, each smoothing a different rough spot. Use whenever the user invokes /improve-design or says "smooth out the design", "make the animations smoother", "polish the UI", "the transitions feel janky/abrupt/laggy", "make it feel more fluid / premium / high-quality", "fix the easing/timing", "clean up the spacing and alignment", "make the motion feel nicer", "add subtle animations", "make it look less default", "improve the look and feel", "make the UI buttery / snappy / refined", or "the app feels stiff/cheap". Keywords: animation, transition, easing, curve, spring, timing, duration, motion, micro-interaction, hover, ripple, fade, slide, morph, stagger, parallax, scroll, gesture, feedback, polish, smooth, fluid, buttery, snappy, refined, premium, jank, stutter, frame drop, 60fps/120fps, spacing, padding, margin, alignment, rhythm, hierarchy, typography, kerning, line-height, color, contrast, palette, gradient, shadow, elevation, depth, corner radius, border, focus state, hover state, pressed state, disabled state, loading state, skeleton, shimmer, empty state, layout shift, responsiveness. Frameworks: HTML, CSS, JS, Tailwind, React, React Native, Flutter, Dart, Python, Tkinter, CustomTkinter, PyQt, PySide, Kivy, C++, Qt, QML, Dear ImGui, JUCE. Pairs with [[improve]] (measured general improvement), [[flutter-design]] (Material 3 from scratch), and [[improve-performance]] (which fixes the jank underneath the motion).
---

# Improve Design — smooth down the look and feel

Take a UI that already works and make it *feel* good: fluid motion, calm timing, clean spacing, coherent color and type, and micro-interactions that respond the way a person expects. The bar is "this feels considered and premium," not "this technically renders." You are refining what's there, not redesigning it.

## What this is — and isn't

- **This polishes the existing UI.** Same screens, same layout intent, same features — made to feel smoother. If the user wants a from-scratch redesign, that's a different job (for Flutter specifically, [[flutter-design]] builds fresh Material 3).
- **Feel is the deliverable.** The win is the UI feeling fluid, quiet, and intentional. Abrupt jumps become eased transitions; cramped or ragged spacing becomes rhythmic; harsh or muddy color becomes balanced; a dead button gains a hover/press response.
- **Restraint is the whole craft.** Good motion is *felt, not noticed*. The failure mode of a "smooth it out" pass is the opposite of stiff — it's a UI that now bounces, spins, parallaxes, and fades on everything until it feels like a toy. Every animation must earn its place by guiding attention or confirming an action. When in doubt, less motion, shorter duration, subtler easing.

## Invocation

- **`improve-design`** → one polish round: find the roughest, most-seen spot and smooth it.
- **`improve-design N`** (e.g. `improve-design 10`) → N rounds, each taking the next-roughest spot. Rotate across the palette below so it doesn't over-polish one screen while others stay stiff.

## Step 1: See it before you touch it

You cannot smooth what you haven't watched move. Design is visual, so look, don't guess:

- **Run it / view it.** Launch the app or open the page and actually watch the interactions — the transition between screens, the button press, the list scroll, the menu open, the loading state. Use the browser preview for web; run the app for Flutter/Python/C++. A screenshot shows layout; only running shows *motion*.
- **Name the specific roughness.** Not "it feels off" — "the modal pops in with no transition", "the hover has no feedback", "the page-change is an instant jump", "the list items all animate at once and it flickers", "the spacing between cards is inconsistent (12/16/9px)", "the primary and heading share the same weight so there's no hierarchy". A precise defect is a fixable defect.
- **Check the frame rate where motion already exists.** If an existing animation stutters, that's often not a design problem but a performance one (layout thrash, animating an expensive property, work on the UI thread) — hand that part to [[improve-performance]]; smoothing the *curve* won't fix dropped frames.

## Step 2: The polish palette — what "smooth" is made of

Work these dimensions. Each round, pick the one that buys the most felt improvement for the spot you're on.

### Motion — the big one
- **Never animate from nothing to done in one jump.** State changes (open/close, show/hide, add/remove, navigate) get a transition. An element that appears should fade/scale/slide in, not blink into existence.
- **Easing, not linear.** Linear motion feels mechanical. Use ease-out for things entering/responding to the user (fast start, gentle settle — feels responsive), ease-in for things leaving, and ease-in-out for moves between two on-screen states. Reserve spring/overshoot for playful, physical interactions — not for everything.
- **Duration is short.** Most UI transitions live in **150–300ms**. Under ~100ms reads as instant (no smoothing gained); over ~400ms feels sluggish and makes the app feel slow. Enters can be a touch longer than exits.
- **Stagger lists, don't flash them.** When several items appear together, offset each by ~20–40ms so they cascade instead of popping as a block. Cap the total so a long list doesn't crawl.
- **Interruptible and reversible.** A menu closed mid-open should reverse from where it is, not jump to fully-open then close. Animate the property continuously rather than firing fire-and-forget tweens.
- **Respect reduced-motion.** Honor the OS/browser "reduce motion" preference — drop or shorten animations when it's set. This is correctness, not optional.

### Micro-interactions — make it respond
- Every interactive element earns **hover / focus / pressed / disabled** states with a quick transition between them (background, elevation, scale ~0.97 on press). A control that looks identical whether or not you're touching it feels dead.
- Confirm actions: a subtle ripple/flash/checkmark on success, a gentle shake on error. Feedback closes the loop.
- Loading isn't a frozen screen: skeletons/shimmer for content, a spinner or progress for actions, an optimistic update where safe.

### Space, rhythm, hierarchy
- **Spacing on a scale.** Snap paddings/margins/gaps to a consistent scale (4/8/12/16/24/32…) instead of ad-hoc 9/13/17px values. Consistent rhythm is most of what "clean" means.
- **Alignment.** Edges line up; related things share a baseline/grid; optical centering where math-centering looks off.
- **Hierarchy.** Size, weight, and color should make the eye land on the primary thing first. If everything is bold, nothing is.

### Color, type, depth
- **Restrained palette.** One or two accents, a neutral range, consistent semantic colors (success/warn/error). Check contrast for legibility.
- **Type scale.** A small set of sizes/weights with comfortable line-height (~1.4–1.6 body) and sane line length; don't mix five font sizes at random.
- **Depth with intent.** Soft, consistent shadows/elevation to separate layers — one light source, not a shadow on everything. Corner radii consistent across the UI.

## Step 3: Per-platform — how to actually implement the smoothing

The principles are universal; the mechanism differs. Match the framework's idiom, and prefer the platform's cheap-to-animate properties (transform/opacity almost everywhere) over expensive relayouts.

- **HTML / CSS / JS** — `transition` and `@keyframes` for the common cases; animate `transform` and `opacity` (GPU-friendly), not `width`/`top`/`margin` (layout thrash). `cubic-bezier()` for custom easing; `@media (prefers-reduced-motion: reduce)` to honor the setting. Reach for the Web Animations API or a library (Framer Motion in React, GSAP, Motion One) only when CSS can't express it. `scroll-behavior: smooth`, `:hover`/`:focus-visible`/`:active` states, `will-change` sparingly.
- **Flutter / Dart** — `AnimatedContainer`, `AnimatedOpacity`, `AnimatedSwitcher`, and the `Animated*` family for implicit animations; `Hero` for shared-element screen transitions; `PageRouteBuilder` for custom route transitions; `Curves.easeOut`/`easeInOut`/`Curves.easeOutCubic` and springs via `CurvedAnimation`/`SpringSimulation`. `InkWell`/`InkResponse` for ripples, `AnimationController` for orchestrated/staggered motion, `flutter_animate` for terse choreography. Keep animations off the build hot path; use `RepaintBoundary` for isolated animated widgets. (For a from-scratch Material look, use [[flutter-design]].)
- **Python — Tkinter / CustomTkinter** — no built-in animation engine, so tween by hand: an `after(16, ...)` loop stepping a value through an easing function (~60fps), animating geometry/color/alpha. CustomTkinter gives smoother widgets, rounded corners, hover states, and theming out of the box; use its `configure()` in the tween. Keep the loop light and cancel it on teardown.
- **Python — PyQt / PySide** — `QPropertyAnimation` / `QVariantAnimation` with `QEasingCurve` (`OutCubic`, `InOutQuad`), `QParallelAnimationGroup` / `QSequentialAnimationGroup` for orchestration, `QGraphicsOpacityEffect` for fades, `QStateMachine` for state transitions. Style with QSS (`:hover`/`:pressed`/`:disabled`).
- **Python — Kivy** — the `Animation` class with `transition='out_cubic'`, `+` and `&` to sequence/parallel, animating widget `pos`/`size`/`opacity`; the built-in easing set covers most needs.
- **C++ — Qt / QML** — QML is the smooth path: `Behavior on <prop>`, `NumberAnimation`/`PropertyAnimation` with `easing.type: Easing.OutCubic`, `Transition`s on `State`s, `SpringAnimation`, and `Item` `states`/`transitions`. Widget Qt uses the same `QPropertyAnimation`/`QEasingCurve` as PySide.
- **C++ — Dear ImGui** — immediate-mode has no retained animation, so drive it yourself: keep per-widget animated floats, lerp them toward the target each frame using `ImGui::GetIO().DeltaTime` and an easing function, and feed the eased value into colors/positions/alpha. Smooth hover with a `t` that eases toward 1 while hovered and back toward 0 when not.
- **C++ — JUCE / native** — JUCE `Component::animator`/`ComponentAnimator` and `Timer`-driven lerps; for other native toolkits, a timer/`requestAnimationFrame`-equivalent stepping an eased value.
- **React / React Native** — Framer Motion (`motion`, `AnimatePresence`, layout animations) or React Native Reanimated (`useSharedValue`, `withTiming`/`withSpring`, `Layout` transitions) running motion on the UI thread; `LayoutAnimation` for the simple cases. Same easing/duration rules as everywhere else.

## Step 4: Prove it's actually smoother, keep what wins

This is an `/improve`-family skill, so the discipline holds: a change only counts if it's genuinely better, and "better" here is *felt fluidity*, not lines of animation code added.

- **Watch it again, before and after.** Run the same interaction and confirm it now feels smoother, not just different. If you can capture a quick before/after (screenshot the states, or note the visible behavior change), do.
- **Check the frame rate didn't drop.** A "smoother"-looking animation that stutters at 30fps is worse than the instant version. If your new motion janks, either simplify it (animate transform/opacity only) or hand the underlying cost to [[improve-performance]]. Smooth *design* on a janky *frame budget* is not smooth.
- **Revert overshoot.** If a round made the UI busier, bouncier, or slower-feeling rather than calmer, undo it. Motion that draws attention to itself failed. Keep only the changes that make the thing feel more considered.
- **Don't break behavior.** Polish is cosmetic-plus-motion; it must not change what buttons do, what data shows, or how the app functions. Re-check the interaction still works, not just that it looks nicer.

## Ground rules

- **Refine, don't rebuild.** Keep the existing structure and intent; change how it feels, not what it is.
- **Consistency beats cleverness.** One easing curve, one duration scale, one spacing scale, one shadow language used *everywhere* reads as far more premium than five different flashy effects. Define the tokens once and reuse them.
- **Subtle wins.** If a reviewer would say "nice animation," it's probably too much; the goal is they feel the app is nice without being able to point at why.
- **Honor reduced-motion and accessibility.** Smoother must never mean less usable — keep contrast, focus states, hit targets, and the reduce-motion setting intact.
- **Match the round count to real roughness.** If the UI is already smooth, say so and stop rather than manufacturing motion for its own sake (unless running under a work-until-limit-style directive, where you switch to the next real polish target instead of padding one).
