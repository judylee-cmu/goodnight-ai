"""SVG scene parts, in the Goodnight, AI visual language.

All motion shares one 2.0s period (LOOP), so 24 frames at 12fps cover a full
cycle and can be repeated for any page length without a visible seam.

The prototype does not generate images. It hand-draws flat vector scenes with a
paper-grain filter, so the character is identical on every page and the palette
never drifts. These parts rebuild that language as something a script can
assemble, page by page.

LOOP = 2.0

Stage is 1600x900 (same as the prototype). The reel crops to 9:16.
"""

LOOP = 2.0

# From the prototype: fractal noise displacement plus a grain overlay.
PAINT_FILTER = """
<filter id="paint" x="-8%" y="-8%" width="116%" height="116%">
  <feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="3" result="w"/>
  <feDisplacementMap in="SourceGraphic" in2="w" scale="3.5"
      xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="11" result="g"/>
  <feColorMatrix in="g" type="matrix"
      values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -.9 .62" result="ga"/>
  <feComposite in="ga" in2="d" operator="in" result="gi"/>
  <feMerge><feMergeNode in="d"/><feMergeNode in="gi"/></feMerge>
</filter>"""

# One gradient per tone. Same structure as the prototype's #bsky.
SKIES = {
    "warm":    ("#241C4A", "#6A3E6E", "#C9705E"),
    "calm":    ("#141230", "#241C4A", "#3C2F63"),
    "curious": ("#1A1A3E", "#332C66", "#5B4A8A"),
    "quiet":   ("#0E0C22", "#1A1A2E", "#272046"),
    "excited": ("#2A1F52", "#6A3E6E", "#F7A23B"),
}

GROUND = {"warm": "#7A4E7E", "calm": "#2A2550", "curious": "#3A3070",
          "quiet": "#1C1838", "excited": "#8A5A7E"}


def sky(tone):
    a, b, c = SKIES.get(tone, SKIES["calm"])
    return (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{a}"/>'
            f'<stop offset=".7" stop-color="{b}"/>'
            f'<stop offset="1" stop-color="{c}"/></linearGradient>')


