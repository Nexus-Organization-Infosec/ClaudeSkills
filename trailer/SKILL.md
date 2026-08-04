---
name: trailer
description: Build a product trailer as HTML scenes rendered to MP4 — the Nexus/Qontext house style. Covers the architecture (every frame a pure function of time, so scrubbing, rendering and parallelism all fall out of it), the editing discipline that makes a cut feel like a film instead of a slideshow (shot-length variance, hard cuts, dissolve limits, scored cuts), the look rules that stop it reading as AI-generated, a custom synth score per film, and a GPU + multi-worker renderer. Also carries the CSS traps that cost real hours on the two films this came from — silent ones a linter has to catch because nothing errors. Use whenever the user invokes /trailer or asks to "make a trailer", "build a promo video", "an Apple-style product film", "a launch video for X", or wants to work on an existing trailer project. Bias toward measuring (shot ratios, sharpness, alignment) over eyeballing.
---

# Trailer

Build a product film as HTML scenes, scrub it live, render it to MP4. This
is the house style of two real trailers (Nexus, Qontext) and everything in
it was paid for by a rejected cut or a silent bug.

The tooling lives in `trailerkit/` (a studio, a 22-scene library, 85
combinable design pieces). This skill is the *judgement* — what to build,
what to cut, and what to never do again.

## The one architectural rule

**Every frame is a pure function of its timestamp.** `window.__nexus.seek(T)`
rebuilds the frame from scratch: CSS animations are paused and their
`currentTime` set to T, JS-painted text is computed from a PRNG seeded on T.

Everything good follows from that:

- you can scrub anywhere instantly, and the render is exactly what you
  scrubbed past
- a screenshot at time T is reproducible, so verification is measurement
  rather than opinion
- **frames are independent, so the render is embarrassingly parallel**

Never introduce state that depends on playback history. If a frame's
appearance depends on how you got there, the render and the preview will
disagree and you will not find out until late.

## Scenes are standalone files, and the build must refuse collisions

One `.html` per scene, carrying its own `<style>`. The build concatenates
every scene's CSS into ONE stylesheet, so two scenes declaring the same
class silently restyle each other. **Fail the build on it.** This is the
single most expensive class of bug in the architecture and it never
announces itself.

Prefix every scene's own classes (`s07-`, `gl-`, `cd-`). It caught a real
one on the Qontext film: a new scene used `cl-` and the close scene already
owned `cl-rule`.

## Editing: the part that decides whether it feels like a film

This is where four rejected cuts of the Qontext trailer went wrong, and
none of them were fixed by changing the look.

**Shot-length variance IS the drama.** Not the average — the ratio. A cut
where every shot is 4.6–6.8s (ratio 1.48) is a metronome; viewers map the
pattern in about nine seconds and stop watching. Aim for **6× or more**
between the longest and shortest shot. Put a 0.9s run directly against a
6s hold.

**Cut hard. Dissolve rarely.** A single global crossfade on every
transition is a slideshow. Make crossfade PER SCENE (`data-xf`, 0 = hard
cut) and let most transitions be hard. Target under 10% of runtime spent
dissolving; the Qontext film went from 15% to 5%.

**A dissolve may not exceed ~40% of the outgoing shot.** It is subtracted
from the END of that shot, so a 600ms fade after a 900ms shot leaves it at
33% opacity two thirds of the way through — the shot renders grey and
nothing tells you why. Enforce it in the build with the maximum it would
accept. You dissolve out of a held shot and cut out of a fast one.

**Every hard cut carries a sound.** A hard cut with silence reads as a
broken edit: the eye jumps and the ear does not. Assert it in the audio
build — a cue within 60ms of every hard cut — and refuse to build
otherwise.

**Then break that rule exactly once.** One deliberately silent cut is a
device. On Qontext it is the discarded line, measurably the quietest cut
in the film, which is what makes it read as *thrown away* rather than
merely next.

**Do not cut between two near-identical frames.** A "match cut" where only
a few words change reads as a dropped frame, not as an edit — there is
nothing for the eye to attribute the change to. Framing them pixel-identical
does not help (measured both at `left=240, top=455` and it still failed).
Make it ONE shot where the thing edits itself in place.

**Give edits room.** Four text edits inside 0.85s look like the sentence
rearranging in one movement; nobody reads the original. Half a second per
edit plus a beat of air.

## The look: what stops it reading as AI-generated

Real notes from the user, and what actually fixed them.

