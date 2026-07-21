# create-video — command library

Copy-paste commands for the pipeline. Needs `ffmpeg` on PATH; Remotion needs Node.

## Windows / Git Bash gotchas (learned the hard way — read these)

- **Complex `-vf` filter strings get mangled by Git Bash.** The colons and slashes (`scale=...:...`, `(ow-iw)/2`) get turned into `;` and `\2`, and paths like `/Windows/...` get rewritten. **Fix:** write the filtergraph to a file and pass it with `-/vf filter.txt` (ffmpeg 7+ reads an option value from a file), or run the ffmpeg line from a `.bat`. Simple commands (record, cut, concat) are fine directly; only the filter graphs need this.
- **Write the filter file with NO trailing newline** — `-/vf` treats a trailing `\n` as an empty extra filter and errors with "Error parsing a filter description around:". Use `printf '%s' '...' > filter.txt`, not an editor that appends a newline.
- **`drawtext` fonts on Windows:** do NOT use `font=Arial` (fontconfig often has no config file and segfaults). Use `fontfile=`. And a drive-letter **colon in the font path breaks the filter parser**, even escaped. **Fix:** copy the `.ttf` into the working dir (`cp /c/Windows/Fonts/arialbd.ttf font.ttf`) and reference it colon-free as `fontfile=font.ttf`, running ffmpeg from that dir. Inside the filter, escape commas in expressions: `enable=between(t\,0.5\,4)`.

## Capture (record the screen)

