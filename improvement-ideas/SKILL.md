---
name: improvement-ideas
description: Give the user a curated list of IDEAS for the project — things to improve, bugs or weaknesses worth fixing, features that could be freshly implemented, and opportunities they may not have considered. This skill only PROPOSES; it does not build anything. Study the actual project first, then hand back a ranked, concrete idea list (what, why it helps, rough effort). Use whenever the user invokes /improvement-ideas or asks "what could I improve", "give me ideas", "what should I add next", "what's worth fixing", "how could this be better", or "what would you build into this". Ends by asking which ideas (if any) to actually do. Pairs with [[improve]], [[new-features]], [[fix]], and [[later-ideas]] for acting on the picks.
---

# improvement-ideas

Hand the user a concrete, ranked menu of ideas for THEIR project. This is a proposal skill — you investigate and suggest, you do **not** implement. Nothing gets built until the user picks.

## Step 1: Actually look at the project

Ideas must come from the real codebase, not from generic "best practices". Before writing a single suggestion:

- Skim the structure, entry points, README/docs, and the main modules to learn what the project *is* and what it's trying to do.
- Note the current state: what works, what's rough, what's stubbed or half-done, what looks fragile, what's missing.
- Check for existing signals: `TODO`/`FIXME`, open notes, a backlog/ideas file, recent changes, failing or absent tests.

Generic ideas that could apply to any repo ("add tests", "improve error handling") are near-worthless unless you tie them to a specific place and reason in *this* code. Ground every idea.

## Step 2: Build the idea list — four kinds

Cover these categories (skip one only if it genuinely has nothing):

1. **Improvements** — make something existing better: clarity, performance, UX, robustness, structure. Point at the specific thing.
2. **Fix ideas** — real bugs, weaknesses, risks, or fragile spots worth fixing. Say what breaks and when.
3. **Fresh implementations** — new features or capabilities that would genuinely fit the project and add value. Not filler; things that make sense for what this is.
4. **Opportunities** — bigger-picture or non-obvious ideas: a direction, an integration, a simplification, something the user probably hasn't considered.

## Step 3: Present it — ranked and concrete

- **Rank by value-for-effort** — best bang-for-buck first, so the top of the list is the stuff most worth doing.
- For **each idea** give, briefly:
  - **What** — the concrete change, tied to a real file/area where possible.
  - **Why** — the benefit, or what it fixes/unlocks. If it's a bug, when it bites.
  - **Effort** — a rough size (small / medium / large).
- Keep each idea tight — a couple of lines, not an essay. Aim for roughly 6–12 solid ideas, not a padded wall. Quality and specificity over quantity; a few sharp ideas beat twenty vague ones.
- Group by the four kinds, or interleave by rank — whichever reads clearer for this project.

## Step 4: Hand off

End by asking which ideas the user wants to actually do — then act on the picks with the right skill: [[improve]] for polishing, [[new-features]] for building, [[fix]]/[[quick-fix]] for bugs, or [[later-ideas]] to park the ones for when the project is bigger. Do NOT start building anything in this skill; proposing is the whole job.
