---
name: save-usage
description: Reduce how fast the account's weekly (and session/daily) usage burns, so the limit lasts longer. Diagnoses what's actually driving the user's usage (via the /usage breakdown) and applies the real levers — smaller context, shorter sessions, targeted work, cheaper models. Use whenever the user invokes /save-usage or asks to "keep my weekly usage low", "use less quota", "make my limit last", "why is my usage so high", or "conserve tokens". The opposite intent of /work-until-limit (which deliberately spends the budget).
---

# Save Usage — make the limit last

Usage burns roughly in proportion to **how many tokens get processed per turn × how many turns** — and by far the biggest hidden driver is **context size**: every turn re-processes the whole conversation + files + tools in context, so a bloated context makes *every* turn expensive. The goal here is to cut that waste without cutting the work.

## Step 1: Diagnose — don't guess, read the actual drivers

The `/usage` command shows a "What's contributing to your limits usage" breakdown. Read it and target the top contributor. Always read usage with this exact PowerShell form (Git Bash mangles the `/usage` argument, and `2>&1 | Out-String` captures the whole panel including stderr as one string):

```bash
powershell.exe -NoProfile -Command 'claude -p "/usage" 2>&1 | Out-String; $out'
```

Look at the contributing factors, e.g. "*95% of your usage was at >150k context*" or "*81% came from sessions active for 8+ hours*". Those two are the usual culprits and both point at the same fix: **context has grown too big and sessions run too long.**

## Step 2: The levers, biggest first

### 1. Keep context small (the #1 lever)
Because every turn re-bills the full context, a 150k-token context can cost several times what a 40k one does for the *same* task.
- **`/clear` between unrelated tasks** — start a fresh, small context instead of dragging the whole history along.
- **`/compact` when a session gets long** — collapse the back-history into a summary so the token count drops.
- **Read narrowly** — open only the relevant part of a file (offset/limit), not whole huge files; don't re-read files already in context.
- **Trim what's always loaded** — disable MCP servers you're not using (their tool defs sit in every turn), and keep `CLAUDE.md` / memory lean. Big tool lists and long instruction files are a per-turn tax.

### 2. Shorter, focused sessions
Long marathon sessions accumulate context and rack up turns on top of it. Break work into shorter sessions; `/clear` when you switch topics. A quick task in a fresh session is cheap; the same task 6 hours into a giant session is not.

### 3. Be targeted — fewer, higher-value turns
- Plan, then execute — avoid exploratory thrashing and redundant tool calls.
- Don't re-run searches/reads you've already done; reuse what's in context.
- Prefer one well-scoped request over ten vague back-and-forths.

### 4. Match the model to the task
Use a smaller/faster model (Haiku/Sonnet) for routine edits, boilerplate, and simple questions; reserve the most expensive model for genuinely hard reasoning. Lower thinking/effort for simple tasks.

### 5. Don't deliberately burn
Obvious but worth stating: `/work-until-limit`, `/ultragoal`, and long autonomous runs *intentionally* spend to the ceiling. If you're trying to conserve, don't run those — they're the opposite of this skill.

## Step 3: Give a concrete, personalized plan

Don't dump the whole list — tell the user the one or two changes that will move *their* number most, based on Step 1. If their driver is high context, lead with `/clear`/`/compact` habits and trimming loaded files/MCPs. If it's long sessions, lead with breaking sessions up. Quantify where you can ("your usage is ~95% at >150k context — clearing between tasks to stay under ~60k could cut that dramatically").

## Note

Prompt caching already discounts an unchanged context prefix within a session, so the worst waste is *growing* the context and *thrashing* the stable parts (tools, system prompt, early history). Keeping context small and stable is the through-line behind every lever above.
