"""Story cards for a Threads / Instagram carousel.

One page, one square-ish card, read at arm's length on a phone. The reference
format: a big headline, the character acting it out, nothing else competing.

4:5 (1080x1350) is the tallest a feed shows without cropping.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pip import pip, LOOP, POSES  # noqa: E402
import parts  # noqa: E402

W, H = 1080, 1350
PAPER, INK, BLUE, GLOW, SOFT = "#FFF4DE", "#141E3C", "#4A6FE8", "#FFD23F", "#8C93B8"

# Which pose fits each beat of the story.
SLOT_POSE = {
    "cover": "wave", "character": "read", "news_discovery": "point",
    "exploration": "peek", "challenge": "lost", "turning_point": "stand",
    "resolution": "cheer", "reflection": "sleep", "real_world_facts": "point",
    "quiz": "think",
}

TAG_COLOR = {"true": "#2E9E6B", "maybe": "#E0922B",
             "imagine": "#7B5EC7", "explain": "#3A7BD5"}


def _wrap(text, per_line):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > per_line and cur:
            lines.append(cur); cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "’"))


def card(page, total, title=""):
    text = page["text"]
    pose = SLOT_POSE.get(page["slot"], "stand")
    mood = page["tone"]

    # Pick the largest size that still fits the headline box whole. Nothing is
    # ever truncated: a cut-off sentence is worse than a smaller one.
    BOX_H, MIN_SIZE = 400, 40
    for size in range(78, MIN_SIZE - 1, -2):
        per = max(12, int(1180 / size * 1.08))     # chars per line at this size
        lines = _wrap(text, per)
        if len(lines) * size * 1.24 <= BOX_H:
            break
    lh = size * 1.24
    top = 268 + (BOX_H - len(lines) * lh) / 2

    head = "".join(
        f'<text x="{W//2}" y="{top + i*lh:.0f}" text-anchor="middle" '
        f'font-family="Verdana,DejaVu Sans,system-ui,sans-serif" font-size="{size}" '
        f'font-weight="700" fill="{INK}">{_esc(l)}</text>'
        for i, l in enumerate(lines))

    tags = sorted(set(page.get("tags", [])))
    chips, cx = [], W // 2 - (len(tags) * 126) // 2
    for t in tags:
        c = TAG_COLOR.get(t, SOFT)
        chips.append(
            f'<g transform="translate({cx},158)">'
            f'<rect x="0" y="-30" width="112" height="46" rx="23" fill="{c}" opacity=".15"/>'
            f'<text x="56" y="3" text-anchor="middle" font-family="Verdana,system-ui" '
            f'font-size="25" font-weight="700" fill="{c}">{t}</text></g>')
        cx += 126

    brand = (f'<text x="64" y="{H-64}" font-family="Verdana,system-ui" font-size="26" '
             f'font-weight="700" fill="{SOFT}">Goodnight, AI</text>'
             f'<text x="{W-64}" y="{H-64}" text-anchor="end" '
             f'font-family="Verdana,system-ui" font-size="26" font-weight="700" '
             f'fill="{SOFT}">{page["page"]} / {total}</text>')

    # A soft disc behind Pip lifts him off the paper without adding clutter.
    halo = (f'<circle cx="{W//2}" cy="965" r="272" fill="{GLOW}" opacity=".26"/>'
            f'<circle cx="{W//2}" cy="965" r="272" fill="{BLUE}" opacity=".07"/>')

    return f"""<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs>{parts.PAINT_FILTER}</defs>
<rect width="{W}" height="{H}" fill="{PAPER}"/>
<text x="{W//2}" y="104" text-anchor="middle" font-family="Verdana,system-ui"
 font-size="26" font-weight="700" letter-spacing="6" fill="{SOFT}">
 {_esc(page["slot"].replace("_", " ").upper())}</text>
{halo}
{head}
{pip(W//2, 1152, 1.40, mood, pose)}
{"".join(chips)}
{brand}
</svg>"""
