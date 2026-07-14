---
name: sort-prompt
description: Take a big, messy, stream-of-consciousness prompt or spec and reorganize it into clean, structured, readable text — grouped by topic, in logical order, every requirement preserved. Does NOT build or implement anything; it only sorts and clarifies what the user wrote, and flags contradictions/ambiguities for them to confirm. Use whenever the user invokes /sort-prompt or says "sort this", "clean this up", "organize these requirements", "make sense of this brain-dump", or pastes a long unsorted list of features/ideas and wants it tidied. Faithful reorganization, not redesign.
---

# Sort Prompt

The user has dumped a lot of thoughts at once — run-on sentences, jumbled order, ALL-CAPS emphasis, repeated or half-finished points. Turn it into clean, organized text they (and later, whoever builds it) can actually read and act on. **You are sorting and clarifying, not designing or building.**

The one rule that matters most: **be faithful.** Preserve every requirement and every specific value the user gave (numbers, timings, names, ordering). Don't drop anything, don't invent anything, don't "improve" their idea or resolve their contradictions silently. If they said 10 seconds, it stays 10 seconds.

## How to sort

1. **Extract every distinct point.** Read the whole dump and pull out each separate requirement/intent as its own atom — including the ones buried mid-sentence or shouted in caps. Losing a detail is the main failure mode; be thorough.
2. **Group into logical sections.** Cluster related atoms under clear headings (e.g. "Login flow", "Invite codes", "Server CLI", "Panic mode"). Let the natural topics emerge from the content.
3. **Order sensibly.** Within a section, sequence things logically (a described flow in step order; settings grouped). Put the most foundational sections first.
4. **Rewrite each point cleanly** — concise bullet or numbered step, fixed grammar/typos, but the **same meaning and the same exact values.** Keep a hard requirement's emphasis (a "MUST") when the caps clearly signal one; drop the shouting, keep the intent.
5. **Separate facts from questions.** Put clear requirements in the body; collect anything **contradictory, ambiguous, or underspecified** into an **"Open questions / to confirm"** list at the end — surface them, don't decide them. (E.g. two timings that don't add up, a "delete files" with unclear scope, "strong encryption" with no method named.)
6. **Do NOT implement, design an architecture, or add features.** Only when they later say "build it" does that begin — this skill stops at clean text. Offer to save it to a file (e.g. `SPEC.md` / `REQUIREMENTS.md`) if useful.

## Output shape

```markdown
# <Title> — sorted requirements

## <Section>
- clean requirement (exact values preserved)
- ...

## <Section>
1. step one
2. step two   (ordered flows as numbered lists)

## Open questions / to confirm
- the ambiguity or contradiction, phrased as a question for the user
```

## Detect duplicates

Brain-dumps repeat themselves — the same requirement stated twice in different words, or a point circled back to later. **Consolidate each into one clean entry**, but don't silently vanish the repeats: note where you merged them (e.g. "*(consolidated from 2 mentions)*") so the user can see nothing was lost and confirm you read them as the same thing. If two "duplicates" actually differ in a detail, that's not a duplicate — keep both and, if they conflict, flag it in Open questions.

## What not to do

- Don't drop or merge-away any requirement, however small or oddly phrased.
- Don't add requirements, features, or "you should also…" suggestions — that's not sorting. (If you genuinely spot a gap, put it as a *question* in Open questions, not as a new requirement.)
- Don't silently resolve contradictions or pick values the user didn't give.
- Don't start building. Clean text is the whole deliverable.

## After sorting

Give the user the clean text. Then, if they want to act on it, the sorted spec is a perfect input for [[map]] (turn it into tasks) or [[later-ideas]] (park the parts that are too early) — point them there rather than jumping into code yourself.
