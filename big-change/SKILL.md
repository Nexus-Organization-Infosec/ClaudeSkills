---
name: big-change
description: Like /improve, but every change is BIG — bold, ambitious, high-impact rewrites and redesigns rather than small safe tweaks. Sweeps the codebase FILE BY FILE in a fixed sorted order — big change to file 1 finished fully, then file 2, 3, 4… until every file is reached — and deliberately does NOT jump around following dependencies (if file 1 depends on file 4, it still improves file 1 now and gets to file 4 in order). Each file's change is made fully and proven better before moving on. Every big change must be REAL working functional code — comments, placeholders, TODOs, dummy/mock logic, API-key/stub placeholders, dead scaffolding and cosmetic churn do NOT count as big changes and are never used to mark a file done. Invoked as "big-change" for the full file-by-file sweep, or "big-change N" (e.g. "big-change 5") to stop after N files. Use whenever the user invokes /big-change or says "make big changes", "go big", "don't hold back", "make crazy-good large changes", "rewrite this properly", or "improve all the files and make big changes". The ambitious, large-scope sibling of [[improve]] — same measure-and-keep-only-what-wins discipline, much larger unit of change, applied one file at a time in order.
---

# Big Change

Make the work **dramatically** better with **big, bold changes** — the kind most passes are too timid to attempt. Where [[improve]] picks the single highest-value *small* change per round, this picks the single highest-value *large* one: the rearchitecture, the real replacement for a naive approach, the redesign that would obviously make things better if only someone dared to do it. Go big. Then prove it landed.

**The discipline is what makes "big" safe.** A big change that isn't verified is how a working project turns into a broken one while looking more impressive. So the rule is unchanged from `/improve` — measure, keep only what genuinely wins, revert what doesn't — but the *ambition per round* is turned all the way up. Bold in what you attempt; ruthless about proving it worked.

## Work file by file, in order — do NOT jump around

This is the defining rule of the skill. When the target is a whole codebase ("improve all the files and make big changes"), you go through the files **one at a time, in a fixed sorted order**, and you **finish one file before moving to the next**. File 1 gets its big change and is done; then file 2, then 3, 4, 5, 6 … until every file has been reached. You do not hop to a different file mid-file.

- **Build the file list first and sort it once.** List every file in scope and put it in a stable order (a sensible default: dependency/foundation order — shared types, core/util, then things built on them; otherwise alphabetical by path). Write the ordered list down (e.g. `BIG-CHANGE.md`) with a checkbox per file so progress is visible and a compaction can't lose your place. This order is fixed for the run.
- **One file is the unit of work.** For the current file, make its big change fully (see "What one file's big change is"), verify, keep-or-revert, tick it off — *then* advance to the next file in the list. Never skip ahead.
- **Dependencies do NOT reorder the work.** This is the trap to avoid: if file 1 would be better once file 4 changes, you **do not** jump to file 4. You make file 1's big change now, working with file 4 as it currently is; file 4 gets its own big change when the sweep reaches it in order. Following dependency links around the tree is exactly the jumping-around this skill forbids — it leaves half-changed files everywhere and loses the plot. Sorted order wins over dependency convenience.
  - The one exception: if changing the current file *forces* a small mechanical edit in another file to keep the project runnable (e.g. you renamed an export and its importers must update), make that minimal follow-through edit — but that's carrying your change's blast radius, not "improving file 4." File 4 still gets its own big change later, in order.
- **Reached-everything is the finish line.** The sweep ends when every file on the list has had its turn (each either got a kept big change, or was consciously judged to need none — recorded either way).

## How many changes / how much scope

Parse the invocation:
- **`big-change`** (no number) → the default **full file-by-file sweep**: every file in scope, in order, as above.
- **`big-change N`** → do the sweep but stop after **N files** have had their turn (e.g. `big-change 5` → files 1–5 in order, then stop). Resume from file 6 next time.
- **A single named target** ("big-change on parser.py") → just that file's big change.

If there's no obvious target (no current project/task in play), ask the user what to transform before starting.

**Pin a baseline before file 1.** Capture what "better" means for this work up front — test count/pass rate, the benchmark/backtest number, bundle size, latency, lint-clean status, the actual UX, whatever applies — and note it. Big changes move big numbers; you'll compare against this fixed start and report the net delta at the end, so the impact is concrete ("312→196 ms p95, 480→512 tests, three modules collapsed into one") not a vibe.

## What makes a change a "big change"

A big change is one that alters *structure, approach, or scope* — not just a line here and there. Reach for these:

- **Rearchitect** a module or the boundaries between modules — split a god-object, collapse three overlapping systems into one, invert a bad dependency.
- **Replace a naive approach with a real one** — swap the O(n²) loop for the right algorithm/data structure, the polling for events, the ad-hoc parser for a proper one, the toy version for the production one (pairs with [[full-implement]]).
- **Redesign** a UI/flow/API surface so it's genuinely good, not just repainted.
- **Change the data model** — the schema, the core types, the state shape — and carry every call site with it.
- **Cut hard** — delete a whole subsystem that's carrying its weight in complexity but not value, and fold what's needed into something simpler.
- **Introduce the abstraction that was missing** — the one that makes a dozen scattered special-cases become one clean path.

