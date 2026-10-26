"""Build a 2.5D (isometric) service architecture page for Goodnight, AI."""
import json, math
SP = '/tmp/claude-0/-home-claude/3e881c95-6cf0-56cd-aa41-2012ca221448/scratchpad/'
cast = json.load(open(SP + 'cast.json'))
DEFS = cast['defs']
PIP = cast['indexPip']          # Pip, viewBox 0 -24 270 324

C30, S30 = math.cos(math.radians(30)), 0.5
OX, OY = 330, 250                 # screen origin

def P(x, y, z=0):
    return (OX + (x - y) * C30, OY + (x + y) * S30 - z)

def poly(pts, fill, extra=''):
    return '<polygon points="%s" fill="%s" %s/>' % (' '.join('%.1f,%.1f' % p for p in pts), fill, extra)

def shade(hexc, f):
    h = hexc.lstrip('#'); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return '#%02X%02X%02X' % tuple(max(0, min(255, int(c * f))) for c in (r, g, b))

def box(x, y, z, sx, sy, sz, color, paint=True, top=None):
    """Iso cuboid: top face, left (front-left, +y side) face, right (front-right, +x side) face."""
    t = top or color
    top_f = poly([P(x, y, z+sz), P(x+sx, y, z+sz), P(x+sx, y+sy, z+sz), P(x, y+sy, z+sz)], t)
    left_f = poly([P(x, y+sy, z), P(x+sx, y+sy, z), P(x+sx, y+sy, z+sz), P(x, y+sy, z+sz)], shade(color, .78))
    right_f = poly([P(x+sx, y, z), P(x+sx, y+sy, z), P(x+sx, y+sy, z+sz), P(x+sx, y, z+sz)], shade(color, .62))
    g = left_f + right_f + top_f
    return f'<g filter="url(#paint)">{g}</g>' if paint else f'<g>{g}</g>'

def prism_roof(x, y, z, sx, sy, h, color):
    """Gable roof along x."""
    a, b = P(x, y, z), P(x+sx, y, z)
    c, d = P(x+sx, y+sy, z), P(x, y+sy, z)
    r1, r2 = P(x, y+sy/2, z+h), P(x+sx, y+sy/2, z+h)
    front = poly([d, c, r2, r1], shade(color, .85))
    side = poly([b, c, r2], shade(color, .62))
    back = poly([a, b, r2, r1], color)
    return f'<g filter="url(#paint)">{back}{front}{side}</g>'

def flat(x, y, z, svg_inner, w, h, vb, dx=0, dy=0):
    """Billboard: a flat drawing standing at an iso point."""
    sx, sy = P(x, y, z)
    return f'<svg x="{sx - w/2 + dx:.1f}" y="{sy - h + dy:.1f}" width="{w}" height="{h}" viewBox="{vb}" overflow="visible">{svg_inner}</svg>'

def top_disc(x, y, z, r, color, txt='', tcolor='#121A33'):
    cx, cy = P(x, y, z)
    s = f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{r*1.15:.1f}" ry="{r*.66:.1f}" fill="{color}"/>'
    if txt:
        s += f'<text x="{cx:.1f}" y="{cy+4.5:.1f}" text-anchor="middle" font-family="Fredoka, Arial" font-weight="600" font-size="13" fill="{tcolor}">{txt}</text>'
    return s

# ---------------- layout: five platforms in a screen-horizontal row ----------------
SLAB_H = 24
SZ = 180
STEP = 205
OX, OY = 200, 330
def G(k, x, y):
    return (k * STEP + x, -k * STEP + y)
def B(k, x, y, z, sx, sy, sz, c, **kw):
    gx, gy = G(k, x, y); return box(gx, gy, z, sx, sy, sz, c, **kw)
def PT(k, x, y, z):
    gx, gy = G(k, x, y); return P(gx, gy, z)
plats = [
    ('#3B4F96', '1', 'News sources', 'Approved feeds only'),
    ('#4B5FB0', '2', 'Story agent', 'Find, check, rewrite, self check'),
    ('#3A7F45', '3', 'Family settings', 'Rules, age, memory'),
    ('#B7791F', '4', 'Parent gate', 'Green shares, the rest waits'),
    ('#C9604A', '5', 'Bedtime', 'Pip reads, family talks'),
]
parts = []
for k in range(5):
    parts.append(B(k, -14, -14, -34, SZ + 28, SZ + 28, 14, '#24305A', top='#2B3A6E'))
