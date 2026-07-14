---
name: placeholder-replacer
description: Find every piece of non-real code in the project — stubs and TODOs, fake/mock/simulated logic, hardcoded dummy return values, truncated "… rest of code" / "implementation omitted" gaps, "your code here" placeholders, and commented-out code standing in for functionality — and replace it with REAL, complete, working implementations. Use whenever the user invokes /placeholder-replacer or asks to "replace the placeholders", "make the fake code real", "finish the stubs", "no more mock/simulated code", or "fill in the TODOs with actual implementations". Ground every replacement in the real intended behavior — never swap one placeholder for a confident guess.
---

# Placeholder Replacer

AI-written and half-finished code is full of stand-ins: `pass`, `# TODO`, `raise NotImplementedError`, `return "dummy"`, `# ... rest of the implementation`, `# simulated for now`, commented-out logic. This skill hunts them all down and turns them into **real, working code** — code that actually does the thing, not another approximation.

The one hard rule: **real means grounded, not invented.** The failure mode here is replacing a placeholder with confident-looking code that does the *wrong* thing — that's worse than the honest stub, because it hides the gap. Every replacement must be anchored in what the code is genuinely supposed to do (name, signature, docstring, callers, tests, spec). If you can't determine that, you stop and ask — you don't guess.

## Phase 1: Find the placeholders

Hunt systematically with grep, then read around each hit. Common markers:

```
rg -n "TODO|FIXME|XXX|HACK|NotImplementedError|placeholder|stub|dummy|simulate[d]?|mock|fake"
rg -n "\.\.\.|rest of (the )?(code|implementation)|omitted|implement (this|here)|your code here|for now|temporar(y|ily)"
rg -n "^\s*pass\s*$"                         # bare 'pass' bodies (may be placeholder OR legit no-op)
rg -n "return\s+(None|0|0\.0|\"\"|''|\[\]|\{\}|True|False)\s*#"   # suspicious hardcoded returns
```

Also scan for **commented-out code** (lines that are clearly code behind a `#`/`//`) and **hardcoded sample/fake data** used where real computation or a real data source belongs.

## Phase 2: Triage each hit — placeholder vs. legitimate

Not every match is a placeholder to replace. **Leave these alone:**
- Abstract methods / interface / `Protocol` / base-class methods that are *meant* to be empty (`pass`/`...` as an intentional contract).
- Deliberate no-ops (an empty `except` that's genuinely correct, an intentionally empty default).
- Real example code in docs, tests, or fixtures.
- Commented-out code that's a deliberate reference note, not disabled functionality.

**Replace these:** anything that is a stand-in for functionality that should exist — a stub body, a fake/simulated result, a `# TODO: actually do X`, a truncated section, a hardcoded value where logic belongs, commented-out logic that was meant to run.

When it's genuinely unclear which kind it is, treat it as the ambiguous case (Phase 4) — don't assume.

## Phase 2.5: For a big sweep, report the list first

If the scan turns up more than a handful of real placeholders, **list them before mass-replacing** — a short table of each confirmed placeholder (type + `file:line` + what it stands in for) so the user sees the scope and can confirm. This matters because some placeholders need a decision (Phase 4), and the user may want to prioritize or exclude a few. For one or two obvious placeholders, just fix them; report-first is for the large sweep.

## Phase 3: Implement for real

For each true placeholder:
1. **Determine the intended behavior from evidence** — the function/variable name, its signature and types, the docstring/comments, what the callers expect back, existing tests, sibling implementations doing something similar, and any spec the user has given. Build the real behavior from these, not from imagination.
2. **Write the complete, working implementation** — no new placeholders, no "simplified version," no re-stubbing. It should actually perform the task and handle the obvious cases.
3. **Match the surrounding code** — style, naming, error handling, patterns already in the file.
4. **For truncated "… rest of code"** — reconstruct the full logic that belongs there from context; don't just remove the comment and leave a hole.
5. **For commented-out logic** that should run — restore it as real code, but check it's still correct against the current codebase before un-disabling it (it may have been commented out because it broke).

## Phase 4: When you can't ground it — ask, don't fabricate

If you cannot determine what the real implementation should actually do — the behavior depends on a spec you don't have, an external API/contract you can't see, a business rule only the user knows — **do not invent a plausible implementation.** Stop and either ask the user for the missing detail, or leave the placeholder in place with a precise note on exactly what's needed to finish it. A clearly-marked gap beats silent wrong code. Report these as a list at the end.

## Phase 5: Verify

- After replacing, **run the project's tests and exercise the affected paths** — the whole point is real *working* code, so prove it works, ideally after each meaningful chunk.
- Add a quick test where a replacement is important and untested, so the now-real behavior is pinned.
- Set up a revert safety net first if the project has one (git commit / backup), since you're changing real logic — detect git with `git rev-parse --is-inside-work-tree 2>/dev/null`; if absent, a quick backup copy, never error on missing git.

## Finish

Summarize: **Replaced** (what became real, and that it's verified), **Left as-is** (legitimate stubs you correctly didn't touch), and **Couldn't complete** (placeholders that need a decision/spec from the user, with the specific question). Be honest — don't report a placeholder as "done" if you actually guessed at it.

## Notes

- Pairs with **`/fix`** (if a replacement reveals a bug), **`/careful`**, **`/control`** (STOP button for a big sweep), and complements **`/cleanup`** (which removes dead commented-out code rather than reviving it — opposite call, so decide per block which applies). Respects **`/no-talk`**.