If the change you're about to make could be described as "a tweak," it's an `/improve` change, not a big one. Pick something with real blast radius. **"Improve all the files and make big changes" means sweep the whole tree and, wherever a file (or a cluster of files) would benefit from a bold rewrite, do the bold rewrite — not a light polish.**

## What does NOT count as a big change (non-negotiable)

A big change is **real, working, functional code that changes what the file actually does.** The following are explicitly **not** big changes and must never be counted as one, presented as one, or used to mark a file "done":

- **Comments, docstrings, or renaming** — documenting or relabeling existing code changes nothing about how it runs. (Comment where genuinely needed as a *side effect* of a real change, but the comment is never the change.)
- **Placeholders of any kind** — `TODO`, `FIXME`, "your logic here", "implementation left as an exercise," a function that just `pass`/`return None`/`throw NotImplemented`.
- **Non-functional or dummy code** — hardcoded fake return values, canned sample data standing in for real logic, mock/simulated behavior presented as the real thing, a UI that looks wired but does nothing.
- **API / integration placeholders** — `API_KEY = "your-key-here"`, a stubbed client that returns a fixed response, an endpoint that echoes a fixture instead of doing the work, a "connect X later" shim.
- **Dead scaffolding** — empty classes/interfaces/config blocks, commented-out "future" code, feature flags gating nothing.
- **Cosmetic churn** — reformatting, reordering imports, whitespace, moving a file (that's [[sort]]) — none of it changes behavior.

If a file's "big change" would consist of any of the above, it is **not done** — either make a real functional change to that file or record it as *left as-is* (needs none). And the reverse: a big change must **replace** placeholders/stubs/dummy logic with real implementations, never introduce them. Turning a stub into working code is a perfect big change; turning working code into a prettier stub is a regression. If you find you *can't* implement the real thing for a file (missing spec, external dependency you don't have), say so plainly and leave it — do **not** paper it over with a placeholder and call it a change. This pairs with [[placeholder-replacer]] and [[full-implement]], whose whole job is making non-real code real.

## "Real" is not "big" — the size-and-ambition bar (the loophole this skill actually falls through)

The list above catches *fake* changes. This section catches the far more common way `/big-change` underdelivers: **small, real, safe changes counted as big.** A change can be 100% genuine working functional code and still not be a big change. Real is necessary; it is not sufficient. **Big is about structural blast radius**, and the tell that you missed the bar is simple: if someone diffs your "big change" and the biggest thing in the whole sweep is a handful of lines, they will say *"the biggest change you made was 60 lines lol"* — and they will be right that you ran [[improve]] and mislabeled it.

**These are `/improve`-tier, NOT big changes — no matter how clean or correct:**
- Extracting a duplicated helper into a shared file (`ip_link()`/`pid_running()` → `lib/common.sh`). Good dedup. Not a rearchitecture.
- Adding a flag or option to an existing script (`--status`, `--stop`, `--alert-below`, `--list`).
- Adding a `confirm()` gate, a guard, a timeout, or an error check around code that otherwise runs unchanged.
- Merging two near-identical functions into one (`run_device`+`run_network` → `run_filter`). Nice consolidation. Still a tweak in size.
- Fixing a bug, honest-return-value corrections, a one-line safety net.

Every one of those is a legitimate, valuable `/improve` change — and if the biggest thing you did to a file (or across the entire sweep) is one of them, **you did an improve pass, not a big-change pass.** Ship them under `/improve`; don't dress them up as big.

**What clears the bar — the diff reads like a rewrite, not a patch:**
- A large fraction of the file is rewritten, or a whole new capability/subsystem is added or removed.
- The file's *core approach* changes: the algorithm, the data model, the control flow, the module boundary — not just what's wrapped around it.
- A naive implementation is replaced by a real one end to end (the whole point of pairing with [[full-implement]]).

Rules of thumb, for calibration (not hard gates): a real big change usually moves a *substantial* portion of the file, not ~20 lines around otherwise-untouched code. If the whole sweep's largest single change is tiny, the sweep was not bold — it was cautious, and that's fine only if you **say so honestly** instead of relabeling caution as ambition.

**The self-check, per file and at the end:** *"If I showed this diff to the user and called it a 'big change,' would they laugh?"* If yes, there are exactly two honest moves — **go bigger** (make the change this skill actually asks for), or **record the file as consciously-left-small with the real reason** (already excellent; genuinely trivial; incident-prone code you're deliberately not rearchitecting — see below). Dressing the tweak up as big is the one move that's banned.

**Caution on risky files does not excuse timidity everywhere.** Deliberately leaving incident-prone code alone (radio/bridge/anything that already bit you this session) is legitimate and correct — record it and move on. But that verdict applies to *those* files, not as blanket permission to make every *other* file's change small and safe. The files you *do* choose to change must get actual big changes, or the run isn't a big-change run. A sweep where the risky files were skipped (fine) **and** every touched file got a 20-line dedup (not fine) is an improve sweep wearing this skill's name.

## What one file's big change is

For the current file in the ordered list:

1. **Read the file and decide its big change.** Look at *this* file and pick the one transformation that would most improve it — the boldest change that makes sense for this file (from the menu above: rearchitect it, replace its naive approach, redesign its surface, tighten its data handling, cut its dead weight, introduce the missing abstraction). Across the sweep, the *kind* of change naturally varies file to file — don't force the same move on every file.
2. **Plan its blast radius before you cut.** A big change to one file still ripples outward — the callers, imports, tests, config, docs that touch it. Know what your change to *this* file will affect so you carry those references and don't leave the tree half-wired. Sketch it first for a large one; show the user for a risky one.
3. **Make the change fully — end to end, no half-migration.** This is the core of the skill: don't be timid, don't leave the old and new paths both half-wired inside the file. Do the whole thing for this file, and carry the minimal follow-through edits its blast radius forces in other files (step 2) so the project still runs. A file left half-rewritten is worse than not starting — finish it before moving on.
4. **Prove it's actually better — measure, don't assume.** Run the real tests/benchmark/build and compare against the state *before* this file's change. Big changes have big downsides when wrong; a shallow "looks fine" is not enough. Verify the way the project actually validates. For UI/UX, verify concretely (it runs, it renders, the flow works).
5. **Keep it only if it genuinely wins; otherwise revert cleanly.** A bold change that measures neutral-or-worse gets fully reverted — that file still counts as *reached* (you tried, you learned). A partial revert that leaves debris is not acceptable; because you planned the blast radius (step 2) you can undo the whole thing (prefer git — see safety net).
6. **Tick the file off and log it** briefly: file → what you rewrote → what you measured → kept or reverted. Then, and only then, **advance to the next file in the sorted list.**

## Safety net (big changes need one)

Because each file's change moves a lot of code, make reverting trivial **before** you start cutting:
- **Git repo?** Ensure the tree is clean or commit first, so a bad change reverts with `git restore`/`git reset`. Commit after each *kept* file so every file's big change is an isolated, revertible unit — this pairs perfectly with the file-by-file order. Consider a branch for the whole sweep.
- **Not a git repo?** Offer to `git init`, or at minimum back the project up first. Say plainly that without version control, a big change is much harder to undo by hand.

## Running the sweep

Walk the sorted file list top to bottom. For each file, do "What one file's big change is," then move to the next — **in order, no jumping.** Between files, keep the project runnable and (ideally) committed. Update the checkbox list as you go so progress survives a compaction.

**Every file gets reached.** A file counts as done when it either got a kept big change or was consciously judged to need none (a file that's already excellent, or genuinely trivial — record that verdict, don't invent a rewrite for it). Don't silently skip files; an untouched file must be a recorded decision, not an oversight.

**Don't manufacture churn.** If a file genuinely doesn't want a big change, say so and move on — a pointless rewrite that risks working code is worse than leaving a good file alone. Boldness is the default, but "this file is already right" is a legitimate verdict when it's true (and it usually isn't, on files that look rough).

**Waiting on data / a build / a background job does not pause the sweep.** Keep moving down the file list; the order doesn't depend on any external job.

## Composes with

Pair with **`/control`** for a STOP button on a long run, **`/work-until-limit`** to bound it by quota (there the ceiling wins over "ran out of changes" — switch kinds and keep going), **`/full-implement`** when the big change is "make this toy real," **`/backup`** for a pre-run snapshot, and **`/shutdown-when-done`** to power off at the end. If a change turns out to need care rather than boldness in one spot, that spot can be handled with [[fix]] — but this skill's default is: go big.

## Finish

Summarize **by file, in the order you swept them**: for each file, what its big change rewrote/redesigned, what was measured, and whether it was kept, reverted, or left as-is — plus the **net improvement from start to finish** as concrete numbers, and how many of the in-scope files were reached. Be honest — if only 4 of 12 files got a change that actually won, say so; a handful of real transformations with evidence beat a dozen impressive-sounding rewrites with none.

**Name the single biggest change, with its size.** State the largest transformation in the whole sweep and roughly how much it moved (lines rewritten, module collapsed, approach replaced). This is the honesty check the whole skill turns on: if the biggest thing across the entire run is a small dedup or an added flag, the summary must say plainly *"this ended up an improve-tier sweep, not a big-change one — I chose consolidation/caution over bold rewrites"* and why, rather than presenting a pile of tweaks as bold work. A run that reports its own largest change as 60 lines has answered the question — that wasn't a big-change sweep, and the report should admit it instead of dressing it up.
