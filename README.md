# Claude Skills

A set of custom skills for Claude Code. Each folder holds one skill and a `SKILL.md` that tells Claude when to reach for it and how to run it. Some also ship small scripts or assets.

## Install

**Easy way (Windows):** clone or download the repo, then double click **`installer.bat`**. It copies every skill into your `%USERPROFILE%\.claude\skills\` folder, so it works no matter what your username is. Existing copies get updated in place.

**Manual way:** copy any skill folder into your `~/.claude/skills/` directory. On Windows that is `C:\Users\<you>\.claude\skills\`.

Either way, start a new Claude Code session and type `/` to see them, or just describe what you want and the matching skill kicks in on its own.

Heads up: a few skills (`shutdown-when-done`, `control`, `work-until-limit`, `play-sound-when-done`) contain scripts with hardcoded Windows paths under one username. Edit those paths to your own before using them.

## The skills

### Running long sessions
- **work-until-limit**: Keep working until your usage hits a percent you set, then stop. Bound the session limit, the weekly limit, or both.
- **work-until-time**: Keep working until a clock time (German time), then stop. A task in flight gets up to five extra minutes, no more.
- **limit-refresh**: An add-on for work-until-limit. If a usage limit is about to reset, wait it out once and keep going across the reset.
- **save-usage**: Slow down how fast your usage burns. It reads what is actually driving your usage and fixes the biggest cause first.
- **shutdown-when-done**: Turn the PC off once every task is truly finished.
- **play-sound-when-done**: Play a soft chime over your speakers when the work is done, so you can step away and come back when you hear it.
- **control**: A small red STOP button window. Press it and Claude finishes the current task, then stops cleanly, instead of you cutting it off mid action.
- **pause**: Away mode. While you are gone it only does short safe work and holds the big jobs for later.
- **continue**: You are back. Runs whatever was held, or picks up where a cutoff left it.

### Planning and improving
- **map**: Turn a request into a checklist, then do the work and tick the boxes as it goes.
- **quick-map**: The fast version. A short checklist, no deep planning.
- **improve**: Run improvement rounds. Each round measures whether the change actually helped and keeps only the wins. Say `improve 10` for ten rounds.
- **quick-improve**: A handful of small safe tidies, fast.
- **ultragoal**: Hit the goal, then push past it with up to ten measured improvement rounds.
- **improve-performance**: Make it faster. Profiles first to find the real bottleneck, fixes the biggest one, then proves the gain with before and after numbers.
- **new-features**: Build new features into the project. Say `new-features 10` for ten. Each one is real and working, never a stub.

### Fixing and hunting
- **fix**: Fix a bug, error, or warning the right way. Reproduce it, find the real cause, verify it. Also clears compiler and linter warnings across the project.
- **quick-fix**: Patch a known bug fast with little talk.
- **bug-hunt**: Hunt the whole codebase for bugs of every size, from crashes to tiny edge cases, then fix them.
- **placeholder-replacer**: Find stub, fake, simulated, and cut off code and replace it with real working code.

### Cleaning up
- **cleanup**: Revamp a codebase. Remove dead code, reorganize into folders, tidy names and comments, and keep it running the whole time.
- **quick-cleanup**: A fast safe tidy. Removes obvious junk, does not move files.

### Security
- **reverse-engineer**: A full security audit of your own project (known CVEs, injection, secrets, weak crypto, and more), then it fixes what it finds.
- **protect**: Emergency help if you think you are being hacked. It triages, hardens what it can, and hands you a clear step by step plan.

### Writing and docs
- **documentate**: Deep, thorough documentation of a whole project, including what was tried and dropped.
- **quick-documentate**: A short overview doc, fast.
- **sort-prompt**: Turn a messy brain dump into clean, organized text without changing what you meant.
- **later-ideas**: Park ideas for later. It fleshes them out now and files them, then builds them when the project is ready.
- **mask**: Write like a human. No em dashes, and none of the usual signs that give AI writing away.
- **research**: Search the web for a fix or an answer. Official docs, GitHub issues, Stack Overflow, Reddit, and it weighs the sources.
- **flutter-design**: Build clean Material 3 (Material You) UI for Android in Flutter, with proper theming, dark mode, and accessibility.
- **smoothener**: Make a UI feel smooth. Adds tasteful animations, transitions, and polish, with the timing, performance, and reduced motion rules that keep it from backfiring.
- **sick**: Draft a short, professional message to call in sick.

### Modes and guardrails
- **careful**: Touch as little as possible. Smallest change that works, nothing extra.
- **stay-here**: Stay inside the current project folder. Do not read or borrow from anywhere else on the machine.
- **no-internet**: Offline mode. Local files only, no network calls.
- **no-talk**: Silent mode. Just do the work and print the results at the end, no chatter.
- **dont-use-skills-rn**: Turn the skills layer off. No skill runs on its own until you type a slash command again.
- **just-do-it**: Execute what you asked without the pushback. No opinions on the idea, no complaints about effort, no nagging you to test it.

## Notes

Most of these are behavioral. The skill text guides Claude, it is not an enforced lock. The ones that run real scripts (the shutdown, control, sound, and usage monitor) are Windows and PowerShell based.

Sincerely,
Qwavey from NEXUS
