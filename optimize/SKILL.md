---
name: optimize
description: Make software or firmware measurably faster, smaller, or more memory-efficient the way serious system programmers always have — profile the real workload, find where the time or bytes actually go, make the fix with the biggest payoff, measure again, keep only the wins. Covers runtime (hot path), memory (RAM / heap / stack), size (binary / flash), startup time, and energy. Use whenever the user invokes /optimize or says "make this faster", "make this smaller", "cut the RAM usage", "optimize this firmware", "reduce the binary size", "speed up the startup", "profile this and improve", or "the way they optimized Linux back in the day". Invoked as "optimize" for one full pass, or "optimize N" (e.g. "optimize 5") to run N successive measured rounds.
---

# Optimize

Make software or firmware measurably better — faster, smaller, lighter on RAM — the way serious system work has always been done: **measure, don't guess**; attack the biggest cost first; prove each change made things better; keep only the wins. This is how classic systems — the Linux kernel, SQLite, Redis, embedded firmware with 32 KB of RAM — got shipped. The discipline is older than every "clever trick" on the internet.

This is **optimization** (make existing-correct code use less of a resource), not **cleanup** (readability) or **bug-hunt** (find defects). The code should already be correct. If it isn't, do [[fix]] first — optimizing broken code just makes the bug faster.

## How it's invoked

Read the invocation and pick the mode:

- **`optimize` (no number)** — do **one** full optimization pass: baseline measurement → find hotspots → apply the fixes with the best payoff → re-measure → keep what actually improved → report.
- **`optimize N`** (e.g. `optimize 5`) — do **N successive rounds**. Each round is a full pass. Each round should attack a **fresh resource or hotspot**:
  - round 1 might target CPU time on the hottest function
  - round 2 might target heap / allocation pressure
  - round 3 might target stack usage
  - round 4 might target binary / flash size
  - round 5 might target startup time or energy
  - rotate so you're not re-polishing the same loop every round. **N COUNTS ROUNDS, not percent-improvement.** `optimize 10` means ten measured rounds, each on a different target — not "stop when you've saved 10% total". How much you save never changes how many rounds you owe.
  - If a round finds nothing worth changing (the current spot is already near-optimal), **report that honestly** as a clean round and move on to the next area. Never invent an "optimization" that doesn't improve numbers — a measurement showing +0.3% within noise is **not** an optimization. Clean round, move on.
- **With `/work-until-limit`** — optimize continuously until the usage ceiling, rotating resources & hotspots the same way. Switch target when the current one has no more cheap wins; the ceiling is what stops you, never "I ran out of ideas" (always a different resource to look at).

## The one rule that beats every clever trick

> **Measure before. Measure after. Keep only what actually improves the numbers.**

This is the whole discipline. Every classic optimization story — Carmack's inner loops, Fabrice Bellard's demos, the SQLite "100× over 10 years" rewrite, the Linux kernel scheduler debates — followed it. Every "optimization" that *didn't* follow it was almost always a regression hiding as cleverness: made the code slower, bigger, or buggier because the author never measured.

Do not skip the measurement step **even if the change seems obviously good.** Compilers are smarter than you think, and "obvious" wins frequently vanish into whichever instruction cache they came from. The measurement is the whole point; the code change is just how you get a new measurement.

## Phase 1: Decide what to optimize

Ask (or infer) which resource matters here. The right fix for CPU time is often the wrong fix for RAM, and vice versa. Pick ONE primary target per round. Common targets:

| Target | Typical ask | Where it hurts if ignored |
|---|---|---|
| **Runtime / throughput** | "make X faster", "cut tick latency", "handle more RPS" | Users wait; batch jobs run overnight instead of in minutes |
| **Heap / peak RAM** | "fits in 256 KB", "OOM under load" | Device reboots, process gets killed, allocations fail silently |
| **Stack** | "task stack overflow", "crashes in deep recursion" | Hard crash, often with a corrupt callback or memory stomp |
| **Binary / flash size** | "won't fit in 2 MB OTA partition" | Can't ship update, partition layout breaks |
| **Startup time** | "cold boot is 8 s", "device boot visible to attacker" | UX feels sluggish; stealth features defeated |
| **Energy** | "battery dies in 4 h not 24 h" | Field life, remote devices, mobile apps |

