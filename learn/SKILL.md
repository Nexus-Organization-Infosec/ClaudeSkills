---
name: learn
description: Study the project before touching it — read the structure, find the entry points, trace how it actually works, learn its conventions — and then carry straight on with whatever the user asked for. A preface to the real request, never a replacement for it: the turn ends with the work done, not with a summary of the codebase. Depth is proportional — a wide cheap sweep of the whole project, then deep reading only where the request lands. Invoked as "learn" before a request, "learn <area>" to focus (e.g. "learn the radio path"), or "learn only" when the user genuinely wants just the explanation. Use whenever the user invokes /learn or says "look through the project first", "understand how this works before you change it", "get familiar with the codebase", "learn the project then do X", or drops you into an unfamiliar repo and asks for work. Pairs with [[map]] (which plans and tracks the work) and [[careful]] (which minimizes what you touch).
---

# Learn — understand the project, then do the work

Read the project properly before acting on it: what it is, how it's laid out, how it runs, how the pieces talk, what conventions it follows. Then **do what the user actually asked**, informed by all of that.

## This is a preface, not a deliverable

The failure this skill has to design against is the one it invites: spend the whole turn exploring, produce a beautiful architecture write-up, and hand back with *"now that I understand the project, would you like me to proceed?"* The user asked for a change, got a book report, and has to ask again.

- **The turn ends with the request done.** Learning is what you do *on the way*, not instead. If the user said "learn the project and fix the login bug", the deliverable is the fix.
- **Don't narrate the reading.** A running commentary of every file you opened is noise. What you learned shows up as *better work* and, where it matters, a few sentences of context alongside it.
- **`learn only` is the exception.** If the user explicitly wants just the explanation — "learn the project and tell me how it works", "explain this codebase" — then the explanation is the deliverable. That is the only case where a summary is a complete answer.
- **Stopping to ask is not learning.** "I've explored it, which area should I start with?" is a hand-back. Pick the area the request implies and start.

## "Everything" means the right things, not every byte

On any real project, reading every file is impossible, and it is also the wrong goal — most files won't touch the request. Aim for **complete shape, selective depth**:

- **Wide and cheap first.** Get the whole project's outline in your head: what it is, its parts, how they relate. Directory listings, manifests, and entry-point names carry enormous signal per token.
- **Deep only where the work lands.** Once you know where the request touches, read *those* files properly — whole, not skimmed — plus their callers and their tests.
- **Match the depth to the stakes.** A one-line copy change needs the shape and one file. A refactor of the core loop needs the mechanism, the invariants, and every caller.

## Step 1: The shape

Establish what this project *is* before opening any source file:

- **Manifests and build files** — `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, `Makefile`, `CMakeLists.txt`, `*.csproj`, `platformio.ini`. These give you the language, the dependencies, the entry points, the build and test commands, and the project's own name for itself.
- **Directory layout** — the top two levels. Where does source live, where do tests live, what are the top-level modules, is it a monorepo.
- **Entry points** — `main`, `index`, `app`, `cli`, `__main__`, `setup()`/`loop()`, service units, `Dockerfile` `CMD`. Everything the program does starts at one of these; find them and you have the spine.
- **How it runs and how it's tested** — the actual commands. Read the test directory's shape while you're there: tests are the most honest description of intended behavior in most projects.
- **Recent history** — `git log --oneline -20` and what changed lately. It tells you which parts are alive, which are abandoned, and what the team was in the middle of. (Skip if not a repo.)
- **Project instructions** — `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `CONTRIBUTING.md`. These are binding, unlike the README.

## Step 2: The mechanism

Now trace how it actually works — by following one real path end to end, not by opening files alphabetically.

Pick the path the user's request touches (a request to fix login → follow a login from entry point to storage and back). Walk it through every layer: entry point → routing/dispatch → the logic → I/O, storage, or hardware → the response. Read the functions on that path properly.

That single trace teaches you more than a survey of twenty files, because it shows you the project's **actual** structure: its layering, its data flow, its error handling, where state lives, what talks to what.

Then note the things that generalize beyond that path:

- **Data model** — the core types/structs/tables everything else revolves around.
- **State and lifecycle** — what's held in memory vs. persisted, what happens at startup and shutdown.
- **Boundaries** — where the project talks to the outside: network, filesystem, hardware, other services.
- **Cross-cutting mechanisms** — config loading, logging, error handling, auth. Learn these once; they recur everywhere.

## Step 3: The conventions

Code you add should be indistinguishable from the code already there, which means reading for style, not just behavior: naming, file and folder organization, error-handling idiom, logging style, comment density, test structure and naming, and how new units get registered (a table? a decorator? a folder scan?). Note the patterns the project uses *consistently* — those are the house rules, and consistency matters more than your preference.

## Step 4: Trust the code over the prose

Docs drift; code doesn't. When the README and the source disagree, **the source is what runs** — believe it, and mention the discrepancy to the user if it's load-bearing.

So verify the important beliefs cheaply instead of assuming: run the tests, run the build, execute the thing, grep for the function you think is the entry point and confirm who calls it. A wrong mental model produces confident, wrong work — one command is cheaper than the debugging it prevents. Concretely: before editing a function, check its callers; before changing a config key, grep everywhere it's read.

## Step 5: Write down what survives

Long sessions get compacted, and what you learned is exactly what you don't want to lose.

- Keep a short scratch note (`notes.md` in the scratch area) with the shape, entry points, key files, run/test commands, and any gotchas. Terse and factual.
- **Don't put codebase structure in memory.** File layouts, function names, and how the code works are re-derivable by reading the repo, and they go stale the moment someone refactors. Memory is for what the repo *doesn't* record — the user's constraints, decisions and their rationale, the "we tried X and it broke Y" that no file mentions.

## Step 6: Do the work

Go straight from understanding into the request. No "ready to proceed?" checkpoint, no summary handed back in place of the work.

Where the learning changes the plan, say so in a sentence and keep going: *"the retry logic already lives in `client.py:88`, so I'm extending that instead of adding a new one."* That single line is worth more than a page of architecture notes, because it tells the user what changed and why.

## Ground rules

- **Read before you write. Always.** The whole point is not editing a file you haven't understood — no blind edits, no pattern-matched changes to code you only skimmed.
- **Reading is not progress.** A turn that produced only understanding produced nothing the user can use (except under `learn only`). If the budget is tight, learn less and ship the change.
- **Scale to the project.** A 10-file script needs minutes of orientation, not a full survey. Very large repos are the case for a broad parallel sweep — dispatch read-only exploration across subsystems and keep the conclusions, not the file dumps.
- **Don't fabricate structure.** If you didn't confirm how something works, say "I haven't checked X" rather than presenting a plausible guess as fact. A confident wrong model is the expensive failure here.
- **Respect what you find.** Existing patterns win over your preferences; if something looks wrong, flag it rather than silently rewriting it as part of an unrelated request (see [[careful]]).
