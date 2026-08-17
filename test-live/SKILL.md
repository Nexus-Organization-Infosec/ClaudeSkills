---
name: test-live
description: Verify a change by actually RUNNING the real thing and observing it work — launch the app, drive the real UI, hit the live endpoint, watch it in a browser, screenshot the screen, read the real logs — not just writing unit tests or asserting "the code looks correct." A green headless test suite proves the code does what the test says; a live test proves the feature actually works for a user. Invoked as "test-live" to live-test the current change, or "test-live <feature>" to focus on one flow. Use whenever the user invokes /test-live or says "actually run it", "test it for real / live", "don't just write unit tests", "prove it works in the real app", "click through it", "see it in the browser", "run the actual app and check", "does it really work", or "stop saying it works without running it". Covers web (browser preview + click/screenshot), servers/APIs (real requests), CLIs (real invocations), desktop/GUI apps (launch and drive), and hardware/device flows (what can be checked in software vs. what needs the physical device). Pairs with [[run]] (launch the app), [[test]] (the test suite), and [[bug-hunt]] (what live testing turns up).
---

# Test Live — prove it works by running it, not by trusting the code

Confirm the change works by **exercising the real thing and watching what happens** — the running app, the live endpoint, the actual screen — instead of concluding it works because the code reads correctly or a headless unit test passed. Unit tests check the code against your idea of what it should do; a live test checks the product against reality. They catch different failures, and this skill is about the second kind.

## Why this exists — "the tests pass" is not "it works"

The trap this skill designs against: writing a passing test (or just reading the diff) and reporting the feature done, when the thing a user actually does was never performed once. Green unit tests routinely coexist with a broken product — the button is wired to the wrong handler, the page 500s on load, the config never loads, the endpoint returns 200 with an empty body, the two components were each tested in isolation and don't talk, the mock hid the real API's actual shape. **A test that mocks the thing under test proves the mock works.** Live testing is the check that no amount of headless assertion replaces: *did the real behavior actually happen, observed, end to end.*

This is not anti-unit-test. Unit tests are fast, precise, and belong in the suite. This skill adds the layer on top: after the code is written and the fast tests pass, **go run it for real.**

## The core rule

**Do not claim a feature works until you have observed the real thing doing it.** "Observed" means one of: you saw the rendered UI in a browser/screenshot, you got the real HTTP response back, you ran the actual command and read its real output, you launched the app and drove the flow, you read the live logs showing the code path executed. "The code should do X," "the unit test for X passes," and "I added handling for X" are **not** observations of X happening — they are reasons to go check.

If you cannot run it (no hardware, no credentials, a step that needs the user), say exactly that and say precisely what remains unverified — don't let "I wrote it" quietly become "it works."

## Step 1: Name the real user-visible behavior to verify

Before running anything, state the concrete thing a user would do and the observable result that proves it worked. Not "the auth module functions" — "submitting the login form with valid creds lands on the dashboard; with bad creds shows the error." That sentence is your pass/fail contract, and it must be about *observable behavior*, not internal state.

Verify the **actual changed behavior**, plus the one or two flows most likely to have broken from the change. Don't re-test the whole app; do test the thing you touched, live.

## Step 2: Run it the way it's actually used

Get the real thing running (use [[run]] to launch it) and drive the real path. Match the method to what it is:

- **Web UI** — open it in the browser preview, don't just curl the HTML. Actually **navigate, click, type, submit**, and **watch the result render**; take a screenshot of the working (or broken) state. Read the browser console for errors and the network tab for failed/blank requests — a page that "loads" while the console is red is not working. Check the real viewport (and mobile width if it matters).
- **Server / API** — send **real requests** to the running server (the actual routes, real-ish payloads, auth headers) and inspect the real responses: status, body shape, values, error cases. A route that returns `200 {}` when it should return data is a fail even though nothing threw. Hit the unhappy paths too (bad input, missing auth, not-found).
- **CLI / script** — **run the actual command** with real arguments and read the real stdout/stderr and exit code. Run it the way a user would, including a wrong-usage invocation to see the error path.
- **Desktop / GUI (Flutter, PyQt, Tkinter, Qt, Electron, etc.)** — **launch the app** and drive the flow — open the screen, trigger the action, watch the UI update. Screenshot the result. Where the toolkit allows scripted/driver-based interaction, use it; otherwise launch it and walk the steps, reporting what you saw.
- **Background job / pipeline / event flow** — actually **trigger it** (enqueue the job, fire the event, drop the input file) and confirm the real downstream effect happened — the record written, the file produced, the message delivered — by inspecting the real output, not by asserting the handler was called.
- **Hardware / device flow** — run **everything that can run in software**: the logic, the protocol encoding/decoding against captured real data, the driver against a loopback/mock at the I/O boundary. Then state clearly which final step needs the physical device and hand that to the user as a specific check ("flash this, press button A, confirm the OLED shows X"). Software-verify the maximum; never claim the on-device behavior works when no device ran it.

## Step 3: Observe honestly — read the real output, not your expectation of it

The failure mode here is running the thing and then *seeing what you expected* rather than what happened. Guard against it:

- **Look at the actual result**, all of it — the rendered screen, the full response body, the real log lines, the exit code. Not the first line that looks right.
- **Check the negatives.** No red console errors, no stack trace in the logs, no 4xx/5xx you didn't intend, no silent empty state where data should be, no layout collapse. Absence of a crash is not success.
- **Confirm it was actually your code that ran.** A cached page, a stale build, a mock still wired in, or a server you didn't restart will happily show "working" behavior that has nothing to do with your change. Force a fresh build/reload; add a temporary log line and confirm you see it if unsure.
- **Watch it, don't watch a proxy for it.** A passing test that calls the function is a proxy; the rendered dashboard is the thing. Prefer the thing.

## Step 4: When it fails live (it often does)

A live test that fails is the skill working — it caught what the unit tests didn't. Then:

1. Read the real error — console, logs, response body, stack trace — for what *actually* went wrong, not what you assume.
2. Fix it.
3. **Re-run live.** Fixing and re-asserting the code is right is the exact trap; run the real flow again and watch it work this time. A fix isn't done until the live test that failed now passes live.
4. Consider adding a fast automated test that captures this failure so it's caught cheaply next time — the live test found it; a unit/integration test can guard it going forward.

## Step 5: Report what you actually saw

State it in terms of observed reality, with the evidence:

- **What passed live**, and how you know — "opened `/dashboard`, logged in as a test user, saw the three cards render with real data (screenshot); logout returns to the login screen." Concrete and observed.
- **What you could not verify live**, and exactly why — "the payment goes through Stripe test mode which needs your key; wired and unit-tested, but I have not run a real charge." Name the specific remaining check.
- **Never round up.** "The code is correct and the unit tests pass, so it works" is precisely the claim this skill forbids. If you didn't run the real flow, say you didn't.

## Ground rules

- **Running beats reading; observing beats asserting.** The whole point is that seeing the real behavior outranks any argument that the code should produce it.
- **A mock is not the thing.** Mocks and fakes are fine *inside* unit tests; they cannot stand in for the live check. If the live test still hits a mock, it isn't a live test.
- **One real end-to-end pass is worth ten green units.** Don't substitute more headless tests for the thing this asks for — actually run it once, for real, all the way through.
- **Restart / rebuild before you trust it.** Half of "it works" surprises are stale state. Fresh build, fresh reload, real request.
- **Be honest about the boundary.** What genuinely needs hardware, a paid service, or a user action gets named as an explicit remaining step — not silently folded into "done."
- **Clean up.** Remove temporary log lines, test users, and scratch data you added to observe, once you've observed.
