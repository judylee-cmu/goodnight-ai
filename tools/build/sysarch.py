"""2.5D system architecture page for Goodnight, AI (generic components, no vendor branding)."""
import json, math
SP = '/tmp/claude-0/-home-claude/3e881c95-6cf0-56cd-aa41-2012ca221448/scratchpad/'
cast = json.load(open(SP + 'cast.json'))
DEFS, PIP = cast['defs'], cast['indexPip']

C30 = math.cos(math.radians(30))
OX, OY = 380, 60
def P(x, y, z=0):
    return (OX + (x - y) * C30, OY + (x + y) * 0.5 - z)
def poly(pts, fill, extra=''):
    return '<polygon points="%s" fill="%s" %s/>' % (' '.join('%.1f,%.1f' % p for p in pts), fill, extra)
def shade(h, f):
    h = h.lstrip('#'); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return '#%02X%02X%02X' % tuple(max(0, min(255, int(c * f))) for c in (r, g, b))
def box(x, y, z, sx, sy, sz, c, top=None, paint=True):
    t = poly([P(x, y, z+sz), P(x+sx, y, z+sz), P(x+sx, y+sy, z+sz), P(x, y+sy, z+sz)], top or c)
    l = poly([P(x, y+sy, z), P(x+sx, y+sy, z), P(x+sx, y+sy, z+sz), P(x, y+sy, z+sz)], shade(c, .78))
    r = poly([P(x+sx, y, z), P(x+sx, y+sy, z), P(x+sx, y+sy, z+sz), P(x+sx, y, z+sz)], shade(c, .62))
    g = l + r + t
    return f'<g filter="url(#paint)">{g}</g>' if paint else f'<g>{g}</g>'
def cyl(x, y, z, r, h, c, rings=3):
    cx, cy = P(x, y, z); rx, ry = r * 1.22, r * .7
    s = f'<rect x="{cx-rx:.1f}" y="{cy-h:.1f}" width="{2*rx:.1f}" height="{h:.1f}" fill="{shade(c, .72)}"/>'
    s += f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{shade(c, .72)}"/>'
    for i in range(1, rings):
        yy = cy - h * i / rings
        s += f'<path d="M{cx-rx:.1f} {yy:.1f} A{rx:.1f} {ry:.1f} 0 0 0 {cx+rx:.1f} {yy:.1f}" fill="none" stroke="{shade(c, 1.15)}" stroke-width="2.5"/>'
    s += f'<ellipse cx="{cx:.1f}" cy="{cy-h:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{c}"/>'
    return f'<g filter="url(#paint)">{s}</g>'

NODES = {}     # name -> anchor screen point (top of the component)
ITEMS = []     # (depth, svg)
LABELS = []
def put(depth, svg): ITEMS.append((depth, svg))
def label(name, x, y, z, text, tag, dy=16):
    sx, sy = P(x, y, z)
    NODES[name] = P(x, y, z + 10)
    w = len(text) * 8.9 + 36
    col = '#FFD23F' if tag == 'p' else 'none'
    stroke = '' if tag == 'p' else ' stroke="#9AA6C4" stroke-width="1.5" stroke-dasharray="3 3"'
    LABELS.append(f'<g transform="translate({sx:.0f} {sy + dy:.0f})"><rect x="{-w/2:.0f}" y="0" width="{w:.0f}" height="30" rx="15" fill="#121A33" opacity=".92"/>'
                  f'<circle cx="{-w/2+15:.0f}" cy="15" r="5.5" fill="{col}"{stroke}/>'
                  f'<text x="{-w/2+27:.0f}" y="20.5" font-family="Nunito Sans, Arial" font-weight="700" font-size="15" fill="#F7F1E3">{text}</text></g>')