If the user hasn't said which, **ask**, or pick the one that would make the biggest observable difference and name it in the report.

## Phase 2: Measure the baseline

You cannot optimize what you have not measured. Pick the right tool for the resource:

- **Runtime (CPU)** — a wall-clock benchmark of the real workload, a profiler, `perf` / `time` / `gprof`, cycle counters (`esp_timer_get_time`, `rdtsc`, `__builtin_ia32_rdtsc`), or ad-hoc timers around hot sections. For embedded, log timestamps around the loop. For code with external I/O, isolate: measure the CPU alone, measure the I/O alone.
- **Heap / RAM** — `heap_caps_get_free_size`, `esp_get_minimum_free_heap_size`, `/proc/<pid>/status`, Valgrind massif, `ps_mem`, Chrome DevTools "Memory" tab. Log before/after key events (boot complete, after first request, after N requests). Look for the *minimum* free value, not the current one.
- **Stack** — `uxTaskGetStackHighWaterMark` (FreeRTOS), `pthread_attr_getstacksize` + fill-pattern probe (Linux), `-fstack-usage` from the compiler for per-function static worst-case.
- **Binary / flash** — `size <elf>`, `riscv32-esp-elf-size -A build/*.elf`, `idf.py size-components`, `objdump -h`, `nm --size-sort`, `bloaty` (very good at diffing). For dynamically-linked apps, strip and compare.
- **Startup** — `systemd-analyze blame`, `perf trace boot`, timestamped log lines through `app_main`, bootchart. For firmware: `boot_trace`, log each phase.
- **Energy** — hardware (USB tester, INA219, power profiler kit), or sleep-time ratio from the OS/RTOS.

Write the baseline number down — committed to a file in the project, or at minimum stated at the top of the report. **Every claim later references this.**

## Phase 3: Find the hotspot

Spend 80 % of your effort on the 20 % of code that matters. Almost always one of these is where the pain is:

### Runtime
- A loop or function that runs millions of times — one allocation inside it kills throughput, one unnecessary syscall ruins latency.
- Repeated work: recomputing the same hash, re-parsing a config, re-scanning a list that doesn't change.
- Pathological algorithmic complexity: O(n²) where you only need O(n) with a hash set; linear scan where a binary search fits.
- Lock contention: single mutex guarding an entire pool when per-shard would suffice.
- I/O amplification: one logical request becoming 100 database queries ("N+1"); a request that forks 50 subprocesses; a loop that does one tiny HTTP call per item.
- Blocking in a hot path: `sleep`, `.wait()`, synchronous DNS, blocking file I/O on a tight loop.

### Memory
- Per-request allocations in a request handler.
- Caches that grow forever (missing eviction).
- Big arrays of pointers to small objects (cache-unfriendly + overhead), where a struct-of-arrays or packed array wins.
- Default string buffers (`char buf[4096]`) multiplied by every task / connection.
- JSON / XML parsers that load the whole document before returning the one field you want.
- Framework overhead: an ORM materializing full objects when a `SELECT id, name` would do.

### Stack
- Big `char buf[8192]` on the stack of a task with 4 KB stack.
- Deep recursion where iteration would do.
- Large structs passed by value.
- Variable-length arrays sized by untrusted input.

### Binary size
- Debug symbols left in release builds.
- Unused library linked in whole-archive mode (`--whole-archive`, `-Wl,--no-as-needed`).
- Full `printf` family when only `puts` / `snprintf` is used — the format family pulls in float formatting + locale.
- Logging-every-level compiled in a release build (`CONFIG_LOG_DEFAULT_LEVEL_VERBOSE`).
- Dead features behind compile flags that are always on.
- Static data: large const tables, pre-expanded `.rodata`, embedded files that could be compressed or omitted.

### Startup
- Everything serialized onto `main()` / `app_main` — WiFi init blocking boot when it could run in a task; filesystem mount before anything that needs it.
- Expensive one-shot work that should be lazy: loading all plugins up front, pre-touching cache files.
- NVS / flash scan that walks every entry.
- Spin loops with `sleep(1)` where a condition variable or event-group bit would wake instantly.

