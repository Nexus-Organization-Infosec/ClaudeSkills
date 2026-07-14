---
name: quick-documentate
description: Write a concise overview doc for the project quickly — what it is, how to run it, and the key files — as a short Markdown file, with minimal talk. No deep code investigation, no exhaustive sections. Use whenever the user invokes /quick-documentate or says "quick docs", "just a short README", or "brief overview of this project". The lightweight counterpart to [[documentate]] — for the deep, exhaustive writeup (architecture, findings, what-was-lost, every component), use that instead. Part of the /quick family — do the work, keep the chatter to a minimum.
---

# Quick Documentate

Produce a short, useful overview of the project fast — no deep investigation, minimal talk. This is the light version of [[documentate]]: skip the exhaustive architecture-and-findings audit; just capture the essentials someone needs to understand and run the thing.

## Output

Default to a Markdown file (`OVERVIEW.md` in the project root, unless the user names another) — no format question, keep it quick. Cover just the essentials, concisely:

```markdown
# <Project> — Overview
One or two sentences on what it is and does.

## How to run
The concrete command(s) to set up and run it.

## Key files
- path — what it's for   (the handful that matter, not everything)

## Notes
Anything important to know at a glance (main config/knobs, gotchas).
```

## How to work

- **Update, don't duplicate.** First check for an existing `README.md` / `OVERVIEW.md` / docs. If one exists, refresh *that* file rather than creating a competing new one — two overlapping overview docs is worse than one. Only create `OVERVIEW.md` when there's nothing to update.
- **Skim, don't excavate.** Read the entry point and the few key files to get it right — but this is a quick overview, not the deep `/documentate` investigation of every module, decision, and dead end.
- Be accurate over exhaustive: a short doc that's correct beats a long one padded with guesses. If you're unsure about something, leave it out or note it briefly rather than inventing it.
- Report in a line when done (where the file is). No essay.

## Escalate when needed

If the user actually wants the deep writeup — architecture, component-by-component, findings, what-was-tried-and-abandoned — that's [[documentate]], not this. Point them there.
