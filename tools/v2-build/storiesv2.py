"""Restyle the three story animations in index-v2.html to the new hand drawn cast.
Keeps every class name the animation code depends on."""
import re, base64, io, random
from PIL import Image

P = '/tmp/claude-0/-home-claude/3e881c95-6cf0-56cd-aa41-2012ca221448/scratchpad/build/index-v2.html'
s = open(P).read()
INK = '#1A1A2E'
PAINT = 'filter="url(#gn-paint)"'

def sub(old, new, count=1):
    global s
    assert old in s, old[:80]
    s = s.replace(old, new, count)

def sub_block(start_marker, end_marker, new):
    """Replace from start_marker up to (not including) end_marker."""
    global s
    a = s.index(start_marker); b = s.index(end_marker, a)
    s = s[:a] + new + s[b:]

# ---------- shared: paper grain tile and a cop version of Pip ----------
random.seed(7)
im = Image.new('LA', (180, 180))
im.putdata([(random.randint(0, 255), random.randint(0, 70)) for _ in range(180 * 180)])
buf = io.BytesIO(); im.save(buf, 'PNG')
grain = base64.b64encode(buf.getvalue()).decode()
sub('</defs></svg>', f'<pattern id="gn-grain" width="180" height="180" patternUnits="userSpaceOnUse"><image href="data:image/png;base64,{grain}" width="180" height="180"/></pattern></defs></svg>')
GRAIN = '<rect class="gn-grain" width="1600" height="900" fill="url(#gn-grain)" opacity=".5" style="mix-blend-mode:multiply;pointer-events:none"/>'

# Pip without antenna, for the police cap
pip_g = re.search(r'<g id="pip">.*?\n </g></g></g>', s, re.S).group(0)
cop = pip_g.replace('<g id="pip">', '<g id="pip-cop">')
cop = re.sub(r'<circle class="p-glow"[^>]*/>', '', cop)
cop = re.sub(r'<path d="M140 58 C138 44 146 32 146 18"[^>]*/>', '', cop)
cop = re.sub(r'<g filter="url\(#gn-paint\)"><path d="M172 14[^"]*" fill="#FFD23F"/></g>', '', cop)
cop = cop.replace('class="p-arm-r wave"', 'class="p-arm-r"')
s = s.replace(pip_g, pip_g + '\n' + cop, 1)

def eyes(x1, y1, x2, y2, r, dx, dy, pr):
    return (f'<g class="p-eyes"><circle cx="{x1}" cy="{y1}" r="{r}" fill="#FFFDF6"/><circle cx="{x2}" cy="{y2}" r="{r}" fill="#FFFDF6"/>'
            f'<circle cx="{x1+dx}" cy="{y1+dy}" r="{pr}" fill="{INK}"/><circle cx="{x2+dx}" cy="{y2+dy}" r="{pr}" fill="{INK}"/></g>')
def blush(x1, y1, x2, y2, r):
    return (f'<circle cx="{x1}" cy="{y1}" r="{r}" fill="#F48FB1" opacity=".7" filter="url(#gn-fuzz)"/>'
            f'<circle cx="{x2}" cy="{y2}" r="{r}" fill="#F48FB1" opacity=".7" filter="url(#gn-fuzz)"/>')
def boots(lx, rx, y, w=20):
    return (f'<path d="M{lx} {y-12} h{w*0.7:.0f} v6 c6 0 {w*0.5:.0f} 2 {w*0.5:.0f} 8 h-{w*1.2:.0f}z" fill="#F48FB1"/>'
            f'<path d="M{rx} {y-12} h{w*0.7:.0f} v6 c6 0 {w*0.5:.0f} 2 {w*0.5:.0f} 8 h-{w*1.2:.0f}z" fill="#FFD23F"/>')

# ================= Story 1: The Magic Key =================
sub('<rect width="1600" height="900" fill="url(#sky)"/>', '<rect width="1600" height="900" fill="#1F2F6B"/>')
sub('<circle cx="1360" cy="120" r="70" fill="#F2C94C"/><circle cx="1392" cy="100" r="62" fill="#18224A"/>',
    f'<g {PAINT}><circle cx="1360" cy="120" r="70" fill="#FFD23F"/></g><circle cx="1392" cy="100" r="62" fill="#1F2F6B"/>')