ZONES = [  # gx, gy, sx, sy, color, title
    (-60, 560, 240, 250, '#3B4F96', 'Families'),
    (270, 430, 180, 210, '#4B5FB0', 'Edge and API'),
    (560, 110, 320, 320, '#3A4FA8', 'Agent core'),
    (980, -170, 200, 280, '#7A4F86', 'AI services'),
    (980, 230, 200, 190, '#3A7F45', 'Approved sources'),
    (600, 540, 320, 200, '#B7791F', 'Data'),
    (270, 60, 180, 210, '#2F6F7A', 'Ops'),
]
ZH = 18
zone_svg = [box(gx, gy, -12, sx, sy, ZH, c) for gx, gy, sx, sy, c, t in ZONES]
Z = ZH - 12
def L(i, x, y):
    return ZONES[i][0] + x, ZONES[i][1] + y

# Families
x, y = L(0, 110, 40);  put(x + y, box(x, y, Z, 46, 26, 72, '#2B2F3A', top='#6C8BEF')); label('parent', x + 23, y + 13, Z + 72, 'Parent app', 'p', -62)
px_, py_ = P(*L(0, 50, 60), Z)
put(L(0, 50, 60)[0] + L(0, 50, 60)[1], f'<ellipse cx="{px_:.0f}" cy="{py_:.0f}" rx="42" ry="12" fill="#000" opacity=".25"/><svg x="{px_-66:.0f}" y="{py_-132:.0f}" width="132" height="138" viewBox="0 0 210 220" overflow="visible">{cast["parentFace"]}</svg>')
PERSON_P = (px_, py_)
kx_, ky_ = P(*L(0, 60, 190), Z)
put(L(0, 60, 190)[0] + L(0, 60, 190)[1], f'<ellipse cx="{kx_:.0f}" cy="{ky_:.0f}" rx="30" ry="9" fill="#000" opacity=".25"/><svg x="{kx_-56:.0f}" y="{ky_-112:.0f}" width="112" height="117" viewBox="0 0 210 220" overflow="visible">{cast["kid"]}</svg>')
PERSON_K = (kx_, ky_)
x, y = L(0, 120, 140); put(x + y, box(x, y, Z, 92, 60, 10, '#2B2F3A', top='#F48FB1'))
gx_, gy_ = P(x + 46, y + 30, Z + 10)
put(x + y + 1, f'<svg x="{gx_-17:.0f}" y="{gy_-38:.0f}" width="34" height="40" viewBox="0 -24 270 324" overflow="visible">{PIP}</svg>')
label('kid', x + 46, y + 30, Z + 10, 'Kid app', 'p', 12)

# Edge and API
x, y = L(1, 20, 150);  put(x + y, box(x, y, Z, 54, 54, 42, '#FFF1C9')); label('cdn', x + 27, y + 27, Z + 42, 'Static hosting and CDN', 'p', -52)
x, y = L(1, 110, 20);  put(x + y, box(x, y, Z, 54, 54, 28, '#6C8BEF')); label('api', x + 27, y + 27, Z + 28, 'API and parent approval', 'p', 10)

# Agent core
x, y = L(6, 162, 150); put(x + y, cyl(x, y, Z, 18, 40, '#F7A23B', 2)); label('sched', x, y, Z + 40, 'Nightly scheduler', 'n', 50)
x, y = L(2, 120, 150)
gx_, gy_ = P(x, y, Z)
put(x + y, f'<svg x="{gx_-60:.0f}" y="{gy_-142:.0f}" width="120" height="145" viewBox="0 -24 270 324" overflow="visible">{PIP}</svg>')
NODES['orch'] = P(x, y, Z + 60); label('orch', x, y, Z, 'Orchestrator', 'p', 8)
wc = ['#6C8BEF', '#F7A23B', '#F7A23B', '#4FA65B', '#4FA65B']
for i, c in enumerate(wc):
    wx, wy = L(2, 230, 24 + i * 56)
    put(wx + wy, box(wx, wy, Z, 42, 36, 28, c))
wx, wy = L(2, 250, 150); NODES['workers'] = P(wx, wy, Z + 32)
wl = P(*L(2, 230, 10), Z + 40)
LABELS.append(f'<g transform="translate({wl[0]+40:.0f} {wl[1]-40:.0f})"><rect x="-178" y="0" width="356" height="30" rx="15" fill="#121A33" opacity=".92"/><circle cx="-163" cy="15" r="5.5" fill="#FFD23F"/><text x="-151" y="20.5" font-family="Nunito Sans, Arial" font-weight="700" font-size="15" fill="#F7F1E3">Workers: discover, verify, rewrite, check, risk</text></g>')

