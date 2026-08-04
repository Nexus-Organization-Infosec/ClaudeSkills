---
name: checklist
description: Put a list of ideas in front of the user as a clickable approval checklist — a bundled CustomTkinter window with a checkbox per idea and a Send/Approve button. Claude writes the ideas to an ideas.txt, launches the panel, and only the CHECKED ideas come back approved (unchecked ones are rejected). Claude then builds only the approved ones. Use whenever the user invokes /checklist or says "let me approve which ideas to do", "show me a checklist to pick from", "give me checkboxes for these", or "I'll tick the ones I want". Great after /improvement-ideas or /new-features for letting the user choose before you build.
---

# Checklist

Turn a list of ideas into a **clickable approval UI**. Claude proposes; the user ticks the ones they want in a real window; Claude builds only those. The user stays in control of what actually gets done, with one click instead of a back-and-forth.

The panel is bundled: `scripts/checklist_panel.py` (CustomTkinter, falls back to plain tkinter). It reads ideas from a file, shows a checkbox per idea (checked by default), and on **Send/Approve** writes the checked ones back and a done flag.

## The file handshake (all in `.claude/checklist/`)

- **`ideas.txt`** — input, **Claude writes it**: one idea per line; blank lines and `#` comments ignored.
- **`approved.txt`** — output, the **panel writes it**: the checked ideas, one per line.
- **`done.txt`** — output, the **panel writes it** when the user acts: `APPROVED` or `CANCELLED`.

## Step 1: Write the ideas

Produce the candidate ideas (your own, or from [[improvement-ideas]] / [[new-features]]) and write them one per line to `.claude/checklist/ideas.txt`. Keep each line a short, clear, self-contained idea the user can judge at a glance — not a paragraph. Create the folder if needed.

```bash
mkdir -p .claude/checklist
cat > .claude/checklist/ideas.txt <<'EOF'
Add a dark-mode toggle to settings
Cache the daily panel to disk (cuts warm-up ~5min)
Add retry+backoff to the price fetcher
# lines starting with # are ignored
EOF
```

## Step 2: Launch the panel (background)

Start it as a background task (Bash tool, `run_in_background: true`) so it doesn't block — use `pythonw` for no console window (`python` also works):

```bash
pythonw C:/Users/flori/.claude/skills/checklist/scripts/checklist_panel.py .claude/checklist/ideas.txt .claude/checklist/approved.txt .claude/checklist/done.txt
```

Tell the user the checklist window is up: tick the ideas you want, then **Send/Approve**; unticked ideas won't be built. (Closing the window with the X approves nothing.)

## Step 3: Wait WITHOUT idling — keep working, or launch a wait task

You need the user's approval before building the ideas — but per [[no-waiting]], **do not block on a `sleep`.** Two acceptable ways:

- **Preferred — keep doing other useful work** while the panel is open, and check for the done flag at each task boundary (a single instant command, never a sleep-then-check):
  ```bash
  [ -f .claude/checklist/done.txt ] && echo READY || echo waiting
  ```
  `waiting` → go do more real work, check again later. `READY` → go to Step 4.
- **If there is genuinely nothing else to do**, launch a proper wait task (the Monitor tool with an until-condition on `.claude/checklist/done.txt` existing) rather than a fixed `sleep`. The harness notifies you when it appears.

Either way: the panel runs on its own and the user clicks when they click — you never freeze waiting for them.

## Step 4: Act on the approved ideas ONLY

When `done.txt` exists:
- If it's `CANCELLED` (or `approved.txt` is empty) → the user approved nothing; don't build anything. Ask if they want a different list or to skip.
- If it's `APPROVED` → read `.claude/checklist/approved.txt`. Those lines are the approved ideas. **Build only those**, in a sensible order. The ideas that were unchecked are **rejected — do not build them**, don't second-guess the user and add them back.

```bash
cat .claude/checklist/done.txt; echo '---'; cat .claude/checklist/approved.txt
```

Then implement each approved idea for real (pair with [[full-implement]] / [[new-features]] / [[fix]] as fits), verify, and report what you built.

## Notes

- Re-runnable: to ask again, overwrite `ideas.txt` with a new list and relaunch (the panel clears the old `done.txt`/`approved.txt` on start).
- Pairs with [[improvement-ideas]] and [[new-features]] (generate the candidates), [[control]] (a STOP button for the build that follows), and [[full-implement]] (build the approved ones properly). Respects [[no-talk]].
- The approval is real user consent gathered through the UI — treat unchecked as an explicit "no", not an oversight.