for k, (col, *_r) in enumerate(plats):
    parts.append(B(k, 0, 0, 0, SZ, SZ, SLAB_H, col))

flows = []
for k in range(4):
    a_ = PT(k, SZ, SZ / 2, SLAB_H / 2); b_ = PT(k + 1, 0, SZ / 2, SLAB_H / 2)
    flows.append('<path class="flow" d="M%.1f %.1f L%.1f %.1f" />' % (a_[0], a_[1], b_[0], b_[1]))
    ang = math.degrees(math.atan2(b_[1]-a_[1], b_[0]-a_[0]))
    flows.append('<path d="M-9 -6 L0 0 L-9 6" transform="translate(%.1f %.1f) rotate(%.1f)" fill="none" stroke="#FFD23F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' % (b_[0], b_[1], ang))

obj = []
Z = SLAB_H
for (px, py) in [(20, 30), (20, 100), (90, 110)]:
    for j in range(3):
        obj.append(B(0, px + j*2, py - j*2, Z + j*7, 56, 44, 6, ['#FFF8E6', '#F3E5C8', '#FFF1C9'][j]))
obj.append(B(0, 110, 20, Z, 30, 30, 76, '#6C8BEF'))
tx, ty = PT(0, 125, 35, Z + 76)
obj.append('<g fill="none" stroke="#FFD23F" stroke-width="3" stroke-linecap="round"><path d="M%.0f %.0f a14 14 0 0 1 20 0"/><path d="M%.0f %.0f a24 24 0 0 1 34 0"/></g>' % (tx-10, ty-12, tx-17, ty-20))

steps = ['#6C8BEF', '#6C8BEF', '#F7A23B', '#F7A23B', '#4FA65B', '#4FA65B', '#F48FB1']
ring = [(14, 14), (73, 8), (132, 14), (136, 76), (132, 138), (73, 144), (14, 138)]
for i in sorted(range(7), key=lambda i: ring[i][0] + ring[i][1]):
    sx_, sy_ = ring[i]
    obj.append(B(1, sx_, sy_, Z, 32, 32, 20, steps[i]))
    cx, cy = PT(1, sx_ + 16, sy_ + 16, Z + 20)
    obj.append('<ellipse cx="%.1f" cy="%.1f" rx="12.5" ry="7.5" fill="#FFF8E6"/><text x="%.1f" y="%.1f" text-anchor="middle" font-family="Fredoka, Arial" font-weight="600" font-size="13" fill="#121A33">%d</text>' % (cx, cy, cx, cy+4.5, i+1))
gx, gy = G(1, 90, 90)
obj.insert(len(obj) - 6, flat(gx, gy, Z, PIP, 104, 125, '0 -24 270 324'))

obj.append(B(2, 20, 20, Z, 84, 74, 50, '#FFF1C9'))
obj.append(prism_roof(*G(2, 20, 20), Z + 50, 84, 74, 36, '#F08A6E'))
for i, (c, ln) in enumerate([('#3DBE8B', 70), ('#F2C94C', 40), ('#F08A6E', 16)]):
    obj.append(B(2, 20, 112 + i * 22, Z, 140, 9, 4, '#1C2647', paint=False))
    obj.append(B(2, 20 + ln, 110 + i * 22, Z + 4, 18, 13, 12, c))

obj.append(B(3, 20, 60, Z, 24, 24, 108, '#FFF1C9'))
obj.append(B(3, 20, 60, Z + 108, 140, 24, 20, '#F7A23B'))
obj.append(B(3, 136, 60, Z, 24, 24, 108, '#FFF1C9'))
for i, c in enumerate(['#3DBE8B', '#F2C94C', '#F08A6E']):
    lx, ly = PT(3, 55 + i * 35, 84, Z + 118)
    obj.append('<circle cx="%.1f" cy="%.1f" r="9" fill="%s" stroke="#121A33" stroke-width="2.5"/>' % (lx, ly, c))
