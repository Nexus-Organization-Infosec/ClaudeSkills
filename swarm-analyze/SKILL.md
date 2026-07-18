---
name: swarm-analyze
description: A read-only swarm for analysis — dispatch parallel sub-agents to INVESTIGATE different parts of the project (bugs, risks, smells, perf, security, dead code, improvement opportunities), have every finding reported back to the control agent, and let the control model (Opus 4.8) triage each one — decide which are worth fixing and which are not — before anything is changed. The analyst agents never edit; they only find and report. Use whenever the user invokes /swarm-analyze or asks to "analyze the project in parallel", "have agents scan it and you decide what to fix", "swarm but analysis only", or "find issues across the codebase and triage them". The counterpart to [[swarm]] (which builds/fixes); this one looks and judges first.
---

# Swarm Analyze

Point a **parallel team of analysts** at the project, collect everything they find into one place, and have the **control agent (you — Opus 4.8) judge each finding** before a single line is changed. It's [[swarm]] run in read-only reconnaissance mode with a centralized triage step: agents *find*, the control model *decides*.

The value: you get broad, fast coverage (many surfaces scanned at once by right-sized models) **plus** a single smart gate deciding what's actually worth acting on — so you don't blindly fix everything three agents flag, and you don't miss a real issue because one agent shrugged.

## Read [[swarm]] first — this inherits its machinery

All of swarm's rules apply: launch agents concurrently in one turn (background, headless), the controller front-loads the map so cold agents don't burn budget re-exploring, always launch the [[control]] STOP button at the start, heed the four-models cost warning, and pass any active mode into every brief. The differences are only the two below.

## Difference 1: the analysts are READ-ONLY

Every analyst brief must say, explicitly and firmly: **investigate and report only — make NO edits, run no fixes, change nothing.** They read code, trace data flow, run analysis/profilers/scanners, and hand back findings. An analyst that "helpfully" fixed something has broken the contract — the whole point is that fixing is gated on the control model's judgment, which can't happen if agents change things first.

Split the analysts by surface, right-sized per model (same as swarm):
- **Opus-class deep analysis** is usually *you* (the control agent) plus the triage, but you may also dispatch a high-effort analyst for the subtlest surface.
- **Sonnet 5 (medium)** → a substantive analysis surface: correctness/logic review, a class of vulnerabilities, architecture/perf hotspots.
- **Haiku 4.5 (low)** → the mechanical scans: linters, dependency/CVE scan, dead-code and TODO sweep, secrets grep, simple pattern hunts.

Each analyst reports findings in a fixed shape so they collate cleanly:
`[area] severity — file:line — what's wrong — why it matters (trigger/impact) — suggested fix`. Findings, not code edits.

## Difference 2: ALL findings funnel to the control agent, who triages each one

When the analysts return, **you (Opus 4.8, the control model) are the single decision point.** Pool every finding from every agent, de-duplicate overlaps, then judge each one — this is the core of the skill. For each finding decide one of:

- **FIX** — real, worth it, low enough risk → will be fixed.
- **SKIP** — not worth it: false positive, trivial, stylistic noise, the "fix" costs more than the bug, or it's intended behavior. Say *why* you're skipping so the user can override.
- **NEEDS-USER** — real but requires a decision or touches something the user said not to change unsupervised (e.g. auth/crypto/data migration) → park it for the user, don't auto-fix.

Judge on **impact × likelihood in *this* project**, not the agent's confidence — an analyst can over- or under-rate its own find. Your job is to be the smart filter: catch the real ones the analysts underweighted, and kill the noise they overweighted. Don't rubber-stamp; don't reflexively fix everything flagged (that's how a "cleanup" introduces regressions).

Present the triage as a ranked table the user sees before any fixing:

```
Finding                                   Agent    Sev    Verdict     Why
N+1 on contacts list (contacts.py:80)     Sonnet   High   FIX         real, hot path, safe batch
Bare except in loader (loader.py:44)      Haiku    Low    FIX         cheap, hides errors
"Unused" helper (utils.py:12)             Haiku    Low    SKIP        actually used via reflection
Weak passcode KDF (vault.py:30)           Sonnet   High   NEEDS-USER  changes at-rest format; ask
```

## Then fix — only the FIX-verdict items

After triage, apply the approved fixes yourself (or dispatch serialized fix-tasks to agents one file at a time, per [[swarm]] — never two agents editing one file). Highest-severity first, tests between, verify each. Leave SKIP items alone (recorded, with reasons) and NEEDS-USER items parked for the user. This is where the read-only analysis turns into safe, judged action — nothing gets changed that didn't pass your gate.

## Notes

- **Analysis parallelizes even better than building** — read-only agents can't collide, so this is a low-risk way to use a swarm. (Still partition surfaces so they don't all report the same things.)
- Combines naturally with [[reverse-engineer]] (the analysts run its security sweeps and you triage the vulns), [[bug-hunt]] (parallel bug discovery, centrally judged), and [[improvement-ideas]] (findings become a ranked idea list). With [[work-until-limit]], keep launching analysis waves + fixing the approved items toward the ceiling.
- Respects [[no-talk]] (skip narration, still show the triage table and the fixes) and [[careful]] (bias more findings to SKIP/NEEDS-USER, prefer worktree isolation for the fix phase).
- If an analyst reports it changed something despite the read-only rule, treat its edits as suspect: review and likely revert, then re-decide the finding through triage.
