---
name: swarm
description: Attack one prompt with a parallel team of sub-agents, each on the model that fits its job — Opus 4.8 for the core coding, Sonnet 5 for secondary coding, Haiku 4.5 for the light supporting work — all running at the same time, then merge their results. Effort per agent is settable, e.g. "swarm opus high sonnet5 low haiku4.5 low". This orchestrating model dispatches the agents concurrently (headless, no GUI), monitors them, and can feed each new prompts mid-run. Use whenever the user invokes /swarm or asks to "run a swarm", "parallelize this", "use multiple agents", "split this across models", or "throw a team at it". Best for tasks that break into independent parts; a single tightly-coupled change is better done directly.
---

# Swarm

Run one prompt as a **parallel team** instead of a single sequential pass. You (the lead) decompose the request, dispatch several sub-agents at once — each pinned to the model that suits its part — let them work concurrently, then merge, reconcile, and verify. Faster wall-clock, and each piece runs on the right-sized model.

There is no special "swarm" engine underneath — this is the **Agent tool with a `model` override**, launched in parallel, and **you (the model reading this) are the orchestrator**: you dispatch the agents, watch them, merge them, and can send any of them a new prompt while it runs.

## Invocation & per-agent effort

Grammar: `swarm [<model> <effort>] [<model> <effort>] ...` — e.g.

```
swarm opus high sonnet5 low haiku4.5 low
swarm opus ultra sonnet high            (two agents; Haiku sits out)
swarm                                    (no args → auto: pick the roster and sensible effort per stream)
```

- Model tokens map loosely: `opus`/`opus4.8` → Opus 4.8, `sonnet`/`sonnet5` → Sonnet 5, `haiku`/`haiku4.5` → Haiku 4.5.
- The word after a model is that agent's **effort**. If the user names only some models, launch only those. If no effort is given for a model, use its default (below). If no args at all, you choose the roster and effort from the prompt.

### Effort ladder (what each level means and which models support it)

Effort is set by how you write that agent's brief — the extended-thinking keyword you put in it plus how thorough you tell it to be. There is no numeric knob on the Agent tool; the brief *is* the knob.

| Effort | Put in the brief | Behavior | Best on |
|---|---|---|---|
| **low** | (no thinking keyword) | Fast, direct, minimal deliberation. Mechanical/well-specified work. | Haiku 4.5, Sonnet 5 |
| **medium** | `think` | Normal reasoning, some planning before acting. | Sonnet 5, Opus 4.8 |
| **high** | `think hard` | Deep, careful reasoning; considers edge cases and alternatives. | Opus 4.8, Sonnet 5 |
| **ultra** (a.k.a. `max` / "ultracode") | `ultrathink` | Maximum reasoning budget; deepest analysis, slowest. | **Opus 4.8 only** |

- **Not every model benefits from every tier.** Opus 4.8 supports the whole ladder up to **ultra** — that's the "ultracode" tier. Sonnet 5 tops out usefully around **high**. Haiku 4.5 is built for speed: keep it **low** (medium at most); asking Haiku for `ultra` mostly wastes time for little gain, so if the user requests it, honor it but note it's not Haiku's strength.
- **Match effort to the job, not just the model.** The core/ambiguous stream on Opus deserves `high`/`ultra`; a mechanical test-writing stream on Haiku should be `low` even though it *could* go higher. High effort on trivial work is the same waste `/full-speed` warns about.
- **Defaults when unspecified:** Opus → high, Sonnet → medium, Haiku → low.

Echo the resolved plan back to the user (model + effort + territory per agent) before launching, so they can see what each got.

## The roster (who gets which model)

Assign every work stream to one of these by the *nature* of the task, not by size alone:

- **Opus 4.8 — the core coder.** The hardest, most central, highest-risk coding: the main feature, tricky logic, architecture-level changes, anything subtle where a mistake is expensive. The load-bearing work goes here.
- **Sonnet 5 — the secondary coder.** Real coding that supports the core but is more self-contained: adjacent modules, wiring, a second feature area, refactors, integration glue, straightforward implementation from a clear spec.
- **Haiku 4.5 — the light hands.** Fast, well-scoped supporting work: tests and fixtures, docs/comments, boilerplate and scaffolding, config, simple search-and-report, mechanical edits, formatting. High volume, low ambiguity.

Use `subagent_type: "general-purpose"` for coding streams (full tool access) and set `model` to `"opus"`, `"sonnet"`, or `"haiku"`. For pure investigation streams, `Explore` (read-only) is a fine subagent_type. You don't have to use all three every time — pick the ones the prompt actually needs (see "Right-sizing").

## Step 1: Decompose the prompt into work streams

Read the user's request and split it into **independent** pieces — parts that can proceed without waiting on each other and, ideally, touch **different files**. For each stream decide: what it produces, which files it owns, and which model fits.

