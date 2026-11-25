---
name: judge
description: Give an honest, evidence-based verdict on a project (or a part of one) on a fixed 10-level scale from Broken (1) to Perfect (10). Establishes what the project is FOR, gathers fresh evidence (builds, tests, lint, docs, measurements) instead of trusting claims, scores each dimension with the evidence behind it, applies the cap rule (the property the project exists for limits the overall level), and ends with the concrete steps to reach the next level. Invoked as "judge" for the current project, "judge <path or part>" for a specific target, or "judge strict" to also flag every unverified claim. Use whenever the user invokes /judge or asks "rate this project", "how good is this, 1 to 10", "judge my code", "is this production-ready", "be brutally honest about this", or "where does this stand".
---

# Judge

Give the user a verdict they can trust: one level on a fixed scale, the evidence behind it, and what it would take to go one level higher. A judgment is only useful if it's calibrated. Inflated praise wastes the user's time and hides the risk that matters most. Gratuitous harshness is just as wrong. Rate what you can show.

## Invocation

- **`judge`** judges the project in play (the current repo or the work in this conversation).
- **`judge <path or part>`** judges that target only, such as `judge src/net` or `judge the GUI`.
- **`judge strict`** also lists every claim you could not verify (in docs, comments, or earlier messages) with the reason.

If there is no project in play and none named, ask what to judge.

## The scale

| Level | Name | Meaning |
|---:|---|---|
| 1 | Broken | Does not build or run, or does active harm (data loss, a security hole by design). |
| 2 | Fragile | Runs on the happy path only. Wrong or crashing in common cases. No tests. |
| 3 | Toy | Works for a demo. Little error handling, untested edges, unclear purpose. |
| 4 | Prototype | Main features work and some are tested. Clear gaps, including in the property the project exists for. |
| 5 | Solid prototype | Well-engineered, tested, documented. The purpose-critical property is still unproven, so it is not fit for real use yet. |
| 6 | Beta | Fit for low-stakes real use. Core properties verified. Rough edges and missing polish remain. |
| 7 | Production-ready | Fit for its stated purpose. Failure modes handled, verified by tests that would catch a regression. Someone else could maintain it. |
| 8 | Mature | Proven in real use, reviewed by people other than its author, monitored or released through CI. Few known issues. |
| 9 | Excellent | Best in its niche. Independently audited or benchmarked. Exemplary tests and docs. |
| 10 | Perfect | Reference grade: nothing material left to improve, and others learn from it. Practically unreachable; do not award it casually. |

Most real projects land between 3 and 6. A 9 needs outside evidence (an audit, a benchmark, sustained real use), never only your own reading.

## How to judge

### 1. Establish what it is for

Write one sentence: what the project is supposed to do, for whom, and at what stakes. The same code can be a 7 as a weekend tool and a 3 as banking software. If the purpose isn't stated anywhere, infer it from the README, the code, and the conversation, and say that you inferred it.

Then name the **purpose-critical property**: the one thing that, if it fails, makes the project worthless or dangerous. Examples: confidentiality for an encryption tool, correctness of results for a calculator, not losing data for a backup tool, uptime for a server.

### 2. Gather fresh evidence

Never judge from memory, from the README's claims, or from what you remember building. Check now:

- **Build:** does it build cleanly? Count warnings.
- **Tests:** run them. Record the pass/fail counts and what they actually cover. A test only counts if it would fail when the thing it protects broke. Look for tests that cannot fail, such as statistical checks without a positive control or "regression vectors" that only pin current output.
- **Lint and static checks:** run the project's linter if one exists.
- **The purpose-critical property:** what evidence exists that it holds? Tests, measurements, a review, a proof, real-world use, or nothing?
- **Docs:** do they match the code? Spot-check two or three claims against reality.
- **History:** recent commits, open TODOs, known issues the project itself lists.
- **Measure** anything the verdict depends on (speed, size, error rates) instead of quoting numbers.

Keep the evidence brief, but keep it real: numbers, file names, test names.

### 3. Score the dimensions

Score each dimension 1–10 on the same scale, with one line of evidence. Use the dimensions that fit the project. The usual set:

- **Purpose-critical property** (always first)
- Correctness and tests
- Robustness and failure handling
- Security (if it touches untrusted input, secrets, or a network)
- Usability (UI, CLI, API ergonomics)
- Performance (against what the purpose needs, not against an abstract ideal)
- Documentation and honesty
- Maintainability (structure, lint, build, CI)

### 4. Apply the cap rule

**The overall level cannot exceed the purpose-critical score + 3**, and it can never reach 6 (Beta, "fit for real use") while the purpose-critical property is unverified. Great engineering around an unproven core is a Solid prototype (5), not a product. Otherwise the overall is roughly the typical dimension score, not the best one. Say which rule set the number.

### 5. Deliver the verdict

Use this structure:

1. **Level N/10: Name.** One sentence that a person could act on.
2. **What it is for**, and the purpose-critical property (one or two lines).
3. **Dimension table:** dimension, score, the evidence in a few words.
4. **What caps it.** The one or two reasons it isn't a level higher.
5. **Strongest points.** Two or three, with evidence. Being specific about what is good makes the criticism credible.
6. **To reach the next level.** Concrete, ordered steps. Each should be something a person could start tomorrow.
7. **Not checked.** Anything you could not verify, and why. In `strict` mode, also list each unverified claim.

## Calibration rules

- **No grade inflation.** Effort, line count, and the number of features do not raise the level. A huge, untested codebase is still a Toy.
- **Judging your own work:** if you built or changed this project in the conversation, say so up front and apply extra skepticism. Check your own earlier claims as hard as anyone else's.
- **Separate "well made" from "fit for purpose".** Say both when they differ. That is often the most useful sentence in the verdict.
- **Name the risk the user most needs to hear** even if it is unwelcome, such as "this should not protect real data yet". Say it once, plainly, with the evidence, and without lecturing.
- **Prefer the user's goals to generic ideals.** Performance that is fine for the stated purpose scores fine.
- **Half levels are not allowed.** Pick the level whose description fits better, and say what tipped it.
