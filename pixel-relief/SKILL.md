---
name: pixel-relief
description: Turn a photo into the animated "pixel relief" hero effect, the one from the LAB-3 experiment website. The photo becomes thousands of small square pixels in WebGL. They fly together from depth on load, the whole image tilts toward the mouse, and pixels near the cursor lift up. Bundled are a Python converter (photo to embedded data-URL source) and a drop-in JS module (PixelRelief.mount). Use whenever the user invokes /pixel-relief or says "mach das Foto zu Pixeln", "Pixel-Effekt für dieses Bild", "Pixel-Relief", "das Bild soll der Maus folgen wie im Experiment", "convert this photo into the pixel animation", or wants a hero or header image in that style. It works offline (file://) and falls back to the plain photo without WebGL.
---

# Pixel relief: a photo as an animated pixel relief

The photo is shown as a fine pixel grid (about 300–400 columns) in WebGL:
- On load, the pixels fly together from depth.
- The relief then tilts toward the mouse.
- Pixels near the cursor lift up.
- Bright pixels stand slightly forward of dark ones, which produces the relief.

The user likes this effect. It counts as a signature look and should be reused deliberately.

Bundled:
- `scripts/foto_zu_pixel.py`: photo to `<name>-pixel.js`, containing the downscaled photo as a data URL in `window.<VARIABLE>`. Optionally writes a standalone preview HTML.
- `assets/pixel-relief.js`: the module. `PixelRelief.mount(container, options)` creates the canvas inside the container, handles mouse, intro, resize and visibility, and returns `{destroy}`.

## Workflow

1. **Convert the photo.** The skill folder is `~/.claude/skills/pixel-relief`.
   ```bash
   python "<skill>/scripts/foto_zu_pixel.py" pfad/zum/foto.jpg --spalten 320 --ausgabe js/hero-pixel.js --variable HERO_PIXEL --demo vorschau.html
   ```
   - `--spalten` sets the fineness. 320 is the tested default. Go to 400 for finer pixels and 240 for coarser ones; above 450 it gets heavy.
   - `--zuschnitt l,o,r,u` crops first. `--helligkeit 1.1` brightens dark photos.
   - `--demo` writes a standalone preview. Open it, look at it, and send it to the user if needed.
2. **Copy the module** `assets/pixel-relief.js` into the project, e.g. `js/pixel-relief.js`, and load it after the source:
   ```html
   <section class="hero" style="position:relative">
     <img class="hero-foto" src="assets/hero.jpg" alt="…">   <!-- stays as the fallback -->
     <div class="hero-text">…</div>                          <!-- needs z-index ≥ 1 -->
   </section>
   <script src="js/hero-pixel.js"></script>
   <script src="js/pixel-relief.js"></script>
   <script>
     PixelRelief.mount(document.querySelector('.hero'), { source: window.HERO_PIXEL, background: '#212326' });
   </script>
   ```
3. **Hide the photo only while the effect is running:** `.pixel-relief-active .hero-foto{opacity:0}`. Without WebGL the container gets `pixel-relief-fallback` and the photo stays visible. Text over the image needs `position:relative; z-index:1` or higher, because the canvas sits at `z-index:0`.
4. **Check it.** Take a screenshot with headless Chrome without `--disable-gpu`, because WebGL needs it. Move the mouse over the image and compare two screenshots: the tilt should be visible. Also check phone width (portrait zooms automatically) and `prefers-reduced-motion` (no intro, no swaying, mouse tilt stays).

## Options (`PixelRelief.mount(el, {...})`)

| Option | Default | Meaning |
|---|---|---|
| `background` | `#212326` | Color between the pixels. Use exactly the page or section background. |
| `size` | `0.86` | Pixel size in the grid. 1 = no gaps, 0.8 = clearly visible grid. |
| `depth` | `0.045` | Relief depth relative to width. |
| `tiltX` / `tiltY` | `0.42` / `0.24` | Tilt toward the mouse. Halve it for calmer pages. |
| `lift`, `liftRadius` | `1.5`, `0.2` | Pixels lifting at the cursor. `lift: 0` turns it off. |
| `intro` | `2200` | Fly-in duration in ms. `0` = no intro. |
| `startAfter` | `null` | Promise, e.g. the end of a loading screen. The intro starts after it. |
| `fit` | `cover` | `contain` shows the whole image, e.g. for a product photo. |
| `brightness` | `1.12` | Compensates for the darkening caused by the gaps. |

## What makes the effect work (from feedback)

- **Fine pixels.** The user explicitly asked for "more pixels, not so big". Under 240 columns it looks coarse.
- **No retro gimmicks.** Scanlines, CRT curvature, glitch rows, pixel fonts and RGB split were rejected as "harsh styles that don't fit". Fonts, colors and the rest of the page stay in the website's own design. Only the image is pixelated.
- **Background color = section color.** Otherwise the gaps between the pixels show up as a foreign grid.
- **Restrained motion.** Fly in once, then react only to the mouse plus a very slight sway. Nothing flickers.
- **The data URL is mandatory.** A normal `<img src>` file cannot be read into the canvas under file://. The effect would silently stay empty.
- **Performance:** about 70,000 points run smoothly in WebGL. Don't rebuild this with Canvas 2D, which stutters at this pixel count.
