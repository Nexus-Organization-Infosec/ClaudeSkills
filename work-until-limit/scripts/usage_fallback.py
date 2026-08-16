"""Fallback usage reader: reconstruct the meter from local Claude Code transcripts.

Used when `claude -p "/usage"` returns the cost/token stub instead of the
"Current session: N% used" panel. Needs no CLI and no auth - it only reads
~/.claude/projects/**/*.jsonl, which every Claude Code session writes.

CRITICAL: records are deduplicated by message id. Transcripts replay history
into multiple files on resume, so a naive sum overcounts by 2x or more
(measured 313 records for 147 real messages).

Output is a status file in the same key=value format usage_monitor.ps1 writes,
so the skill's stop logic can read either one.

Usage:
  python usage_fallback.py [-StatusFile PATH] [--session-pct-per-dollar N]

Calibration (turn tokens/cost into a percentage) via env vars:
  WUL_DOLLARS_PER_PCT   USD of session spend per 1% of the session meter
  WUL_TOKENS_PER_PCT    billable tokens per 1% of the session meter
  WUL_WEEK_DOLLARS_PER_PCT / WUL_WEEK_TOKENS_PER_PCT   same for the weekly meter
Anchor these once against a real reading (see SKILL.md "Calibrate the proxy").
Without them the script still reports absolute usage, and PERCENT stays -1.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"
SESSION_WINDOW = timedelta(hours=5)
WEEK_WINDOW = timedelta(days=7)

# USD per million tokens, used only to price the local transcript data when
# ccusage is unavailable. Keys are matched as substrings of the model id.
# Cache write is the 5-minute rate (1.25x input); cache read is 0.1x input.
# Opus 5 / Opus 4.8 / Opus 4.7 / Opus 4.6 are all $5/$25.
PRICES = {
    "fable": {"in": 10.0, "out": 50.0, "cache_w": 12.5, "cache_r": 1.0},
    "mythos": {"in": 10.0, "out": 50.0, "cache_w": 12.5, "cache_r": 1.0},
    "opus": {"in": 5.0, "out": 25.0, "cache_w": 6.25, "cache_r": 0.5},
    "sonnet": {"in": 3.0, "out": 15.0, "cache_w": 3.75, "cache_r": 0.3},
    "haiku": {"in": 1.0, "out": 5.0, "cache_w": 1.25, "cache_r": 0.1},
}
DEFAULT_PRICE = PRICES["opus"]


def price_for(model):
    lowered = (model or "").lower()
    for key, table in PRICES.items():
        if key in lowered:
            return table
    return DEFAULT_PRICE


def parse_ts(raw):
    try:
        return datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def collect(now):
    """Return {window: {...totals}} deduplicated by message id."""
    seen = {}  # msg_id -> (timestamp, model, usage)
    if not PROJECTS.is_dir():
        return None
    for path in PROJECTS.rglob("*.jsonl"):
        try:
            if now - datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > WEEK_WINDOW:
                continue  # file untouched for a week cannot hold in-window records
        except OSError:
            continue
        try:
            handle = path.open("r", encoding="utf-8", errors="replace")
        except OSError:
            continue
        with handle:
            for line in handle:
                if '"usage"' not in line:
                    continue
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                msg = rec.get("message") or {}
                usage = msg.get("usage")
                if not isinstance(usage, dict):
                    continue
                ts = parse_ts(rec.get("timestamp"))
                if ts is None or now - ts > WEEK_WINDOW:
                    continue
                key = msg.get("id") or rec.get("uuid")
                if key is None:
                    continue
                # Same id can appear many times; keep one copy.
                seen[key] = (ts, msg.get("model", ""), usage)

    windows = {"session": SESSION_WINDOW, "week": WEEK_WINDOW}
    out = {}
    for name, span in windows.items():
        totals = {"msgs": 0, "in": 0, "out": 0, "cache_w": 0, "cache_r": 0, "cost": 0.0}
        for ts, model, usage in seen.values():
            if now - ts > span:
                continue
            tin = usage.get("input_tokens", 0) or 0
            tout = usage.get("output_tokens", 0) or 0
            tcw = usage.get("cache_creation_input_tokens", 0) or 0
            tcr = usage.get("cache_read_input_tokens", 0) or 0
            price = price_for(model)
            totals["msgs"] += 1
            totals["in"] += tin
            totals["out"] += tout
            totals["cache_w"] += tcw
            totals["cache_r"] += tcr
            totals["cost"] += (
                tin * price["in"] + tout * price["out"]
                + tcw * price["cache_w"] + tcr * price["cache_r"]
            ) / 1_000_000
        totals["billable"] = totals["in"] + totals["out"] + totals["cache_w"]
        out[name] = totals
    return out


def env_float(name):
    raw = os.environ.get(name)
    if not raw:
        return None
    try:
        value = float(raw)
    except ValueError:
        print(f"warning: {name}={raw!r} is not a number, ignoring", file=sys.stderr)
        return None
    return value if value > 0 else None


def to_percent(totals, dollars_key, tokens_key):
    """Percent from whichever calibration anchor is set; cost wins if both are."""
    per_dollar = env_float(dollars_key)
    if per_dollar:
        return round(totals["cost"] / per_dollar, 1), "cost"
    per_token = env_float(tokens_key)
    if per_token:
        return round(totals["billable"] / per_token, 1), "tokens"
    return -1, "uncalibrated"


def bar(pct, width=20):
    if pct < 0:
        return "(uncalibrated - absolute usage only)"
    filled = max(0, min(width, int(round(pct / 100 * width))))
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-StatusFile", "--status-file", dest="status_file")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    data = collect(now)
    if data is None:
        print("STATUS=UNKNOWN\nreason=no ~/.claude/projects directory", file=sys.stderr)
        return 2

    session, week = data["session"], data["week"]
    spct, sbasis = to_percent(session, "WUL_DOLLARS_PER_PCT", "WUL_TOKENS_PER_PCT")
    wpct, _ = to_percent(week, "WUL_WEEK_DOLLARS_PER_PCT", "WUL_WEEK_TOKENS_PER_PCT")
    higher = max(spct, wpct)

    lines = [
        "STATUS=ESTIMATE",
        "SOURCE=local-transcripts",
        f"BASIS={sbasis}",
        f"PERCENT={higher}",
        f"SESSION={spct}",
        f"WEEK={wpct}",
        f"SESSION_MSGS={session['msgs']}",
        f"SESSION_BILLABLE={session['billable']}",
        f"SESSION_CACHE_READ={session['cache_r']}",
        f"SESSION_COST_USD={session['cost']:.2f}",
        f"WEEK_MSGS={week['msgs']}",
        f"WEEK_BILLABLE={week['billable']}",
        f"WEEK_COST_USD={week['cost']:.2f}",
        f"BAR={bar(spct)}",
        f"UPDATED={now.astimezone().strftime('%Y-%m-%d %H:%M:%S')}",
    ]
    text = "\n".join(lines) + "\n"

    if args.status_file:
        try:
            Path(args.status_file).parent.mkdir(parents=True, exist_ok=True)
            Path(args.status_file).write_text(text, encoding="utf-8")
        except OSError as exc:
            print(f"warning: could not write status file: {exc}", file=sys.stderr)
    if not args.quiet:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
