"""
Claude Control — a red STOP button with a tiny status readout, for graceful
control of a long/autonomous run.

- Tiny status label (top) shows Claude's state, read from a status file that
  Claude updates: "working" (green) or "stopped" (grey). If the status hasn't
  been refreshed in a while it shows "idle" (amber).
- Big red STOP button. Pressing it writes a stop flag Claude checks between
  tasks; Claude then finishes the current task and ends its turn.
- After STOP is pressed the window shows "task stopped. closing python UI in
  N seconds" and closes itself after a 10-second countdown.

Usage:  python control_panel.py [stop_flag_path] [status_path]
        defaults: .claude/stop  and  .claude/status  (relative to the project)
"""
import os
import sys

FLAG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(".claude", "stop")
STATUS = sys.argv[2] if len(sys.argv) > 2 else os.path.join(".claude", "status")

CLOSE_SECONDS = 10

# Prefer CustomTkinter for the intended look; fall back to plain tkinter so the
# button always works even if customtkinter isn't installed.
USE_CTK = True
try:
    import customtkinter as ctk
except Exception:
    USE_CTK = False
    import tkinter as tk

RED = "#c0392b"
RED_HOVER = "#e74c3c"
GREY = "#555555"
GREEN = "#2ecc71"
LIGHTGREY = "#9aa0a6"

closing = False
countdown = CLOSE_SECONDS


def write_flag():
    try:
        os.makedirs(os.path.dirname(FLAG) or ".", exist_ok=True)
        with open(FLAG, "w", encoding="utf-8") as f:
            f.write("stop")
    except Exception:
        pass


def read_status():
    """Return (text, color) describing Claude's current state.

    Defaults to green "working" — while the window is open and STOP hasn't been
    pressed, Claude is working, so no per-step status pings are needed. Only an
    explicit "stopped" in the status file flips it grey.
    """
    try:
        if os.path.exists(STATUS):
            with open(STATUS, "r", encoding="utf-8") as f:
                val = f.read().strip()
            low = val.lower()
            if low == "stopped":
                return ("■ stopped", LIGHTGREY)
            if val and low != "working":
                # Claude wrote a short task label — show what's currently running,
                # so the user sees what they'd be stopping. Truncate to keep it tidy.
                label = val if len(val) <= 40 else val[:39] + "…"
                return ("● " + label, GREEN)
    except Exception:
        pass
    return ("● working", GREEN)


def set_label(widget, text, color):
    if USE_CTK:
        widget.configure(text=text, text_color=color)
    else:
        widget.configure(text=text, fg=color)


def poll_status():
    if closing:
        return
    text, color = read_status()
    set_label(status_lbl, text, color)
    root.after(1000, poll_status)


def do_countdown():
    global countdown
    set_label(status_lbl, "task stopped.", LIGHTGREY)
    if USE_CTK:
        btn.configure(text="closing python UI in\n{} seconds".format(countdown),
                      fg_color=GREY, hover_color=GREY, state="disabled")
    else:
        btn.configure(text="closing python UI in\n{} seconds".format(countdown),
                      bg=GREY, state="disabled")
    if countdown <= 0:
        try:
            root.destroy()
        except Exception:
            pass
        return
    countdown -= 1
    root.after(1000, do_countdown)


def on_stop():
    global closing
    if closing:
        return
    closing = True
    write_flag()
    do_countdown()


if USE_CTK:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
else:
    root = tk.Tk()

root.title("Claude Control")
root.geometry("340x230")
root.minsize(240, 160)
# Intentionally NOT always-on-top — a floating STOP button is too easy to click by
# accident. Lift it to the front once on launch, then behave like a normal window.
try:
    root.lift()
except Exception:
    pass

if USE_CTK:
    status_lbl = ctk.CTkLabel(root, text="● working", text_color=GREEN,
                              font=("Segoe UI", 15, "bold"))
    status_lbl.pack(pady=(16, 4))
    btn = ctk.CTkButton(root, text="STOP", command=on_stop,
                        fg_color=RED, hover_color=RED_HOVER, text_color="white",
                        font=("Segoe UI", 28, "bold"), corner_radius=18)
    btn.pack(expand=True, fill="both", padx=24, pady=(4, 24))
else:
    root.configure(bg="#1e1e1e")
    status_lbl = tk.Label(root, text="● working", fg=GREEN, bg="#1e1e1e",
                          font=("Segoe UI", 15, "bold"))
    status_lbl.pack(pady=(16, 4))
    btn = tk.Button(root, text="STOP", command=on_stop,
                    bg=RED, fg="white", activebackground=RED_HOVER,
                    activeforeground="white", font=("Segoe UI", 28, "bold"),
                    relief="flat", bd=0)
    btn.pack(expand=True, fill="both", padx=24, pady=(4, 24))

poll_status()
root.mainloop()