sub('<path d="M0 700 H1600 V900 H0 Z" fill="#1A2347"/>', '<path d="M0 700 H1600 V900 H0 Z" fill="#172457"/>')

# raccoons
a = s.index('<g id="racc">'); b = s.index('</g>', a) + 4
s = s[:a] + f'''<g id="racc"><g {PAINT}>
          <path d="M14 -34 q-56 -6 -50 -64" stroke="#8C8FB8" stroke-width="18" fill="none" stroke-linecap="round"/>
          <path d="M-24 -60 l16 7 M-34 -78 l17 3" stroke="#2B2F4A" stroke-width="8" stroke-linecap="round"/>
          <rect x="30" y="-24" width="11" height="18" rx="5" fill="#8C8FB8"/><rect x="56" y="-24" width="11" height="18" rx="5" fill="#8C8FB8"/>
          {boots(26, 52, 2, 22)}
          <ellipse cx="48" cy="-42" rx="33" ry="34" fill="#8C8FB8"/>
          <ellipse cx="50" cy="-34" rx="18" ry="20" fill="#FFF1C9"/>
          <circle cx="28" cy="-122" r="11" fill="#8C8FB8"/><circle cx="74" cy="-122" r="11" fill="#8C8FB8"/>
          <circle cx="28" cy="-122" r="5" fill="#F48FB1"/><circle cx="74" cy="-122" r="5" fill="#F48FB1"/>
          <circle cx="51" cy="-96" r="32" fill="#8C8FB8"/>
          <path d="M20 -104 C34 -116 70 -116 83 -104 C85 -92 70 -88 51 -93 C32 -88 17 -92 20 -104Z" fill="#2B2F4A"/>
          <circle cx="51" cy="-80" r="5" fill="#2B2F4A"/>
        </g>
        {eyes(38, -101, 64, -101, 7, 3, 0, 3.2)}
        <path d="M43 -72 Q52 -67 61 -74" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>
        {blush(30, -82, 72, -82, 6)}
        </g>''' + s[b:]

# AI helper used by the raccoons
sub_block('<g class="hop">', '<text class="huh"', f'''<g class="hop">
          <path d="M0 -80 C-5 -88 5 -92 0 -100" stroke="#FFF1C9" stroke-width="5" fill="none" stroke-linecap="round"/>
          <circle class="bot-light" cx="0" cy="-104" r="9" fill="#FF8A3D"/>
          <g {PAINT}>
           <path d="M-38 -70 C-36 -84 -14 -86 2 -86 C24 -86 40 -82 39 -66 C41 -50 41 -34 34 -26 C24 -18 -22 -18 -34 -26 C-41 -36 -41 -56 -38 -70Z" fill="#7FD3B4"/>
           <circle cx="-20" cy="-12" r="12" fill="#2B2F4A"/><circle cx="20" cy="-12" r="12" fill="#2B2F4A"/>
           <circle cx="-20" cy="-12" r="4" fill="#FFF1C9"/><circle cx="20" cy="-12" r="4" fill="#FFF1C9"/>
          </g>
          {eyes(-13, -58, 13, -62, 9, 2, 0, 4)}
          <path d="M-8 -40 q8 6 16 0" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>
          {blush(-26, -44, 26, -46, 6)}
          ''')

# computer police: Pip in a police cap with a flashlight
a = s.index('<g transform="translate(-60,-150) scale(1.3)">')
b = s.index('</g>\n      </g>\n      <g class="bubble">', a)
s = s[:a] + f'''<g transform="translate(-60,-150) scale(1.3)">
          <use href="#pip-cop"/>
          <g {PAINT}><path d="M32 36 C34 20 86 18 88 34 Z" fill="#2F6FD6"/><rect x="26" y="32" width="70" height="8" rx="4" fill="#1F4FA0"/></g>
          <circle class="siren" cx="60" cy="18" r="7" fill="#7FC8F8"/>
          <path d="M40 78 l3 6 7 1 -5 5 1 7 -6 -3 -6 3 1 -7 -5 -5 7 -1 z" fill="#FFD23F"/>
          <rect x="10" y="98" width="24" height="11" rx="5" fill="#FFD23F"/>
        ''' + s[b:]

# key: brighter yellow with paint texture
sub('<g fill="#F2C94C">\n          <circle cx="0" cy="0" r="36"/>', f'<g fill="#FFD23F" {PAINT}>\n          <circle cx="0" cy="0" r="36"/>')

