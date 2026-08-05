# Hooks

Optional Claude Code hooks that make some skill rules mechanical (enforced), not just guidance.

## no_wait_loops.py — prevent blocking waits (pairs with the /no-waiting skill)

A `PreToolUse` hook that blocks Bash commands whose only purpose is to sit and wait:
polling loops (`while`/`until` + `sleep`) and long fixed foreground sleeps (>= 20s). It
allows backgrounded commands, short sleeps, and quick non-blocking checks. Escape hatch:
put `#allow-wait` in the command.

### Install
1. Copy `no_wait_loops.py` to `~/.claude/hooks/` (Windows: `C:\Users\<you>\.claude\hooks\`).
2. In `~/.claude/settings.json` add:
```json
"hooks": {
  "PreToolUse": [
    { "matcher": "Bash",
      "hooks": [ { "type": "command", "command": "python ~/.claude/hooks/no_wait_loops.py" } ] }
  ]
}
```
   (use the absolute path to the script). Takes effect on a new session.
