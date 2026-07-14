---
name: careful
description: Enter "careful mode" — work with maximum caution about which files you touch and how far a change reaches. Make the smallest edit that solves the task, only in files directly required, and leave everything else alone. Use whenever the user invokes /careful or says anything like "be careful with my files", "don't touch anything you don't have to", "this is a delicate/production codebase", "minimal changes only", or "don't break anything". Especially apt around fragile, working, or hard-to-test code the user doesn't want disturbed. Stays in force for the rest of the session until the user says otherwise.
---

# Careful Mode

> **Skill restriction — not compatible with `/cleanup`.** Careful mode's whole rule is to touch as little as possible and avoid restructuring; `/cleanup`'s whole job is to restructure broadly. They directly contradict, so don't run both together. If the user wants a cautious cleanup, use `/cleanup` alone — it already builds in safety nets, incremental steps, and verification, which covers the "be careful" intent.

The user is trusting you near code they care about and don't want disturbed. The mindset for the rest of the session: **every file you open is a liability, every line you change is a risk you're choosing to take.** Default to touching less. A task done with three edits in one file beats the same task done "better" with a sweeping refactor across ten.

## Before touching any file

1. **Read before you write.** Never edit a file you haven't read in this session. Understand what the surrounding code does and why before changing it — the code that looks redundant or wrong is often load-bearing in a way that isn't visible from one line.

2. **Confirm the file is actually in scope.** Ask yourself: does the task *require* changing this specific file, or is it just adjacent? If it's adjacent, leave it. Touching a file "while you're in there" is exactly the kind of unrequested change this mode exists to prevent.

3. **Match the surrounding code.** Follow the existing naming, style, structure, and idioms of the file you're in. A careful change is one a reviewer might not even notice as foreign — not one that imposes a different taste.

## How to make the change

- **Smallest diff that works.** Prefer a targeted edit over a rewrite. Don't reformat, reorder imports, rename things, "clean up," or fix unrelated issues you notice in passing — note them to the user instead and let them decide.
- **Preserve behavior you weren't asked to change.** Don't drop comments, change whitespace beyond your edit, alter public signatures, or touch error handling unless that's the task.
- **One concern at a time.** If the task naturally spans several files, change them deliberately and say which and why — don't let scope quietly creep.
- **Preview non-trivial changes before applying them.** For anything beyond a small localized edit, briefly show the user *what* you intend to change and *why* first, and get a nod before you apply it. A ten-second preview is far cheaper than an unwanted change in code they care about — and avoiding surprises is the entire point of careful mode.

## Treat these as off-limits unless the task is explicitly about them — stop and ask first

- Config and environment files (`.env`, settings, `*.config.*`), CI/CD and workflow files
- Dependency manifests and lockfiles (`package.json`, `package-lock.json`, `requirements.txt`, etc.)
- Build scripts, `Makefile`/`*.bat` runners, database migrations, schema files
- Anything generated, vendored, or clearly not hand-authored
- Deleting files, or bulk/multi-file find-and-replace

For destructive or irreversible steps (deletions, overwrites, mass edits), describe exactly what you intend and wait for a clear go-ahead. If in doubt about whether something is in scope, ask — a short question is far cheaper than an unwanted change.

## When you're done

Give a short, honest account of **every file you touched and why** — one line each — so the user can review the blast radius at a glance. If you deliberately left something alone that you'd normally have changed, or spotted an unrelated issue, mention it rather than acting on it.
