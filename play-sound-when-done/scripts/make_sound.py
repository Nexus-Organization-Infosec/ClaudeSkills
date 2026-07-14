"""
Generate claude_done.wav — a warm, friendly completion chime.

A soft ascending major arpeggio (C5-E5-G5-C6) with a bell-like timbre (a few
harmonics) and a gentle exponential decay so the notes ring and overlap into a
warm chord. Deliberately soft (peaks ~0.5) so it's pleasant over speakers, not
startling. Pure stdlib — no numpy needed.
"""
import math
import os
import struct
import wave

SR = 44100
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "claude_done.wav")

# (frequency Hz, start seconds, duration seconds, relative amplitude)
NOTES = [
    (523.25, 0.00, 1.10, 1.00),   # C5
    (659.25, 0.13, 1.10, 0.92),   # E5
    (783.99, 0.26, 1.20, 0.85),   # G5
    (1046.50, 0.40, 1.30, 0.55),  # C6 — soft sparkle on top
]
TOTAL = 1.9


def main():
    n = int(SR * TOTAL)
    buf = [0.0] * n
    for freq, start, dur, amp in NOTES:
        s0 = int(start * SR)
        ns = int(dur * SR)
        for i in range(ns):
            t = i / SR
            attack = min(1.0, t / 0.006)          # ~6 ms soft attack
            env = attack * math.exp(-t / 0.45)     # bell-like decay
            w = (math.sin(2 * math.pi * freq * t)
                 + 0.22 * math.sin(2 * math.pi * 2 * freq * t)
                 + 0.05 * math.sin(2 * math.pi * 3 * freq * t))
            idx = s0 + i
            if idx < n:
                buf[idx] += amp * env * w

    # "Muffler" — a gentle low-pass (one-pole, applied twice ≈12 dB/oct) rolls off
    # the highs so the chime sounds soft and muffled, like a cloth laid over it.
    cutoff = 2000.0
    dt = 1.0 / SR
    a = dt / (1.0 / (2 * math.pi * cutoff) + dt)
    for _ in range(2):
        y = 0.0
        for i in range(n):
            y += a * (buf[i] - y)
            buf[i] = y

    peak = max(1e-9, max(abs(x) for x in buf))
    scale = 0.38 / peak  # quieter, muffled level

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with wave.open(OUT, "w") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        frames = bytearray()
        for x in buf:
            v = int(max(-1.0, min(1.0, x * scale)) * 32767)
            frames += struct.pack("<hh", v, v)
        wf.writeframes(bytes(frames))
    print("wrote", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
