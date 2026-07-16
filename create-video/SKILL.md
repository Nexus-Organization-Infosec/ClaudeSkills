---
name: create-video
description: Record and edit a real video end to end — capture the screen (OBS or FFmpeg), transcribe and plan the edit, cut deterministically with FFmpeg, add overlays and motion graphics with Remotion, add music, reframe for social, and render the final MP4. Use whenever the user invokes /create-video or says "make a video", "record a demo / trailer", "edit this footage", "cut a clip for TikTok/YouTube", or "screen record and edit it". Handles both halves: record, then edit. Uses only non-watermarked, properly licensed assets.
---

# Create Video

Take a video from nothing to a finished MP4: **record it, then edit it clean.** The pipeline is a stack of layers, each doing the part it's best at. Full command library is in `references/commands.md` — read it and copy the exact commands from there.

**Prerequisites** (check first, tell the user what's missing): `ffmpeg` on PATH (the workhorse), Node + `npx remotion` for overlays/motion graphics, and a transcription tool (`whisper`) if you need a transcript.

**Installing editing tools is allowed — up to 10GB.** If a needed tool is missing, go ahead and install it; you don't have to ask. The one limit: **do not install any single tool, model, or download larger than 10GB.** Check the size before installing anything big, and if it would exceed 10GB, stop, tell the user, and offer a smaller option (for example a smaller Whisper model like `small` or `base` instead of `large`, or a lighter package) or a workaround. Under 10GB, just install it and carry on.

## How this runs (read first)

- **Everything happens locally, on the user's own PC.** Record, transcribe, cut, compose, and render all with local tools (FFmpeg, Remotion, Whisper) writing to local files. Do NOT push the footage or the edit to a cloud service to do the work. The user's machine is where the video gets made, start to finish.
- **Launch the STOP button first.** At the very start of a create-video run, launch the [[control]] panel (its red STOP button) so the user can stop gracefully at any point without hard-killing a render mid-write. Then check the flag between steps of the pipeline (after each cut batch, before a long render) — if STOP was pressed, finish the current step cleanly, leave the files in a consistent state, and hand back. Relaunch it on `/continue`.
- **Do not stop until the edit is actually finished.** This is a long, multi-step job (record → plan → cut → compose → render → verify), and it is not done until there is a final, playable MP4 that has been verified. Don't hand back half-edited at a "good stopping point", don't stop because a step was tedious or slow, and don't call it finished before the render completes and `ffprobe` confirms it plays. See it all the way through to the finished file. The only things that end a run early are: the user pressing STOP (or interrupting), or a real blocker you cannot get past (a missing tool you can't install, footage that won't record) — and then you say exactly what blocked you, not "this looks about done."

## Layer 1 — Capture

Get the source footage.

- **OBS** if it's installed: launch it recording (`obs64.exe --startrecording --minimize-to-tray`), or drive precise start/stop through the OBS WebSocket if that's set up.
- **No OBS / no OBS control?** Use **FFmpeg screen capture** (`gdigrab` on Windows) — see `commands.md`. It records the desktop or a named window with audio, no extra software.
- **Driving the app while recording** (the common case): start the screen recording, then do the actual thing on screen — launch the app, open the browser, click through the flow — then stop the recording. Record at a fast preset (`ultrafast`); quality re-encode happens later.

## Layer 2 — Transcribe and plan the edit

This is where the thinking happens, before any cut.

1. **Transcribe:** extract audio and run Whisper to get a timestamped transcript (`commands.md`).
2. **Label topics and themes:** read the transcript, mark what each section is about.
3. **Plan structure:** decide what stays, what gets cut, what order works. Best-first for a trailer; logical flow for a demo.
4. **Find dead sections:** pauses, tangents, repeated takes, "um" gaps. Use FFmpeg **silence detection** and **scene detection** (`commands.md`) to find them automatically, then confirm against the transcript.
5. **Write the edit decision list:** a `cuts.txt` of `start,end,label` lines — the exact segments to keep, in order. This is the plan the next layer executes.

## Layer 3 — Deterministic cuts (FFmpeg)

FFmpeg does the boring, exact work: split, trim, concatenate, preprocess. Drive it from the `cuts.txt`:
- Batch-extract each segment by timestamp, concatenate in order into `assembled.mp4`.
- Make a low-res **proxy** for fast scrubbing, **normalize** loudness so levels are even.
- All commands in `commands.md`. Remember `-c copy` snaps to keyframes; re-encode for frame-accurate cuts.

## Layer 4 — Programmable composition (Remotion)

Use Remotion for the things a plain cut can't do, expressed as code:
- **Overlays:** titles, lower-thirds, branding, captions.
- **Motion graphics:** transitions, animated numbers, explainer bits.
- **Product demos:** annotated screenshots, UI highlights, callouts.
- **Reusable scenes:** templates shared across videos.

Bundled, ready to use (MIT, from the claude-code-video-toolkit — see `assets/NOTICE.txt`):
- **`assets/transitions/`** — clean, composable transition components. Import these for consistent fades/wipes instead of hand-rolling them (matches "clean transitions").
- **`assets/brand.json`** — brand tokens (colors, spacing, a type scale, font stacks). Pull styles from here so overlays look coherent, or swap the values for the user's brand.

Compose in `src/`, put segments in `public/segments/`, render with `npx remotion render`.

## Music

Add music only if the user asks. They can hand you a **local file or a link** — use that. Mix it as a bed *under* the voice, ducked so speech stays clear (mix command in `commands.md`). Never add music the user didn't provide or approve.

## Social reframing

Different platforms need different shapes. Reframe the finished cut with FFmpeg (center-crop table + commands in `commands.md`): 16:9 for YouTube, 9:16 for TikTok/Reels, 1:1 for Instagram. For a short-form clip, use the transcript + scene timestamps to pick the most engaging 30-second moments before reframing.

## Hard rules

- **Only non-watermarked, properly licensed assets.** If you fetch stock footage, music, fonts, or images, use genuinely free / royalty-free / CC0 sources (Pexels, Pixabay, and similar) and respect each licence. Never rip watermarked, paid, or copyrighted content, and never try to strip a watermark off someone's work. If the user needs something only available watermarked or paid, tell them, don't work around it.
- **Verify the output actually plays.** After each render, check the file exists, has sane duration and both streams (`ffprobe`), and spot-check it. A corrupt or silent MP4 reported as "done" is the main failure mode here.
- **Keep it clean and simple** unless asked otherwise — restrained cuts, one consistent transition, readable text. Flashy beats nothing, but clean beats flashy.

## Worked example

> `/create-video A trailer for my app in this directory. Launch it with flutter run, open Chrome, record footage while I use and test it in the browser, host my local server so it connects. Then edit cleanly, find stock footage (no watermarks), clean transitions, simplistic.`

1. **Prep:** confirm ffmpeg/node present. Start the app's **local server** so the browser build actually connects, then `flutter run -d chrome` (or build web + serve) so it's live in Chrome.
2. **Record:** start FFmpeg screen capture of the Chrome window, then drive the app — open screens, click the real features, show it working. Stop the capture → `raw.mp4`.
3. **Plan:** transcribe if there's narration; otherwise use scene detection to find the good moments. Write `cuts.txt` keeping the clean, working bits, dropping loading/dead time.
4. **Cut:** FFmpeg extracts + concatenates the kept segments → `assembled.mp4`, normalized.
5. **Compose:** Remotion adds a simple title card, the app name/logo, and clean transitions from `assets/transitions/`, styled from `brand.json`. Optionally a bit of licensed stock B-roll.
6. **Render + reframe:** render to 1080p 16:9, and a 9:16 cut if they want a short.
7. **Verify + hand off:** `ffprobe` the output, confirm it plays, report where it is and its length.

## Notes

Pairs with `/flutter-design` and `/smoothener` (for the app being demoed) and `/research` (finding licensed stock/fonts). The bundled transitions and brand tokens come from the MIT [claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit); that toolkit also has cloud-AI voiceover/image/music generation if the user wants to go further than record-and-edit.
