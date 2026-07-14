---
name: quick-map
description: Quickly turn a request into a short task checklist and get going — a lightweight Tasks.md with GitHub checkboxes, no deep planning, minimal talk. Use whenever the user invokes /quick-map or says "quick plan", "just list the steps", or "break this into a few tasks and start". The lightweight counterpart to [[map]] — for deep up-front planning (a full scratch Plan.md, alternatives weighed, detailed per-task descriptions), use that instead. Part of the /quick family — do the work, keep the chatter to a minimum.
---

# Quick Map

Turn the request into a short task list and start — fast, minimal talk. This is the light version of [[map]]: skip the deep scratch `Plan.md` and the elaborate planning; just lay out the steps and go.

## What to do

1. **Write a short `Tasks.md`** in the project root — GitHub-style checkboxes, one short line per task, in order:

   ```markdown
   # Tasks
   1. [ ] First step
   2. [ ] Second step
   3. [ ] Third step
   ```

   Keep the space in `[ ]` (open) / use `[x]` (done) so it renders as real checkboxes on GitHub. A brief description under a task only if it's genuinely unclear — otherwise the titles are enough (that's what makes this the *quick* version).

2. **Execute**, flipping `[ ]` → `[x]` in `Tasks.md` as each task is genuinely done, so the list always reflects reality.

3. **Report in a line** when done. No essay.

## Keep it light

- **No `Plan.md`, no deep-planning ceremony.** If the request is big or high-stakes enough that getting the plan right up front really matters — weighing alternatives, thinking through architecture — that's [[map]], not this. Point there and switch.
- **For a tiny job (≤3 steps), skip the file entirely.** Don't write a `Tasks.md` for three obvious steps — just track them inline with the harness task list and do them. The file is worth it only when there are enough tasks that a written, checkable list actually helps; below that it's ceremony that slows the quick path down.
- Don't over-decompose; a handful of clear tasks beats twenty micro-steps.