**CHECK THE BACKDROP FIRST.** Before redrawing a single scene, look at
what is behind all of them. An animated accent-coloured radial gradient
drifting behind every frame is, by name, the most-cited tell of generated
design — "animated accent-glow backgrounds", "gradient orbs floating
behind the hero". One film spent hours having individual shots redrawn to
look less generated while that sat behind all sixteen of them, which is
why nothing the content did ever fixed it. **The tell is usually not in
the content.** Apple's answer is the opposite of decoration: vast
expanses of near-pure black, the interface retreating until it is
invisible. Go flat and let the frame be black.

Film grain is not a gradient and can stay — it is real cinema language,
and the renderer replaces it with temporal noise anyway.

**No soft glows.** `box-shadow: 0 0 26px rgba(accent)` on a dot, a bar or
a word is the single most generatively-styled thing you can do. Nothing
in Apple, Braun or Swiss reference work glows — hierarchy comes from
size, weight and position, and colour is flat and precise. Count them
before you defend a scene: nine had crept into one film.

**A glowing accent orb on a smooth curve is THE canonical AI image.**
If a scene is glowing nodes on a sine wave, it does not matter how well
it is animated. Delete it.

**Illustrate BEHAVIOUR, not the name.** The strongest test for a weak
scene: is it showing the product *doing* something, or explaining what it
is called? A quipu cord illustrating a library named after a quipu is
decoration, and no amount of polish fixes decoration. Go read the source
for behaviour nothing has shown yet — a supersede path, a duress code, an
unsend. That is where the good scenes are hiding.

**No rounded translucent cards.** A rounded rectangle with a border, a
tinted fill and a header divider is the house style of every generated
mockup on earth. Three scenes got rejected for exactly this. Replace with
typography: hairline rules, figures in the margin, or nothing at all —
let the content be the type.

**Watch the micro-label tic.** Wide-tracked uppercase monospace captions
are useful once or twice and become a sci-fi-dashboard signature by the
thirteenth. Count those too.

**No chat mockups.** `USER` / `MODEL` labels in small caps is the single
most borrowed form there is. Show the product's *actual* interface instead
— a REPL call, a real prompt, the literal thing. It is more specific AND
makes a better argument.

**Vary the layout.** Thirty of forty scenes on the first film used the
identical centred kicker/headline/sub template. However well each one is
made, one template forty times is what makes a deck read as generated.

**Texture, not fill.** An even field of one dim grey reads as mush. Give
every element its own opacity and light a few, so the eye has somewhere to
land.

**Never claim a feature that does not exist.** One scene on the Nexus film
described something the app did not do. Verify against the source.

## Scoring

**A custom synth per film.** A shared sound bank is how two trailers end up
sounding like the same trailer. Each project gets its own `audio/qsynth.py`.

**Cue by scene STEM, never by filename.** `at("pack")`, not `at("05-pack")`.
The running order gets re-laid constantly and a cue naming a file silently
points at the wrong scene the moment anything moves. Fail loudly on an
unknown stem.

**Derive the timeline from the same source the player uses.** If the audio
build and the player compute starts differently, every cue after the drift
lands early or late and nothing says so.

**One sound should mean one thing.** The Qontext score had 32 plucks in 51
seconds — one every 1.6s — so they stopped meaning anything. Cut to 19,
kept only where a fact is literally being tied. Ask of every cue: what does
this sound *say*?

## Verification is measurement

Eyeballing missed every bug that mattered. What worked:

- **Contact sheets.** Render every scene at 1920×1080 and tile them with
  ffmpeg. Whole-film problems are visible in one image.
- **Shoot before the outgoing fade begins**, or you measure a frame that is
  half faded and conclude the scene is broken.
- **Sharpness as a number.** `mean(abs(diff(gray, axis=1)))` — it proved a
  backdrop-filter was working (0.153 blurred → 1.037 sharp).
- **Alignment as a number.** `getBoundingClientRect()` on both halves of a
  match cut, not a squint.
- **Audio energy per cut.** Short-window RMS at each cut start proves every
  hard cut has an impact and that the silent one really is quietest.

Careful: **in-app browser panes that are not displayed report zero-size
layout**, so geometry checks silently return nonsense. Verify with a real
headless render at a real viewport.

## Rendering: use the GPU and all the cores

Headless Chromium defaults to **SwiftShader**, a software GL. Anything
per-pixel — `backdrop-filter`, `preserve-3d`, big blurs — is then done on
the CPU, and it is catastrophic. Measured on one glass shot:

