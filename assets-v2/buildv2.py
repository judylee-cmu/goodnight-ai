import json, re
SP = '/tmp/claude-0/-home-claude/3e881c95-6cf0-56cd-aa41-2012ca221448/scratchpad/'
R = '/home/claude/gn-repo/'
c = json.load(open(SP + 'cast.json'))

defs = c['defs'] + '<radialGradient id="mglow"><stop offset="0" stop-color="#FFD23F" stop-opacity=".55"/><stop offset="1" stop-color="#FFD23F" stop-opacity="0"/></radialGradient>'
NAMES = re.findall(r'id="([A-Za-z]+)"', defs)
def pref(s):
    for n in NAMES:
        s = s.replace(f'url(#{n})', f'url(#gn-{n})').replace(f'id="{n}"', f'id="gn-{n}"')
    return s
c = {k: pref(v) for k, v in c.items()}
defs = pref(defs)
DEFS_SVG = f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>{defs}</defs></svg>'

def balanced_svg(s, start):
    """Return (start, end) of the <svg ...>...</svg> element beginning at start, honoring nesting."""
    i, depth = start, 0
    tag = re.compile(r'<svg\b|</svg>')
    for m in tag.finditer(s, start):
        depth += 1 if m.group(0) == '<svg' else -1
        if depth == 0:
            return start, m.end()
    raise ValueError('unbalanced')

def replace_svg(s, marker, new):
    i = s.index(marker)
    a, b = balanced_svg(s, i)
    return s[:a] + new + s[b:]


TAPJS = """<script>
/* Pip only blinks on his own. Tap him and he waves. */
document.addEventListener("click", function (e) {
  var t = e.target.closest("svg.pip, .card-page svg, svg.mini-pip, g.p-tap, use[href='#pip']");
  if (!t) return;
  var host = t.tagName.toLowerCase() === "use" ? t.parentNode : t;
  host.classList.remove("waving"); void host.getBoundingClientRect(); host.classList.add("waving");
  clearTimeout(host._wv); host._wv = setTimeout(function () { host.classList.remove("waving") }, 2700);
});
</script>"""


LULLJS = """<script>
/* Optional lullaby: a soft music box playing Twinkle Twinkle Little Star (traditional). Off until tapped. */
(function () {
  var btn = document.getElementById("lullaby"); if (!btn) return;
  var ctx = null, timer = null, i = 0, on = false;
  var N = { C: 523.25, D: 587.33, E: 659.25, F: 698.46, G: 783.99, A: 880 };
  var song = "C C G G A A G- F F E E D D C- G G F F E E D- G G F F E E D- C C G G A A G- F F E E D D C-".split(" ");
  function note(f, t, len) {
    [1, 2].forEach(function (h, k) {
      var o = ctx.createOscillator(), g = ctx.createGain();
      o.type = "sine"; o.frequency.value = f * h;
      g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(k ? 0.025 : 0.09, t + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, t + len + 0.9);
      o.connect(g); g.connect(ctx.destination); o.start(t); o.stop(t + len + 1);
    });
  }
  function step() {
    var n = song[i % song.length], hold = n.slice(-1) === "-", len = hold ? 0.9 : 0.45;
    note(N[n[0]], ctx.currentTime + 0.02, len); i++;
    timer = setTimeout(step, (i % song.length === 0 ? 2.2 : len + 0.05) * 1000);
  }
  btn.addEventListener("click", function () {
    on = !on; btn.setAttribute("aria-pressed", on); btn.textContent = on ? "♪ Lullaby: on" : "♪ Lullaby: off";
    if (on) { ctx = ctx || new (window.AudioContext || window.webkitAudioContext)(); ctx.resume(); i = 0; step() }
    else { clearTimeout(timer) }
  });
})();
</script>"""

# ---------------- pitch-v2 ----------------
s = open(R + 'pitch.html').read()
s = s.replace('<body>', '<body>\n' + DEFS_SVG, 1)
s = replace_svg(s, '<svg class="pip"', c['readHero'])
s = replace_svg(s, '<svg class="bed"', c['bed'])
s = replace_svg(s, '<svg role="img" aria-label="Pip the robot detective', c['detective'])
s = replace_svg(s, '<svg style="width:92px;height:108px" class="mini-pip"', c['mini'])
s = replace_svg(s, '<svg class="sleep-pip"', c['sleep'])