## Phase 4: Apply the fix with the biggest payoff first

Order fixes by **expected measurable gain**, not by how clever they are. A trick that saves 2 ns per call to a function called once per minute is a rounding error; moving one `malloc` out of a 100 KHz loop is huge. Rank candidates roughly:

1. **Algorithmic** — change the complexity class (O(n²) → O(n log n)). Highest ceiling, biggest wins.
2. **Memory layout** — struct-of-arrays, packed structs, reduce indirection. Big cache / RAM wins.
3. **Allocation discipline** — pre-allocate, pool, reuse buffers, move allocations out of hot paths.
4. **Avoid the work** — cache the result, memoize, batch, defer.
5. **Compiler / build** — enable LTO, `-Os` vs `-O2` depending on target, strip, remove unused `-l<lib>`, enable `-ffunction-sections -fdata-sections` + `--gc-sections`.
6. **Low-level micro-optimizations** — SIMD, branchless, `likely`/`unlikely`, cache prefetch. Lowest ceiling, highest risk of making the code worse.

**Only reach for the lower tiers after the higher ones are exhausted.** Starting with SIMD before you've even looked at the algorithm is the classic mistake.

Make **one change at a time** and re-measure. A diff with ten changes bundled together, you cannot tell which one actually helped — some may be regressions hiding under others.

## Phase 5: Measure the result. Keep only the wins.

For each change:

- **Re-run the baseline.** Same workload, same hardware, same time of day if the system has thermal / contention variance. Three runs minimum; report best, median, worst — or at least note the noise level.
- **Compare.** How many percent faster / smaller / less? Is it bigger than the noise? For CPU work, "noise" is usually ±2 %; for memory, ±a few hundred bytes; for firmware size, usually tight.
- **Keep the change** if it won on the metric you were targeting AND didn't regress another critical metric (e.g. 20 % faster but 2× RAM is a trade, not a win — surface the trade-off and let the user decide).
- **Revert the change** if it didn't help, or made things worse, or made the code much less maintainable for a tiny gain. Discipline wins over cleverness.

Prefer committing each kept change on its own so a future bisect can see which commit caused what.

## Phase 6: Report, honestly

The report should let someone reading it (including future-you) understand what moved and by how much. For each round / change:

| Field | What goes there |
|---|---|
| Target resource | runtime / RAM / stack / size / startup / energy |
| Baseline | the measured number before, with units |
| After | the measured number after |
| Delta | absolute AND percent |
| Change | one-line what the code change was |
| Risk | any trade-off (added code complexity, lost readability, used more of a different resource) |

Example:

```
Round 2/5 — RAM, hot path
  Target: peak heap during a /execute request
  Baseline: 48 KB free (min), spike down to 14 KB
  Fix: reuse the 4 KB script buffer across requests instead of malloc/free
  After: 48 KB free (min), spike down to 42 KB
  Delta: +28 KB headroom (2× available at peak)
  Risk: single-threaded only — guarded by a mutex if we ever go multi-worker
```

Be honest when a round finds nothing cheap:

```
Round 4/5 — flash size
  Baseline: 617 KB (71% of 2 MB partition free)
  Looked at: logging strings, duplicate helpers, linker map, -Os settings.
  Nothing cheap — already stripped, LTO on, tables packed. 1-2 KB available
  only by dropping features. Not worth the review cost right now.
  Delta: 0.
```

## What never counts as an optimization

- A change you did not measure. If you haven't run the before and after on the same workload, you did not optimize — you edited.
- A speedup inside noise. ±2 % on one run of one benchmark is noise.
- A micro-optimization in a function that runs twice per boot.
- "I made the code more Pythonic / idiomatic / modern" if the point was to go faster — rewrite for clarity is a different task.
- "I replaced the stdlib with a hand-rolled version" without a measurement proving the stdlib was the bottleneck. 99 % of the time it isn't.
- Removing error handling to shave branches.
- Replacing readable code with unreadable bit-twiddling for 0.5 % — the maintenance cost outweighs the gain.

## When a real redesign is needed