def stars(n=26, seed=7):
    """Deterministic star field, so the same page always renders the same."""
    out, s = [], seed
    for _ in range(n):
        s = (s * 1103515245 + 12345) % 2147483648
        x = 40 + s % 1520
        s = (s * 1103515245 + 12345) % 2147483648
        y = 40 + s % 430
        s = (s * 1103515245 + 12345) % 2147483648
        r = 1.6 + (s % 24) / 10
        s = (s * 1103515245 + 12345) % 2147483648
        off = (s % 20) / 10 * LOOP / 2
        out.append(
            f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="#FFF8E6" opacity=".55">'
            f'<animate attributeName="opacity" values=".2;.85;.2" dur="{LOOP}s" '
            f'begin="-{off:.2f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def moon(x=1380, y=170, r=78, tone="calm"):
    """Crescent cut with a mask, so the dark side matches the sky behind it."""
    mid = SKIES.get(tone, SKIES["calm"])[0]
    return (f'<mask id="mn"><circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/>'
            f'<circle cx="{x - r*.42:.0f}" cy="{y - r*.20:.0f}" r="{r*.88:.0f}" '
            f'fill="#000"/></mask>'
            f'<g filter="url(#paint)">'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{mid}" opacity=".0"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFD23F" mask="url(#mn)"/></g>')


def skyline(ground_y=640, color="#2A2250"):
    """Simple building silhouettes, like the prototype's town."""
    spec = [(60, 150, 210), (250, 110, 150), (400, 170, 120), (1140, 130, 180),
            (1310, 100, 140), (1450, 150, 200)]
    out = []
    for x, w, h in spec:
        out.append(f'<rect x="{x}" y="{ground_y-h}" width="{w}" height="{h}" '
                   f'rx="10" fill="{color}"/>')
        out.append(f'<polygon points="{x-12},{ground_y-h} {x+w//2},{ground_y-h-52} '
                   f'{x+w+12},{ground_y-h}" fill="{color}"/>')
    return f'<g filter="url(#paint)">{"".join(out)}</g>'


def ground(tone, y=640):
    return (f'<g filter="url(#paint)">'
            f'<rect x="0" y="{y}" width="1600" height="{900-y}" '
            f'fill="{GROUND.get(tone, GROUND["calm"])}"/></g>')


def pip(x=800, y=640, scale=1.0, mood="calm"):
    """Pip the robot owl, drawn in the prototype's flat style.

    Blue body, cream chest, glowing yellow eyes, one antenna.
    Breathing and blinking are built in; the antenna tilt carries mood.
    """
    tilt = {"calm": 0, "curious": -14, "excited": 10, "warm": -6, "quiet": 4}.get(mood, 0)
    glow = {"quiet": ".55", "calm": ".8", "warm": ".92", "curious": "1", "excited": "1"}.get(mood, ".8")
    return f"""<g transform="translate({x},{y}) scale({scale})">
  <g filter="url(#paint)">
    <animateTransform attributeName="transform" type="translate"
      values="0,0; 0,-9; 0,0" dur="{LOOP}s" repeatCount="indefinite" additive="sum"/>
    <ellipse cx="0" cy="-8" rx="92" ry="18" fill="#000" opacity=".22"/>
    <path d="M-86 -36 C-86 -168 86 -168 86 -36 C86 -8 50 -4 0 -4 C-50 -4 -86 -8 -86 -36Z"
          fill="#6C8BEF"/>
    <path d="M-86 -64 C-104 -96 -100 -126 -86 -122 Z" fill="#5A79DD"/>
    <path d="M86 -64 C104 -96 100 -126 86 -122 Z" fill="#5A79DD"/>
    <ellipse cx="0" cy="-44" rx="50" ry="40" fill="#FFF8E6"/>
    <g>
      <circle cx="-34" cy="-108" r="27" fill="#FFD23F" opacity="{glow}"/>
      <circle cx="34" cy="-108" r="27" fill="#FFD23F" opacity="{glow}"/>
      <animate attributeName="opacity" values="1;1;.05;1;1"
               dur="{LOOP}s" keyTimes="0;.86;.91;.96;1" repeatCount="indefinite"/>
    </g>
    <polygon points="-15,-92 0,-74 15,-92" fill="#F7A23B"/>
    <g transform="rotate({tilt} 0 -160)">
      <line x1="0" y1="-160" x2="0" y2="-196" stroke="#6C8BEF" stroke-width="9"
            stroke-linecap="round"/>
      <circle cx="0" cy="-204" r="11" fill="#FFD23F">
        <animate attributeName="r" values="11;13.5;11" dur="{LOOP}s" repeatCount="indefinite"/>
      </circle>
    </g>
  </g>
</g>"""


def scene(tone, mood=None, with_skyline=True, with_moon=True, pip_scale=1.0):
    mood = mood or tone
    return f"""<svg viewBox="0 0 1600 900" xmlns="http://www.w3.org/2000/svg">
<defs>{PAINT_FILTER}{sky(tone)}</defs>
<rect width="1600" height="900" fill="url(#sky)"/>
{stars()}
{moon() if with_moon else ""}
{skyline() if with_skyline else ""}
{ground(tone)}
{pip(800, 650, pip_scale, mood)}
</svg>"""


# --- vertical stage, 1080x1920, for Threads and Instagram -------------------

VW, VH = 1080, 1920


def vstars(n=34, seed=19):
    out, s = [], seed
    for _ in range(n):
        s = (s * 1103515245 + 12345) % 2147483648
        x = 30 + s % 1020
        s = (s * 1103515245 + 12345) % 2147483648
        y = 40 + s % 900
        s = (s * 1103515245 + 12345) % 2147483648
        r = 1.8 + (s % 26) / 10
        s = (s * 1103515245 + 12345) % 2147483648
        off = (s % 20) / 10 * LOOP / 2
        out.append(
            f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="#FFF8E6" opacity=".55">'
            f'<animate attributeName="opacity" values=".2;.85;.2" dur="{LOOP}s" '
            f'begin="-{off:.2f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def vskyline(ground_y=1180, color="#2A2250"):
    spec = [(-20, 150, 190), (150, 110, 130), (760, 130, 165), (920, 150, 220)]
    out = []
    for x, w, h in spec:
        out.append(f'<rect x="{x}" y="{ground_y-h}" width="{w}" height="{h}" '
                   f'rx="10" fill="{color}"/>')
        out.append(f'<polygon points="{x-12},{ground_y-h} {x+w//2},{ground_y-h-50} '
                   f'{x+w+12},{ground_y-h}" fill="{color}"/>')
    return f'<g filter="url(#paint)">{"".join(out)}</g>'


def vscene(tone, text="", slot="", mood=None):
    """Portrait card: sky and Pip up top, caption burned in below."""
    mood = mood or tone
    g = GROUND.get(tone, GROUND["calm"])
    lines = _wrap(text, 24)
    y0 = 1420
    caption = "".join(
        f'<text x="540" y="{y0 + i*78}" font-family="system-ui,-apple-system,sans-serif" '
        f'font-size="60" font-weight="600" fill="#FFF8E6" text-anchor="middle">'
        f'{_esc(l)}</text>' for i, l in enumerate(lines))
    label = (f'<text x="540" y="180" font-family="system-ui,sans-serif" font-size="32" '
             f'letter-spacing="4" fill="#6C8BEF" text-anchor="middle">'
             f'{_esc(slot.replace("_"," ").upper())}</text>') if slot else ""
    return f"""<svg viewBox="0 0 {VW} {VH}" xmlns="http://www.w3.org/2000/svg">
<defs>{PAINT_FILTER}{sky(tone)}</defs>
<rect width="{VW}" height="{VH}" fill="url(#sky)"/>
{vstars()}
{moon(840, 300, 96, tone)}
{vskyline()}
<g filter="url(#paint)"><rect x="0" y="1180" width="{VW}" height="{VH-1180}" fill="{g}"/></g>
{label}
{pip(540, 1215, 1.45, mood)}
<rect x="0" y="1290" width="{VW}" height="{VH-1290}" fill="#0E0C22" opacity=".55"/>
{caption}
</svg>"""


def _wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur); cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines[:5]


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#8217;"))
