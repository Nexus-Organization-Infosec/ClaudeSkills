---
name: exploded
description: Turn a 3D-printed / CNC case part set (OpenSCAD lid + floor + PCB STL + extras) into an exploded-view animation - a standalone HTML page (three.js, pure black, one seamless loop) plus an MP4 and a contact sheet - one per module. Use whenever the user invokes /exploded or asks for "exploded view video/animation", "make the module explode", "animate the case parts apart", or "turn the exploded render into a video/HTML". Pairs with the /trailer skill (same rules: frame = pure function of t, black, no glows, GPU parallel render, verify by contact sheet).
---

# Exploded

Every module of a hardware project gets one looping exploded-view film: assembled → lid lifts, floor drops,
board stays → hold while the camera drifts → reassemble → loop. Delivered as

- `<part>.html` — standalone (meshes embedded, three.js from cdnjs), opens in any browser, loops forever,
  `?t=1.5` freezes one frame (that is also how frames are captured)
- `<part>.mp4` — 1280×720 H.264, 6 s at 30 fps, the exact same frames
- `<part>_sheet.jpg` — 6 frames tiled 3×2: check THIS, not the video, before showing anyone

## The tool

The project script does all of it (LINK / FERMION project: `hardware/tools/exploded.py`):

```
python hardware/tools/exploded.py [part ...] [--mp4] [--sec 6] [--fps 30] [--size 1280x720] [--workers 4]
```

Parts come from `hardware/tools/render_sheet.py` `PARTS` (name → include file, lid call, floor call,
board call `|| extra`, title). Output: `hardware/shells/exploded/`. For a new project, copy the script and
point `PARTS` at that project's OpenSCAD part calls; nothing else is project-specific.

How it works:
1. OpenSCAD exports every piece (lid, floor, board, extra) to STL in the real-world orientation
   (`mirror([0,1,0])` like the render views).
2. Positions are quantised to Int16 against each piece's bounding box (6 bytes/vertex), base64'd into the
   page — a module is ~1–3 MB of HTML, no server, no fetch (file:// pages cannot fetch).
3. The page builds a three.js scene; `seek(t)` sets every piece's offset and the camera from `t` alone.
4. Frames: Playwright drives the installed Chrome (`channel="chrome"`, d3d11): ONE page per worker loads the
   page once and calls `window.__link.seek(t)` per frame — ~0.3–0.7 s/frame instead of reloading a 3–8 MB page
   per frame (that was ~5 min per module). Exact frame slices per worker; anything missing falls back to
   one headless Chrome per frame. ffmpeg encodes, ffmpeg tiles the contact sheet.
5. The loop (11 s default, on an 11-step grid scaled to SEC): hold → explode → reassemble → turn the part
   over about its long axis (a pivot group at the part's centre) → explode the UNDERSIDE (local z offsets flip
   with the pivot, so the floor lifts away and the board's bottom side shows) → reassemble → turn back → loop.
   `explode(t, d)` = sum of four smootherstep phases, `flip(t)` = 0 → 180° → 360°; still a pure function of t.
6. Lid-held parts (gold plates / pad board, magnets, platforms, button) carry `follow`: they ride WITH the lid
   first, so nothing ever looks sunk in its window, and separate only once the lid is clearly apart.

Trailer: `hardware/tools/trailer.py` reuses `export()` + `pack()` for a multi-shot three.js film (shots are
functions of local time, hard cuts, custom numpy synth score checked per cut, `--reuse` skips the 5-min mesh
export). Shot ideas that worked: macro on the joint face, a run of 0.9 s module cuts, the product DOING its
thing (modules dropping onto the chip, plates pressing 0.3 mm when docked), a slow orbit of the whole stick.

## Detailed PCBs (mandatory — a flat green slab is a rejected render)

The board piece is NOT the plain OpenSCAD/STL mesh. It comes from KiCad's own coloured 3D export:

```
kicad-cli pcb export glb --subst-models --include-tracks --include-pads --include-silkscreen --include-soldermask -f -o board.glb board.kicad_pcb
```

`tools/glbmesh.py` (no dependencies) flattens the GLB into world-space triangles grouped by material;
`exploded.py` maps every material to a look and embeds each group as its own mesh with the board's motion:
- copper (metallic, yellow) → ENIG gold `#D8AE4E`, metalness ~0.45 (keep it < 0.6 without an env map or it goes
  brown/black); drop copper side-wall triangles (|n_z| < 0.5), they are invisible and ~half the triangle count
- solder mask → green `#1D6E48` at opacity ~0.86 (depthWrite off, renderOrder 2) so the tracks read through it,
  like a real board; pads stay bright gold through the mask openings
- silkscreen → off-white, rough; FR4 core → `#B8AA74` (visible on the board edges)
- component materials → their GLB baseColor converted linear → sRGB (`c ** (1/2.2)`)

Frame mapping: GLB is metres, Y up → KiCad mm = (1000x, 1000z, 1000y) (x, y-down, z-up). Then apply the same
transform the OpenSCAD `board()` module gives the STL (here `x - 100`, `100 - y` after the render mirror) and take
the z offset from the OpenSCAD board STL (`min z` difference) so it lands exactly where the case expects it;
warn if x/y disagree by > 0.3 mm. Find the `.kicad_pcb` by reading the `import("stl/<name>.stl")` inside the
board module (follow a `JOINT == ... ? :` ternary). Use `--flat-pcb` only for a quick geometry check.

Model gotchas found this way (fix the model, not the render):
- KiCad ignores the model `scale` for STEP files (`--subst-models`): a wrong-height part needs its own correctly
  sized model file, not a scale factor.
- EasyEDA (easyeda2kicad) models can sit millimetres off their pads — compare the model bbox with the courtyard
  and fix the footprint's model offset.

Check one still at 1600×900 (`?t=0.2` assembled, `?t=3.0` exploded) before rendering the MP4: mask, gold, silk
and parts must all be visible and nothing may poke through a part that should hide it.

## Rules (inherited from /trailer — each one cost a broken render once)

- **Every frame is a pure function of t.** No state from playback history: the browser loop and the
  capture must produce identical frames, and frames must render in any order.
- **Flat black, nothing behind the object.** No gradients, no glow, no bloom, no orbiting particles.
  Hierarchy from light and position only. One quiet line of type (`LINK  <module>`), bottom-left.
- **Materials honest:** anodised aluminium = mid grey, low metalness without an env map (metal renders
  black otherwise), PCB green, inserts near-black, gold pads flat gold.
- **Motion:** smootherstep easing, lid first, floor 8 % later, extras last; hold assembled at the start and
  end so the loop seam is invisible; camera drift is a sine of t (loops exactly).
- **Windows: headless Chrome needs `--use-angle=d3d11`.** `--use-angle=gl` renders an empty canvas with no
  error. If frames come back black, test one frame with d3d11 / swiftshader before touching the scene.
- Centre and frame on the lid + floor only (board STLs carry far-flung component models).
- Verify by measurement: contact sheet for framing/clipping; count frames (`ok == n`) — a dropped frame
  makes ffmpeg stop early and the MP4 silently shrinks to a few KB.

## Do / don't

- Do render all modules in the background and check each contact sheet; re-render only the ones that fail.
- Don't render MP4s until the geometry is final — it is the slow step and invalidates on any change.
- Don't add a soundtrack unless asked; if asked, follow /trailer scoring (custom synth, one sound = one meaning).
