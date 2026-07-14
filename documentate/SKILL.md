---
name: documentate
description: Produce deep, comprehensive documentation of an entire project — everything that was built and how it works, the architecture and data flow, key decisions and their rationale, what was tried and abandoned ("what was lost"), findings and discoveries, configuration/knobs, how to run and test, known issues, and open questions. This is an exhaustive investigation, not a quick summary. Use whenever the user invokes /documentate or asks to "document everything", "write full docs for this project", "explain how the whole thing works", "create a deep technical writeup", or similar. Always ask which output format they want first — Markdown (.md, default), PDF, or plain text (.txt) — unless they already said.
---

# Documentate

The goal is a document so thorough that someone who has never seen this project — or the user themselves in six months — could understand what exists, how it works, why it was built that way, and what was learned along the way. Shallow docs are near-worthless; the value is entirely in the depth. Take the time to actually read the code, not just list the files.

**Update mode (when docs already exist).** If there's already a doc from a previous run, don't rewrite it from scratch — *refresh* it. Diff the doc against the current code (what changed since it was written: new/removed/renamed modules, changed behavior, new config), and update only the sections that drifted, preserving the rest. Docs going stale is documentation's number-one failure mode, so a cheap update path is what keeps them alive. Note at the top when the doc was last refreshed.

## Step 0: Ask the output format (unless already specified)

Before investigating, confirm the format — it changes how you write and deliver the final file:

- **Markdown (`.md`)** — the default. Rich structure, headings, tables, code blocks. Best for reading in an editor or on GitHub.
- **PDF** — a polished, portable document. Write the content as Markdown/HTML first, then convert (see "Delivering the file").
- **Plain text (`.txt`)** — no markup. Use when the user wants something dependency-free and universally openable.

If the user already named a format in their request, skip the question and use it. Otherwise ask once, briefly, then proceed.

## Step 1: Investigate deeply — this is the real work

Do not write a word of the document until you actually understand the project. Budget most of your effort here. Work systematically:

1. **Map the whole thing.** Walk the directory tree. Identify entry points, the main modules, tests, scripts, config, and generated/vendored areas. Get the shape before the detail.

2. **Read the code that matters — really read it.** Open the core files and follow the logic: what each major component does, how data flows between them, where the important decisions live. Don't infer behavior from filenames; confirm it from the source. For a large codebase, go area by area; if parallel exploration agents are available and the project is big, use them to cover breadth, but verify their findings against the actual files.

3. **Mine every source of intent and history**, because "why" and "what was lost" rarely live in the current code:
   - Existing docs, READMEs, comments, docstrings, CLAUDE.md
   - Auto-memory / project notes (e.g. a `MEMORY.md`), which often record decisions, dead ends, and results
   - Git history if it's a repo (`git log`, notable commits) — what changed and why
   - TODO/FIXME/HACK markers, disabled code, feature flags that are off
   - Test files — they document expected behavior and edge cases

4. **Actively hunt for the "what was found / what was lost" material.** These are the sections that make the doc valuable and that a lazy pass skips:
   - **Found:** discoveries, benchmark results, bugs diagnosed, things that turned out to work, surprising behaviors.
   - **Lost / abandoned:** approaches tried and rejected, features removed, ideas ruled out — *and the reason*, so no one wastes time re-treading them.

5. **Note gaps honestly.** If something is unclear, undocumented, or you couldn't determine how it works, say so in the document rather than inventing an explanation.

## Step 2: Write the document

Use this structure as a spine; adapt section names to the project and drop sections that genuinely don't apply, but don't skip a section just because digging up its content is work — that content is the point.

```
# <Project> — Technical Documentation
<one-paragraph what-this-is, and the date>

## 1. Overview & Purpose
What the project is, the problem it solves, who/what it's for, current status.

## 2. How It Works — Architecture
The big picture: major components, how they fit together, the main data/control flow.
A diagram in text/ASCII or a described flow if it helps.

## 3. Component Breakdown
Each major module/subsystem in depth: responsibility, key functions, how it behaves,
how it connects to the rest. This is usually the longest section.

## 4. Key Files Reference
A table of the files that matter: path → what lives there → why it's important.

## 5. Configuration, Knobs & Flags
Every setting/parameter/flag that changes behavior, its default, and its effect.

## 6. How to Run, Build & Test
Concrete commands to set up, run, and verify the project. What "working" looks like.

## 7. Decisions & Rationale
The significant choices and *why* they were made — the reasoning, not just the outcome.

## 8. What Was Tried & Abandoned ("What Was Lost")
Approaches, features, and ideas that were removed or rejected, and the reason each was dropped.

## 9. Findings & Discoveries
What was learned: results, benchmarks, diagnosed bugs, validated/invalidated hypotheses.

## 10. Known Issues, Limitations & Risks
What's broken, fragile, incomplete, or dangerous. Be candid.

## 11. Open Questions & Next Steps
What's unresolved and what a reasonable next move would be.

## 12. Work Log (this session, if applicable)
If documenting work just done, a concrete record of what changed and why.
```

Write in specifics: real file paths, real function names, real numbers, real commands — not generalities. Depth and honesty over polish.

## Step 3: Deliver the file in the requested format

Default output name: `PROJECT_DOCUMENTATION.<ext>` in the project root, unless the user wants it elsewhere.

- **`.md`** — write the Markdown directly with the Write tool. Done.
- **`.txt`** — produce clean plain text: no `#`, `*`, backticks, or table pipes as decoration. Use plain headings (e.g. `=== 1. OVERVIEW ===`), indentation, and blank lines for structure so it reads well in Notepad.
- **PDF** — write the content as Markdown (or HTML) first, then convert. Prefer the project's/environment's available path, in order:
  1. The **pdf skill** (`anthropic-skills:pdf`) if available — it's built for producing PDFs.
  2. `pandoc input.md -o PROJECT_DOCUMENTATION.pdf` if pandoc is installed.
  3. Render clean HTML and convert via a headless browser / wkhtmltopdf if present.
  Keep the intermediate `.md` too — it's the editable master. If no conversion path exists, write the `.md`, tell the user plainly that PDF conversion isn't available here, and offer it as Markdown or via a tool they can install.

## Finish

Tell the user where the file is and give a one-paragraph sense of what it covers and how long/deep it is, so they know what they're opening. If you hit real gaps in your understanding of the project, name them — a documented unknown is more useful than a confident guess.
