"""
gen_sound.py — a small, dependency-free sound synthesizer for the /sound-generator skill.

Drive it with a JSON spec (a file path, or piped on stdin) describing notes and
global shaping, and it writes a 16-bit stereo WAV. Pure Python stdlib — no numpy,
no external audio libs — so it runs anywhere Python does.

USAGE
  python gen_sound.py --spec spec.json                 # write the WAV named in the spec
  echo '{...}' | python gen_sound.py --spec -           # spec on stdin
  python gen_sound.py --spec spec.json --play           # write, then play it (Windows)
  python gen_sound.py --demo chime --out out.wav --play # built-in example spec

SPEC SHAPE (all fields optional except notes)
  {
    "out": "path/to/file.wav",     # output path (or pass --out)
    "sr": 44100,                    # sample rate
    "gain": 0.4,                    # final peak level 0..1 (headroom; keep <=0.8)
    "lowpass": 2000,                # optional one-pole low-pass cutoff Hz (softens/muffles); omit for bright
    "notes": [
      {
        "note": "C5",              # note name (C0..B8, sharps '#', flats 'b') OR "freq": 523.25
        "start": 0.0,               # seconds from t0
        "dur": 1.0,                 # seconds
        "amp": 1.0,                 # relative amplitude 0..1
        "wave": "bell",            # sine | square | saw | triangle | bell | noise
        "attack": 0.006,            # seconds fade-in
        "decay": 0.45,              # exp decay time-constant (bigger = rings longer); 0 = flat+release
        "vibrato": 0.0,             # Hz depth of pitch wobble (0 = none)
        "vibrato_rate": 5.0         # Hz of the wobble
      }
    ]
  }

Percussive/alert sounds: use "wave":"noise" or "square" with short dur (0.05-0.15)
and small decay. Melodic/pleasant: "bell"/"sine" with longer dur and a lowpass.
"""
import argparse
import json
import math
import os
import struct
import sys
import wave

A4 = 440.0
NAME_TO_SEMITONE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def note_to_freq(name):
    """'C5', 'F#4', 'Bb3' -> Hz. A4=440. MIDI: C4=60."""
    name = name.strip()
    letter = name[0].upper()
    if letter not in NAME_TO_SEMITONE:
        raise ValueError(f"bad note name: {name!r}")
    i = 1
    semis = NAME_TO_SEMITONE[letter]
    while i < len(name) and name[i] in "#b":
        semis += 1 if name[i] == "#" else -1
        i += 1
    octave = int(name[i:])
    midi = (octave + 1) * 12 + semis   # C4 -> (4+1)*12 + 0 = 60
    return A4 * (2 ** ((midi - 69) / 12.0))


def _wave_sample(kind, phase, t, freq):
    """One oscillator sample. phase is in turns (0..1 per cycle)."""
    if kind == "sine":
        return math.sin(2 * math.pi * phase)
    if kind == "square":
        return 1.0 if (phase % 1.0) < 0.5 else -1.0
    if kind == "saw":
        return 2.0 * (phase % 1.0) - 1.0
    if kind == "triangle":
        p = phase % 1.0
        return 4.0 * abs(p - 0.5) - 1.0
    if kind == "bell":
        # a few harmonics -> warm, bell-like
        return (math.sin(2 * math.pi * phase)
                + 0.22 * math.sin(2 * math.pi * 2 * phase)
                + 0.05 * math.sin(2 * math.pi * 3 * phase))
    if kind == "noise":
        # deterministic-ish pseudo noise (no import random needed per-sample cost)
        x = math.sin((t * freq * 12.9898 + 78.233) * 43758.5453)
        return 2.0 * (x - math.floor(x)) - 1.0
    # default
    return math.sin(2 * math.pi * phase)


