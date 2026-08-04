"""
checklist_panel.py — a CustomTkinter approval checklist for the /checklist skill.

Claude writes a list of ideas (one per line) to an ideas file; this panel shows
each as a checkbox with an Approve (send) button. When the user clicks Approve,
the CHECKED items are written to the approved file and a done flag is written, so
Claude knows the user has responded and which ideas to act on. Unchecked items
are NOT approved. Closing the window without approving counts as approve-nothing.

Usage:
    python checklist_panel.py <ideas_file> <approved_file> <done_file>

Files:
    ideas_file    (input)  one idea per line; blank lines and lines starting with
                           '#' are ignored. Claude writes this.
    approved_file (output) the checked ideas, one per line. Panel writes this.
    done_file     (output) written when the user acts: "APPROVED" or "CANCELLED".
                           Claude polls/waits for this to appear.

Falls back to plain tkinter if customtkinter isn't installed.
"""
import os
import sys

try:
    import customtkinter as ctk
    HAVE_CTK = True
except Exception:
    HAVE_CTK = False
    import tkinter as tk


def read_ideas(path):
    ideas = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                t = line.strip()
                if t and not t.startswith("#"):
                    ideas.append(t)
    except FileNotFoundError:
        pass
    return ideas


def atomic_write(path, text):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def main():
    if len(sys.argv) < 4:
        print("usage: checklist_panel.py <ideas_file> <approved_file> <done_file>")
        sys.exit(2)
    ideas_file, approved_file, done_file = sys.argv[1], sys.argv[2], sys.argv[3]
    ideas = read_ideas(ideas_file)

    # clear any stale done flag from a previous round
    for p in (done_file, approved_file):
        try:
            if os.path.exists(p):
                os.remove(p)
        except OSError:
            pass

    if not ideas:
        atomic_write(approved_file, "")
        atomic_write(done_file, "CANCELLED")
        print("no ideas to show; wrote empty approval.")
        return

    # ---- build the UI ----
    if HAVE_CTK:
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        root = ctk.CTk()
    else:
        root = tk.Tk()
        root.configure(bg="#1a1a1a")

    root.title("Approve ideas")
    root.geometry("560x620")
    try:
        root.attributes("-topmost", True)
    except Exception:
        pass

    vars_and_text = []

    def approve():
        checked = [txt for (v, txt) in vars_and_text if bool(v.get())]
        atomic_write(approved_file, "\n".join(checked) + ("\n" if checked else ""))
        atomic_write(done_file, "APPROVED")
        root.destroy()

    def cancel():
        atomic_write(approved_file, "")
        atomic_write(done_file, "CANCELLED")
        root.destroy()

    if HAVE_CTK:
        header = ctk.CTkLabel(root, text="Check the ideas you approve, then Send.",
                              font=ctk.CTkFont(size=15, weight="bold"))
        header.pack(padx=16, pady=(16, 4), anchor="w")
        sub = ctk.CTkLabel(root, text="Unchecked ideas are NOT approved.",
                           text_color="#9aa0a6", font=ctk.CTkFont(size=12))
        sub.pack(padx=16, pady=(0, 10), anchor="w")

        # select-all / none row
        row = ctk.CTkFrame(root, fg_color="transparent")
        row.pack(fill="x", padx=12)
        def set_all(val):
            for (v, _t) in vars_and_text:
                v.set(1 if val else 0)
        ctk.CTkButton(row, text="Select all", width=100, height=26,
                      fg_color="#3a3a3a", hover_color="#4a4a4a",
                      command=lambda: set_all(True)).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="Clear all", width=100, height=26,
                      fg_color="#3a3a3a", hover_color="#4a4a4a",
                      command=lambda: set_all(False)).pack(side="left")

        scroll = ctk.CTkScrollableFrame(root, fg_color="#202020")
        scroll.pack(fill="both", expand=True, padx=12, pady=12)
        for txt in ideas:
            v = ctk.IntVar(value=1)  # default: checked (approve unless unchecked)
            cb = ctk.CTkCheckBox(scroll, text=txt, variable=v, onvalue=1, offvalue=0,
                                 font=ctk.CTkFont(size=13))
            cb.pack(anchor="w", padx=8, pady=6, fill="x")
            vars_and_text.append((v, txt))

        btnrow = ctk.CTkFrame(root, fg_color="transparent")
        btnrow.pack(fill="x", padx=12, pady=(0, 14))
        ctk.CTkButton(btnrow, text="Cancel", width=120, height=40,
                      fg_color="#5a2a2a", hover_color="#6a3030",
                      command=cancel).pack(side="left")
        ctk.CTkButton(btnrow, text="Send / Approve", height=40,
                      font=ctk.CTkFont(size=15, weight="bold"),
                      fg_color="#2e7d32", hover_color="#256628",
                      command=approve).pack(side="right", fill="x", expand=True, padx=(10, 0))
    else:
        tk.Label(root, text="Check the ideas you approve, then Send.\nUnchecked ideas are NOT approved.",
                 bg="#1a1a1a", fg="white", justify="left").pack(padx=16, pady=12, anchor="w")
        frame = tk.Frame(root, bg="#202020")
        frame.pack(fill="both", expand=True, padx=12, pady=12)
        canvas = tk.Canvas(frame, bg="#202020", highlightthickness=0)
        sb = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg="#202020")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        for txt in ideas:
            v = tk.IntVar(value=1)
            tk.Checkbutton(inner, text=txt, variable=v, bg="#202020", fg="white",
                           selectcolor="#202020", activebackground="#202020",
                           anchor="w", justify="left", wraplength=460).pack(anchor="w", fill="x")
            vars_and_text.append((v, txt))
        br = tk.Frame(root, bg="#1a1a1a"); br.pack(fill="x", padx=12, pady=10)
        tk.Button(br, text="Cancel", command=cancel, bg="#5a2a2a", fg="white").pack(side="left")
        tk.Button(br, text="Send / Approve", command=approve, bg="#2e7d32", fg="white").pack(side="right")

    root.protocol("WM_DELETE_WINDOW", cancel)  # closing the X = approve nothing
    root.mainloop()


if __name__ == "__main__":
    main()
