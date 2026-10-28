#!/usr/bin/env python3
"""Build ReviiewCo lead-magnet PDF guides (letter size) in the reviiewco.com look.

Usage: python3 -I guides/build_guides.py   (run from the repo root after `npm install`)
Writes guides/<slug>.pdf for every guide in guides/content/*.html.

Each content file starts with a JSON front-matter line:
<!-- {"title": "...", "subtitle": "...", "keyword": "BAD"} -->
followed by HTML body sections. Allowed classes: .box, .tip, .sample, table.
"""
import base64, json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FONTS = ROOT / "node_modules" / "@fontsource"


def font(pkg, name):
    return "data:font/woff2;base64," + base64.b64encode((FONTS / pkg / "files" / name).read_bytes()).decode()


def img(p):
    p = ROOT / p
    mime = "image/png" if p.suffix == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


CLOSE = """
<section class="close">
  <div class="eyebrow">Do it yourself, or hand it off</div>
  <h2>That's the whole playbook.</h2>
  <p>Everything above works, and you can do every bit of it yourself. Most owners we talk to don't have the time, because they're out doing the work. That's exactly what ReviiewCo is for.</p>
  <div class="cols">
    <div class="col"><h3>Do it yourself</h3><ul>
      <li>Ask every customer, every job, the same way</li>
      <li>Work your old customer list in steady batches</li>
      <li>Reply to every review within a few days</li>
      <li>Keep it going when the schedule gets busy</li></ul></div>
    <div class="col amberbox"><h3>Or we do it for you</h3><ul>
      <li>A friendly text after every job, plus up to two reminders</li>
      <li>Your past-customer list worked for you</li>
      <li>A reply to every review, in your voice</li>
      <li>Missed-Call-Text Back included</li></ul>
      <p class="price">$297/month. No contract. No setup fee.</p></div>
  </div>
  <p class="small">Guarantee: at least 10 new Google reviews in 30 days when you send us a list of 300+ past customers, or every dollar back. The 30 days start once we have your list and access to your Google profile.</p>
  <div class="ctas">
    <div><b>Talk it through with Rob (30 min, no pressure)</b><br>reviiewco.com/book</div>
    <div><b>Get started</b><br>reviiewco.com/start</div>
    <div><b>Call or text, answered 24/7</b><br>864-528-1909</div>
  </div>
</section>
"""


