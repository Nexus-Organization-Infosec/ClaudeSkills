"""Foto -> Pixel-Relief-Quelle.

Verkleinert ein Foto auf ein Pixelraster (Standard 320 Spalten) und schreibt es als Daten-URL in eine kleine
JavaScript-Datei. Diese Datei setzt window.<VARIABLE>; pixel-relief.js liest sie. Eine Daten-URL ist nötig, weil
der Browser Bildpixel aus Dateien nicht auslesen lässt, wenn die Seite per Doppelklick (file://) geöffnet wird.

Beispiele:
  python foto_zu_pixel.py hero.jpg
  python foto_zu_pixel.py hero.jpg --spalten 360 --ausgabe js/hero-pixel.js --variable HERO_PIXEL
  python foto_zu_pixel.py hero.jpg --demo vorschau.html      (eigenständige Vorschau zum Ausprobieren)
"""
import argparse, base64, io, json, pathlib, sys

from PIL import Image, ImageOps

SKILL = pathlib.Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("foto", help="Eingabefoto (jpg, png, webp …)")
    ap.add_argument("--spalten", type=int, default=320, help="Pixel in der Breite (mehr = feiner, 240–420 sinnvoll)")
    ap.add_argument("--ausgabe", help="Ziel-JS-Datei (Standard: <foto>-pixel.js neben dem Foto)")
    ap.add_argument("--variable", default="PIXEL_QUELLE", help="Name der globalen Variable (Standard PIXEL_QUELLE)")
    ap.add_argument("--qualitaet", type=int, default=90, help="JPEG-Qualität der eingebetteten Fassung")
    ap.add_argument("--zuschnitt", help="Ausschnitt vorher: links,oben,rechts,unten in Pixeln des Originals")
    ap.add_argument("--helligkeit", type=float, default=1.0, help="Helligkeit vorher anpassen, z. B. 1.15")
    ap.add_argument("--demo", help="zusätzlich eine eigenständige Vorschau-HTML schreiben")
    ap.add_argument("--hintergrund", default="#212326", help="Hintergrundfarbe der Vorschau")
    a = ap.parse_args()

    src = pathlib.Path(a.foto)
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    if a.zuschnitt:
        im = im.crop(tuple(int(v) for v in a.zuschnitt.split(",")))
    if a.helligkeit != 1.0:
        from PIL import ImageEnhance
        im = ImageEnhance.Brightness(im).enhance(a.helligkeit)
    rows = max(1, round(a.spalten * im.height / im.width))
    small = im.resize((a.spalten, rows), Image.LANCZOS)
    buf = io.BytesIO()
    small.save(buf, "JPEG", quality=a.qualitaet)
    data_url = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

    out = pathlib.Path(a.ausgabe) if a.ausgabe else src.with_name(src.stem + "-pixel.js")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"/* Pixel-Relief-Quelle aus {src.name}: {a.spalten} x {rows} Pixel, erzeugt mit foto_zu_pixel.py. */\n"
                   f"window.{a.variable} = {json.dumps(data_url)};\n", encoding="utf-8")
    print(f"Quelle: {out} ({a.spalten} x {rows} = {a.spalten * rows} Pixel, {len(data_url) // 1024} KB)")

    if a.demo:
        # beim Einbetten in <script> darf kein schließendes Script-Tag im Code stehen
        module = (SKILL / "assets" / "pixel-relief.js").read_text(encoding="utf-8").replace("</script", r"<\/script")
        demo = pathlib.Path(a.demo)
        demo.write_text(f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pixel-Relief Vorschau</title>
<style>
  html,body{{margin:0;height:100%;background:{a.hintergrund};color:#fff;font-family:Arial,sans-serif}}
  .stage{{position:relative;height:100vh;overflow:hidden}}
  .stage p{{position:absolute;left:24px;bottom:20px;margin:0;font-size:13px;opacity:.7;z-index:1}}
</style></head>
<body><div class="stage"><p>Maus bewegen: das Relief neigt sich, Pixel am Zeiger heben sich an.</p></div>
<script>window.{a.variable} = {json.dumps(data_url)};</script>
<script>{module}</script>
<script>PixelRelief.mount(document.querySelector('.stage'), {{ source: window.{a.variable}, background: {json.dumps(a.hintergrund)} }});</script>
</body></html>
""", encoding="utf-8")
        print(f"Vorschau: {demo}")


if __name__ == "__main__":
    sys.exit(main())