obj.append(B(3, 60, 120, Z, 60, 42, 7, '#FFF8E6'))
cx_, cy_ = PT(3, 90, 141, Z + 7)
obj.append('<path d="M%.0f %.0f l6 5 12 -9" fill="none" stroke="#3DBE8B" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>' % (cx_-9, cy_))

obj.append(B(4, 20, 30, Z, 16, 120, 66, '#7A4E2D'))
obj.append(B(4, 20, 30, Z, 140, 120, 22, '#C4864F'))
obj.append(B(4, 38, 40, Z + 22, 32, 100, 12, '#FFF8E6'))
obj.append(B(4, 72, 34, Z + 22, 88, 112, 14, '#F48FB1', top='#F7A6C8'))
obj.append(B(4, 92, 72, Z + 36, 40, 30, 4, '#2B2F3A'))
gx, gy = G(4, 112, 87)
obj.append(flat(gx, gy, Z + 40, PIP, 34, 40, '0 -24 270 324'))
mx, my = PT(4, 200, -60, Z + 290)
obj.append('<g filter="url(#paint)"><path d="M{a} {b} C{c} {d} {e} {f} {g} {h} C{i} {j} {k} {l} {a} {b}Z" fill="#FFD23F"/></g>'.format(
    a=round(mx+22), b=round(my-26), c=round(mx-8), d=round(my-22), e=round(mx-16), f=round(my+20), g=round(mx+16), h=round(my+30), i=round(mx-2), j=round(my+16), k=round(mx), l=round(my-10)))

fa = PT(4, 40, SZ + 14, -34); fb = PT(1, 130, SZ + 14, -34)
mid = ((fa[0] + fb[0]) / 2, max(fa[1], fb[1]) + 120)
feedback = ('<path class="loopline" d="M%.0f %.0f Q%.0f %.0f %.0f %.0f"/>' % (fa[0], fa[1], mid[0], mid[1], fb[0], fb[1])
            + '<path d="M-10 -7 L0 0 L-10 7" transform="translate(%.0f %.0f) rotate(-120)" fill="none" stroke="#CBD3E8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' % (fb[0], fb[1]))
fl = (mid[0], (fa[1] + fb[1]) / 4 + mid[1] / 2 + 6)

labels = []
for k, (col, n, name, sub) in enumerate(plats):
    lx, ly = PT(k, SZ / 2, SZ / 2, 0)
    ly -= 215
    w = max(len(name) * 12.4, len(sub) * 8.4) + 78
    labels.append(
      '<g transform="translate(%.0f %.0f)"><g class="lab" style="animation-delay:%.1fs">' % (lx, ly, -k * 1.1)
      + '<rect x="%.0f" y="-58" width="%.0f" height="70" rx="20" fill="#FFF8E6"/>' % (-w/2, w)
      + '<circle cx="%.0f" cy="-23" r="17" fill="%s"/><text x="%.0f" y="-16" text-anchor="middle" font-family="Fredoka, Arial" font-weight="600" font-size="19" fill="#fff">%s</text>' % (-w/2+30, col, -w/2+30, n)
      + '<text x="%.0f" y="-28" font-family="Fredoka, Arial" font-weight="600" font-size="22" fill="#121A33">%s</text>' % (-w/2+58, name)
      + '<text x="%.0f" y="-5" font-family="Nunito Sans, Arial" font-size="15.5" fill="#4A5568">%s</text></g></g>' % (-w/2+58, sub))

tl = PT(0, -14, SZ + 14, -34)
trust_label = ('<g transform="translate(%.0f %.0f)"><rect x="0" y="-18" width="312" height="38" rx="19" fill="#121A33" stroke="#FFD23F" stroke-width="2"/>' % (tl[0]-10, tl[1]+38)
               + '<text x="18" y="7" font-family="Fredoka, Arial" font-weight="600" font-size="17" fill="#FFD23F">✓ Trust layer under every step</text></g>')
loop_label = ('<g transform="translate(%.0f %.0f)"><rect x="-164" y="-20" width="328" height="38" rx="19" fill="#121A33" stroke="#CBD3E8" stroke-width="2"/>' % fl
              + '<text x="0" y="5" text-anchor="middle" font-family="Fredoka, Arial" font-weight="600" font-size="17" fill="#CBD3E8">↺ Feedback makes tomorrow better</text></g>')

