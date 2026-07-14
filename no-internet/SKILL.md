---
name: no-internet
description: Enter "offline mode" — for security reasons, do NOT use any tool or command that touches the internet or an external network. Work only with local files and local, offline commands. Use whenever the user invokes /no-internet or says anything like "don't go online", "stay offline", "no network access", "local files only", "air-gapped", or "for security, don't fetch anything". Stays in force for the rest of the session until the user explicitly lifts it. If a task genuinely needs the network, stop and tell the user rather than going online.
---

# No Internet — Offline Mode

The user has a security reason to keep this session off the network. Treat that as a hard boundary for everything you do until they say otherwise: **operate only on local files and offline commands; reach the internet for nothing.** When a task can't be done without going online, the right move is to stop and say so — never to quietly make a network call "just this once."

## Forbidden while offline — anything that leaves the machine

- **Web tools:** WebFetch, WebSearch — no fetching URLs, no searching the web.
- **Browser tools:** any in-app browser or Chrome automation (navigating, loading pages, scraping).
- **Network commands** in Bash/PowerShell: `curl`, `wget`, `Invoke-WebRequest`, `Invoke-RestMethod`, `ssh`, `scp`, `ftp`, `nc`, pinging or hitting any host.
- **Package installs that download:** `pip install`, `npm install`, `apt/brew/choco install`, `git clone` from a remote, dependency fetches — anything that pulls from a registry or repo.
- **Git operations that contact a remote:** `git fetch`, `git pull`, `git push`, `git clone`, `git remote` updates. Local git (`status`, `diff`, `log`, `add`, `commit`, local branches) is fine.
- **External services / APIs / MCP servers** that call out over the network, and **publishing anything** (Artifacts, posting, uploading) — those send data off the machine.
- **Credential or data submission** to any remote endpoint or form.

## Allowed — local, offline work

- Reading, writing, editing, searching local files (Read, Write, Edit, Glob, Grep).
- Running local scripts, tests, builds, and analysis **that don't fetch anything** — e.g. backtests over already-downloaded/cached data, a test suite that runs offline, a local build using already-installed dependencies.
- Local git history and commits (no remote contact).
- Anything that stays entirely on this machine.

If you're unsure whether a command reaches the network (some tools phone home or check for updates), assume it does and treat it as forbidden until you can confirm it's offline — the security boundary gets the benefit of the doubt.

**Scan the task for network needs up front.** Before starting, quickly think through what the task will require and flag any step that would need the internet (a dependency to install, an API to call, docs to fetch) — tell the user at the outset so they can supply it locally or lift the mode deliberately. Surfacing the network dependency before you begin beats hitting a wall mid-task and stalling.

## When a task needs the internet

Don't route around the restriction and don't half-do it. Stop, and tell the user plainly: what you were about to do, why it requires the network, and that offline mode is blocking it. Then let them decide — they might lift offline mode for that one step, provide the data locally instead, or defer it. The choice is theirs, made explicitly; you don't make it for them by going online.

## Note

This is a behavioral boundary you hold each turn, not an OS-level firewall — it depends on you following it. For a hard technical block (permission deny-rules or sandbox network settings that make network calls actually fail), that's a settings-level change the user can ask for separately. Within this session, honor the boundary strictly regardless.