# houses: flat bright colors with paint texture
sub('''var colors = [["#3B4A7A", "#2A3560"], ["#4A3F73", "#352C57"], ["#2F5D6E", "#21454F"], ["#5A4A6E", "#3F3350"],
                ["#3E5B7E", "#2B4060"], ["#4F4370", "#3A3055"], ["#2F566A", "#21404F"]];''',
    '''var colors = [["#F08A6E", "#C9604A"], ["#6C8BEF", "#4B67C9"], ["#4FA65B", "#3A7F45"], ["#F48FB1", "#D0668C"],
                ["#F7A23B", "#C97E22"], ["#7FD3B4", "#4FA68A"], ["#9B8BE0", "#7363B8"]];''')
sub("""'<polygon points="' + (cx - 100) + ',470 ' + cx + ',380 ' + (cx + 100) + ',470" fill="' + c[1] + '"/>' +
      '<rect x="' + (cx - 85) + '" y="470" width="170" height="230" rx="10" fill="' + c[0] + '"/>' +""",
    """'<g filter="url(#gn-paint)"><polygon points="' + (cx - 100) + ',470 ' + cx + ',380 ' + (cx + 100) + ',470" fill="' + c[1] + '"/>' +
      '<rect x="' + (cx - 85) + '" y="470" width="170" height="230" rx="10" fill="' + c[0] + '"/></g>' +""")
sub("""fill="#7FC8F8"/>' +
      '<path d="M' + (cx - 40) + ' 510 h50""", """fill="#FFF1C9"/>' +
      '<path d="M' + (cx - 40) + ' 510 h50""")

# ================= Story 2: The Little Builder =================
sub('<rect width="1600" height="900" fill="url(#bsky)"/>', '<rect width="1600" height="900" fill="#4B3C7A"/><rect y="520" width="1600" height="180" fill="#7A4F86"/>')
sub('<circle cx="1340" cy="660" r="110" fill="#F6B26B" opacity=".9"/>', f'<g {PAINT}><circle cx="1340" cy="660" r="110" fill="#F7A23B"/></g>')
sub('<rect x="0" y="700" width="1600" height="200" fill="#2E2450"/>', '<rect x="0" y="700" width="1600" height="200" fill="#2E2A5E"/>')
sub('<polygon class="bd-roof" points="620,430 838,300 1056,430" fill="#7A3F5E"/>', f'<polygon class="bd-roof" points="620,430 838,300 1056,430" fill="#C9604A" {PAINT}/>')
sub("""fill="' + ((r + k) % 2 ? "#D9774B" : "#C8643A") +
        '" stroke="#8A3B1F" stroke-width="3\"""", """fill="' + ((r + k) % 2 ? "#F08A6E" : "#E8705A") +
        '" stroke="#B5503C" stroke-width="3\"""")
sub('<g class="bd-wall"><g id="bricks"></g></g>', f'<g class="bd-wall" {PAINT}><g id="bricks"></g></g>')

# the kid symbol (Mia, the tiny builder, Lily)
a = s.index('<g id="kid">'); b = s.index('</g>', a) + 4
s = s[:a] + f'''<g id="kid"><g {PAINT}>
          <rect x="-20" y="-60" width="14" height="54" rx="7" fill="#6C8BEF"/><rect x="6" y="-60" width="14" height="54" rx="7" fill="#6C8BEF"/>
          {boots(-26, 4, 2, 22)}
          <path d="M-34 -122 C-32 -132 32 -132 34 -122 L36 -58 C36 -50 -36 -50 -36 -58Z" fill="url(#gn-shirtRed)"/>
          <rect x="-8" y="-136" width="16" height="12" rx="3" fill="#E9B394"/>
          <circle cx="-35" cy="-160" r="7" fill="#F6C4A8"/><circle cx="35" cy="-160" r="7" fill="#F6C4A8"/>
          <ellipse cx="0" cy="-162" rx="36" ry="34" fill="#F6C4A8"/>
        </g>
        <circle cx="-12" cy="-156" r="4.4" fill="{INK}"/><circle cx="12" cy="-156" r="4.4" fill="{INK}"/>
        <path d="M-8 -142 Q0 -135 8 -142" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>
        {blush(-22, -146, 22, -146, 7)}
        </g>''' + s[b:]