stars = ''.join(f'<circle class="tw" cx="{x}" cy="{y}" r="{r}" fill="#F7F1E3" style="animation-delay:{d}s"/>' for x, y, r, d in
                [(60, 80, 2, 0), (300, 50, 1.6, 1), (620, 60, 2, 2), (980, 50, 1.8, .5), (1300, 70, 2.2, 1.5), (1560, 60, 1.6, 2.5), (1760, 300, 2, .8), (40, 420, 1.6, 1.8)])

svg = f'''<svg class="iso" viewBox="0 30 1820 670" role="img" aria-label="A 2.5D map of the service. Five platforms in a row: news sources, the story agent with Pip and seven step blocks, family settings with a house and three sliders, the parent gate with green, yellow and red lights, and bedtime with a bed and a tablet. All platforms sit on a trust layer. A feedback arc goes from bedtime back to the agent.">
  <defs>{DEFS}<radialGradient id="mglow"><stop offset="0" stop-color="#FFD23F" stop-opacity=".55"/><stop offset="1" stop-color="#FFD23F" stop-opacity="0"/></radialGradient></defs>
  {stars}
  {''.join(parts)}
  {''.join(flows)}
  {''.join(obj)}
  {feedback}{loop_label}
  {trust_label}
  {''.join(labels)}
</svg>'''

def card(n, col, name, items, tags):
    lis = ''.join(f'<li><span>{t}</span>{" <em>Next</em>" if g == "n" else ""}</li>' for t, g in zip(items, tags))
    return f'<div class="dc"><p class="dh"><span class="dn" style="background:{col}">{n}</span>{name}</p><ul>{lis}</ul></div>'

cards = ''.join([
    card('1', '#3B4F96', 'News sources', ['Trusted AI news feeds', 'Company and lab posts', 'Safety and security alerts', 'Approved list only, every item keeps its link and time'], 'pppp'),
    card('2', '#4B5FB0', 'Story agent', ['1 Discover, 2 Pick and skip with reasons', '3 Verify facts, label company claims', '4 Rewrite for age, 5 Self check every line', '6 Sort by risk: green, yellow, red', '7 Make pictures, animation and voice'], 'ppppn'),
    card('3', '#3A7F45', 'Family settings', ['Parent rules for each topic', 'Kid age and level, no kid account', 'Family memory links stories over time'], 'pnn'),
    card('4', '#B7791F', 'Parent gate', ['Green shares itself', 'Yellow and red wait for the parent', 'Share, not tonight, or make it simpler', 'Ready to read alert'], 'pppn'),
    card('5', '#C9604A', 'Bedtime', ['Story shelf with only shared stories', 'Pip reads aloud with pictures', 'Talk about it together', 'Ask Pip, answered only from sources'], 'pppn'),
])

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Goodnight, AI · Service Architecture</title>
<meta name="description" content="A 2.5D map of how the full Goodnight, AI service could work, with a parent in charge.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&family=Nunito+Sans:wght@400;600;700&display=swap">
<style>
:root {{ --night:#121A33; --night2:#1C2647; --night3:#24305A; --cream:#F7F1E3; --paper:#FFF8E6; --gold:#FFD23F; --mist:#CBD3E8; --mist2:#9AA6C4; --ink:#1A1A2E; --ink2:#4A5568;
  --f-display: Fredoka, "Trebuchet MS", Arial, sans-serif; --f-body: "Nunito Sans", Arial, sans-serif; color-scheme: dark }}