The hard constraint: **parallel agents must not edit the same files.** Two agents writing the same module will clobber each other. Partition by file or directory so each stream owns its territory. If parts are genuinely coupled (B needs A's output), they are *not* parallel — either sequence them (A first, then B) or give both to one agent. When in doubt, isolate: launch agents in separate git **worktrees** (`isolation: "worktree"`) so their edits can't collide, and you merge afterward.

If the prompt does **not** split cleanly — one tightly-coupled change, or a tiny task — say so and just do it directly (or with one agent). A swarm on an indivisible task is pure overhead. Don't force three agents onto a one-file fix.

## Step 2: Write a self-contained brief for each agent

Each sub-agent starts cold — it does **not** see this conversation. Its prompt must stand alone. For every agent include:

- **The goal** — exactly what to build/produce, in concrete terms.
- **Its territory** — which files/dirs it owns and, explicitly, which it must NOT touch (the other agents' files).
- **Context it needs** — relevant paths, the interface/contract it must match (function signatures, data shapes, API), conventions to follow. If stream B must call something stream A builds, define that seam *up front* in both briefs so they agree without talking.
- **Definition of done + how to verify** — tests to write/run, the command that proves its piece works.
- **Report format** — what to hand back (files changed, what was done, anything the lead must reconcile).

Fixing the shared interface in advance is what lets independent agents integrate cleanly — pin the seams before launch.

## Step 3: Launch them in parallel

**The default and required way — native background sub-agents, all launched together.** This is what guarantees the three agents work **at the same time, headless, under your control**:

1. **Launch them in ONE message.** Put all the `Agent` calls in a single turn, each with `run_in_background: true`. Launched together in one turn, they execute **concurrently** — the three models work simultaneously, not one waiting for the next. Launching them in separate turns would serialize them; do not do that. One turn, all agents.
2. **Headless by design.** Background sub-agents have **no GUI and open no windows** — they run silently under this session. That is exactly the "headless" the user wants; you don't need `cmd` or `claude -p` to be headless. (A separate *visible-terminal* mode exists as a fallback below, but it is not required and is weaker.)
3. **You stay in control and can re-prompt them.** You (this orchestrating model) are the controller: you get notified as each agent finishes, and you can send **new prompts to a still-running or finished agent with `SendMessage`** (addressed by its id/name), keeping its context — steer it, correct its course, or hand it the next task without re-spawning cold. Record each agent's id/name at launch so you can reach it. This satisfies "the model I'm running controls them and gives them new prompts": that is precisely `SendMessage` to the live agents.
4. **Set the model AND effort per call.** `model: "opus" | "sonnet" | "haiku"`, and bake the resolved effort into that agent's `prompt` (the `think`/`think hard`/`ultrathink` keyword + thoroughness, per the effort ladder). Model + effort together are what make this a real multi-model, multi-effort swarm rather than three identical agents.

**Do not fake concurrency.** If you ever find yourself running one agent, waiting, then the next, that is not a swarm — it defeats the entire point. All agents go out in the same turn.

**Optional fallback — visible headless OS processes.** Only if the user explicitly wants separate terminal windows to watch live: spawn `claude -p "<self-contained brief>" &` per agent (or a `.bat` firing three `start` windows). Downsides: each is a cold one-shot process — you can't cleanly send it new prompts mid-run (no `SendMessage` channel), it has its own auth/cwd, and you must collect each one's output from a file and merge blind. Because the user wants *this model to control and re-prompt the agents*, the native sub-agents above are the correct choice; this fallback trades that control away for visible windows.

**Alternative — headless OS processes (only if the user wants separate visible terminals).** You can instead spawn real background processes with the Bash tool: `claude -p "<self-contained brief>" &` once per agent (or a small `.bat` that launches three `start` windows). This also runs three at once, but each is a cold external process with its own auth/working-dir, no structured hand-back, and you must collect each one's output yourself (have each write to a known file) and merge blind. Only reach for this if the user explicitly wants three independent terminals to watch; otherwise the native sub-agents above are strictly better (structured results, model pinning, `SendMessage` follow-up, integrated verification).

Tell the user the plan before/as you launch: the streams, the model on each, and the file territories — e.g.:

```
Swarm launched (3 agents, parallel):
  • Opus 4.8   → core: implement the order-router in bot/router/        (owns bot/router/*)
  • Sonnet 5   → integration: wire router into live loop in bot/live.py (owns bot/live.py)
  • Haiku 4.5  → tests + docs for the router                            (owns tests/test_router.py, docs/)
```

## Step 4: Merge, reconcile, verify

When the agents return, you are the integrator — this is where a swarm is won or lost:

- **Collect** each agent's output and changed files.
- **Reconcile the seams** — check the pieces actually fit: the integration calls the core's real interface, names/types match, no duplicated or conflicting definitions. If two agents diverged on a shared contract, fix the mismatch (you defined the seam, so you arbitrate).
- **Merge worktrees** if you isolated them; resolve any conflicts.
- **Verify the whole**, not just the parts — run the full build/test suite and the real flow end to end. Individual agents verified their slice; only the lead can confirm the assembled result works. Green parts can still fail together.
- **Report** a short roll-up: what each agent did, how they integrated, final verification result, anything left.

## Right-sizing the swarm

- Scale the roster to the work: a big multi-part feature may use all three (or several of one model); a two-part task might be just Opus + Haiku. Don't spin up an agent with nothing real to own.
- **Don't over-parallelize.** More agents = more merge/reconcile cost. Use the fewest streams that capture the genuine parallelism.
- Keep the **load-bearing, ambiguous, high-risk** work on Opus; push **well-specified, mechanical, high-volume** work to Haiku; Sonnet takes the solid middle. Matching model to task is the point of the skill.

## Notes

- Each spawned agent is a fresh context and a real cost — a swarm trades tokens for wall-clock speed and model-fit. Worth it for genuinely parallel work; wasteful for a small or coupled task (do those directly).
- Pairs with **`/map`** (plan the decomposition first), **`/control`** (STOP button while the swarm runs), and **`/dont-stop-till-complete`** (see the integration all the way through). Respects **`/no-talk`**. Under **`/careful`**, prefer worktree isolation so agents can't touch each other's files.
