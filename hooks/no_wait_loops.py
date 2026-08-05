#!/usr/bin/env python3
"""
PreToolUse hook: block blocking WAIT loops in Bash commands.

This fires on every Bash tool call, regardless of which skill is active, and
denies commands whose only purpose is to sit and wait for something — the
classic time-waster:

    until grep -q "done" out.txt; do sleep 90; done      # polling wait
    sleep 300; check_result                               # long fixed wait

Waiting like this freezes the session for minutes while a job that was already
running on its own finishes. The fix (see the /no-waiting skill) is to launch
the long job in the BACKGROUND (run_in_background) and keep doing other real
work, checking on it with a quick non-blocking peek at task boundaries.

The hook ALLOWS:
  - backgrounded commands (run_in_background=true) — a sleep there isn't blocking
  - short sleeps (< 20s, no loop) — a brief legit pause
  - an explicit escape hatch: put  #allow-wait  in the command if you truly must

Blocks with exit code 2 so the reason is fed back to the model.
"""
import json
import re
import sys


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # can't parse — don't interfere

    if data.get("tool_name") != "Bash":
        sys.exit(0)

    ti = data.get("tool_input") or {}
    # A sleep/loop inside a BACKGROUND command doesn't block the session — allow it.
    if ti.get("run_in_background") is True:
        sys.exit(0)

    cmd = ti.get("command") or ""
    if not cmd:
        sys.exit(0)

    # explicit escape hatch
    if "#allow-wait" in cmd.replace(" ", "").lower() or "# allow-wait" in cmd.lower():
        sys.exit(0)

    reason = None

    # 1) polling loop: while/until ... do ... sleep ... done
    if re.search(r"\b(while|until)\b[\s\S]*\bdo\b[\s\S]*\bsleep\b", cmd) or \
       re.search(r"\b(while|until)\b[\s\S]*\bsleep\b", cmd):
        reason = ("This is a polling WAIT loop (while/until + sleep). It freezes the "
                  "session while a job that is already running finishes.")
    else:
        # 2) a long fixed foreground sleep used to wait (>= 20s, or any m/h/d suffix)
        for m in re.finditer(r"\bsleep\s+([0-9]+(?:\.[0-9]+)?)\s*([smhd]?)", cmd):
            val = float(m.group(1))
            unit = m.group(2)
            long = unit in ("m", "h", "d") or (unit in ("", "s") and val >= 20)
            if long:
                reason = (f"This is a long blocking sleep ({m.group(0).strip()}) used to wait. "
                          "It wastes minutes of session time.")
                break

    if reason:
        msg = (
            "BLOCKED: " + reason + "\n"
            "Do NOT wait like this. Instead:\n"
            "  1. Launch the long job in the BACKGROUND (Bash tool run_in_background: true, "
            "or a detached process writing to a file).\n"
            "  2. Keep doing OTHER useful work in the same turn while it runs.\n"
            "  3. Check on it with ONE quick non-blocking peek at a boundary "
            "(e.g. `tail -3 out.txt`), never a sleep-then-check.\n"
            "The job finishes on its own and the harness notifies you. "
            "See the /no-waiting skill. (If you truly must wait, add `#allow-wait` to the command.)"
        )
        print(msg, file=sys.stderr)
        sys.exit(2)  # exit 2 = block the tool call, feed stderr back to the model

    sys.exit(0)


if __name__ == "__main__":
    main()
