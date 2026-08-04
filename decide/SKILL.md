---
name: decide
description: Let the model choose which skill(s) to apply to the request on its own — read the task, pick the best-fitting skills from the library, and use them, always AT LEAST ONE. Use whenever the user invokes /decide or says "you pick the skill", "choose the right approach", "use whatever skills fit", "decide how to handle this", or "figure out the best way yourself". The user is delegating the skill choice to you; you must commit to at least one skill and say which you chose and why, then carry the task out under it.
---

# Decide

The user is handing you the choice of *how* to approach the task — which skill or skills fit best. Your job: read the request, survey the available skills, pick the ones that genuinely match, announce them, and then do the work under them. **You must select at least one skill — "none" is not an allowed answer.**

## Step 1: Read the task for what it actually needs

Look past the surface wording to the real shape of the request:
- Is it a **bug/error** to fix? a **new capability** to build? **cleanup**? **docs**? **performance**? **security**? **planning** a big multi-step job? a **long autonomous** run? a **UI**? a **sound/video**? a **decision/idea** request?
- What **mode** does the user seem to want — careful and minimal, fast and quiet, exhaustive, offline, parallel?
- Are there cues about **duration or autonomy** (leaving, overnight, "until the limit", "don't stop")?

## Step 2: Match to the skills — pick the best fit(s)

Go through the skill library (the descriptions you can see) and select what genuinely applies. Match on the *purpose* of each skill, not a keyword. Typical mappings:

- Fix a specific bug/error → `/fix` (or `/quick-fix` if it's obvious and you just want it patched).
- Find unknown bugs → `/bug-hunt`. Security audit → `/reverse-engineer`. Under active attack → `/protect`.
- Make it better → `/improve` (or `/improve N`). Faster → `/improve-performance`. Add features → `/new-features N`.
- Clean/organize → `/cleanup` (`/quick-cleanup` for a light pass). Document → `/documentate` (`/quick-documentate` short).
- Plan a big job first → `/map`. Ideas/backlog → `/improvement-ideas` or `/later-ideas`.
- Finish stubs/fake code → `/placeholder-replacer`. Level up shallow code → `/full-implement`.
- Flutter/Material UI → `/flutter-design`. UI polish/animation → `/smoothener`. Sound → `/sound-generator`. Video → `/create-video`.
- Long autonomous run → `/work-until-limit` (+ `/control`), until a time → `/work-until-time`. Parallel multi-model → `/swarm`.
- Behavior modes that ride *alongside* the above → `/careful`, `/full-speed`, `/no-talk`, `/no-internet`, `/stay-here`, `/just-do-it`, `/dont-stop-till-complete`.

Prefer the **smallest set that fully serves the task.** One well-chosen skill usually beats a pile. Add a second (often a mode like `/careful` or `/quick-*`, or a companion like `/control` for a long run) only when it clearly adds value.

## Step 3: Respect the combination rules

Some skills cannot be combined — honor the same restrictions the skills themselves state (e.g. `/pause` and `/continue` are opposites; `/no-talk` conflicts with skills whose whole point is discussion; `/dont-use-skills-rn` turns the layer off). If two candidates conflict, pick the one that better serves the request; don't stack contradictory modes. If the user has `/dont-use-skills-rn` active, note that `/decide` is an explicit slash invocation and so is honored, but keep the chosen set minimal.

## Step 4: Commit, announce, and do it

- **Always land on at least one skill.** If nothing screams a match, choose the closest reasonable fit rather than defaulting to nothing — e.g. a plain "improve this" with no specifics → `/improve`; an ambiguous coding task → `/just-do-it` or `/map`. There is always a defensible pick; make it.
- **Say what you chose and why**, in one or two lines: `Using /fix (root-cause a real bug) + /careful (production code, minimal touch).` Keep it short.
- Then **carry out the task under those skills**, following each chosen skill's discipline. Don't just name them — actually apply them.

## Notes

- `/decide` picks the *approach*; it doesn't change what the user asked for. Deliver the actual task, just under the skill(s) you selected.
- If the request is genuinely trivial and no specialized skill adds anything, the minimal honest pick is a lightweight mode like `/just-do-it` or `/full-speed` — that still satisfies "at least one" without over-engineering.
- Respects [[no-talk]] (state the pick in one line, then work), and defers to an explicit skill the user names themselves — if they already said `/cleanup`, there's nothing to decide.
