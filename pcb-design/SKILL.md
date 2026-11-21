---
name: pcb-design
description: Design a real, orderable PCB for a request - parts chosen from JLCPCB/LCSC stock, a Python KiCad 10 generator (schematic + board), placement, Freerouting auto-route with keep-best, A* finishing, DRC/ERC/parity checks, JLCPCB gerbers + BOM + CPL. ALWAYS asks its questions first with the AskUserQuestion tool. Use whenever the user invokes /pcb-design or asks to "design a PCB / board / circuit board", "make a module board", "route this board", "make it orderable at JLC". Pairs with /3d (renders + OpenSCAD case) and /exploded.
---

# PCB design

Turn a request into a board that is actually routed and orderable — never a sketch, never "simulated".
This is the method that produced 25+ fully routed boards in the FERMION/LINK project.

## Step 0 — ask first (MANDATORY, with the AskUserQuestion tool)

Before any file is written, ask (one AskUserQuestion call, up to 4 questions, tailor the options to the request):
1. **Function + interfaces** — what it must do; connectors (USB-C, pins, pads, antenna), power source.
2. **Size / form factor** — outline mm, layer count (2 or 4; default 4: GND / 3V3 planes), fixed holes or a case to fit.
3. **Assembly** — JLC full assembly (Basic/Extended parts), hand-solder, or mixed; quantity.
4. **Must-haves / avoid** — specific chips, max height, budget, mechanical keep-outs.
If the user skips, default: 4-layer, JLC assembly, parts in stock ≥ 1000, 0402 passives.

## Toolchain (Windows paths from this machine — check they still exist)

- KiCad 10 python: `"C:\Program Files\KiCad\10.0\bin\python.exe"` runs the generators (pcbnew module).
- Freerouting (needs Java 25) via the project wrapper; `kicad-cli` for DRC/ERC/gerbers/STL.
- Parts: `easyeda2kicad --full --lcsc_id=Cxxxx --output "<lib>\<name>\<name>"` (output path INCLUDES the lib
  name twice). Then fix 3D model paths: easyeda2kicad writes them relative ("lib/...") → sed to absolute or STL
  exports miss the models.
- Stock/price search: JLC API `https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList`
  POST `{"keyword": ..., "currentPage": 1, "pageSize": n}` (exact MPN works best; free text is weak).
  The FERMION repo has it as `hardware/tools/jlcsearch.py`.

## The generator pattern (copy from hardware/tools/fermion.py in the FERMION repo when available)

One Python file per board: `b = Board(name, title, outline)` → `b.add(ref, symbol, value, footprint, lcsc,
{pin_name: net}, at=(x,y), rot, side)`, `b.R/C(...)`, `b.track(net, layer, pts, w)` pre-routes, `b.via`,
`b.zone(net, layer, poly)`, `b.keepout`, `b.netclass(name, track, clearance, via, drill, nets)`,
`b.fanout_refs += [QFN refs]`, `b.route_attempts = N`, `b.write_all(route=...)`. Coordinates in mm from the
board corner. Schematic is generated from the same netlist (ERC clean, parity 0).

## Order of work

1. Pick parts (stock, footprint, height). Import missing ones. Read pin names from the imported symbol before
   wiring (pin names, not numbers; duplicates like VDD3P3 map together).
2. Place: functional groups, ICs first, decaps at their pins, connectors at edges with mouths outward,
   RF feeds pre-routed as straight F.Cu tracks, nothing in mechanical keep-outs. Bottom side for small 0402s
   when the top is full (the case floor then needs a shallow pocket).
3. `check.py` until DRC has **0 errors** before routing (courtyards, clearances, edge clearance 0.25).
4. Route in the background (`--route`, 6–8 attempts keep-best). Then the A* finisher (`--grid 0.05`, add
   `--width 0.12 --via 0.45 --nets A,B` for tight spots), then `layer_route.py` for nets boxed in by pours.
5. Check: 0 unconnected, 0 DRC errors, parity 0. Fab: gerbers zip + BOM + CPL with LCSC codes.

## Gotchas that each cost a reroute

- QFN exposed pads: the finisher's GND re-stitch deletes EP vias → add EP vias AFTER the finisher, then
  re-check: a via can short an inner-layer track (remove only the offenders by exact position).
- Freerouting drops hand-drawn pre-routes (B.Cu feeds + their vias) and the post-route prune removes
  "unused" vias on hand-drawn track electrodes → re-add with patch ops after every reroute.
- Pins trapped between two parts (0.16 mm gap, MSOP facing MSOP) can never route → fix placement, not routing
  (rotate the part so its signal side faces where the nets go, spread parts 2 mm).
- A pin row boxed in by a neighbour's escape → give the blocked net first pick (`--nets X,Y`) or move a
  pull-up resistor next to the blocked via.
- Inner GND pour + dense stitching vias = no via spot: `layer_route.py --eat GND` removes stitching vias in the way.
- KiCad custom pads must resolve to ONE polygon including the anchor: put the anchor inside the copper.
- Freerouting writes the .ses a moment after exit → wait/retry; one failed attempt must not kill the run.
- Power nets in a netclass with 0.1 clearance when USB-C pads sit 0.1 apart.
- A pin's strap function (ESP32 GPIO2/8/9) decides pull-ups and LED polarity.
- Verify everything by DRC output and a copper plot (`copperplot.py --hl NET`), never by assumption.

## Deliverable

`boards/<name>.py`, routed `.kicad_pcb`, `fab/` (gerbers.zip, BOM.csv, CPL.csv), a status line
(0 open / DRC clean / fab), and a STATUS.md note with anything unverified (pinouts of off-board parts,
values taken from reference designs). Offer /3d for the case and renders.
