---
name: invent
description: Think like an inventor and produce a genuinely NEW invention — not a rehash of something that exists, not an incremental tweak, but an original idea worked out into something real. Explore the problem from first principles, generate bold and unobvious concepts, pick the strongest, and develop it into a concrete, buildable design (how it works, why it's novel, what it takes to make). Use whenever the user invokes /invent or says "invent something new", "think like an inventor", "come up with an original idea/product/mechanism", "what could we create that doesn't exist yet", or "give me a real invention". Bias hard toward originality and feasibility over safe, obvious answers.
---

# Invent

Put on the inventor's hat and create something **new**. The whole point is originality — a real invention, not a summary of what already exists, not "app X but with Y", not a trivial variation. Think from first principles, chase the non-obvious, then ground the best idea into something concrete enough to actually build or prototype.

## The inventor's mindset

- **Start from the problem or the phenomenon, not from existing products.** Ask what people actually need, what's fundamentally hard, what a physical/mathematical/economic principle would *allow* if someone bothered to exploit it. Inventions come from the gap between "what's possible" and "what exists."
- **Question the assumptions everyone else accepts.** The best inventions delete a constraint others treat as fixed ("why does it need a battery at all?", "why must this be centralized?", "why is this done in software when the medium could do it?").
- **Combine distant fields.** Novelty often lives at the collision of two unrelated domains — biology × logistics, acoustics × security, thermodynamics × UI. Deliberately import a mechanism from a field far from the problem.
- **Chase the idea that sounds slightly absurd** but you can't immediately prove impossible. Safe and obvious is the enemy here; the target is "wait, could that actually work?"

## How to invent (the process)

1. **Frame it.** If the user gave a domain or problem, anchor there; if they gave nothing, pick a rich vein (or ask what area excites them). State the problem or opportunity crisply, including the constraint you suspect can be broken.
2. **Diverge — generate many bold candidates, using the idea engines below.** Produce a spread of genuinely different concepts, not five flavors of one. Push past the first obvious answers (those are what everyone already thought of) into the unobvious ones. Quantity and range first; judge later. Don't just "be creative" — run the engines.
3. **Select.** Pick the single strongest candidate on **novelty × feasibility × value** — it must be actually new, plausibly buildable, and worth building. Say briefly why it beats the others.
   - **Verify the novelty — prior-art check.** Before committing to "this is new," actually check that it doesn't already exist: search for it ([[research]] / the web), name the closest existing things, and confirm your idea does something they don't. If it turns out to exist, that's a *good* outcome caught early — either sharpen the idea until it's genuinely differentiated, or drop to your next candidate. Claimed novelty that a five-minute search would disprove is the most embarrassing failure of an "invention."
4. **Develop it into a real invention.** Work the chosen idea out concretely:
   - **What it is** — one sharp sentence a smart person immediately gets.
   - **How it works** — the actual mechanism/principle, in enough detail that it's clearly not hand-waving. The core novel step is the heart of it — make that explicit.
   - **Why it's new** — what it does that nothing existing does, and which assumption it breaks. Note the closest existing things and how this differs (so it's genuinely novel, not reinvented).
   - **Why it matters** — the value: who benefits, how much, why now.
   - **How to build it** — the concrete path: key components, the hardest technical risk, the cheapest prototype that would prove the core idea, and roughly what it'd take.
5. **Pressure-test it honestly.** Name the biggest reason it might fail (physics, cost, adoption, a hidden assumption) and whether there's a way around it. An invention you've stress-tested is worth ten you've only celebrated. If the core idea collapses under the test, say so and either fix it or swap to your next-best candidate — don't dress up a broken idea.

## Idea engines — concrete ways to force novelty (don't just "brainstorm")

"Be creative" produces safe, obvious ideas. Real inventors run *mechanisms* that manufacture the unobvious. Use these on the diverge step — run several, they each surface different ideas:

- **The contradiction method (the big one).** Most problems hide a **trade-off everyone treats as a law**: "to make it stronger you must make it heavier", "to make it more secure you must make it slower", "to make it cheaper you must make it worse". Name that contradiction explicitly — *improving X currently forces Y to get worse*. Then invent the thing that **refuses the trade-off** — that gets X *without* paying Y — instead of balancing it. Breakthroughs are almost always a resolved contradiction, not a compromise. Ask: what would have to be true for this trade-off to simply not exist? Then build toward that.
- **Assumption inversion.** List the assumptions everyone accepts about how this is done, then deliberately flip each one and see what becomes possible. "It must be centralized" → what if it's peer-to-peer? "It needs a battery" → what if it harvests its own power? "The reader is active, the tag passive" → what if it's the other way round? The invention often lives on the far side of one flipped assumption.
- **Cross-domain transplant.** Take a mechanism that works brilliantly in a *distant* field and import it into this problem. Retroreflectors (optics) → acoustics. Immune systems (biology) → intrusion detection. Ant foraging → routing. Force the transplant even when it feels wrong; the friction is where novelty hides.
- **Push to the extreme.** Ask what the solution looks like at the limits — if it had to be 100× cheaper, 1000× faster, work with zero power, scale to a billion, or run for a century unattended. Extremes break normal approaches and force a fundamentally different one.
- **Remove the expensive part.** Whatever is the most costly, fragile, or complex component of how this is done today — ask what the thing looks like *without it at all*. The best inventions often *delete* a component everyone assumed was mandatory.

Run at least the contradiction method plus one other; name which engine produced the candidate you pick, so the novelty is traceable to a mechanism, not luck.

## Build it, if asked

`/invent` defaults to producing the invention *concept* worked out as above. If the user wants it made real ("and build it", "prototype it"), go straight into implementing the cheapest proof-of-core from step 4 — real code/design, not a mockup — and pair with [[full-implement]] for a production-grade build.

## What NOT to do

- Don't hand back something that already exists under a new name, or an incremental feature of a known product. That's not an invention.
- Don't stop at the first idea — the first idea is almost always the obvious one. Push for the unobvious.
- Don't hide behind vagueness. "An AI-powered platform for X" is not an invention; the *mechanism* is the invention. Be concrete about the novel step.
- Don't fake feasibility. If the clever part depends on something that can't work, say so — honest constraints make the next idea better.

## Notes

- Pairs with [[full-implement]] (turn the invention into a real, complete build), [[later-ideas]] (park promising inventions for when the project's ready), [[improvement-ideas]] (that one improves an existing project; this one creates something new), and [[research]] (check whether a candidate already exists / find the prior art to differentiate against).
- Bias toward originality and concreteness the whole way through — a bold, buildable, clearly-novel idea is the deliverable, not a safe familiar one.