| mode | fps |
|---|---|
| 1 worker, software GL | 0.8 |
| 6 workers, software GL | 0.4 — *worse*, they thrash each other |
| 1 worker, GPU | 4.5 |
| **4 workers + GPU** | **11.25** |

Full film: 24 minutes → **43 seconds**.

- GPU flags: `--use-angle=gl --enable-gpu-rasterization --ignore-gpu-blocklist`
- Parallel: slice the frame range across N processes, concat with the
  demuxer (`-c copy`, no re-encode). **Slice in exact frames, not seconds** —
  rounding at each seam drops or doubles a frame per boundary.
- Capture JPEG q100, not PNG: measured sharpness-equivalent, 134ms vs 500ms
  a frame. (q95 measured 10.8% softer on fine detail — visible as blurry
  text. Use 100.)
- Encoding is NOT the bottleneck; do not reach for NVENC first.

## The CSS traps

Every one of these is SILENT. Nothing errors, nothing warns, the element
simply does not do what it says. Put them in a linter.

| trap | what happens |
|---|---|
| `var(--x)` with no fallback inside `calc()` inside an `animation` shorthand | invalid at computed-value time, so the **whole** declaration is dropped — name included — and the element never animates |
| a percentage inside `translate()` | resolves against the element's **own** box. A 32% throw moved an element 32% of its own text width. `-50%` is the centring idiom and is fine |
| `animation` is a shorthand | a later rule naming `animation` on the same element drops the earlier one entirely |
| `opacity < 1` on an ancestor | creates a backdrop root (kills `backdrop-filter` inside it) AND is a grouping property (forces `transform-style` back to flat, collapsing 3D). `.content` animating opacity broke both, twice |
| `filter` on an ancestor | same |
| during `animation-delay` | the element shows its **base** style, not the 0% keyframe. Set the hidden state in the base rule |
| `stroke-linecap: round` | paints a cap dot even at full `stroke-dashoffset`, so a "hidden" line speckles the frame |
| `stroke-dasharray` < path length | the line cannot reach the end and a stub stays painted for the whole scene |
| `box-shadow` / `border` on a `clip-path` element | follow the element BOX, not the clip. An inset outline drew a rectangle across the frame. Draw edges as real geometry (SVG) |
| CSS columns | are only as tall as their content. Too few rows and everything balances into column one |
| perspective on a distant ancestor | does essentially nothing — measured 0.27px of near/far spread from the page wrapper vs 21px from the grid's own parent. Put the lens one level above the object |
| SVG children scale about the viewBox origin | unless `transform-box: fill-box` |
| a CSS circle + HTML dots | two coordinate systems; measured 44px of drift. Put ring, spokes and stops in ONE SVG in viewBox units |
| overlapping `backdrop-filter` elements | the blur applies twice and the frame goes milky grey. Tiling partitions (Voronoi) do not overlap; scattered blobs do |
| `opacity: 0` elements with `backdrop-filter` | still composited every frame. Use `visibility: hidden` — it is not interpolated, so it flips at the keyframe and drops the layer |

## Effects worth stealing

- **Glass fracture**: Voronoi partition (each cell = frame rect clipped by
  perpendicular bisectors — Sutherland-Hodgman, no dependencies). Cells tile
  by definition. Seed densely at 2–3 nucleation points and sparsely at the
  edges so shard size varies ~100×. Cell area drives the throw: a big shard
  is heavy, leaves later, slower, turns less. The *cracks* read as glass,
  not the shards — draw them as SVG with staggered `stroke-dashoffset` so
  the fracture races outward. Cracks must leave WITH the glass.
- **3D cord**: beads placed with `translate3d` along a parametric curve
  beat computing `rotate3d` for connected segments, and get perspective
  foreshortening free. Labels alternate above/below — perspective squeezes
  the far half, so evenly spaced anchors do not give evenly spaced labels.
- **Text painters** (pure functions of T): scramble (resolves out of noise),
  degrade (starts readable and rots — usually what people actually mean),
  cipher (needs a per-element `data-seed` or every block shows identical
  characters), odometer (support both a runaway counter and a target it
  eases into).
- **Compression over particles**: scattered fragments on random vectors is
  every generated "data particles" loop there is. Compressing a real object
  — a transcript closing to three lines — says something.

## Working with the user on this

They will reject cuts. The notes are usually about *rhythm* or *borrowed
form*, even when phrased as "looks bad". Before changing the look for a
fourth time, measure the shot-length ratio and count the dissolves.

Show contact sheets, not descriptions. Do not render until asked — it is
the slow step and it invalidates the moment anything changes.
