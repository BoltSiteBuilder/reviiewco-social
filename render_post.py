#!/usr/bin/env python3
"""Render a ReviiewCo 1080x1350 feed post image in the reviiewco.com look.

Usage:
  python3 render_post.py spec.json out.jpg

spec.json keys:
  eyebrow   short uppercase label above the headline (optional)
  headline  big Anton headline; wrap a phrase in [[ ]] to make it amber
  body      one or two short sentences (optional)
  cta       amber button text (optional, default "reviiewco.com")
  photo     path or https URL of a reviiewco.com image (optional)
  layout    "photo" (photo top, text bottom) or "type" (text only)

Needs: playwright (chromium), @fontsource/anton and
@fontsource/plus-jakarta-sans installed in ./node_modules, and the site
logo at ./assets/logo-reviiewco-dark.png (falls back to the site URL).
"""
import base64, html, json, os, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
FONTS = HERE / "node_modules" / "@fontsource"


def font_uri(pkg, name):
    p = FONTS / pkg / "files" / name
    return "data:font/woff2;base64," + base64.b64encode(p.read_bytes()).decode()


def img_uri(src):
    if not src:
        return ""
    if src.startswith("http"):
        return src
    p = Path(src)
    if not p.is_absolute():
        p = HERE / p
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def headline_html(text):
    t = html.escape(text)
    return re.sub(r"\[\[(.+?)\]\]", r'<span class="amber">\1</span>', t)


def build(spec):
    logo = HERE / "assets" / "logo-reviiewco-dark.png"
    logo_src = img_uri(str(logo)) if logo.exists() else "https://reviiewco.com/images/logo-reviiewco-dark.png"
    layout = spec.get("layout", "photo" if spec.get("photo") else "type")
    photo = img_uri(spec.get("photo", "")) if layout == "photo" else ""
    hl = headline_html(spec["headline"])
    n = len(re.sub(r"\[\[|\]\]", "", spec["headline"]))
    size = 112 if layout == "photo" else 150
    if n > 40: size -= 16
    if n > 60: size -= 18
    if n > 80: size -= 14
    eyebrow = html.escape(spec.get("eyebrow", ""))
    body = html.escape(spec.get("body", ""))
    cta = html.escape(spec.get("cta", "reviiewco.com"))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Anton;src:url({font_uri('anton','anton-latin-400-normal.woff2')})}}
@font-face{{font-family:PJS;font-weight:500;src:url({font_uri('plus-jakarta-sans','plus-jakarta-sans-latin-500-normal.woff2')})}}
@font-face{{font-family:PJS;font-weight:700;src:url({font_uri('plus-jakarta-sans','plus-jakarta-sans-latin-700-normal.woff2')})}}
@font-face{{font-family:PJS;font-weight:800;src:url({font_uri('plus-jakarta-sans','plus-jakarta-sans-latin-800-normal.woff2')})}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;background:#0B1220;color:#fff;font-family:PJS,sans-serif;overflow:hidden;position:relative}}
.photo{{position:absolute;inset:0 0 auto 0;height:{'720px' if layout=='photo' else '0'};background:url('{photo}') center/cover no-repeat}}
.photo:after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,18,32,.05) 40%,#0B1220 100%)}}
.glow{{position:absolute;width:900px;height:900px;border-radius:50%;right:-380px;top:-380px;background:radial-gradient(circle,rgba(37,99,235,.35),rgba(37,99,235,0) 65%)}}
.wrap{{position:absolute;left:84px;right:84px;bottom:190px;{'top:640px' if layout=='photo' else 'top:170px'};display:flex;flex-direction:column;justify-content:{'flex-start' if layout=='photo' else 'center'};gap:34px}}
.eyebrow{{font-weight:800;font-size:28px;letter-spacing:.14em;text-transform:uppercase;color:#FBBF24}}
h1{{font-family:Anton,sans-serif;font-weight:400;text-transform:uppercase;font-size:{size}px;line-height:1.02;letter-spacing:.005em}}
.amber{{color:#FBBF24}}
p{{font-weight:500;font-size:38px;line-height:1.38;color:#CBD5E1;max-width:880px}}
.foot{{position:absolute;left:84px;right:84px;bottom:72px;display:flex;align-items:center;justify-content:space-between}}
.foot img{{height:64px}}
.cta{{background:#FBBF24;color:#0F172A;font-weight:800;font-size:30px;padding:20px 34px;border-radius:999px}}
</style></head><body>
{'<div class="photo"></div>' if layout=='photo' else '<div class="glow"></div>'}
<div class="wrap">
{f'<div class="eyebrow">{eyebrow}</div>' if eyebrow else ''}
<h1>{hl}</h1>
{f'<p>{body}</p>' if body else ''}
</div>
<div class="foot"><img src="{logo_src}"><div class="cta">{cta}</div></div>
</body></html>"""


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    out = Path(sys.argv[2])
    page_html = build(spec)
    tmp = out.with_suffix(".html")
    tmp.write_text(page_html)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        pg.goto(tmp.resolve().as_uri())
        pg.wait_for_timeout(600)
        png = out.with_suffix(".png")
        pg.screenshot(path=str(png))
        b.close()
    from PIL import Image
    Image.open(png).convert("RGB").save(out, "JPEG", quality=88, optimize=True)
    os.remove(png)
    print(out, out.stat().st_size)


if __name__ == "__main__":
    main()