# Problem faces: three people, new style
fa = s.index('<div class="faces">'); fb = s.index('<p class="src">', fa)
faces = [('kid', 'A 6 year old'), ('grandma', 'Your grandma'), ('friend', 'Your non tech friend')]
html = '<div class="faces">' + ''.join(
    f'<figure class="reveal" style="--d:{i*0.12}s"><div class="face">{c[k]}<span class="bubble" style="--b:{i*0.4}s">?</span></div><figcaption>{n}</figcaption></figure>'
    for i, (k, n) in enumerate(faces)) + '</div>\n    '
s = s[:fa] + html + s[fb:]

css = '''
/* v2 cast */
.faces { grid-template-columns: repeat(3, minmax(0, 1fr)) !important; max-width: 900px; margin-left: auto; margin-right: auto }
.face { background: #FFF1DA; border-radius: 50%; overflow: visible }
.face svg { filter: none !important }
.hero .pip { width: min(100%, 380px) }
@media (max-width: 760px) { .hero .pip { width: 220px } }
.sleeper { width: 130px }
.p-arm-r.wave { transform-origin: 0% 100%; animation: var(--wave, none) !important }
.p-bob, .p-shadow, .p-glow { animation: none !important }
@keyframes wave { 0%, 100% { transform: rotate(0) } 30% { transform: rotate(22deg) } 60% { transform: rotate(-6deg) } 80% { transform: rotate(18deg) } }
.waving { --wave: wave 1.3s ease-in-out 2 }
svg.pip, .card-page svg, .who svg.bed { cursor: pointer }
/* bedtime hero */
.hero::before { content: ""; position: absolute; inset: 0; background: #070B1C; opacity: 0; animation: nightfall 40s ease-in forwards; pointer-events: none }
@keyframes nightfall { to { opacity: .45 } }
.hero .wrap { z-index: 1 }
.hero .wrap { grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr) !important }
.hero h1 { font-size: clamp(52px, 8vw, 104px) }
.hero .pip.reader { width: min(100%, 620px); justify-self: end }
@media (max-width: 760px) { .hero .wrap { grid-template-columns: 1fr !important } .hero .pip.reader { width: min(100%, 360px); justify-self: center } }
.tw circle { animation: twinkle 5s ease-in-out infinite !important }
.tw circle:nth-child(2n) { animation-delay: 1.7s !important } .tw circle:nth-child(3n) { animation-delay: 3.1s !important }
@keyframes twinkle { 0%, 100% { opacity: 1 } 50% { opacity: .2 } }
.book-glow, .lamp-glow { animation: glowbreath 4.5s ease-in-out infinite; transform-box: fill-box; transform-origin: center }
.lamp-glow { animation-delay: -2s }
@keyframes glowbreath { 50% { opacity: .65; transform: scale(.94) } }
.floaty { opacity: 0; animation: floatup 5s ease-out infinite; transform-box: fill-box; transform-origin: center }
@keyframes floatup { 0% { opacity: 0; transform: translateY(0) scale(.5) } 20% { opacity: 1 } 100% { opacity: 0; transform: translateY(-120px) scale(1) } }
.flip-page { transform-box: view-box; transform-origin: 300px 330px }
.waving .flip-page { animation: pageflip 1.1s ease-in-out }
@keyframes pageflip { 0% { transform: scaleX(1) } 50% { transform: scaleX(0) } 100% { transform: scaleX(-1) } }
.lullaby { margin-top: 14px; background: none; border: 2px solid var(--night3); color: var(--mist); font: inherit; font-weight: 700; font-size: 15px; padding: 8px 16px; border-radius: 999px; cursor: pointer; min-height: 40px }
.lullaby[aria-pressed="true"] { border-color: var(--gold); color: var(--gold) }
.lullaby:focus-visible { outline: 3px solid var(--green); outline-offset: 3px }
@media (prefers-reduced-motion: reduce) { .hero::before { animation: none; opacity: .3 } .floaty { display: none } }
@media (max-width: 860px) { .faces { grid-template-columns: repeat(3, minmax(0, 1fr)) !important } }
@media (max-width: 520px) { .faces { grid-template-columns: repeat(2, minmax(0, 1fr)) !important } }
'''
s = s.replace('</style>', css + '</style>', 1)
s = s.replace('</body>', TAPJS + LULLJS + '\n</body>', 1)
s = s.replace('<circle class="moonglow" cx="1000" cy="150" r="170" fill="url(#mgr)"/><circle cx="1000" cy="150" r="90" fill="#F2C94C"/><circle cx="1036" cy="126" r="82" fill="#1E2851"/>', '<circle class="moonglow" cx="1060" cy="110" r="120" fill="url(#mgr)"/><mask id="crescent"><rect width="1200" height="700" fill="#fff"/><circle cx="1086" cy="92" r="52" fill="#000"/></mask><g filter="url(#gn-paint)"><circle cx="1060" cy="110" r="58" fill="#FFD23F" mask="url(#crescent)"/></g>')
assert 'mask="url(#crescent)"' in s
s = s.replace('.faces { grid-template-columns: repeat(3, minmax(0, 1fr)) !important; max-width: 900px;', '.faces { grid-template-columns: repeat(3, minmax(0, 1fr)) !important; max-width: 1000px;')
s = s.replace('href="index.html"', 'href="index-v2.html"')
s = s.replace('<title>Goodnight, AI · Pitch</title>', '<title>Goodnight, AI · Pitch v2</title>')
s = s.replace('<a class="btn ghost" href="#how">See how it works</a>\n      </div>', '<a class="btn ghost" href="#how">See how it works</a>\n      </div>\n      <button type="button" class="lullaby" id="lullaby" aria-pressed="false">♪ Lullaby: off</button>', 1)
assert 'id="lullaby"' in s
# a few more stars in the hero sky
s = s.replace('<g fill="#F7F1E3" class="tw"><circle cx="120" cy="80" r="3"/>', '<g fill="#F7F1E3" class="tw"><circle cx="300" cy="200" r="2"/><circle cx="980" cy="90" r="2.5"/><circle cx="1080" cy="260" r="2"/><circle cx="860" cy="560" r="2.5"/><circle cx="240" cy="420" r="2"/><circle cx="120" cy="80" r="3"/>', 1)
open(R + 'pitch-v2.html', 'w').write(s)

