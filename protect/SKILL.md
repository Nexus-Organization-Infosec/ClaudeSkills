---
name: protect
description: Emergency defensive response when the user believes they're under active attack — hacked, compromised, credentials stolen, suspicious account activity, ransomware, unauthorized trades/withdrawals. Triage what's happening, harden what can be hardened in their project, and give a clear, prioritized list of the actions the user must take NOW (rotate credentials, enable MFA, revoke access, contact providers). Use whenever the user invokes /protect or says "I'm being hacked", "someone's in my account", "secure my system", "I think I'm compromised", or similar. Defensive only, on the user's own systems.
---

# Protect — active-incident response

The user thinks they're under attack. Be the calm, systematic one: panic causes mistakes (wiping evidence, missing the real entry point, locking themselves out). Move fast but in priority order — **stop the bleeding first**, especially anything touching money or master credentials.

A hard reality that shapes this whole skill: **the highest-impact incident actions are ones only the user can do, and ones you must not do for them.** You cannot log into their accounts, enter their passwords, change security settings, or move funds — and an active incident is exactly when doing that wrong makes things worse. So your job splits in two: **harden what you legitimately can in their project**, and **hand the user a precise action list for everything else.** Doing it wrong or slowly isn't better than guiding them to do it right.

## Step 1: Triage — what's actually happening

Before reacting, get a quick, factual picture (2–3 minutes, not an investigation):
- **What's the evidence?** Suspicious login/email/alert, unfamiliar account activity, unexpected trades/withdrawals, files encrypted, unknown processes, a leaked key? Pin down what's actually observed vs feared.
- **What's exposed?** Which accounts/systems/credentials could be affected, and which are highest-stakes (email — because it's the reset hub for everything — banking, exchange, cloud, password manager).
- **Is it still ongoing?** Active exfiltration/ransomware in progress calls for immediate isolation; a stale phishing click is less urgent.

Don't destroy evidence while triaging (don't delete logs/emails); you may need them.

## Step 2: The protection plan (do this in order)

Give the user a clear, ordered playbook. There are two parallel tracks — **clean the device** and **secure the accounts** — plus one ordering rule that ties them together. Lead with whatever is bleeding fastest (active encryption/exfiltration, or money at risk).

### Track A — clean the compromised device

1. **Isolate it now.** Disconnect the device from the internet and network — unplug Ethernet, turn Wi-Fi off. This cuts the attacker's remote access and stops data being exfiltrated. Also unplug external/USB drives so malware (especially ransomware) can't spread to them. If ransomware is actively encrypting and forensics/recovery might matter, **isolate rather than power off** (a hard shutdown can lose recoverable state).
2. **Run a full malware scan** (not a quick scan). On Windows 11, Microsoft Defender is built in — from PowerShell:
   - `Update-MpSignature` — get the latest definitions.
   - `Start-MpScan -ScanType FullScan` — full system scan.
   - `Get-MpThreatDetection` / `Get-MpThreat` — see what it found.
   Then run a reputable **second-opinion scanner** (e.g. Malwarebytes) for another pass — download it on a *clean* device to a USB stick if the infected one is offline.
3. **Use Safe Mode if malware resists.** If a scan is blocked or threats keep returning, boot into **Safe Mode** (networking off) and scan again — many threats can't load there.
4. **Hunt for persistence.** Attackers plant things that auto-run. Check startup items, scheduled tasks, and services for anything unfamiliar:
   - `Get-CimInstance Win32_StartupCommand | Select Name, Command, Location`
   - `Get-ScheduledTask | Where-Object State -ne 'Disabled'`
   - unfamiliar processes via `Get-Process` / Task Manager.
5. **Remove and re-scan until clean twice.** Quarantine/remove detections, reboot, scan again. One clean scan isn't proof — confirm it comes back clean on a second full pass.
6. **Patch everything.** Update the OS and all software — Windows Update, browsers, apps — to close the hole they came in through. Outdated software is a top entry point.
7. **If it can't be trusted clean, reimage.** For a deep compromise (rootkit, ransomware, or you simply can't be sure), the only reliable fix is: back up your data to **offline** media, wipe, and reinstall the OS from scratch. Restore *data*, not programs, and only from a backup predating the compromise.

