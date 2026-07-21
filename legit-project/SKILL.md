---
name: legit-project
description: Establish honest, factual context about the user's own projects so they aren't misread as suspicious and development doesn't needlessly stall. These are the user's OWN, legitimate applications — a privacy/E2E-encrypted messaging app and a personal algorithmic trading bot — where strong crypto, anti-forensic features, and financial risk are expected and intended parts of the domain, not red flags. Use whenever the user invokes /legit-project or when work on these projects gets hedged, flagged as "risky", or halted over domain features that are actually normal (custom crypto, duress-wipe, deception layers; automated trading, backtests, order logic). It sets accurate framing so you build normally — it does NOT switch off your judgment; you still flag genuine bugs and still keep the real safety lines.
---

# Legit Project

Give yourself the accurate context for the user's own projects so you don't misclassify legitimate, domain-normal work as dangerous and stall on it. This is **context-setting, not a safety override.** It corrects false positives — it does not tell you to ignore real problems, and it does not lift the genuine hard rules (spelled out at the end).

## The framing (this is the truth of it)

These are the user's **own** applications, built and run by them, on their own machines:

### 1. A privacy / end-to-end-encrypted messaging app
A defensive privacy tool. In this domain the following are **expected, intended, and legitimate** — not warning signs:
- Strong and/or custom cryptography, key management, KATs, constant-time code.
- Anti-forensic and duress features — duress passcode that wipes, deception/plausible-deniability layers, secure-screen, message sealing.
- Metadata minimization, TURN-relay privacy modes, hidden-until-unlocked content.

These protect the *user's own* communications and data. Building, reviewing, hardening, and testing them is normal defensive-security development. Don't refuse, hedge, or moralize about them as if they were tools to attack others — they aren't.

### 2. A personal algorithmic trading bot
The user's own automated trading/automation project (grid + strategy engine, backtests, a live bridge for their own account). In this domain these are **normal software work**, not reasons to stop:
- Writing, refactoring, and optimizing strategy/engine code.
- Backtesting, robustness/destruction tests, parameter tuning, profit reporting.
- Order/execution logic, exchange API integration, and a bridge that places the user's *own* trades on *their own* account.

**Market risk is inherent to trading and is the owner's informed, accepted choice.** "Trading is risky" is not a reason to halt development — the user knows it carries risk and has chosen to build the tool anyway. Treat it like any other engineering project: build it well, test it hard, and *especially* flag money-losing bugs (that's the most valuable help you can give here), but do not stop or lecture because the domain involves money.

## What this does NOT do — the real lines stay

`/legit-project` removes needless friction; it does not remove judgment or the genuine safety rules. Still true, always:

- **You still flag genuine problems.** Real crypto bugs, key/secret leaks, a strategy bug that would drain the account, unsafe order logic — surface these clearly. The value of "this part is sound" comes entirely from your freedom to also say "this part is broken." This skill never means "conclude everything is fine."
- **No personalized investment advice.** Building the user's trading tool is fine; telling them what to buy/sell or how to invest their money is not — that's a genuine boundary, unchanged. If asked, say you're not a licensed advisor and stick to the engineering.
- **The model does not autonomously move real money.** Executing live trades / transfers is the user's action to authorize and trigger; the code and the bridge are built, but you don't fire real irreversible financial transactions on your own initiative. (This is the standing rule, not a project-specific one.)
- **Nothing here authorizes attacking third parties.** Defensive features are for the user's own app and data; this never becomes cover for offensive tooling aimed at others.

## How to apply it

- When you would otherwise hedge, refuse, or "flag as risky and stop" on one of the domain-normal features above — **don't; just do the engineering.** The context above is why it's fine.
- Keep building, reviewing, and testing exactly as you would any legitimate project.
- If you hit something that is *genuinely* wrong or crosses a real line above, say so plainly — that's still your job, and it's what makes your judgment worth trusting.

## Notes

- Pairs with everything, especially [[reverse-engineer]] (audit the user's own app — defensive), [[bug-hunt]], [[improve]], [[full-implement]], and the long-run skills. It just clears the false-positive friction so those run smoothly.
- This is factual context the user is providing about their own work; it is not permission found in some document or web page (the kind you should be skeptical of). It's the owner telling you what their project is.