# ---------------- index-v2 ----------------
t = open(R + 'index.html').read()
t = t.replace('<body>', '<body>\n' + DEFS_SVG, 1)
a = t.index('<g id="pip">'); b = t.index('</g>', a) + 4
t = t[:a] + f'<g id="pip"><g transform="translate(3 10) scale(.42)">{c["indexPip"]}</g></g>' + t[b:]
t = t.replace('href="pitch.html"', 'href="pitch-v2.html"')
t = t.replace('<title>', '<title>v2 · ', 1)
t = t.replace('</style>', '''
/* v2 Pip: blink on his own, wave when tapped */
.p-eyes { animation: pipblink 5.5s infinite; transform-box: fill-box; transform-origin: center }
@keyframes pipblink { 0%, 93%, 100% { transform: scaleY(1) } 96% { transform: scaleY(.1) } }
.p-arm-r.wave { transform-box: fill-box; transform-origin: 0% 100%; animation: var(--wave, none) }
@keyframes pipwave { 0%, 100% { transform: rotate(0) } 30% { transform: rotate(22deg) } 60% { transform: rotate(-6deg) } 80% { transform: rotate(18deg) } }
.waving { --wave: pipwave 1.3s ease-in-out 2 }
use[href="#pip"] { cursor: pointer }
@media (prefers-reduced-motion: reduce) { .p-eyes, .p-arm-r.wave { animation: none !important } }
</style>''', 1)
t = t.replace('</body>', TAPJS + '\n</body>', 1)
open(R + 'index-v2.html', 'w').write(t)
print('ok', len(s), len(t))