def render(spec):
    sr = int(spec.get("sr", 44100))
    notes = spec.get("notes", [])
    if not notes:
        raise ValueError("spec has no notes")

    total = max((n.get("start", 0.0) + n.get("dur", 1.0)) for n in notes) + 0.15
    n_total = int(sr * total)
    buf = [0.0] * n_total

    for note in notes:
        if "freq" in note:
            freq = float(note["freq"])
        else:
            freq = note_to_freq(note["note"])
        start = float(note.get("start", 0.0))
        dur = float(note.get("dur", 1.0))
        amp = float(note.get("amp", 1.0))
        kind = note.get("wave", "sine")
        attack = float(note.get("attack", 0.006))
        decay = float(note.get("decay", 0.45))
        vib = float(note.get("vibrato", 0.0))
        vib_rate = float(note.get("vibrato_rate", 5.0))

        s0 = int(start * sr)
        ns = int(dur * sr)
        phase = 0.0
        for i in range(ns):
            t = i / sr
            # envelope
            a = min(1.0, t / attack) if attack > 0 else 1.0
            if decay > 0:
                env = a * math.exp(-t / decay)
            else:
                # flat with a short release at the tail
                rel = min(1.0, (dur - t) / 0.02) if dur - t < 0.02 else 1.0
                env = a * max(0.0, rel)
            # instantaneous frequency with optional vibrato
            f = freq * (1.0 + (vib / freq) * math.sin(2 * math.pi * vib_rate * t)) if vib > 0 else freq
            phase += f / sr
            w = _wave_sample(kind, phase, t, freq)
            idx = s0 + i
            if 0 <= idx < n_total:
                buf[idx] += amp * env * w

    # optional low-pass (one-pole applied twice ~= 12 dB/oct) to soften/muffle
    cutoff = spec.get("lowpass")
    if cutoff:
        dt = 1.0 / sr
        coef = dt / (1.0 / (2 * math.pi * float(cutoff)) + dt)
        for _ in range(2):
            y = 0.0
            for i in range(n_total):
                y += coef * (buf[i] - y)
                buf[i] = y

    peak = max(1e-9, max(abs(x) for x in buf))
    gain = float(spec.get("gain", 0.4))
    scale = gain / peak
    return sr, buf, scale


def write_wav(path, sr, buf, scale):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with wave.open(path, "w") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        frames = bytearray()
        for x in buf:
            v = int(max(-1.0, min(1.0, x * scale)) * 32767)
            frames += struct.pack("<hh", v, v)
        wf.writeframes(bytes(frames))


DEMOS = {
    # warm ascending arpeggio (like the done-chime)
    "chime": {
        "gain": 0.4, "lowpass": 2200,
        "notes": [
            {"note": "C5", "start": 0.00, "dur": 1.1, "amp": 1.00, "wave": "bell", "decay": 0.45},
            {"note": "E5", "start": 0.13, "dur": 1.1, "amp": 0.92, "wave": "bell", "decay": 0.45},
            {"note": "G5", "start": 0.26, "dur": 1.2, "amp": 0.85, "wave": "bell", "decay": 0.45},
            {"note": "C6", "start": 0.40, "dur": 1.3, "amp": 0.55, "wave": "bell", "decay": 0.45},
        ],
    },
    # two quick blips — a notification
    "alert": {
        "gain": 0.5,
        "notes": [
            {"note": "A5", "start": 0.00, "dur": 0.09, "amp": 1.0, "wave": "square", "decay": 0.05},
            {"note": "A5", "start": 0.14, "dur": 0.09, "amp": 1.0, "wave": "square", "decay": 0.05},
        ],
    },
    # low error buzz
    "error": {
        "gain": 0.5,
        "notes": [
            {"note": "A3", "start": 0.00, "dur": 0.28, "amp": 1.0, "wave": "saw", "decay": 0.0},
            {"note": "F3", "start": 0.18, "dur": 0.34, "amp": 1.0, "wave": "saw", "decay": 0.0},
        ],
    },
    # success rising three-note jingle
    "success": {
        "gain": 0.45, "lowpass": 3000,
        "notes": [
            {"note": "E5", "start": 0.00, "dur": 0.18, "amp": 1.0, "wave": "triangle", "decay": 0.0},
            {"note": "G5", "start": 0.16, "dur": 0.18, "amp": 1.0, "wave": "triangle", "decay": 0.0},
            {"note": "C6", "start": 0.32, "dur": 0.55, "amp": 1.0, "wave": "bell", "decay": 0.4},
        ],
    },
}


def play(path):
    """Play a WAV synchronously on Windows via .NET SoundPlayer."""
    import subprocess
    ps = (
        "$p = New-Object System.Media.SoundPlayer '{}'; "
        "$p.PlaySync();"
    ).format(os.path.abspath(path).replace("'", "''"))
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", help="JSON spec file, or '-' for stdin")
    ap.add_argument("--demo", choices=sorted(DEMOS), help="use a built-in example spec")
    ap.add_argument("--out", help="output WAV path (overrides spec's 'out')")
    ap.add_argument("--play", action="store_true", help="play the result after writing")
    args = ap.parse_args()

    if args.demo:
        spec = dict(DEMOS[args.demo])
    elif args.spec == "-":
        spec = json.load(sys.stdin)
    elif args.spec:
        with open(args.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
    else:
        ap.error("need --spec or --demo")

    out = args.out or spec.get("out")
    if not out:
        ap.error("no output path (use --out or 'out' in the spec)")

    sr, buf, scale = render(spec)
    write_wav(out, sr, buf, scale)
    print("wrote", os.path.abspath(out), f"({len(buf)/sr:.2f}s)")
    if args.play:
        play(out)


if __name__ == "__main__":
    main()
