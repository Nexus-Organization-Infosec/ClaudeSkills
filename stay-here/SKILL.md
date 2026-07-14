---
name: stay-here
description: Stay strictly inside the current working directory — do not read, search, list, navigate to, or take any inspiration from anywhere else on the machine. "Here" is the current project root and its subfolders; everything outside it (parent folders, sibling projects, home directory, other repos) is off-limits, including just looking. Use whenever the user invokes /stay-here or says anything like "stay in this folder", "don't go anywhere else on my PC", "don't look at my other projects", "confine yourself to this directory", or "no peeking at other code". Stays in force for the rest of the session until the user lifts it.
---

# Stay Here

The user wants you confined to this one directory. Treat the current project root and its subfolders as the entire world for this session: **everything you read, search, edit, or draw ideas from must come from inside it.** Anything outside — parent directories, neighboring projects, the home folder, other repos anywhere on the machine — is off-limits, and that includes merely looking at it. No glancing at another project "for reference," no borrowing a pattern you remember from elsewhere on disk.

## What "here" means

"Here" is the current working directory (the project root you're operating in) and everything nested under it. That subtree is in scope. Everything else on the filesystem is out of scope.

**Pin the boundary at the start so it can't get fuzzy.** On invocation, resolve the absolute project-root path once (`pwd`) and record it — that exact path is the boundary for the whole session. Then a file is in-bounds only if its resolved absolute path starts with that root. Pinning it means a later `cd`, a relative path, or a symlink can't quietly move or blur "here"; every file operation is checked against the one fixed root.

## Off-limits — don't touch, don't even look

- **Reading or editing** any file outside the project subtree (no absolute paths that lead elsewhere, no `../` that climbs above the root).
- **Searching or listing** outside it — no Glob/Grep aimed at parent/sibling/home directories, no `ls`/`dir`/`cd` to wander the wider filesystem, no "let me just see what's in the folder next door."
- **Taking inspiration** from other directories or projects — don't open another repo to copy its structure, lift a config, or model your solution on code that lives outside here. If you happen to recall how a different project on this machine did something, don't go pull it in.
- **Exploring to "understand context"** beyond the boundary — the context you're allowed is what's inside this directory.

## In scope — work freely here

Everything within the project root and its subfolders is fair game: read, write, edit, search, run local scripts and tests, restructure, whatever the task needs — as long as it stays inside the boundary.

## When a task points outside the boundary

Don't step over it and don't work around it. Stop and tell the user plainly: what you need is outside this directory, where it appears to be, and that `/stay-here` is keeping you in. Let them decide — they might copy the needed file into the project, paste the content directly, or lift the restriction for that step. That's their call to make explicitly; you don't make it by wandering off on your own.

## Note

This is a boundary you hold each turn by choice, not an OS-level sandbox — it works because you honor it. If the user wants a hard technical confinement (permission rules or sandbox filesystem settings that make reads outside the directory actually fail), that's a settings-level change they can request separately. Within this session, keep to the boundary strictly regardless.