### Track B — secure the accounts (from a KNOWN-CLEAN device, in parallel)

1. **Change passwords** — email first (it's the master key that resets everything else), then financial/exchange, then anything reusing that password. Unique passwords each.
2. **Turn on MFA / 2FA** everywhere it isn't already — especially email, bank, exchange, password manager.
3. **Revoke active sessions and third-party access** — sign out all devices, remove unknown OAuth/app grants, and check for malicious email rules/forwarding/filters the attacker may have added.
4. **Financial / trading — top priority:** rotate or delete exchange **API keys immediately**; disable withdrawals / confirm a withdrawal allowlist is set; review for unauthorized orders/withdrawals; call the bank/exchange to flag fraud. For this trading project specifically, any leaked exchange key with trade or withdrawal permission is a fund-loss emergency.

### The ordering rule that ties them together

**Don't type new passwords into a machine that might still be infected** — a keylogger would capture them the moment you set them. Do the account track (B) from a *separate clean device* right away, and only trust the compromised machine for logins after Track A confirms it's clean.

## Step 3: What you (Claude) can do — in their project, defensively

These are in-scope and genuinely useful:
- **Secrets sweep:** find hardcoded keys/tokens/passwords in the code/config (see [[reverse-engineer]] patterns). Anything found → remove from code, and tell the user to **rotate it now** (assume it's compromised).
- **Look for signs of tampering:** recently modified files, injected/obfuscated code, new/unexpected network calls to unknown hosts, added dependencies, backdoors, unfamiliar scheduled tasks or startup hooks *inside the project*. Flag anything suspicious with `file:line`.
- **Harden project config:** tighten obviously loose settings, remove committed secrets, ensure credential files are git-ignored (and warn a committed secret persists in git history until purged + rotated).
- Help **read logs** for indicators of compromise if they share them.

Stay defensive and in-project; don't attack back, don't probe others' systems.

## Step 4: What only the USER can do — direct them, don't attempt it

State plainly that you can't and won't do these (it's a safety boundary, not a limitation of effort) — they must:
- Enter passwords, log into or recover accounts, change account/security settings.
- Contact providers/bank/exchange security teams, initiate fraud claims, freeze cards/accounts.
- Move or freeze funds, reverse transactions.
- Install/run system-level security tools, reimage a machine, restore from backup.

Give them the *specific* steps and where to click, but the actions are theirs.

## Step 5: Recover and verify

- Confirm access is regained on the critical accounts and the attacker's access is cut (sessions revoked, keys rotated, MFA on).
- Watch for **persistence** — attackers leave backdoors: recheck email rules/forwarding, OAuth grants, API keys, new users, and any startup/scheduled hooks after the initial cleanup.
- Restore from a known-clean backup only (not one that may contain the compromise).

## Step 6: Escalate when it's beyond self-help

Say so honestly when the situation warrants professionals:
- **Real financial theft / fraud** → bank and exchange fraud teams now; consider law enforcement.
- **Ransomware, or a business/serious compromise** → a professional incident-response service; generally don't pay ransoms without expert advice.
- **Identity theft** → the relevant national identity-theft/reporting service and credit freezes.
You are first-response triage and project hardening — not a substitute for a bank's fraud team or a professional responder when real money or serious compromise is involved.

## Keep a running incident record

As you work through the response, maintain an **`INCIDENT.md`** in the project (or the user's home) — a timestamped checklist of what's been done and what's still pending. During a stressful incident this is genuinely valuable: it stops steps being missed or double-done, and it becomes the timeline the user may later need for their bank, exchange, insurer, or a report. Format simply:

```markdown
# Incident — <date>
## Timeline
- 14:02 isolated laptop from network
- 14:05 changed email password from phone (clean device)
- 14:09 rotated Binance API keys, withdrawals disabled
## Still to do
- [ ] revoke Google OAuth grants
- [ ] full Defender scan (running)
```

Update it as each step completes. It costs almost nothing and turns a panicked scramble into a tracked process.

## Tone

Calm, concrete, prioritized. Lead with the one or two things that matter most right now, then the rest. Short, numbered, do-this-now — not a wall of caveats. Reassure by being organized, not by minimizing.