**OBS** (if installed) — launch already recording, stop via its hotkey or `--shutdown`:
```
obs64.exe --startrecording --minimize-to-tray
```
(Precise programmatic start/stop wants the OBS WebSocket + `obs-cli`/`obws`. If that's not set up, use the ffmpeg fallback below.)

**FFmpeg screen capture (Windows, no OBS needed):**
```
# whole desktop, 30fps, with system + mic audio (adjust device names via: ffmpeg -list_devices true -f dshow -i dummy)
ffmpeg -f gdigrab -framerate 30 -i desktop -f dshow -i audio="Microphone (Realtek Audio)" -c:v libx264 -preset ultrafast -crf 20 raw.mp4

# a single window by title
ffmpeg -f gdigrab -framerate 30 -i title="Chrome" -c:v libx264 -preset ultrafast -crf 20 raw.mp4
```
Stop with `q` on the ffmpeg process (or send it a graceful stop). Record at a fast preset; re-encode later.

## Transcribe

```
# extract 16kHz mono wav for transcription
ffmpeg -i raw.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav

# transcribe with Whisper (pip install openai-whisper) — produces srt with timestamps
whisper audio.wav --model small --output_format srt
```

## Deterministic cuts (FFmpeg)

```
# extract one segment by timestamp (stream copy = fast, no re-encode)
ffmpeg -i raw.mp4 -ss 00:12:30 -to 00:15:45 -c copy segment_01.mp4

# batch cuts from an edit decision list (cuts.txt lines: start,end,label)
mkdir -p segments
while IFS=, read -r start end label; do
  ffmpeg -i raw.mp4 -ss "$start" -to "$end" -c copy "segments/${label}.mp4"
done < cuts.txt

# concatenate segments in order
for f in segments/*.mp4; do echo "file '$f'"; done > concat.txt
ffmpeg -f concat -safe 0 -i concat.txt -c copy assembled.mp4

# fast low-res proxy for scrubbing/editing
ffmpeg -i raw.mp4 -vf "scale=960:-2" -c:v libx264 -preset ultrafast -crf 28 proxy.mp4

# normalize loudness
ffmpeg -i segment.mp4 -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:v copy normalized.mp4
```
Note: `-c copy` cuts snap to keyframes. For frame-accurate cuts, re-encode (`-c:v libx264 -crf 18` instead of `-c copy`).

## Scene + silence detection (for auto-cutting)

```
# scene changes (0.3 = moderate sensitivity) → timestamps
ffmpeg -i input.mp4 -vf "select='gt(scene,0.3)',showinfo" -vsync vfr -f null - 2>&1 | grep showinfo

# silent stretches (dead air), quieter than -30dB for 2s+
ffmpeg -i input.mp4 -af silencedetect=noise=-30dB:d=2 -f null - 2>&1 | grep silence
```

## Social reframing (aspect ratios)

| Platform | Ratio | Resolution |
|---|---|---|
| YouTube | 16:9 | 1920x1080 |
| TikTok / Reels | 9:16 | 1080x1920 |
| Instagram feed | 1:1 | 1080x1080 |
| X / Twitter | 16:9 or 1:1 | 1280x720 or 720x720 |

```
# 16:9 → 9:16 vertical (center crop)
ffmpeg -i input.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" vertical.mp4

# 16:9 → 1:1 square (center crop)
ffmpeg -i input.mp4 -vf "crop=ih:ih,scale=1080:1080" square.mp4
```

## Music

```
# mix a music bed under the video (music quieter, ducked)
ffmpeg -i assembled.mp4 -i music.mp3 -filter_complex \
  "[1:a]volume=0.25[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=2[a]" \
  -map 0:v -map "[a]" -c:v copy final.mp4
```

## Transitions and effects (do NOT ship a bare cut)

**Transitions between segments** with FFmpeg `xfade` (offset = when the transition starts):
```
# crossfade two clips (types: fade, wipeleft, slideup, circleopen, dissolve, smoothleft, radial, ...)
ffmpeg -i a.mp4 -i b.mp4 -filter_complex \
  "[0][1]xfade=transition=smoothleft:duration=0.6:offset=4.4" out.mp4
```
For many segments, chain xfades, or use Remotion transitions (the bundled `../assets/transitions/`) for consistency.

**Ken Burns (slow zoom/pan on stills or flat footage)** — adds life to static shots:
```
ffmpeg -i clip.mp4 -vf "zoompan=z='min(zoom+0.0008,1.15)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080,fps=30" -c:v libx264 out.mp4
```

**Animated title** (slide/fade a caption in, not a static box). Use `alpha` and `x` as functions of time in `drawtext`:
```
# fade a title in over 0.5s and out, moving up slightly (put the filter in a file, see gotchas above)
drawtext=fontfile=font.ttf:text=The Claude App:fontcolor=white:fontsize=110:x=(w-text_w)/2:y=(h-text_h)/2-40*t:alpha='if(lt(t,0.5),t/0.5,if(lt(t,3.5),1,if(lt(t,4),(4-t)/0.5,0)))':enable=between(t\,0\,4)
```

**Color grade / punch** (light, tasteful):
```
ffmpeg -i in.mp4 -vf "eq=contrast=1.06:saturation=1.08:brightness=0.01,unsharp=5:5:0.5" -c:v libx264 out.mp4
```

**Burn-in captions** from an SRT (great for social):
```
ffmpeg -i in.mp4 -vf "subtitles=captions.srt:force_style='Fontsize=22,Outline=2,Shadow=0'" -c:v libx264 out.mp4
```

## Remotion (programmable composition for overlays / motion graphics)

Setup once:
```
npm create video@latest   # or: npx create-video@latest
# put your cut segments in public/segments/, compose in src/, then:
```

Basic composition (`src/VlogComposition.tsx`):
```tsx
import { AbsoluteFill, Sequence, Video, useCurrentFrame } from "remotion";

export const VlogComposition: React.FC = () => {
  return (
    <AbsoluteFill>
      <Sequence from={0} durationInFrames={300}>
        <Video src={require("../public/segments/intro.mp4")} />
      </Sequence>
      <Sequence from={30} durationInFrames={90}>
        <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
          <h1 style={{ fontSize: 72, color: "white", textShadow: "2px 2px 8px rgba(0,0,0,0.8)" }}>
            The AI Editing Stack
          </h1>
        </AbsoluteFill>
      </Sequence>
      <Sequence from={300} durationInFrames={450}>
        <Video src={require("../public/segments/demo.mp4")} />
      </Sequence>
    </AbsoluteFill>
  );
};
```

Render:
```
npx remotion render src/index.ts VlogComposition output.mp4
```

Reusable clean transitions live in `../assets/transitions/` (bundled from the MIT claude-code-video-toolkit) — import them into your Remotion project for consistent fades/wipes. Brand tokens (colors, spacing, type scale) are in `../assets/brand.json`.
