---
name: test
description: Run the project's tests and report the real result — detect the test framework, run the suite (or a targeted subset), and give an honest pass/fail count with the actual failures. Investigates and explains failures, and fixes them if asked. Never fakes green, never weakens a test to make it pass. Use whenever the user invokes /test or says "run the tests", "does it still pass", "run the suite", "test this", "check nothing broke", or "run the tests for X". Run it after changes to confirm nothing regressed.
---

# Test

Run the project's tests and tell the user the truth about the result. The whole value of a test run is an *honest* signal — a faked or hand-waved "all green" is worse than no run at all, because it creates false confidence. Report real numbers, real failures, real skips.

## Step 1: Find how this project tests

Detect the framework and command before running — don't guess. Look for the manifests and config:
- **Python** → `pytest` (look for `tests/`, `pytest.ini`, `pyproject.toml`, `conftest.py`), or `python -m unittest`.
- **Node / JS / TS** → `package.json` `scripts.test` (jest, vitest, mocha, `npm test` / `pnpm test` / `yarn test`).
- **Flutter / Dart** → `flutter test`.
- **Rust** → `cargo test`. **Go** → `go test ./...`. **Java** → `mvn test` / `gradle test`.
- If there's a project **verify/test skill or a Makefile target** (`make test`), prefer it — the project knows its own command best.

If you genuinely can't find a test setup, say so and ask (or offer to scaffold one) rather than inventing a command that won't run.

## Step 2: Pick the scope

- **Full suite** (default for "run the tests" / after a broad change) — the whole thing.
- **Targeted** (faster, for iterating on one area) — just the relevant file/dir/pattern, e.g. `pytest tests/test_router.py -k batching`, `flutter test test/foo_test.dart`. Use this while fixing, then run the full suite once at the end to confirm nothing else broke.

Match scope to the ask: a quick "does X still work" is targeted; "check nothing broke" is full.

## Step 3: Run it and read the ACTUAL output

- Run the real command and capture the real output. Wait for it to finish — a long suite is still running, not passing.
- Read the summary line: **passed / failed / skipped / errored** counts. Report the real numbers, e.g. "1086 passed, 2 failed, 3 skipped".
- **Never claim a result you didn't observe.** "The tests should pass" is not a test result. If you didn't run it (or it timed out), say exactly that — don't report green.
- Note skips and xfails honestly; a suite that's "green" only because half of it is skipped is not green, and the user should know.

## Step 4: On failure — investigate, then report or fix

For each failure:
- Read the actual assertion/error and the traceback. Identify whether it's a **real regression** (the code broke), a **flaky test** (timing/order/randomness — reproduce before believing it), or a **stale test** (the code changed intentionally and the test wasn't updated).
- **Report clearly**: which test, what it expected vs. got, and your read on the cause.
- **If the user asked you to fix** (or a fix is clearly in scope): fix the **root cause**, not the test. Prefer the [[fix]] discipline for anything subtle. Update a test only when the behavior change was intentional and correct — and say so.

## The hard rule: never fake green

- **Do not weaken, skip, comment out, or delete a test to make the suite pass.** Do not loosen an assertion, add a blanket `try/except`, mark it `xfail`/`skip`, or lower a threshold just to turn it green. That converts a real failure into a hidden one.
- If a test is genuinely wrong or obsolete, changing it is legitimate — but only with a clear explanation of *why it's the test that's wrong*, not the code.
- A faster/quieter run is fine; a dishonest one is not.

## Step 5: Report

Give the honest bottom line: the counts, what failed (if anything) and why, what you changed (if you fixed), and whether the suite is now genuinely green. If you only ran a subset, say so and note the full suite wasn't run.

## Notes

- Pairs with [[fix]] (fix a failing test's root cause), [[bug-hunt]] (tests often surface where to hunt), and [[improve]]/[[new-features]] (run after changes to confirm no regression). The built-in `/verify` drives the real app flow end-to-end — use it alongside `/test` when a change has runtime behavior a unit test won't catch.
- Respects [[no-talk]] (just run and print the counts + failures) and [[quick-*]] (targeted scope, minimal chatter).
- Under [[work-until-limit]], running the suite is one activity, not the finish line — a green suite is not a reason to stop the run (only the meter is).