If the only way forward is a serious restructuring — moving the hot work off the main thread, switching data structures, replacing a library — **flag it, don't half-do it.** State the expected gain, the scope, and let the user decide whether to commit. Half-finished redesigns leave the code worse off than before.

## Project-type cheat sheet

### Python / Node / Ruby / general app code

- Profilers: `cProfile`, `py-spy`, `scalene`, `0x`, `clinic`, `node --prof`, `rbspy`.
- Hot spots: N+1 queries, un-indexed DB joins, synchronous HTTP in a loop, parsing JSON per request, logging-every-step at DEBUG, decorator overhead.
- Memory: watch `tracemalloc` snapshots, use `pympler` for Python; `memwatch`, Chrome DevTools heap snapshots for Node.
- Build/dist size: tree-shaking, drop dev deps, lazy-load.

### C / C++ / Rust

- Profilers: `perf`, `valgrind --tool=callgrind` + `kcachegrind`, `heaptrack`, `gperftools`.
- Hot spots: cache misses (`perf stat -e cache-misses`), branch mispredictions, false sharing on hot cache lines, lock contention (`mutrace`, `tsan`).
- Build: `-flto`, `-Os` vs `-O2` depending on target, strip, `-ffunction-sections -fdata-sections -Wl,--gc-sections`, remove unused `-l<lib>`.

### Embedded / firmware (ESP-IDF, STM32, nRF, etc.)

- RAM: `heap_caps_get_free_size`, `esp_get_minimum_free_heap_size`, `uxTaskGetStackHighWaterMark`, `menuconfig`'s "component config" → trim buffer sizes (Wi-Fi RX/TX buffers, HTTPD RX hdr, TinyUSB MSC BUFSIZE, lwIP mbox/sockets).
- Flash: `idf.py size`, `idf.py size-components`, `bloaty`. Drop a log-level, drop a locale, strip. Default `CONFIG_COMPILER_OPTIMIZATION_SIZE=y` for `-Os`.
- Startup: `boot_trace`, each `app_main` phase timed; move WiFi / BT bringup off the main task; defer SPIFFS mount until something needs it; skip LED self-test when "silent startup" is on.
- Energy: use RTC-slow sleep between work, lower CPU freq (`CONFIG_ESP_DEFAULT_CPU_FREQ_MHZ_80` for idle, raise for bursts), disable radio when not in use.

### Databases / SQL

- `EXPLAIN ANALYZE` on every query that shows up in the profile.
- Add indexes where plans show full-table scans.
- Avoid `SELECT *` when a few columns suffice.
- Batch inserts, use prepared statements.
- Materialized views for repeat heavy aggregations.

### Web / frontend

- Lighthouse / Chrome DevTools "Performance" and "Memory" tabs.
- Fewer round trips: HTTP/2, bundle sizes, lazy load, resource hints.
- Images: WebP / AVIF, correct `srcset`, offscreen `loading=lazy`.
- JS: tree-shake, split chunks, defer non-critical, avoid big `polyfill.io` imports.
- CSS: critical path inline, async the rest; drop unused Tailwind utility classes with purging.

## Pairings

- Pair with [[bug-hunt]] when the hot code might be *doing* the wrong thing, not just doing it slowly.
- Pair with [[cleanup]] AFTER optimization: optimize first (don't re-polish prose on code that's about to change shape), then clean up what survives.
- Pair with [[test]] / tests you already have: run them before and after every round. **No regressions.** An "optimization" that breaks a test is a bug.
- Pair with [[big-change]] when the right fix is a redesign of a module rather than nibbling at it.
- Respect [[careful]] when the code is production-critical and the margin is thin — stop at the smallest safe win rather than chasing the last 1 %.

## Classic lessons from the people who did this the hard way

- *"Measure. Don't tune for speed until you've measured, and even then don't unless one part of the code overwhelms the rest."* — Rob Pike's rule #2 (Notes on Programming in C).
- *"Premature optimization is the root of all evil."* — Knuth, who then added: *"Yet we should not pass up our opportunities in that critical 3 %."*
- *"The fastest code is the code that doesn't run."* — folklore; mostly true.
- *"If it isn't tested, it isn't optimized — it's a regression waiting to be noticed."*

These are not aphorisms, they are schedule-savers. Follow them.
