"""Crop shop photos for the site.

Put originals in photos-src/ (not committed), list them in photos.json:
  {"hero": {"src": "bay-dusk.jpg", "focus": [0.55, 0.5]}, "page-bmw-repair": {"src": "bmw-m3.jpg", "focus": [0.6, 0.45]}}
focus = the point (optional: zoom >1 crops tighter, bright >1 lightens)
focus = the point (0..1 across, 0..1 down) that must stay in frame: the car, a badge, a face.
Run: python3 tools/photos.py   -> writes static/img/photos/<slot>.jpg and <slot>-m.jpg (phone crop).
"""
import json, os, sys
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "static/img/photos")
SRC = os.path.join(ROOT, "photos-src")

# slot type -> (desktop size, phone size or None)
SIZES = {
    "hero": ((2000, 1000), (900, 1125)),
    "page": ((2000, 750), (900, 900)),
    "band": ((2000, 750), (900, 750)),
    "approach": ((1400, 1100), (1080, 810)),
    "tile": ((900, 1200), None),
    "team": ((2400, 1030), (1080, 810)),
    "person": ((960, 1200), None),
}
def kind(slot):
    if slot in ("hero", "band", "approach", "team"): return slot
    if slot.startswith("page"): return "page"
    if slot.startswith("person"): return "person"
    return "tile"

def crop_to(im, w, h, fx, fy, zoom=1.0):
    W, H = im.size
    r = w / h
    cw, ch = (W, int(W / r)) if W / H < r else (int(H * r), H)
    cw, ch = int(cw / zoom), int(ch / zoom)
    x = min(max(int(fx * W - cw / 2), 0), W - cw)
    y = min(max(int(fy * H - ch / 2), 0), H - ch)
    return im.crop((x, y, x + cw, y + ch)).resize((w, h), Image.LANCZOS)

def grade(im):
    r, g, b = im.split()
    lut = lambda lo, hi: [min(255, max(0, int(lo + (hi - lo) * ((i / 255) ** 1.08)))) for i in range(256)]
    im = Image.merge("RGB", (r.point(lut(4, 236)), g.point(lut(4, 228)), b.point(lut(6, 214))))
    im = ImageEnhance.Contrast(im).enhance(1.10)
    im = ImageEnhance.Color(im).enhance(0.86)
    return ImageEnhance.Brightness(im).enhance(0.9)

def main():
    cfg = json.load(open(os.path.join(ROOT, "photos.json")))
    os.makedirs(OUT, exist_ok=True)
    for slot, c in cfg.items():
        src = os.path.join(SRC, c["src"])
        if not os.path.exists(src):
            print("missing", src); continue
        im = grade(ImageOps.exif_transpose(Image.open(src)).convert("RGB"))
        if c.get("bright"): im = ImageEnhance.Brightness(im).enhance(c["bright"])
        for blur in c.get("blur", []):  # plates etc: [x0,y0,x1,y1] as fractions
            W, H = im.size; box = tuple(int(v * (W if i % 2 == 0 else H)) for i, v in enumerate(blur))
            reg = im.crop(box); im.paste(reg.resize((5, 3)).resize(reg.size).filter(ImageFilter.GaussianBlur(10)), box)
        fx, fy = c.get("focus", [0.5, 0.5])
        d, m = SIZES[kind(slot)]
        crop_to(im, *d, fx, fy, c.get("zoom", 1.0)).save(os.path.join(OUT, f"{slot}.jpg"), quality=72, optimize=True, progressive=True)
        if m:
            mf = c.get("focus_m", [fx, fy])
            crop_to(im, *m, *mf, c.get("zoom_m", 1.0)).save(os.path.join(OUT, f"{slot}-m.jpg"), quality=72, optimize=True, progressive=True)
        print("ok", slot)

if __name__ == "__main__":
    main()
