---
name: bug-hunt
description: Proactively hunt the codebase for bugs of every size — major reliability bugs (connection/network failures, missing timeouts, unhandled disconnects, no retry/reconnect, crashes on the hot path, data corruption, money/precision errors), correctness/logic bugs and edge cases, and tiny issues (small security nits, defensive gaps) noticed in passing. Rank findings by severity, then fix them safely. Use whenever the user invokes /bug-hunt or asks to "hunt for bugs", "find bugs in my project", "what's broken or fragile here", or "look for connection issues and crashes". Think adversarially: what inputs and conditions break this?
---

# Bug Hunt

Go looking for bugs before they bite — the ones nobody's reported yet. Think like something trying to break the app: what input, what timing, what network hiccup makes it misbehave, crash, or silently produce the wrong result? Hunt across the whole range, from major reliability failures down to tiny defensive gaps, then fix what you find.

This is *discovery* of unknown bugs (vs [[fix]], which fixes one known bug, and [[reverse-engineer]], which goes deep on security specifically). Cast a wide net; verify each catch; fix the real ones.

## Scope: whole-project or recent-changes

Ask (or infer) which scope fits — it changes where you look:
- **Whole-project** (default for a first hunt or "find bugs in my project") — the full sweep below.
- **Recent-changes** (best for iterative work / "check what I just changed") — focus the hunt on code that changed recently: `git diff --name-only HEAD~5..HEAD` or the uncommitted diff (`git status`/`git diff`). New and just-edited code is where fresh bugs concentrate, so this is much higher-yield per minute than re-sweeping stable code. Apply the same categories below, just narrowed to those files and their immediate callers.

## Phase 1: Know where bugs hide

Skim the project to find the high-risk zones — that's where to spend effort:
- **Network / external I/O** — API calls, price feeds, websockets, the browser bridge, any request that can time out, drop, rate-limit, or return partial/garbage data.
- **The hot path** — the code that runs constantly (for a trading bot: the tick/price loop, order logic, state updates). A rare bug here fires often.
- **State & persistence** — state files, caches, anything written/read across runs (partial writes, stale/corrupt state).
- **Money / precision** — anything doing arithmetic on prices, balances, quantities.
- **Edges & concurrency** — parsing, boundary conditions, and any shared/concurrent state.

## Phase 2: Hunt, by category

Work through these deliberately — grep for the patterns, then *read* the code around hits and trace what happens under bad conditions.

### Connection / network reliability (often the biggest, most impactful bugs)
- **Missing timeouts** — any request that can hang forever. `rg -n "requests\.(get|post)\(|urlopen|httpx|websocket|\.recv\("` and check each has a timeout.
- **No retry / backoff** — a single transient failure kills the operation; no exponential backoff, no reconnect loop for a dropped stream/websocket.
- **Unhandled disconnects** — what happens when the connection drops mid-run? Does it crash, hang, or silently stop updating?
- **Rate limits** — is HTTP 429 / exchange rate-limiting detected and backed off, or does it hammer and get banned?
- **Partial / missing / malformed data** — a field missing from an API response, an empty list, a `null` price, a NaN. Does it propagate a bad value (e.g. marking something at price 0) instead of handling the gap? (This class has bitten this project before — a missing price mis-marking net worth — so scrutinize it.)
- **Silent failure** — errors swallowed so the app looks alive but has stopped doing its job.

### Correctness / logic
- Off-by-one, inverted conditionals, wrong operator, comparison vs assignment.
- Edge cases: empty / `None` / zero / negative / very large / duplicate / out-of-order inputs.
- Wrong assumptions about ordering, uniqueness, or units.

### Crashes / stability
- Unhandled exceptions on the hot path, `KeyError`/`IndexError` (dict/list access without `.get`/bounds check), divide-by-zero, `None` where a value is assumed.
- Resource leaks (unclosed files/sockets), unbounded growth (memory/queues).

### Money / precision
- Float rounding on prices/balances, truncation, off-by-a-decimal, mixing units — small errors here are expensive.

### Tiny stuff in passing
- Bare `except:`/`except: pass` hiding real errors, small hardcoded values that should be config, minor input-validation gaps, a stray debug print. Note small **security** nits but defer a real security audit to [[reverse-engineer]].

## Phase 3: Verify each catch (no false alarms)

A "bug" is only a bug if you can show it's real. For each candidate, do the cheapest confirmation available: trace the data/condition that triggers it, write a tiny test that reproduces it, or run the code path. If you can't construct a plausible trigger, mark it low-confidence rather than asserting it. A report full of "might be a problem" trains the user to ignore you — confirmed catches earn trust.

## Phase 4: Report, ranked

List findings worst-first so the user sees what matters:

| Severity | Meaning |
|---|---|
| **Critical** | Data/money loss, silent corruption, crash on the main flow. |
| **Major** | Connection failure that halts/degrades the app, wrong results under common conditions. |
| **Minor** | Edge-case bug, rare crash, mishandled unusual input. |
| **Tiny** | Defensive gap, small nit, cosmetic. |

Per finding: `file:line`, what's wrong, the concrete trigger (how it happens), and the fix. Be honest about coverage — a hunt finds a lot, not everything.

## Phase 5: Fix — safely, worst-first

- **Safety net first — automatic, git-optional, never errors.** Hunting is read-only and needs no git. Before applying fixes, detect git with `git rev-parse --is-inside-work-tree 2>/dev/null`; if it's a repo, ensure the tree is clean/committed; if it's NOT, don't error or require git — just make a quick timestamped backup copy of the project and continue.
- Fix in severity order so the biggest risks go first even if you stop early.
- **Preserve behavior except the bug**; run the project's tests (and the real flow) after fixes — ideally after each — and confirm still-green. For a substantial or subtle bug, prefer the [[fix]] discipline (reproduce → root cause → test).
- Add a regression test where it's cheap, so a fixed bug stays fixed.
- Confirm before risky/irreversible changes; don't "fix" a bug by silencing the error or weakening a check.
- If a fix needs a real redesign, flag it rather than half-doing it.

## Notes

- Pairs with **`/fix`** (thorough fix of a specific catch), **`/careful`**, **`/control`** (STOP button for a long hunt), **`/work-until-limit`**, and **`/map`**. Respects **`/no-talk`**.
- Complements **`/reverse-engineer`**: this hunts functional & reliability bugs broadly; that goes deep on security and CVEs. Its `references/patterns.md` is a useful grep source for the error-handling and tiny-security checks here too.
