---
name: research
description: Research a problem on the internet — search the web and pull answers from authoritative sources (official docs, GitHub issues/PRs, Stack Overflow, Reddit, forums, blogs) to find a fix, a known bug, correct library usage, or best practice. Cross-checks sources, weighs recency and version, and cites links. Use whenever the user invokes /research or asks to "look this up online", "search for a fix", "is this a known issue", "how do others solve X", "find docs for Y", or when you're stuck on an error and need outside information. Needs internet (won't run under /no-internet).
---

# Research — find the answer online

Go find the real answer on the internet instead of guessing — a known bug's fix, the correct way to use a library, why an error happens, what others did about it. The value is in getting a *correct, current, applicable* answer and showing where it came from, not just pasting the first search hit.

Uses the **WebSearch** and **WebFetch** tools (if they're deferred, load them via ToolSearch first). For sites that need a real browser, the Browser tools are a fallback. This skill inherently needs the network — if `/no-internet` is active, say so and stop rather than going online.

## Step 1: Search well

The query is half the battle:
- **Paste the exact error message** in quotes (strip machine-specific bits like file paths, line numbers, memory addresses). Error strings are the highest-signal search you can do.
- **Include the stack + version** — library/framework name and version, language, OS. "flutter 3.x", "python 3.10", the package name.
- Search the *symptom and the goal* separately if one doesn't land.

## Step 2: Go to the authoritative sources, in order

Weight sources by how likely they are to be correct and current:
1. **Official docs / changelogs / release notes** — the ground truth for how something is *supposed* to work, and what changed between versions.
2. **GitHub issues & PRs** — for "is this a known bug?": search the repo's issues for the error. Look for a maintainer's answer, a linked fix PR, or a workaround in the comments. Check whether it's open (still broken) or closed (fixed in which version).
3. **Stack Overflow** — read the accepted *and* the top-voted answers, and the **comments** (they often correct or date-stamp the answer). One highly-upvoted recent answer beats an old accepted one.
4. **Reddit / forums / blogs** — real-world gotchas, "this also bit me" context, and pragmatic workarounds. Lower authority; corroborate before trusting.

Open several sources (WebFetch the promising ones) — don't build a conclusion on a single random post.

## Step 3: Judge what you find (this is where research earns its keep)

- **Recency & version.** Software moves; a 2019 accepted answer may be wrong for today's version. Check dates and the version each answer targets, and prefer solutions that match the user's version. Call out when the best answer is old and might be stale.
- **Cross-check.** If two good sources agree, confidence is high. If they conflict, say so and explain which is more likely right (and why — official doc > random blog).
- **Applicability.** Does this actually fit the user's stack, versions, and situation? A fix for a different OS or major version may not transfer.
- **Safety.** Don't recommend copy-pasted code that runs untrusted commands, disables security (`verify=False`, `sudo curl | bash`), or comes with a licence the user can't use. Flag those instead of blindly relaying them.

## Step 4: Report — answer + evidence

- **The answer / fix**, stated plainly and adapted to the user's actual code/stack (not a raw paste).
- **Why it works** — the underlying cause, briefly, so it's not cargo-culted.
- **Sources** — link the pages you relied on, so the user can verify. Note the key one ("this is confirmed in the library's changelog for v2.4").
- **Caveats** — version constraints, uncertainty, "this is a workaround, the real fix is pending in issue #123".
- If it's a code fix, **apply and verify it** (run the test / the affected path) rather than assuming the internet is right — see [[fix]]. The web gives you the lead; your own verification confirms it.

## Notes

- If nothing authoritative turns up, say so honestly — "no confirmed solution found; here's the most plausible lead and what I'd try" beats presenting a guess as a found answer.
- Respects `/no-internet` (can't run) and `/stay-here` (that's about the filesystem, not the web — unaffected). Pairs with `/fix` and `/bug-hunt` when the research is in service of fixing something.
