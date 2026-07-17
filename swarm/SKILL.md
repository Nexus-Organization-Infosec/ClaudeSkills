---
name: swarm
description: Attack one prompt with a parallel team of sub-agents, each on the model that fits its job — Opus 4.8 for the core coding, Sonnet 5 for secondary coding, Haiku 4.5 for the light supporting work — all running at the same time, then merge their results. Decomposes the prompt into independent work streams, dispatches the three agents concurrently with self-contained briefs, and integrates + verifies the combined output. Use whenever the user invokes /swarm or asks to "run a swarm", "parallelize this", "use multiple agents", "split this across models", or "throw a team at it". Best for tasks that break into independent parts; a single tightly-coupled change is better done directly.
---

# Swarm

Run one prompt as a **parallel team** instead of a single sequential pass. You (the lead) decompose the request, dispatch several sub-agents at once — each pinned to the model that suits its part — let them work concurrently, then merge, reconcile, and verify. Faster wall-clock, and each piece runs on the right-sized model.

There is no special "swarm" engine underneath — this is the **Agent tool with a `model` override**, launched in parallel. That's the whole trick, done deliberately.

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

Dispatch all the agents **in a single message** (multiple Agent calls in one turn) so they run concurrently. Subagents run in the background by default — you'll be notified as each finishes. Note each agent's id/name so you can follow up via `SendMessage` (same context) if a brief needs a tweak, rather than re-spawning cold.

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
