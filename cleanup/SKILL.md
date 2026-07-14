---
name: cleanup
description: Revamp a codebase into a clean, well-organized, production-ready state — remove dead/old code, reorganize files into a sensible folder structure and move them where they belong, add clarifying comments and docstrings, improve naming and formatting, and make the whole thing readable and ready to run. Use whenever the user invokes /cleanup or asks to "clean up the codebase", "restructure this project", "organize these files into folders", "remove old code", "make this production-ready", or "tidy everything up". This changes real files and moves things, so it works incrementally and verifies nothing breaks at each step.
---

# Cleanup

> **Skill restriction — not compatible with `/careful`.** Cleanup restructures the codebase broadly — moving files, removing dead code, reorganizing folders; `/careful` mode forbids exactly that kind of change. They directly contradict, so don't run both together. The "be careful" intent is already built into this skill (safety nets, small verified steps), so run `/cleanup` on its own.

Transform a messy, working codebase into a clean, organized, production-ready one — **without changing what it does.** That constraint is the whole game: a "cleaner" codebase that no longer runs is a failure, not an improvement. Reorganization is deceptively dangerous — moving a file breaks every import that pointed at it, and "old code" is often still referenced somewhere you haven't looked. Move deliberately, verify constantly.

## Step 0: Establish a safety net before touching anything

Restructuring is hard to undo by hand. Before the first move or deletion:

- **If it's a git repo:** confirm the working tree is clean (or commit current state first) so everything is recoverable with `git restore`. Do the whole cleanup on a branch if the user is open to it.
- **If it's NOT a git repo** (check — some projects aren't): this is riskier. Offer to initialize git first for a safety net, or at minimum make a full copy of the project to a backup folder before restructuring. Say plainly that without version control, mistakes are harder to reverse.

Don't skip this. The user is trusting you to reshape their project; give them a way back.

## Step 1: Understand before you change

Survey the whole project first — you can't safely reorganize what you don't understand:

- Map the directory tree, entry points, and how modules import/reference each other.
- Identify what's actually run (entry points, tests, scripts) versus what might be dead.
- Note the existing conventions so your cleanup follows the project's own grain rather than imposing a foreign structure.
- Find how the project is verified — a test suite, a run command, a build. **You'll use this after every structural change**, so locate it now.

## Step 2: Do the work — in this order, verifying as you go

Sequence matters: prove things still work before piling on more change. After each structural step, re-run the project's tests / run command and confirm it's still green before continuing.

### 2a. Remove dead and old code — but prove it's dead first
- Before deleting anything, **search the whole codebase for references** to it (grep for the name, the import, the filename). Code can be reached dynamically — reflection, string-based imports, config, entry points — so absence of a direct call isn't proof it's unused. When in doubt, keep it and flag it to the user rather than deleting.
- Remove commented-out blocks, unused imports, unreachable branches, obsolete files, and duplicate implementations — once confirmed unreferenced.
- **Deletions and anything you're not certain is dead: list them and get the user's go-ahead** before removing. Losing working code is the worst outcome here.

### 2b. Reorganize into a sensible structure
- Group files by responsibility into clear folders (e.g. `src/`, `tests/`, `scripts/`, `config/`, `docs/` — adapt to the language and project).
- **When you move a file, immediately update every reference to it** — imports, path strings, config, build files, test paths. A move isn't done until all references resolve. Move in small batches and verify after each batch, not all at once.
- **Record every move in a `CLEANUP.md` manifest as you go** — a simple `old/path.py → new/path.py` table. After a restructure, the user (and any external scripts, docs, IDE bookmarks, or their own muscle memory) needs a map to find things again; a moved-without-a-map project is disorienting. Keep it updated live, not reconstructed from memory at the end.
- Don't over-engineer the structure; match the project's scale.

### 2c. Improve readability
- Add comments and docstrings where intent isn't obvious — explain the *why*, not the obvious *what*. Don't bury clear code in noise.
- Improve unclear names, fix inconsistent formatting, apply the project's formatter/linter if it has one.
- Preserve behavior exactly — this is tidying, not rewriting logic.

### 2d. Production-readiness pass
- Remove debug prints, leftover scratch/temp files, and dead feature flags.
- Flag (don't silently commit) anything sensitive you find — hardcoded secrets, keys, tokens — and tell the user to rotate/remove them.
- Confirm the project still starts and runs from its entry point, and that setup/run instructions still match reality.

## Step 3: Verify the whole thing end-to-end

After all changes: run the full test suite and the actual entry point one more time. **The bar is that it behaves exactly as it did before cleanup** — same outputs, same tests passing. If anything regressed, fix it or roll that piece back before finishing. Don't hand back a codebase you haven't confirmed still works.

## Step 4: Report

Summarize what changed, grouped for easy review:
- **Removed** — what dead code/files were deleted (and confirm they were verified unused).
- **Moved/restructured** — the new folder layout and what went where.
- **Improved** — comments, naming, formatting changes.
- **Flagged** — anything you deliberately left alone, couldn't verify as dead, or that needs the user's attention (e.g. secrets to rotate).
- **Verification** — that tests/run still pass, stated honestly.

## What not to do

- Don't delete code you can't prove is unused just because it looks obsolete.
- Don't move a batch of files and leave broken imports "to fix later" — resolve references as you go.
- Don't change logic or behavior in the name of cleanup; if you spot a real bug, report it separately rather than silently "fixing" it mid-restructure.
- Don't do the whole revamp in one big unverified sweep — incremental, verified steps are what keep a working codebase working.
