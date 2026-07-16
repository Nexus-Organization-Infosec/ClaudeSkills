---
name: backup
description: Make a timestamped backup of the whole project — a full copy of the file tree plus an infos.txt with the date, project name, size, file count, and git state. Use whenever the user invokes /backup or says "back up the project", "make a backup", "snapshot this before you change it", or "save a copy first". Good to run before anything risky (a cleanup, a restructure, a big refactor). Bundled Windows script.
---

# Backup

Take a full, timestamped snapshot of the project so there's always a way back. Especially worth doing before a risky change like `/cleanup`, a restructure, or a big refactor.

## What it produces

```
BACKUP/
  <ProjectName>_<YYYY-MM-DD_HH-MM-SS>/
    infos.txt          <- date/time, project name, paths, machine, file count, size, git state
    <the whole project, same folder structure>
```

By default `BACKUP/` is created **next to the project** (in its parent folder), so the copy never recurses into itself, and each backup is its own timestamped folder so old ones are never overwritten.

## How to run it

From the Bash tool, pass the project path (or run it with the project as the working directory and no arg):

```bash
C:/Users/flori/.claude/skills/backup/scripts/backup.bat "<full path to the project root>"
```

Optional second argument sets a custom backup root: `backup.bat "<project>" "<backup root>"`.

After it runs, tell the user where the backup landed and the file count / size (the script prints both, and writes them into `infos.txt`).

## Good to know

- **It's a full copy, including `.git`** — a real backup preserves history. If you want to skip heavy regenerable folders (a `node_modules`, a virtualenv, a browser profile, big caches), say so and exclude them; the default keeps everything.
- **Locked files** (an in-use browser profile, an open database) may not copy. The script uses a short retry so it fails fast instead of hanging, and notes any such error in `infos.txt` rather than pretending the backup was perfect.
- **A big project takes a moment** and uses disk space. Each run is a fresh full copy; prune old `BACKUP/` folders yourself when you don't need them.
- This is a local snapshot on the same machine. It protects against a bad edit, not against the disk dying. For off-machine safety, push to a remote or copy the backup elsewhere.

## Notes

Pairs naturally with `/cleanup`, `/reverse-engineer`, and `/placeholder-replacer` (run a backup first, then let them change things). The audit/fix skills already make their own safety net, but an explicit `/backup` is the belt-and-braces option before something large.
