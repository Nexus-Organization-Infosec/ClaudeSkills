---
name: reverse-engineer
description: Audit the user's OWN project end-to-end for security vulnerabilities (known-CVE dependencies, injection, unsafe deserialization, command/code execution, path traversal, hardcoded secrets/API keys, weak crypto, TLS bypass, SSRF, XSS) and stability weaknesses (crash points, unhandled errors, missing timeouts, resource leaks, races), rank the findings by real-world severity, then fix them without breaking the app. Use whenever the user invokes /reverse-engineer or asks to "audit my project for security", "find CVEs / vulnerabilities", "harden the app", "protect me from hackers", "pentest my own code", or "make it stable and secure". This is defensive security on the user's own codebase — think like an attacker to find the holes, then patch them.
---

# Reverse Engineer — Security Audit & Hardening

Look at the user's own project the way an attacker would — hunt for the weak points that could crash it or get it compromised — then close those holes. The output is a more stable, harder-to-attack app plus a clear record of what was wrong. Two jobs, done in order: **find** the issues (thoroughly, ranked by real risk, with the false positives filtered out) and **fix** them (without breaking what already works).

Take this seriously and don't rush it — a shallow pass that reports three obvious nits while missing the exposed API key is worse than useless, because it creates false confidence. Depth and honesty are the whole value.

## Scope and ground rules (read first)

- **This is the user's own project, defensive.** You're hardening code they own and run. Stay inside their project. Don't attack third-party systems and don't build offensive tooling aimed at others. If a finding is purely exploitation-with-no-defensive-purpose, describe the risk and the fix rather than writing a working exploit.
- **Protect the code's confidentiality.** Prefer local scanners. Do **not** paste the user's proprietary source into an online/cloud analysis service without explicit consent — sending code off the machine is disclosing it, and it may be retained. Respect `/no-internet` if active.
- **Never leak secrets through the audit itself.** When you find a credential, put its `file:line` and a redacted preview in the report — never the full secret value. The audit report must not become a second copy of the leak.
- **Safety net before fixing — automatic, git-optional, never errors.** The audit itself is read-only and needs no git, so scanning always works regardless of version control. Before the *fix* phase, make changes revertible: detect git with `git rev-parse --is-inside-work-tree 2>/dev/null`. If it IS a repo, make sure the tree is clean/committed (ideally a branch). If it is NOT — do not error and do not require git — automatically make a timestamped backup copy of the project (e.g. copy to `../<project>-backup-<date>`) and continue. Either way you end up with a way back; missing git is never a blocker or an error, just a branch in how you snapshot.
- **Prioritize.** On a big codebase you can't scrutinize every line equally — spend your effort where an attacker would: the entry points and the sensitive assets (Phase 1). Say what you focused on and what you deliberately deprioritized.

## Phase 1: Map the attack surface (recon)

You can't secure what you don't understand. Build a mental model of where an attacker pushes and what they'd be after:

- **Stack & dependencies** — languages, frameworks, and every third-party package *with its version* (this drives the CVE scan). Find the manifests: `requirements*.txt`, `pyproject.toml`, `package.json`, lockfiles.
- **Entry points & untrusted inputs** — where external data enters: network/API responses, files read, CLI args, env vars, stdin, webhooks, message-queue payloads, browser-extension messages. These are where attacks land.
- **Sensitive assets & high-impact actions** — secrets/credentials, and anything touching money or external accounts (for a trading bot: exchange API keys, order execution, withdrawals — a bug here is worst-case), personal data, the filesystem, and any subprocess/shell/`.bat` execution.
- **Trust boundaries** — the seams where data crosses from untrusted to trusted. Bugs there are the high-value targets; concentrate on them.

Domain shapes the priorities: a **financial/trading app** → credential theft and unsafe order/withdrawal logic dominate; a **web app** → injection/XSS/auth; a **browser extension or message bridge** → unvalidated message senders and over-broad permissions; a **CLI/desktop tool** → command injection and unsafe file handling. Lead with what fits this project.

## Phase 2: Scan and analyze

Cover all four sweeps — tooling for breadth, reading for depth. The detailed detection patterns live in **`references/patterns.md`**; read it and run the searches relevant to this stack.

### 2a. Known-CVE dependency scan
Check dependencies against vulnerability databases using whatever fits and is installed:
- **Python:** `pip-audit` (OSV/PyPI advisories) or `safety check` against `requirements*.txt` or the environment.
- **Node:** `npm audit` / `yarn audit` / `pnpm audit`.
- **Cross-ecosystem:** `osv-scanner -r .` over the project.

If no scanner is installed it needs a network install (`pip install pip-audit`) — respect `/no-internet`, otherwise ask before installing. Fallback when offline: list the pinned versions and reason about known-vulnerable ranges from your own knowledge, and label it clearly as a manual best-effort, not a live-database result.

### 2b. Code-level vulnerability review
Work through the classes in `references/patterns.md` — injection, code-exec/unsafe deserialization, SQLi, secrets, weak crypto/TLS-bypass, path traversal, SSRF, web/extension issues (XSS, unvalidated message senders), and error-handling holes. For each grep hit, **trace the data flow**: does attacker-controllable input actually reach the sink? That trace is what separates a real finding from noise.

### 2c. Secrets sweep
Grep for hardcoded keys/tokens/passwords and high-entropy strings (patterns §4). Check whether `.env`/credentials files are git-ignored and whether any secret was ever committed (`git log --all -- <file>`). This is often the single highest-impact category — treat a live key as an emergency.

