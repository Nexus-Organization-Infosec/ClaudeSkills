---
name: improve-performance
description: Make the app or code measurably faster — UI responsiveness and jank, startup time, request latency, throughput, memory. Profile first to find the real bottleneck, fix the biggest one, then prove the gain with before and after numbers. Use whenever the user invokes /improve-performance or says "make it faster", "the UI is laggy/janky", "optimize this", "it takes too long to load", "reduce latency", "it uses too much memory", or "improve performance". Measurement driven, never guesswork.
---

# Improve Performance

Performance work is measurement work. The single most reliable fact about optimization is that **the bottleneck is almost never where you think it is** — so the whole discipline here is: measure, fix the biggest thing, measure again, keep it only if the number actually moved.

## Rule zero: never optimize on a hunch

Do not touch a line of code until you have data showing where the time actually goes. Guessed optimizations usually make the code uglier, sometimes make it slower, and almost always target the wrong thing. If you find yourself saying "this loop looks slow," stop and profile it.

## Step 1: Define "slow" and get a baseline number

Optimizing without a metric is unfalsifiable. Pin down:
- **Which metric matters here?** Startup time, frame time / jank, request latency (p50 vs p95), throughput, memory, battery.
- **The baseline**, measured now, as a real number ("cold start 3.4s", "list scroll drops to 38fps", "endpoint p95 820ms").
- **The target**, if the user has one ("under 16ms per frame", "sub second").

Write the baseline down. Everything is judged against it.

## Step 2: Profile to find the real bottleneck

Use the profiler for the stack, not intuition:
- **Python:** `cProfile` (+ `snakeviz`/`pstats`) for a call breakdown, `py-spy` for a live/sampling look at a running process, `timeit` for micro comparisons, `line_profiler` for a hot function.
- **Flutter / Dart:** run in **profile mode** (`flutter run --profile`) and use DevTools' performance/timeline view and the frame chart. **Never judge performance in debug mode** — debug builds are misleadingly slow and will send you chasing ghosts.
- **Web / JS:** Chrome DevTools Performance panel, Lighthouse for page load.
- **Database:** `EXPLAIN`/query plans and slow query logs.

Find the top few time sinks and their share of total time. **Amdahl's law is the filter:** something that is 3% of runtime can give you at most a 3% win, no matter how brilliantly you optimize it. Go where the time actually is.

## Step 3: Fix the biggest bottleneck first

Match the fix to what the profile showed.

### UI responsiveness and jank
- **The budget is ~16ms per frame** for 60fps (about 8ms at 120Hz). Anything heavy on the UI/main thread blows it and shows as stutter.
- **Get heavy work off the main thread** — isolates (Dart), workers (JS), threads/async (Python). Parsing, crypto, image decode, and big JSON belong off it.
- **Virtualize long lists.** Build only visible items (`ListView.builder`, windowing). Never build a 10k-item list eagerly.
- **Narrow the rebuilds.** Don't rebuild a big tree for a small state change: `const` constructors, keys, selective/scoped state, `RepaintBoundary` around expensive static subtrees.
- **Debounce/throttle** high-frequency events (scroll, resize, text input, search-as-you-type).
- **Size and cache images.** Decode at display size, not full resolution; cache decoded results. Oversized bitmaps are a classic jank and memory killer.

### Algorithmic (usually the biggest single win)
- Accidental O(n²): nested loops, repeated linear scans, `in` on a list inside a loop. Swap to a `dict`/`set`, sort once, or index it.
- **Cache/memoize** repeated identical work. Recomputing the same derived value every tick is a common hot spot.
- Vectorize per-row loops where the stack supports it (numpy/pandas rather than Python-level iteration).

### I/O, network, and database
- **N+1 queries** → batch or join. **Missing index** → add it (check the query plan).
- **Parallelize independent I/O** instead of awaiting serially.
- Batch and cache network calls; avoid refetching unchanged data.

### Memory
- Leaks, unbounded caches/queues/lists, and allocation churn that drives GC pressure. Memory problems often show up as *speed* problems.

### Startup
- Defer non-critical init, lazy-load modules and screens, move work out of the critical path to first paint.

## Step 4: Prove it, or revert it

- **Re-run the exact same measurement** and compare against the baseline. Same conditions, same input, profile mode not debug.
- **Report the real numbers**: "cold start 3.4s → 1.9s", "p95 820ms → 210ms", "scroll now holds 60fps".
- **If the number didn't move, revert the change.** An optimization that doesn't measurably help is churn, and it usually cost you readability.
- **Run the tests.** A faster wrong answer is worthless. Correctness is not negotiable for speed.

## Step 5: Report

Say what the bottleneck actually was, what you changed, the before → after numbers, and what's still slow (with the next biggest bottleneck named). Be honest if a fix gave less than hoped.

## What not to do

- Don't micro-optimize cold code. Shaving a loop that's 1% of runtime is wasted effort.
- Don't profile in debug mode (especially Flutter) and don't benchmark on a cold cache once and call it data.
- Don't trade real clarity for a tiny gain. A 3% win that makes the code unreadable is a bad trade.
- Don't stack five changes then measure. Change one thing, measure, keep or revert. Otherwise you can't tell what helped.
- Don't break behavior in the name of speed.

## Notes

Pairs with `/improve` (same measure-keep-or-revert discipline, applied broadly), `/bug-hunt` (perf problems and bugs often share a root), and `/careful`. For a UI-specific rebuild, `/flutter-design` covers the Material side.
