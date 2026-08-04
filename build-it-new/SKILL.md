---
name: build-it-new
description: Rebuild an existing thing from scratch — same purpose, but better and self-made. Instead of patching the current (often messy or oddly-built) implementation, throw out the approach and build a clean, superior version yourself from a fresh design. Use whenever the user invokes /build-it-new or says "rebuild this but better", "do it again properly from scratch", "make your own better version of this", "scrap it and build it right", or "same thing, self-made and improved". Combines a fresh from-scratch build with a deliberate step up in quality over what exists.
---

# Build It New

Take something that already exists — a feature, a component, a tool, a messy implementation — and **rebuild it fresh: same purpose, better result, made by you.** This is not patching the current version; it's deciding the current approach isn't worth saving and building the right thing from a clean slate. Two commitments at once: **from scratch** (yours, not a wrapper — see [[selfmade]]) and **better** (a real improvement over what's there, not a sideways rewrite).

## Step 1: Understand what exists and why it falls short

You can't beat something you don't understand:
- **What does the current thing do?** Capture its real purpose and the behavior worth keeping — the requirements, not the implementation. What must the new version still do?
- **Why is it worth rebuilding?** Name the concrete failings of the current one: messy/awkward structure, poor performance, unmaintainable, wrong abstractions, leans on something you want gone, or just built strangely. This list becomes your "do better" checklist.
- **Salvage the requirements, discard the approach.** Keep what it's *for*; feel free to throw away *how* it currently does it.

## Step 2: Design the better version yourself

Design as if the old code (and the library you'd normally reach for) didn't exist:
- Choose the data structures, boundaries, and flow you'd pick knowing what you know now.
- Fix, in the design, every failing you listed in Step 1 — better structure, better performance, cleaner abstractions, sensible placement.
- Decide the scope of "self-made": per [[selfmade]], implement the core yourself; use standard primitives for plumbing unless the user wants truly zero-dependency.

## Step 3: Build it for real, better than before

- Implement the new version from scratch, completely — no stubs, no faking the hard parts (pair with [[full-implement]] for production-grade depth and [[selfmade]] for the from-scratch discipline).
- Hold it to a higher bar than the original on the axes that matter: correctness, clarity, performance, robustness, and how sensible it is to work with.
- Build incrementally and keep it runnable; don't disappear into a giant rewrite with nothing working for a long stretch.

## Step 4: Prove it's actually better

"New" is worthless if it isn't better. Show it:
- **Same behavior where it should match** — the new version meets the salvaged requirements. Test it ([[test]]); exercise the real flow.
- **Better where you claimed** — if you rebuilt for speed, show before/after numbers ([[improve-performance]]); if for clarity/structure, point to the concrete improvement; if for correctness, show the edge cases it now handles that the old one didn't.
- Don't ship the new one as a regression. If it's not genuinely better on the axes that mattered, keep working or say so honestly.

## Step 5: Swap and clean up

- Wire the new version in, migrate what needs migrating, and remove the old implementation once the new one is proven (back it up first if it's significant — [[backup]]).
- Report: what you rebuilt, why the old one fell short, how the new one is better (with evidence), and that it's verified working.

## Notes

- The trio: [[selfmade]] = the from-scratch discipline (implement cores yourself); [[build-it-new]] = rebuild an *existing* thing self-made *and* better; [[make-it-make-sense]] = keep the implementation but fix its strange arrangement. Reach for make-it-make-sense when the code is salvageable-but-awkward; reach for build-it-new when it's better to start over.
- Pairs with [[full-implement]], [[improve-performance]], [[test]], and [[backup]] (snapshot the old version before replacing it).