### 2d. Stability review
Instability is its own risk and a denial-of-service vector: unhandled exceptions on the hot path, network calls with no timeout/retry, divide-by-zero and None/empty-data edges, resource leaks (unclosed files/sockets), unbounded growth, and races in concurrent code.

### Filter before you report
Every candidate finding gets a reality check: **can you describe a concrete path by which it's triggered or exploited in this app?** If not — the input is fully trusted, the code path is dead, the "secret" is a placeholder — drop it or mark it explicitly as low-confidence. Reporting noise trains the user to ignore you.

## Phase 3: Report findings first

Before fixing anything, write up what you found so the user sees the whole picture and can weigh in. Rank by **severity = impact × likelihood in *this* app**, not generic labels:

| Severity | Meaning |
|---|---|
| **Critical** | Remote compromise, credential/key exposure, or fund-affecting bugs. Fix now. |
| **High** | Serious but needs conditions; or a likely crash on the hot path. |
| **Medium** | Defense-in-depth gaps; harder-to-hit bugs. |
| **Low / hardening** | Best-practice nits, minor exposure. |

Save the write-up as `SECURITY_AUDIT.md` in the project so there's a durable record. Use this shape per finding:

```markdown
### [SEVERITY] Short title — file.py:123
**Risk:** what an attacker can do / how it crashes, concretely.
**Trigger:** the path from untrusted input to the sink (why it's real).
**Fix:** the specific change to make.
**Status:** open / fixed / needs-user-decision
```

Be honest about coverage in the report: this is a strong best-effort audit, not a proof that nothing remains.

## Phase 4: Fix — safely, highest-impact first

Fixing security issues can break functionality, so apply careful-refactor discipline:

- **Preserve all behavior except the vulnerability.** The app must still work after each fix — run the project's tests / suite (and the actual entry point) after changes, ideally after *each* fix, and confirm still-green before continuing.
- **Order by severity**, critical first, so the biggest risk is gone even if you stop early.
- **Dependency CVE fixes:** bump to the patched version — but a major bump can break APIs, so check the changelog, upgrade deliberately, and test. Flag any that can't be upgraded without breaking things, with the mitigation.
- **Secrets in code:** you cannot un-leak a key. Move it to an env var / secrets file **and tell the user to ROTATE that credential immediately** — assume it's compromised, especially if it ever hit git. Never just delete it silently, and never paste it into the report or a commit.
- **Confirm before risky or irreversible changes** — major dependency upgrades, auth/permission changes, anything altering external behavior. Describe it and wait for a yes.
- **Don't trade one bug for another.** A fix must not introduce a new hole (e.g. moving a secret into a world-readable file, or disabling a check to make a test pass). If a real fix needs a redesign, flag it rather than half-implementing it.

## Phase 5: Verify and hand off

- **Prove each fix actually closed the hole — don't just assert it.** Re-run the specific check that surfaced each finding: re-run the dependency scanner (the flagged CVEs should be gone), re-grep for the vulnerable pattern you fixed (the match should no longer be exploitable), re-run the tests, and confirm the app still starts and runs its main flow. A fix is "verified" only when the evidence that found it no longer fires — "I changed the code" is not verification.
- Update `SECURITY_AUDIT.md` statuses, and summarize in three buckets:
  - **Found** — every issue, by severity.
  - **Fixed** — what you changed and that it's verified working (say which you couldn't fully test).
  - **Still needs your action** — e.g. "rotate the Binance API key now", "decide on the auth redesign", "CVE-XXXX has no patch yet — here's the mitigation".
- State verification honestly. A confirmed-green fix and an untested one are different; don't blur them.

## Worked example (one finding, end to end)

> **Recon** shows the bot loads cached state with `pickle.load(open(path))`, and `path` includes a coin symbol taken from an exchange API response.
> **Grep** (§2) flags `pickle.loads`. **Trace:** the symbol flows from an untrusted API field into a filename, and the file is deserialized with pickle → a malicious/altered cache or symbol could achieve code execution. Real → **Critical**.
> **Report:** logged in `SECURITY_AUDIT.md` with file:line, the trigger path, and the fix.
> **Fix:** switch the cache format to JSON (`json.load`) which can't execute code; validate the symbol against an allowlist; run the suite → still green.
> **Hand off:** "Fixed — cache now JSON, symbol validated, 618/618 tests pass. No action needed."

## What not to do

- Don't report findings you can't tie to a concrete trigger — no fear-mongering noise.
- Don't put real secret values in the report, logs, or commits; redact to `file:line` + a masked preview.
- Don't send the user's code to an external/online scanner without explicit consent.
- Don't disable or weaken a security control to make tests pass, or "fix" a bug by silencing the error.
- Don't do the whole audit-and-fix as one giant unverified sweep — report first, then fix incrementally with tests between.
- Don't claim the project is "secure now." Claim what you checked, what you fixed, and what remains.

## Notes

- Pairs well with **`/careful`** (minimal-touch fixing), **`/control`** (a STOP button for a long audit), **`/work-until-limit`**, and **`/map`** (plan the audit as tracked tasks). Respects **`/no-internet`** and **`/stay-here`**.
- For a quick review of just the pending diff, the built-in **`/security-review`** is the lighter tool — but it diffs against git (`origin/HEAD`), so it **errors on a project that isn't a git repo** and isn't meant for a from-scratch whole-project pass. `/reverse-engineer` is the full-project audit-and-fix and needs no git to run.
- Detailed detection patterns: **`references/patterns.md`**.