sub('<path d="M-38 -186 a38 32 0 0 1 76 0 h10 v9 h-96 v-9 z" fill="#F2C94C"/>', f'<path d="M-38 -186 a38 32 0 0 1 76 0 h10 v9 h-96 v-9 z" fill="#FFD23F" {PAINT}/>')

# robot helpers
for i in (1, 2, 3):
    a = s.index(f'<g class="bd-rbot r{i}">') + len(f'<g class="bd-rbot r{i}">')
    b = s.index('</g></g>', a)
    s = s[:a] + f'''
          <path d="M0 -76 C-4 -84 4 -88 0 -94" stroke="#FFF1C9" stroke-width="5" fill="none" stroke-linecap="round"/>
          <circle class="bd-rlight" cx="0" cy="-98" r="8" fill="#3DBE8B"/>
          <g {PAINT}><path d="M-34 -64 C-33 -76 -12 -78 2 -78 C22 -78 36 -74 35 -62 C37 -46 37 -32 31 -24 C22 -17 -20 -17 -31 -24 C-37 -33 -37 -52 -34 -64Z" fill="#FFD23F"/>
          <circle cx="-18" cy="-12" r="11" fill="#2B2F4A"/><circle cx="18" cy="-12" r="11" fill="#2B2F4A"/></g>
          {eyes(-11, -52, 12, -55, 8, 1, -2, 3.6)}
          <path d="M-7 -36 q7 5 14 0" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>''' + s[b:]

# school
sub('<rect x="1240" y="420" width="300" height="200" rx="10" fill="#4C6FA8"/>', f'<rect x="1240" y="420" width="300" height="200" rx="10" fill="#6C8BEF" {PAINT}/>')
sub('<polygon points="1220,420 1390,330 1560,420" fill="#2F4C80"/>', f'<polygon points="1220,420 1390,330 1560,420" fill="#4B67C9" {PAINT}/>')
sub('fill="#2F4C80" font-family="Fredoka, sans-serif">SCHOOL</text>', 'fill="#4B67C9" font-family="Fredoka, sans-serif">SCHOOL</text>')

# Grandma Rosa
a = s.index('<g class="bd-gma bd-move">') + len('<g class="bd-gma bd-move">')
b = s.index('<line x1="44" y1="-100"', a)
curls = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in [(-30, -182, 14), (-16, -198, 16), (6, -204, 16), (26, -192, 15), (36, -174, 11), (-36, -164, 10), (0, -218, 13)])
s = s[:a] + f'''
        <g {PAINT}>
        <rect x="-20" y="-58" width="14" height="54" rx="7" fill="#5A4A7E"/><rect x="6" y="-58" width="14" height="54" rx="7" fill="#5A4A7E"/>
        {boots(-26, 4, 2, 22)}
        <path d="M-40 -126 C-38 -140 38 -140 40 -126 L42 -60 C42 -50 -42 -50 -42 -60Z" fill="#F48FB1"/>
        <rect x="-8" y="-140" width="16" height="12" rx="3" fill="#E9BFA2"/>
        <circle cx="-34" cy="-166" r="7" fill="#F8D2BA"/><circle cx="34" cy="-166" r="7" fill="#F8D2BA"/>
        <ellipse cx="0" cy="-168" rx="34" ry="33" fill="#F8D2BA"/>
        <g fill="#D8DBE3">{curls}</g>
        </g>
        <g fill="#FFF9EE"><circle cx="0" cy="-112" r="3.5"/><circle cx="0" cy="-96" r="3.5"/><circle cx="0" cy="-80" r="3.5"/></g>
        <g fill="none" stroke="#E8483A" stroke-width="3"><circle cx="-13" cy="-166" r="10"/><circle cx="13" cy="-166" r="10"/><path d="M-3 -166 h6"/></g>
        <circle cx="-13" cy="-166" r="3.4" fill="{INK}"/><circle cx="13" cy="-166" r="3.4" fill="{INK}"/>
        <path d="M-9 -148 Q0 -141 9 -148" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>
        {blush(-24, -152, 24, -152, 6)}
        ''' + s[b:]

