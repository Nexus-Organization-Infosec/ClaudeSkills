---
name: 3d
description: Render PCBs and designs in 3D and, when asked, design the enclosure / mechanical parts in OpenSCAD - KiCad STL export, parametric OpenSCAD cases fitted to the real board (fit-checked by intersection), clean 2x2 render sheets (outside / inside / exploded / underside), concept option sheets A-D, aluminium CNC split (part + plastic inserts) and STEP export. ALWAYS asks its questions first with the AskUserQuestion tool. Use whenever the user invokes /3d or asks to "render the board", "show it in 3D", "design a case / enclosure / housing", "make it printable / CNC", "show me options". Pairs with /pcb-design and /exploded.
---

# 3D

Make it visible and make it fit. Method from the FERMION/LINK project (20+ cases, all fit-checked).

## Step 0 — ask first (MANDATORY, with the AskUserQuestion tool)

One AskUserQuestion call, options tailored to the request:
1. **What** — render an existing board, design a new case, show design options, or all of these.
2. **Material** — 3D print (PLA/PETG), CNC aluminium (anodised), or both.
3. **Look** — minimal / rounded / rugged; colours; logo or label engraving.
4. **Views** — 2x2 sheet (outside/inside/exploded/underside), option sheet A-D, animation (/exploded).

## Tools (this machine)

- OpenSCAD nightly: `"C:\Program Files\OpenSCAD (Nightly)\openscad.exe" --backend=manifold`.
- Board STL: `kicad-cli pcb export stl --subst-models -f -o out.stl board.kicad_pcb` (run sequentially -
  parallel exports collide).
- Render: `--imgsize=960,640 --viewall --autocenter --colorscheme=Tomorrow --camera=0,0,0,rx,0,rz,0`; preview
  mode keeps colours (`--render` drops them).
- FERMION repo helpers: `tools/render_sheet.py` (2x2 sheets, pure-python PNG + bitmap font),
  `tools/concept_sheet.py` (scad with `SEL = "A".."D"` → option sheet), `tools/case_probe.py` + `case_gen.py`
  (measure the board, generate caps/floors), `tools/alu_export.py` + `alu_step.py` + `step_check.py`.

## Case design rules

- Parametric library: shared frame/constants (wall, seam, plate, PCB z), `vbox(x0,x1,v0,v1,z0,z1)` with
  v = y - centre, generated per-part modules with cut lists as children.
- Rounded aluminium look: rounded box = hull of rotate_extruded "pucks"; clip the 2D profile to x >= 0
  (otherwise OpenSCAD silently drops the shape), and the helper must take the same y convention as the
  rest (a centre-vs-absolute mix shifts every shell sideways). Ends R3, long edges R1.2, seams R0.4 on BOTH
  halves so joints close flush.
- Fit-check every part — but NOT with OpenSCAD `intersection() { part(); board(); }` alone: KiCad board STLs are
  usually NOT closed meshes, the manifold backend then fails and returns an EMPTY result, which looks exactly
  like a pass ("top level object is empty"). Check the log for "NotManifold". Reliable method (FERMION repo
  `tools/fitcheck.py`): export the case part (always a closed solid) and test board points against it with
  trimesh `contains()` — all vertices PLUS ~400k surface samples (faces crossing a thin skin have no vertex
  inside it), ignore points < 0.02 mm deep (contact faces).
- Openings measured from the probe (connector boxes), heights budgeted (parts vs lid).
- Swappable shells: one set of screws from below opens everything (floor posts clamp the PCB).
- Engrave logos 0.3 mm (laser-mark on aluminium).

## 3D print (PLA / PETG / ASA) — when the user picks printing

- Walls >= 1.6 mm (4 perimeters of 0.4), floors >= 1.2 mm; M2 screws into heat-set inserts (hole 3.2 for an
  M2 x 3 insert) or self-tapping into a 1.7 pilot; posts >= 4.2 mm OD.
- Fit clearance 0.2–0.3 mm per side between printed parts (0.1 for aluminium); test-print the joint first.
- Print orientation: lids top-face down on the bed (clean visible face), floors flat; no unsupported overhang
  > 45° — chamfer instead of round on bed-facing edges; bridges <= 10 mm.
- Text/logos: emboss/deboss 0.6 mm minimum (0.3 only works on CNC laser marking).
- Snap-fits and living hinges only in PETG; PLA creeps under screw load and softens at 55 °C (car, sun) → PETG
  or ASA for anything carried around.
- RF windows are free (plastic is transparent to RF): no inserts needed, but keep >= 1 mm air over antennas.
- Export STL per part, plus a 3MF with the plate layout if the user has a printer; JLC3DP / similar for
  ordering (SLA resin for fine detail, MJF PA12 for strength).
- Same fit-check rule as CNC: `intersection() { part(); board(); }` must be empty or contact-only.

When the user chooses BOTH, design for CNC (tighter) and offer a print variant via a `MAT = "PRINT"` switch that
thickens walls, widens clearances and swaps tap holes for insert holes.

## Aluminium (CNC)

Split each part into `alu = part - zones` and `insert = part ∩ zones` (RF windows over antennas, touch
windows, insulating pin guards, light pipes) → together they rebuild the fit-checked shape exactly.
M2 holes as 1.6 tap drills. Sliding faces hard-anodised; contact faces masked. JLCCNC needs STEP:
mesh → sewn solid → ShapeUpgrade_UnifySameDomain (OCP, `pip install cadquery-ocp`), then verify every file
is ONE valid solid with the STL's volume.

## Render pitfalls

- Boards must render with detail (gold pads/tracks, mask, silkscreen, real parts), never as a single-colour
  slab: for three.js / animation use KiCad's GLB export (see /exploded "Detailed PCBs"); for OpenSCAD stills
  use the STL only for fit-checks and composite the GLB/raytraced board for presentation renders.

- Coplanar faces between parts z-fight in preview → offset 0.01–0.05.
- `intersection()` / imported-STL cuts render glitchy in preview → render from exported pieces or rotate the
  cut toward the camera instead.
- Outer `color()` wins over inner colours in this OpenSCAD build → give extras their own slot.
- A file open in a viewer cannot be overwritten on Windows → write a new filename.
- Always look at the sheet you produced before sending it; fix and re-render if anything is clipped,
  floating, mis-coloured or empty.