# AI services
x, y = L(3, 40, 30);   put(x + y, box(x, y, Z, 56, 56, 48, '#B9A6F0')); label('llm', x + 28, y + 28, Z + 48, 'Language model', 'n', -54)
x, y = L(3, 40, 160);  put(x + y, box(x, y, Z, 48, 48, 32, '#F48FB1')); label('voice', x + 24, y + 24, Z + 32, 'Voice', 'p', 10)
x, y = L(3, 130, 110); put(x + y, box(x, y, Z, 48, 48, 30, '#FFD23F')); label('img', x + 24, y + 24, Z + 30, 'Picture maker', 'n', 10)
NODES['ai'] = P(*L(3, 70, 120), Z + 40)

# Sources
for (px, py) in [(30, 30), (110, 40), (50, 110)]:
    for j in range(3):
        x, y = L(4, px + j * 2, py - j * 2)
        put(x + y + j, box(x, y, Z + j * 7, 52, 42, 6, ['#FFF8E6', '#F3E5C8', '#FFF1C9'][j]))
x, y = L(4, 90, 80); NODES['src'] = P(x, y, Z + 30); label('srcl', x, y + 70, Z, 'Approved news feeds', 'p', 6)

# Data
for name, lx, ly, c, t, tag, dy in [('stories', 60, 60, '#FFF1C9', 'Story store', 'p', -52), ('family', 160, 110, '#6C8BEF', 'Family settings', 'p', 8),
                                     ('evidence', 260, 60, '#4FA65B', 'Evidence log', 'n', -52), ('cache', 250, 160, '#F08A6E', 'Cache', 'n', 8)]:
    x, y = L(5, lx, ly)
    put(x + y, cyl(x, y, Z, 20, 44, c)); label(name, x, y, Z + (44 if dy < 0 else 0), t, tag, dy)
NODES['data'] = P(*L(5, 160, 80), Z + 50)

# Ops
x, y = L(6, 30, 30);   put(x + y, box(x, y, Z, 56, 42, 38, '#7FD3B4')); label('mon', x + 28, y + 21, Z + 38, 'Monitoring and evals', 'n', -52)
x, y = L(6, 20, 150);  put(x + y, box(x, y, Z, 48, 42, 26, '#FFD23F')); label('notify', x + 24, y + 21, Z + 26, 'Parent notifications', 'n', 10)

ITEMS.sort(key=lambda t: t[0])

BADGES = []
def badge(x, y, t, fill, ink='#121A33'):
    BADGES.append(f'<g transform="translate({x:.0f} {y:.0f})"><circle r="18" fill="{fill}" stroke="#121A33" stroke-width="3"/>'
                  f'<text y="6.5" text-anchor="middle" font-family="Fredoka, Arial" font-weight="600" font-size="19" fill="{ink}">{t}</text></g>')