# ================= Story 3: Duet =================
sub('<rect width="1600" height="900" fill="#3A3463"/>', '<rect width="1600" height="900" fill="#3A3E7E"/>')
sub('<rect x="0" y="760" width="1600" height="140" fill="#2A2448"/>', '<rect x="0" y="760" width="1600" height="140" fill="#2B2E66"/>')
sub('<rect x="900" y="600" width="340" height="26" rx="6" fill="#7A4E2D"/>', f'<rect x="900" y="600" width="340" height="26" rx="6" fill="#C4864F" {PAINT}/>')
sub('<polygon points="1410,420 1530,420 1500,340 1440,340" fill="#F2C94C"/>', f'<polygon points="1410,420 1530,420 1500,340 1440,340" fill="#FFD23F" {PAINT}/>')
sub('<rect x="652" y="162" width="116" height="86" rx="4" fill="#E07A5F"/><circle cx="710" cy="205" r="22" fill="#F2C94C"/>',
    f'<rect x="652" y="162" width="116" height="86" rx="4" fill="#F08A6E" {PAINT}/><circle cx="710" cy="205" r="22" fill="#FFD23F"/>')

# Mom
a = s.index('<g class="du-mom"><g class="du-mombody">') + len('<g class="du-mom"><g class="du-mombody">')
b = s.index('</g></g>', a)
s = s[:a] + f'''
        <g {PAINT}>
        <path d="M-40 -246 C-44 -284 40 -290 40 -246 L44 -196 C30 -190 -30 -190 -44 -196Z" fill="#4A2E22"/>
        <rect x="-22" y="-82" width="16" height="78" rx="8" fill="#2B3A67"/><rect x="6" y="-82" width="16" height="78" rx="8" fill="#2B3A67"/>
        {boots(-28, 4, 2, 24)}
        <path d="M-42 -192 C-40 -206 40 -206 42 -192 L44 -82 C44 -72 -44 -72 -44 -82Z" fill="#4FA65B"/>
        <rect x="-8" y="-208" width="16" height="14" rx="3" fill="#D99F7E"/>
        <circle cx="-34" cy="-234" r="7" fill="#E9B394"/><circle cx="34" cy="-234" r="7" fill="#E9B394"/>
        <ellipse cx="0" cy="-236" rx="33" ry="33" fill="#E9B394"/>
        <path d="M-36 -240 C-38 -274 36 -278 36 -244 C24 -256 10 -260 2 -266 C-8 -254 -22 -248 -36 -240Z" fill="#4A2E22"/>
        </g>
        <circle cx="-12" cy="-232" r="4.2" fill="{INK}"/><circle cx="12" cy="-232" r="4.2" fill="{INK}"/>
        <path d="M-9 -218 Q0 -211 9 -218" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>
        {blush(-22, -220, 22, -220, 6)}
      ''' + s[b:]

# Duet: a soft blue helper with white eyes
sub('''        <circle r="56" fill="#7FC8F8"/>
        <circle cx="44" cy="-36" r="30" fill="#F2C94C"/>
        <circle cx="-16" cy="-6" r="7" fill="#121A33"/><circle cx="16" cy="-6" r="7" fill="#121A33"/>
        <path d="M-14 16 Q0 26 14 16" stroke="#121A33" stroke-width="4" fill="none" stroke-linecap="round"/>''',
f'''        <g {PAINT}><path d="M-52 -14 C-54 -48 -20 -60 6 -58 C36 -56 58 -36 56 -4 C54 30 30 56 -2 56 C-34 56 -50 28 -52 -14Z" fill="#7FC8F8"/>
        <circle cx="44" cy="-40" r="26" fill="#FFD23F"/></g>
        {eyes(-17, -10, 17, -16, 11, 2, -2, 5)}
        <path d="M-12 16 Q0 26 12 16" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>
        {blush(-32, 8, 32, 4, 8)}''')

# ---------- paper grain on top of each stage ----------
for sid in ('st-key', 'st-build', 'st-duet'):
    a = s.index(f'id="{sid}"')
    a2, depth = a, 0
    for m in re.finditer(r'<svg\b|</svg>', s[s.rfind('<svg', 0, a):]):
        pass
    start = s.rfind('<svg', 0, a)
    depth = 0
    for m in re.finditer(r'<svg\b|</svg>', s[start:]):
        depth += 1 if m.group(0) == '<svg' else -1
        if depth == 0:
            end = start + m.start()
            break
    s = s[:end] + '  ' + GRAIN + '\n    ' + s[end:]

open(P, 'w').write(s)
print('stories restyled', len(s))