* {{ box-sizing: border-box }}
body {{ margin: 0; background: radial-gradient(circle at 80% 0%, var(--night3) 0, var(--night) 60%) fixed, var(--night); color: var(--cream); font-family: var(--f-body); line-height: 1.5 }}
a {{ color: inherit }}
.wrap {{ max-width: 1320px; margin: 0 auto; padding: 24px max(20px, env(safe-area-inset-left, 0px)) 40px }}
.top {{ display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap }}
.brand {{ font-family: var(--f-display); font-weight: 600; font-size: 22px; text-decoration: none }}
.brand span {{ color: var(--gold) }}
.back {{ font-weight: 700; font-size: 15px; color: var(--mist); text-decoration: none; border: 2px solid var(--night3); border-radius: 999px; padding: 8px 16px }}
.back:hover {{ color: var(--gold); border-color: var(--gold) }}
.head {{ display: flex; align-items: flex-end; justify-content: space-between; gap: 24px; flex-wrap: wrap; margin-top: 18px }}
.eyebrow {{ margin: 0 0 6px; font-weight: 700; font-size: 13px; letter-spacing: .22em; text-transform: uppercase; color: var(--gold) }}
h1 {{ margin: 0; font-family: var(--f-display); font-weight: 600; font-size: clamp(28px, 3.2vw, 42px); line-height: 1.1; max-width: 26ch }}
.legend {{ display: flex; gap: 16px; flex-wrap: wrap; font-size: 14px; color: var(--mist) }}
.legend em, .dc em {{ font-style: normal; font-size: 10px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; border: 1.5px dashed var(--mist2); color: var(--mist); border-radius: 999px; padding: 1px 7px; white-space: nowrap }}
.legend b {{ font-size: 10px; letter-spacing: .08em; text-transform: uppercase; background: var(--gold); color: var(--night); border-radius: 999px; padding: 2px 8px }}
.stage {{ margin-top: 6px }}
.iso {{ width: 100%; height: auto; display: block; overflow: visible }}
.flow {{ fill: none; stroke: #FFD23F; stroke-width: 4; stroke-linecap: round; stroke-dasharray: 2 14; animation: flow 1.2s linear infinite }}
@keyframes flow {{ to {{ stroke-dashoffset: -16 }} }}
.loopline {{ fill: none; stroke: #CBD3E8; stroke-width: 3; stroke-dasharray: 8 9; animation: flow 1.6s linear infinite reverse; opacity: .85 }}
.tw {{ animation: tw 4s ease-in-out infinite }}
@keyframes tw {{ 50% {{ opacity: .25 }} }}
.lab {{ animation: bob 5s ease-in-out infinite }}
@keyframes bob {{ 50% {{ transform: translateY(-6px) }} }}
.cards {{ display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; margin-top: 8px }}
.dc {{ background: var(--night2); border: 1px solid var(--night3); border-radius: 18px; padding: 14px 16px }}
.dh {{ margin: 0 0 8px; display: flex; align-items: center; gap: 8px; font-family: var(--f-display); font-weight: 600; font-size: 16px }}
.dn {{ width: 24px; height: 24px; border-radius: 50%; display: grid; place-items: center; font-size: 13px; color: #fff }}
.dc ul {{ margin: 0; padding-left: 16px; display: flex; flex-direction: column; gap: 5px; font-size: 13px; color: var(--mist) }}
.swipe {{ display: none; margin: 14px 0 0; font-size: 13px; font-weight: 700; color: var(--gold) }}
.note {{ margin: 16px 0 0; font-size: 13.5px; color: var(--mist2); max-width: 92ch }}
@media (max-width: 1000px) {{ .cards {{ grid-template-columns: 1fr 1fr }} }}
@media (max-width: 560px) {{ .swipe {{ display: block }} .cards {{ grid-template-columns: 1fr }} .stage {{ overflow-x: auto; -webkit-overflow-scrolling: touch }} .iso {{ width: 900px; max-width: none }} }}
@media (prefers-reduced-motion: reduce) {{ .flow, .loopline, .tw {{ animation: none }} }}
</style>
</head>
<body>
<div class="wrap">
  <div class="top"><a class="brand" href="index.html">Goodnight, <span>AI</span></a><a class="back" href="index.html">← Back to the pitch</a></div>
  <div class="head">
    <div><p class="eyebrow">Possible service architecture</p><h1>From tonight’s AI news to a bedtime story, with a parent in charge</h1></div>
    <div class="legend"><span><b>Prototype</b> in today’s demo</span><span><em>Next</em> for the full service</span></div>
  </div>
  <p class="swipe">Swipe to see all five →</p><div class="stage">{svg}</div>
  <div class="cards">{cards}</div>
  <p class="note">Today’s prototype plays a labeled replay of one real agent run in plain HTML, CSS and JavaScript. In the full service, each agent step becomes a real AI call with its own tools and checks; the flow and the parent gate stay the same. Everything not marked Next is in the prototype.</p>
</div>
</body>
</html>'''
open('/mnt/user-data/outputs/site-v2/architecture.html', 'w').write(html)
print('ok', len(html))