def flow(a, b, cls='flow', bend=0, mark=None, col='#FFD23F', t=.5):
    (x1, y1), (x2, y2) = NODES[a], NODES[b]
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - bend
    ang = math.degrees(math.atan2(y2 - my, x2 - mx))
    if mark:
        u = 1 - t
        badge(u*u*x1 + 2*u*t*mx + t*t*x2, u*u*y1 + 2*u*t*my + t*t*y2, mark, col)
    return (f'<path class="{cls}" d="M{x1:.0f} {y1:.0f} Q{mx:.0f} {my:.0f} {x2:.0f} {y2:.0f}"/>'
            f'<path d="M-9 -6 L0 0 L-9 6" transform="translate({x2:.0f} {y2:.0f}) rotate({ang:.0f})" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
G_ = '#FFD23F'; M_ = '#7FD3B4'; K_ = '#F48FB1'
nightly = ''.join([flow('sched', 'orch', bend=20, mark='1', t=.5), flow('orch', 'workers', bend=30, mark='2', t=.62), flow('workers', 'src', bend=20, mark='3'),
                   flow('workers', 'ai', bend=40, mark='4'), flow('workers', 'data', bend=-10, mark='6'), flow('data', 'notify', bend=40, mark='7')])
wx4, wy4 = NODES['workers']; badge(wx4 + 34, wy4 - 34, '5', G_)
(mx1, my1), (mx2, my2) = NODES['orch'], NODES['mon']
ops_l = flow('orch', 'mon', 'flow4', 40)
_qx, _qy = (mx1 + mx2) / 2, (my1 + my2) / 2 - 40
_bx, _by = .25 * mx1 + .5 * _qx + .25 * mx2, .25 * my1 + .5 * _qy + .25 * my2
BADGES.append(f'<g transform="translate({_bx:.0f} {_by:.0f})"><rect x="-62" y="-15" width="124" height="30" rx="15" fill="#121A33" stroke="#9AA6C4" stroke-width="2" stroke-dasharray="4 4"/><text y="5.5" text-anchor="middle" font-family="Nunito Sans, Arial" font-weight="700" font-size="14" fill="#CBD3E8">logs every step</text></g>')
parent_l = ''.join([flow('notify', 'parent', 'flow2', 40, '8', G_), flow('parent', 'api', 'flow2', 20, 'A', M_), flow('api', 'data', 'flow2', 20, 'B', M_, t=.38)])
kid_l = flow('cdn', 'kid', 'flow3', -30, 'C', K_)
badge(PERSON_K[0] + 52, PERSON_K[1] - 86, 'D', K_)
family = parent_l

def ptag(x, y, title, sub, col):
    w = max(len(title) * 11.5, len(sub) * 8.6) + 40
    return (f'<g transform="translate({x:.0f} {y:.0f})"><rect x="{-w/2:.0f}" y="0" width="{w:.0f}" height="56" rx="16" fill="#FFF8E6" stroke="{col}" stroke-width="3"/>'
            f'<text x="0" y="23" text-anchor="middle" font-family="Fredoka, Arial" font-weight="600" font-size="20" fill="#121A33">{title}</text>'
            f'<text x="0" y="44" text-anchor="middle" font-family="Nunito Sans, Arial" font-size="15" fill="#4A5568">{sub}</text></g>')
person_tags = (ptag(PERSON_P[0] - 10, PERSON_P[1] - 196, 'Parent · the editor', 'Sees facts and sources, approves', '#7FD3B4')
               + ptag(PERSON_K[0] - 40, PERSON_K[1] + 74, 'Kid · read only', 'Only approved stories, no account', '#F48FB1'))
ztitles = []
for gx, gy, sx, sy, c, t in ZONES:
    tx, ty = P(gx, gy + sy, -12) if t == 'Ops' else P(gx + sx, gy + sy, -12)
    w = len(t) * 11 + 32
    ztitles.append(f'<g transform="translate({tx:.0f} {ty+8:.0f})"><rect x="{-w/2:.0f}" y="0" width="{w:.0f}" height="34" rx="17" fill="#FFF8E6"/>'
                   f'<text x="0" y="23" text-anchor="middle" font-family="Fredoka, Arial" font-weight="600" font-size="18" fill="{shade(c, .8)}">{t}</text></g>')

import re as _re
_all = ''.join(zone_svg) + ''.join(x for _, x in ITEMS)
_pts = [tuple(map(float, q.split(','))) for m in _re.findall(r'points="([^"]+)"', _all) for q in m.split()]
_x0 = min(p[0] for p in _pts) - 110; _x1 = max(p[0] for p in _pts) + 30
_y0 = min(p[1] for p in _pts) - 90; _y1 = max(p[1] for p in _pts) + 60
VB = '%.0f %.0f %.0f %.0f' % (_x0, _y0, _x1 - _x0, _y1 - _y0)
svg = f'''<svg class="iso" viewBox="{VB}" role="img" aria-label="2.5D system architecture. Families use a parent app and a kid app served from static hosting. The parent app talks to an API gateway and a parent approval service. A nightly scheduler wakes the orchestrator, which puts jobs on a queue for five agent workers: discover, verify, rewrite, self check and risk. Workers read approved news feeds, call a language model, a voice service and a picture maker, and write to a story store and an evidence log. Data also holds family settings and a cache. Ops has monitoring and evals plus parent notifications.">
  <defs>{DEFS}<radialGradient id="mglow"><stop offset="0" stop-color="#FFD23F" stop-opacity=".55"/><stop offset="1" stop-color="#FFD23F" stop-opacity="0"/></radialGradient></defs>
  {''.join(zone_svg)}
  {''.join(s for _, s in ITEMS)}
  <g class="ops" style="color:#9AA6C4">{ops_l}</g>
  <g class="night" style="color:#FFD23F">{nightly}</g>
  <g class="fam" style="color:#7FD3B4">{family}</g>
  <g class="kidl" style="color:#F48FB1">{kid_l}</g>
  {''.join(ztitles)}
  {''.join(LABELS)}
  {person_tags}
  {''.join(BADGES)}
</svg>'''

def card(t, c, rows):
    lis = ''.join(f'<li><b>{a}</b> {"<em>Next</em>" if g == "n" else "<i>Prototype</i>"}<span>{d}</span></li>' for a, g, d in rows)
    return f'<div class="dc"><p class="dh"><span class="dot" style="background:{c}"></span>{t}</p><ul>{lis}</ul></div>'
cards = ''.join([
    card('Families', '#3B4F96', [('Parent app', 'p', 'Run tonight’s agent, see facts and sources, approve.'), ('Kid app', 'p', 'Story shelf with only shared stories.')]),
    card('Edge and API', '#4B5FB0', [('Static hosting and CDN', 'p', 'Serves both apps fast, anywhere.'), ('API gateway', 'n', 'One door for app requests, with sign in.'), ('Parent approval', 'p', 'Share, not tonight, or make it simpler.')]),
    card('Agent core', '#3A4FA8', [('Orchestrator', 'p', 'One goal, time and cost limits, logs each step.'), ('Job queue and workers', 'n', 'Discover, verify, rewrite, self check, risk, in parallel.')]),
    card('AI services', '#7A4F86', [('Language model', 'n', 'Reads, checks and rewrites, grounded in sources.'), ('Voice', 'p', 'Today: the browser’s built in speech.'), ('Picture maker', 'n', 'Today: hand drawn SVG scenes.')]),
    card('Data and sources', '#B7791F', [('Approved news feeds', 'p', 'Only listed sources, no open scraping.'), ('Story store and family settings', 'p', 'Today: JavaScript objects in the page.'), ('Evidence log and cache', 'n', 'Every line keeps its source and time.')]),
    card('Ops', '#2F6F7A', [('Nightly scheduler', 'n', 'Wakes the agent every evening.'), ('Monitoring and evals', 'n', 'Accuracy checks, cost per story, errors.'), ('Parent notifications', 'n', 'A short note when tonight’s story is ready.')]),
])

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Goodnight, AI · System Architecture</title>
<meta name="description" content="A 2.5D system architecture for the Goodnight, AI service: apps, API, agent core, AI services, sources and data.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&family=Nunito+Sans:wght@400;600;700&display=swap">
<style>
:root {{ --night:#121A33; --night2:#1C2647; --night3:#24305A; --cream:#F7F1E3; --gold:#FFD23F; --mist:#CBD3E8; --mist2:#9AA6C4;
  --f-display: Fredoka, "Trebuchet MS", Arial, sans-serif; --f-body: "Nunito Sans", Arial, sans-serif; color-scheme: dark }}
* {{ box-sizing: border-box }}
body {{ margin: 0; background: radial-gradient(circle at 80% 0%, var(--night3) 0, var(--night) 60%) fixed, var(--night); color: var(--cream); font-family: var(--f-body); line-height: 1.5 }}
a {{ color: inherit }}
.wrap {{ max-width: 1320px; margin: 0 auto; padding: 24px max(20px, env(safe-area-inset-left, 0px)) 40px }}
.top {{ display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap }}
.brand {{ font-family: var(--f-display); font-weight: 600; font-size: 22px; text-decoration: none }} .brand span {{ color: var(--gold) }}
.back {{ font-weight: 700; font-size: 15px; color: var(--mist); text-decoration: none; border: 2px solid var(--night3); border-radius: 999px; padding: 8px 16px }}
.back:hover {{ color: var(--gold); border-color: var(--gold) }}
.head {{ display: flex; align-items: flex-end; justify-content: space-between; gap: 20px; flex-wrap: wrap; margin-top: 18px }}
.eyebrow {{ margin: 0 0 6px; font-weight: 700; font-size: 13px; letter-spacing: .22em; text-transform: uppercase; color: var(--gold) }}
h1 {{ margin: 0; font-family: var(--f-display); font-weight: 600; font-size: clamp(28px, 3.2vw, 42px); line-height: 1.1 }}
.legend {{ display: flex; gap: 16px; flex-wrap: wrap; font-size: 14px; color: var(--mist); align-items: center }}
.legend span {{ display: inline-flex; align-items: center; gap: 7px }}
.k {{ width: 11px; height: 11px; border-radius: 50%; display: inline-block }}
.ln {{ width: 26px; height: 0; border-top: 3px dashed; display: inline-block }}
.stage {{ margin-top: 10px }}
.iso {{ width: 100%; height: auto; display: block; overflow: visible }}
.flow, .flow2 {{ fill: none; stroke: currentColor; stroke-width: 3.2; stroke-linecap: round; stroke-dasharray: 2 11; animation: flow 1.2s linear infinite }}
.flow2 {{ stroke-dasharray: 7 8 }}
.flow4 {{ fill: none; stroke: currentColor; stroke-width: 2.4; stroke-linecap: round; stroke-dasharray: 4 7; opacity: .8 }}
.flow3 {{ fill: none; stroke: currentColor; stroke-width: 3.2; stroke-linecap: round; stroke-dasharray: 7 8; animation: flow 1.2s linear infinite }}
@keyframes flow {{ to {{ stroke-dashoffset: -26 }} }}
.cards {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 10px }}
.dc {{ background: var(--night2); border: 1px solid var(--night3); border-radius: 18px; padding: 14px 16px }}
.dh {{ margin: 0 0 8px; display: flex; align-items: center; gap: 9px; font-family: var(--f-display); font-weight: 600; font-size: 17px }}
.dot {{ width: 14px; height: 14px; border-radius: 4px }}
.dc ul {{ list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px }}
.dc li {{ font-size: 13.5px }} .dc li b {{ color: var(--cream) }}
.dc li span {{ display: block; color: var(--mist) }}
.dc em, .dc i {{ font-style: normal; font-size: 10px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; border-radius: 999px; padding: 1px 7px; margin-left: 4px; vertical-align: 1px }}
.dc i {{ background: var(--gold); color: var(--night) }} .dc em {{ border: 1.5px dashed var(--mist2); color: var(--mist) }}
.seq {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 8px }}
.sq {{ background: var(--night2); border: 1px solid var(--night3); border-radius: 18px; padding: 14px 16px }}
.sqh {{ margin: 0 0 8px; display: flex; align-items: center; gap: 9px; font-family: var(--f-display); font-weight: 600; font-size: 17px }}
.sqd {{ width: 14px; height: 14px; border-radius: 50% }}
.sq ol {{ list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 7px }}
.sq li {{ display: flex; gap: 10px; align-items: flex-start; font-size: 14px; color: var(--mist) }}
.sq li b {{ flex: none; width: 24px; height: 24px; border-radius: 50%; background: var(--gold); color: var(--night); display: grid; place-items: center; font-family: var(--f-display); font-size: 13px; border: 2px solid var(--night) }}
.meet {{ grid-column: 1 / -1; margin: 0; font-size: 14px; color: var(--cream); background: rgba(255,210,63,.1); border: 1px dashed var(--gold); border-radius: 14px; padding: 10px 14px }}
@media (max-width: 760px) {{ .seq {{ grid-template-columns: 1fr }} }}
.note {{ margin: 16px 0 0; font-size: 13.5px; color: var(--mist2); max-width: 96ch }}
.swipe {{ display: none; margin: 12px 0 0; font-size: 13px; font-weight: 700; color: var(--gold) }}
@media (max-width: 900px) {{ .cards {{ grid-template-columns: 1fr 1fr }} }}
@media (max-width: 560px) {{ .cards {{ grid-template-columns: 1fr }} .swipe {{ display: block }} .stage {{ overflow-x: auto; -webkit-overflow-scrolling: touch }} .iso {{ width: 860px; max-width: none }} }}
@media (prefers-reduced-motion: reduce) {{ .flow, .flow2 {{ animation: none }} }}
</style>
</head>
<body>
<div class="wrap">
  <div class="top"><a class="brand" href="index.html">Goodnight, <span>AI</span></a><a class="back" href="index.html">← Back to home</a></div>
  <div class="head">
    <div><p class="eyebrow">System architecture</p><h1>How the Goodnight, AI service is built</h1></div>
    <div class="legend">
      <span><span class="k" style="background:#FFD23F"></span>In today’s prototype</span>
      <span><span class="k" style="border:1.5px dashed #9AA6C4"></span>Next, for the full service</span>
      <span><span class="ln" style="color:#FFD23F;border-top-style:dotted"></span>Nightly agent run</span>
      <span><span class="ln" style="color:#7FD3B4"></span>Parent</span>
      <span><span class="ln" style="color:#F48FB1"></span>Kid, read only</span>
      <span><span class="ln" style="color:#9AA6C4;border-top-style:dotted"></span>Monitoring, always on</span>
    </div>
  </div>
  <p class="swipe">Swipe to see the whole system →</p>
  <div class="stage">{svg}</div>
  <div class="seq">
    <div class="sq"><p class="sqh"><span class="sqd" style="background:#FFD23F"></span>Tonight, automatic</p><ol>
      <li><b>1</b>The scheduler wakes the orchestrator.</li>
      <li><b>2</b>The orchestrator hands jobs to the workers.</li>
      <li><b>3</b>Workers read the approved news feeds.</li>
      <li><b>4</b>AI services help verify, rewrite, voice and draw.</li>
      <li><b>5</b>Self check every line, then sort by risk.</li>
      <li><b>6</b>Save the story with its sources and evidence.</li>
      <li><b>7</b>Saving a story sends a parent notification.</li>
      <li><b>8</b>The parent hears: tonight’s story is ready.</li></ol></div>
    <div class="sq"><p class="sqh"><span class="sqd" style="background:#7FD3B4"></span>At bedtime, with people</p><ol class="abc">
      <li><b style="background:#7FD3B4">A</b>The parent opens the story, the facts and the sources.</li>
      <li><b style="background:#7FD3B4">B</b>The parent approves, skips or asks for a simpler version.</li>
      <li><b style="background:#F48FB1">C</b>Only approved stories appear on the kid’s shelf.</li>
      <li><b style="background:#F48FB1">D</b>Pip reads it aloud, and they talk about it together.</li></ol></div>
    <p class="meet">The two paths meet at the story store. Everything before it is automatic; nothing after it reaches a kid without the risk rules and, when needed, the parent.</p>
  </div>
  <div class="cards">{cards}</div>
  <p class="note">Components use generic names on purpose. Today’s prototype runs as static pages: the orchestrator plays a labeled replay of one real agent run, stories and family rules live in the page, and Pip speaks with the browser’s built in voice. In the full service, each agent worker becomes a real AI call with its own tools and checks, and nothing reaches a kid without passing the risk rules and, when needed, the parent.</p>
</div>
</body>
</html>'''
open('/mnt/user-data/outputs/site-v2/system.html', 'w').write(html)
print('ok', len(html))