def page(meta, body):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Anton;src:url({font('anton','anton-latin-400-normal.woff2')})}}
@font-face{{font-family:PJS;font-weight:500;src:url({font('plus-jakarta-sans','plus-jakarta-sans-latin-500-normal.woff2')})}}
@font-face{{font-family:PJS;font-weight:700;src:url({font('plus-jakarta-sans','plus-jakarta-sans-latin-700-normal.woff2')})}}
@font-face{{font-family:PJS;font-weight:800;src:url({font('plus-jakarta-sans','plus-jakarta-sans-latin-800-normal.woff2')})}}
@page{{size:Letter;margin:0.7in 0.75in 0.8in}}
@page:first{{margin:0}}
*{{box-sizing:border-box}}
body{{font-family:PJS,sans-serif;font-weight:500;color:#0F172A;font-size:11pt;line-height:1.55;margin:0}}
.cover{{height:11in;width:8.5in;background:#0B1220;color:#fff;padding:0.9in 0.85in;position:relative;page-break-after:always;overflow:hidden}}
.cover .glow{{position:absolute;width:7in;height:7in;border-radius:50%;right:-2.6in;top:-2.6in;background:radial-gradient(circle,rgba(37,99,235,.4),rgba(37,99,235,0) 65%)}}
.cover img.logo{{height:44px}}
.cover .eyebrow{{margin-top:2.1in}}
.cover h1{{font-family:Anton;font-weight:400;text-transform:uppercase;font-size:60pt;line-height:1.0;margin:14px 0 22px}}
.cover h1 span{{color:#FBBF24}}
.cover p{{font-size:15pt;color:#CBD5E1;max-width:5.6in}}
.cover .by{{position:absolute;bottom:0.85in;left:0.85in;right:0.85in;font-size:10.5pt;color:#94A3B8;border-top:1px solid #1E293B;padding-top:14px}}
.eyebrow{{font-weight:800;font-size:9.5pt;letter-spacing:.14em;text-transform:uppercase;color:#FBBF24}}
h2{{font-family:Anton;font-weight:400;text-transform:uppercase;font-size:24pt;line-height:1.05;margin:26px 0 8px;color:#0B1220;page-break-after:avoid}}
h3{{font-size:12pt;font-weight:800;margin:16px 0 4px;page-break-after:avoid}}
p{{margin:6px 0 10px}}
ul,ol{{margin:6px 0 12px;padding-left:20px}} li{{margin:3px 0}}
table{{border-collapse:collapse;width:100%;margin:10px 0 14px;font-size:10pt;page-break-inside:avoid}}
th{{background:#0B1220;color:#fff;text-align:left;padding:7px 8px;font-weight:700}}
td{{border-bottom:1px solid #E2E8F0;padding:6px 8px;vertical-align:top}}
.box{{background:#F1F5F9;border-radius:10px;padding:12px 16px;margin:12px 0;page-break-inside:avoid}}
.tip{{border-left:5px solid #FBBF24;background:#FFFBEB;padding:10px 14px;margin:12px 0;page-break-inside:avoid}}
.sample{{background:#0B1220;color:#E2E8F0;border-radius:12px;padding:12px 16px;margin:12px 0;font-size:10.5pt;page-break-inside:avoid}}
.sample b{{color:#FBBF24}}
.formula{{font-family:Anton;font-size:18pt;letter-spacing:.02em;text-align:center;background:#F1F5F9;border-radius:10px;padding:12px;margin:10px 0}}
.do li::marker{{content:"✓  ";color:#16A34A}} .dont li::marker{{content:"✗  ";color:#DC2626}}
.close{{page-break-before:always}}
.cols{{display:flex;gap:14px;margin:14px 0}} .col{{flex:1;background:#F1F5F9;border-radius:12px;padding:6px 16px 10px}}
.amberbox{{background:#0B1220;color:#fff}} .amberbox h3{{color:#FBBF24}}
.price{{font-weight:800;color:#FBBF24;font-size:12.5pt}}
.small{{font-size:9pt;color:#475569}}
.ctas{{display:flex;gap:10px;margin-top:16px}} .ctas div{{flex:1;background:#FBBF24;border-radius:12px;padding:10px 12px;font-size:10pt}}
.src{{font-size:8.5pt;color:#475569;word-break:break-all}} .src li{{margin:1px 0}}
</style></head><body>
<section class="cover"><div class="glow"></div>
<img class="logo" src="{img('assets/logo-reviiewco-dark.png')}">
<div class="eyebrow">Free guide for home service owners</div>
<h1>{meta['title_html']}</h1>
<p>{meta['subtitle']}</p>
<div class="by">By Rob Warfield, founder of ReviiewCo · Greenville, SC · {meta.get('date','October 2026')}<br>reviiewco.com · 864-528-1909</div>
</section>
{body}
{CLOSE}
<p class="small" style="margin-top:18px">General information, not legal advice. Example names, reviews and texts are illustrations, not real customers.</p>
</body></html>"""


def main():
    only = sys.argv[1:]
    with sync_playwright() as p:
        b = p.chromium.launch()
        for f in sorted((HERE / "content").glob("*.html")):
            if only and f.stem not in only:
                continue
            raw = f.read_text()
            m = re.match(r"<!--\s*(\{.*?\})\s*-->", raw, re.S)
            meta = json.loads(m.group(1))
            body = raw[m.end():]
            html = page(meta, body)
            tmp = HERE / f"{f.stem}.tmp.html"
            tmp.write_text(html)
            pg = b.new_page()
            pg.goto(tmp.resolve().as_uri())
            pg.wait_for_timeout(500)
            out = HERE / f"{f.stem}.pdf"
            pg.pdf(path=str(out), format="Letter", print_background=True, prefer_css_page_size=True)
            pg.close()
            tmp.unlink()
            print(out.name, out.stat().st_size)
        b.close()


if __name__ == "__main__":
    main()
