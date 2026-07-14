---
name: map
description: Understand the user's request in depth, plan it thoroughly, and lay out the work as a tracked task list before doing it. Produces a scratch Plan.md (the deep thinking) plus a Tasks.md in the project with numbered checkbox tasks and a description of each, then executes the tasks and checks them off. Use whenever the user invokes /map or asks to "map this out", "plan this first", "break this into tasks", "make a plan and task list", or wants a structured plan-then-execute approach to a non-trivial request. Best for multi-step work where getting the plan right up front matters.
---

# Map

Turn a request into a clear plan and a living task list, then carry it out. Two files with two different jobs:

- **Plan.md** — your deep thinking. Where you work out *how* to approach the problem. It's scratch: it lives in the skill folder (out of the user's project) and gets deleted when the work is done.
- **Tasks.md** — the durable, human-readable checklist. It lives in the project, tracks progress with checkboxes, and stays behind as a record of what was done.

## Step 1: Understand the request — really understand it

Before planning, make sure you know what the user actually wants. Restate the goal in your own words. If something essential is genuinely ambiguous (a fork that would change the whole approach), ask a short clarifying question now — a wrong plan is expensive to unwind. Don't ask about things you can reasonably decide yourself.

## Step 2: Plan greatly — write Plan.md

Write your full plan to **`C:/Users/flori/.claude/skills/map/Plan.md`** (in the skill's own folder, deliberately *not* in the user's project). This is where you think hard and at length — it costs nothing because it's thrown away after. Cover:

- **Goal** — what success looks like, restated precisely.
- **Constraints & context** — what's fixed, what the environment requires, what to avoid.
- **Approach** — the strategy, the architecture, how the pieces fit.
- **Alternatives considered** — options you weighed and why you picked this one (keeps you from second-guessing mid-run).
- **Sequencing & risks** — the order of work, dependencies between steps, and the edge cases or failure points to watch.
- **Task decomposition** — the concrete steps, which become Tasks.md next.

Plan for real here. The quality of everything downstream depends on this being thought through, not rushed.

## Step 3: Derive Tasks.md — in the project

Write **`Tasks.md` in the current project directory** (the project root, not the skill folder). Use GitHub-style checkboxes so the list renders as real, tickable boxes on GitHub — a numbered list where each item is `N. [ ]` (open) or `N. [x]` (done), then a descriptions block where every entry begins with "For N.":

```markdown
# Tasks

1. [ ] Create "Hello World"
2. [ ] Display a UI
3. [ ] Wire the button to the handler

---

For 1. You should create a python script that prints "Hello World", then verify it runs.

For 2. You should build a small window with a single button labeled "Go", using tkinter.

For 3. You should connect the button's click event to the handler from task 1 so pressing it prints the greeting.
```

Rules for Tasks.md:

- **Checkbox states:** `[ ]` (a space between the brackets) = not done yet, `[x]` (lowercase x) = done. Every task starts as `[ ]`. This is the exact syntax GitHub renders as a checkbox — keep the space inside the brackets for open items.
- **Tasks are numbered** (`1.`, `2.`, `3.`…) and each is a short imperative title.
- **Descriptions go below the list**, separated by a `---`. Each description **always starts with "For N."** (matching the task's number) and explains concretely what that task involves — enough that the work is unambiguous.
- Keep titles terse and descriptions specific. Order tasks in the sequence they'll be executed.
- **End each description with a one-line acceptance criterion — `Done when: <objective check>`** (e.g. "Done when: `python game.py` runs and accepts a guess"). This makes "done" verifiable rather than a matter of opinion, so a box only gets ticked when the criterion is actually met — not when it merely *feels* finished.

## Step 4: Execute, checking tasks off as you go

Work through the tasks in order. As each one is genuinely finished, update its line in Tasks.md from `[ ]` to `[x]` — edit the file so the checklist always reflects reality. This makes progress visible to the user at a glance and leaves an accurate record if the session is interrupted. If the plan needs to change mid-run (a task turns out wrong, a new one is needed), update Tasks.md to match — the checklist should never lie.

## Step 5: Clean up — delete Plan.md

Once the run is complete (all tasks done, or the work reached a natural stopping point), **delete `C:/Users/flori/.claude/skills/map/Plan.md`**. Its thinking has served its purpose and shouldn't linger. **Leave Tasks.md in the project** — it's the deliverable record, with its boxes checked.

Then give the user a one or two sentence wrap-up: what got done, and that Tasks.md in the project holds the completed checklist.

## Notes

- If the user only wants the plan and task list *without* executing yet, stop after Step 3, keep Plan.md for now, and tell them the tasks are laid out and ready — delete Plan.md only once the run actually happens.
- Only one Plan.md exists at a time in the skill folder; if a stale one is there from a previous run, overwrite it.
