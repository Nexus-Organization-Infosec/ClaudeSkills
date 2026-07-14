---
name: later-ideas
description: Park and develop ideas for the project without building them yet — the user brainstorms an idea, Claude fleshes it out (angles, how it could work, prerequisites, rough approach) and files it in a backlog, but does NOT implement it now because the project is still too small/early. Invoked as "/later-ideas <idea>" to capture & extend an idea, or "/later-ideas use" to actually implement the parked ideas when the project is ready. Use whenever the user invokes /later-ideas, or says "save this idea for later", "park this", "note this down for when we're bigger", or "don't build it yet, but…". Resurfaces ready ideas when the project has grown enough.
---

# Later Ideas — parked backlog

The user has ideas for where the project could go, but it's too early to build them — the foundation isn't there yet. The job is to **capture and develop** those ideas so none are lost and each is richer for later, **without implementing them now.** Then, when the project has grown enough (or the user says `use`), pick them up.

The discipline that matters: in capture mode, **resist the urge to build.** The user explicitly wants these deferred. Develop the idea on paper; don't touch the code.

## The backlog file

Store everything in **`LATER_IDEAS.md`** in the project root (create it if missing) — visible, versionable, one entry per idea:

```markdown
# Later Ideas — parked backlog
Ideas to build once the project is mature enough. Not implemented yet.

## [ ] <Short idea title>
- **Captured:** <date>
- **The idea (yours):** what the user proposed, in their framing.
- **Extended:** the developed version — angles, variations, how it could work, why it's valuable, risks/trade-offs.
- **Ready when:** the concrete prerequisite(s) — what the project needs to exist/reach before this is worth doing.
- **Rough approach:** a sketch of how it'd be built (not code, just the shape).
```

`[ ]` = parked, `[x]` = done once implemented.

## Mode 1 — Capture & extend (the default)

When the user gives an idea (`/later-ideas <idea>` or "park this for later"):

1. **Understand it** — what they're really after.
2. **Extend it — this is the deliverable.** Turn the one-liner into a developed concept: flesh out how it could work, note variations and alternatives, what makes it valuable, the trade-offs and risks, and where it would hook into the eventual architecture. Add genuine thinking the user didn't spell out — that's the point of parking it with an AI rather than a sticky note.
3. **Judge "ready when"** — honestly name what the project needs first (a real user base, a certain module, more data, whatever), so future-you knows when to pull it off the shelf.
4. **Append it to `LATER_IDEAS.md`** in the format above.
5. **Do NOT implement it.** Confirm it's parked and developed, in a sentence or two — don't start coding it, don't "just scaffold a bit."

## Mode 2 — Use (implement the parked ideas)

When the user invokes **`/later-ideas use`** (or "let's do the parked ideas now"):

1. **Read `LATER_IDEAS.md`.**
2. If there are several, **briefly list them and ask which to build** (or build the ones whose "ready when" is clearly met) — don't assume all at once unless they say so.
3. Implement the chosen idea(s) properly now — this is normal build work; use the [[map]] or [[improve]] skills if it helps.
4. **Mark each done** (`[ ]` → `[x]`) in `LATER_IDEAS.md` as it ships, leaving the record intact.

## Mode 3 — Resurface when ready

The user wants to be reminded when the project is far enough along to tackle a parked idea. Whenever you have the backlog in view — on any `/later-ideas` invocation, and whenever you notice during other work that an idea's **"ready when"** condition is now met — **raise it once**: "the project now has X, so the parked idea *Y* is doable — want me to?" Mention it once and drop it if they pass; don't nag every turn.

**Honest limit:** a skill only runs when invoked, so Claude can't watch the project in the background forever. For a truly proactive nudge, either check `LATER_IDEAS.md` at natural milestones, or drop a note in memory / a scheduled check (the `schedule` skill) so the reminder fires on its own. Offer that if the user wants guaranteed resurfacing.

## Mode 4 — Review (which parked ideas are ready now?)

When the user invokes **`/later-ideas review`** (or "which ideas are ready?", "go through the backlog"):

1. **Read `LATER_IDEAS.md`** and, for each parked idea, **check its "Ready when" against the actual current project state** — does the prerequisite module/scale/data now exist? Look at the code to judge, don't rely on memory of where the project was.
2. **Report a verdict per idea:** ✅ ready now (prerequisite met), ⏳ not yet (say what's still missing), or ❓ needs a call from the user.
3. Offer to build the ready ones (hand off to Mode 2 / [[map]]). This turns the passive backlog into an active, on-demand readiness check — the manual version of the resurfacing in Mode 3.

## Notes

- Keep captured ideas honest — if an idea is genuinely bad or redundant, say so when capturing rather than politely filing junk.
- This is about *project* ideas; it pairs naturally with `/map` and `/improve` when the ideas finally get built.
