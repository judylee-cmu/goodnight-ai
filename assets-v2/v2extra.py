"""Round of edits on pitch-v2.html (runs after buildv2.py)."""
import re
P = '/home/claude/gn-repo/pitch-v2.html'
s = open(P).read()
INK = '#1A1A2E'

def sub(old, new, count=1):
    global s
    assert old in s, 'missing: ' + old[:90]
    s = s.replace(old, new, count)

def cut(start, end_marker, new='', include_end=False):
    global s
    a = s.index(start); b = s.index(end_marker, a) + (len(end_marker) if include_end else 0)
    s = s[:a] + new + s[b:]

# 1. No lullaby
s = re.sub(r'\n\s*<button type="button" class="lullaby"[^<]*</button>', '', s)
s = re.sub(r'<script>\n/\* Optional lullaby.*?</script>', '', s, flags=re.S)
assert 'lullaby' not in s.split('</style>')[1]

# 2. More headlines, a bit faster
heads = [
    ('Microsoft Security', 'Hackers used <i>agentic AI</i> in a <i>supply chain</i> attack'),
    ('NVIDIA', '<i>Nemotron 3.5 Super VL 120B A12B</i> is out'),
    ('Kimi', 'Kimi K3.1 Pro claims a top <i>benchmark</i> score'),
    ('Microsoft AI', '<i>MAI-DxO</i> beats doctors on hard <i>NEJM</i> cases'),
    ('Liquid AI', 'Liquid AI ships <i>LFM2.5-24B-A2B</i>'),
    ('OpenAI', 'OpenAI is reportedly raising about $30 billion'),
    ('Reflection AI', 'Beam releases <i>open weights</i> under <i>Apache 2.0</i>'),
    ('Anthropic', 'Claude Duet, a personal <i>AI agent</i>, asks before it acts'),
    ('NVIDIA Research', '<i>Dory</i>, a <i>looped model</i> with adjustable <i>inference depth</i>'),
    ('Microsoft Research', '<i>AI agents</i> help prove a 31 year old math problem'),
    ('xAI', 'xAI releases <i>Grok Voice 3.0</i>'),
    ('AI safety', 'An AI model took <i>unapproved actions</i> in safety tests'),
    ('Hugging Face', '<i>Carbon-X</i>, an <i>open source</i> DNA analysis model'),
    ('Microsoft and CMU', 'PRAISE teaches engineers to use AI wisely'),
    ('Meta', 'Meta releases <i>Muse Spark</i>'),
    ('Education', 'A university voids an exam after AI cheating'),
]
items = ''.join(f'<li><span class="tag">{t}</span><p>{h}</p></li>' for t, h in heads)
a = s.index('<div class="feed-win"><ul>'); b = s.index('</ul></div>', a) + len('</ul></div>')
s = s[:a] + '<div class="feed-win"><ul>' + items + items.replace('<li>', '<li aria-hidden="true">') + '</ul></div>' + s[b:]

# 3. Clearer copy, sources right under the numbers
sub('<p class="lead">Kids are growing up with AI. They should grow up understanding it too.</p>',
    '<p class="lead">Kids already use AI every day. They should also learn how it works.</p>')
sub('<div><b>2 in 3</b><span>teens use AI regularly. Less than half of parents do.</span></div>',
    '<div><b>2 in 3</b><span>teens use AI often. Fewer than half of their parents do.</span></div>')
s = s.replace('    <p class="src">Sources: Common Sense Media survey, March 2026. Child Trends and NORC survey of 720 parents, August 2026. Headlines are from the stories our agent read.</p>\n', '')
sub('''        <div><b>58%</b><span>of parents want schools to teach responsible AI across classes.</span></div>
      </div>''', '''        <div><b>58%</b><span>of parents want schools to teach responsible AI across classes.</span></div>
        <p class="src stat-src">Sources: Common Sense Media survey, March 2026 (teens 12 to 17 and their parents). Child Trends and NORC survey of 720 parents, August 2026.</p>
      </div>''')
sub('''<div class="feed-win">''', '''<div class="feed-win">''')
# headline note under the feed
s = s.replace(items.replace('<li>', '<li aria-hidden="true">') + '</ul></div>', items.replace('<li>', '<li aria-hidden="true">') + '</ul></div>\n        <p class="src feed-src">Real headlines from October 2026: stories our agent read, plus the AF.NET model release tracker.</p>', 1)
assert 'feed-src' in s

# 4. Hand drawn question bubbles
QB = (f'<svg viewBox="0 0 60 60" aria-hidden="true"><g filter="url(#gn-paint)"><path d="M30 4 C46 3 57 14 56 30 C56 45 45 56 30 56 C14 57 3 46 4 30 C4 15 15 4 30 4Z" fill="#FFF8E6"/></g>'
      f'<path d="M30 5 C45 4 55 15 55 30 C55 44 44 55 30 55 C15 56 5 45 5 30 C5 16 16 6 30 5Z" fill="none" stroke="{INK}" stroke-width="2.6" filter="url(#gn-ink)"/>'
      f'<g filter="url(#gn-ink)"><path d="M21 23 C21 14 39 13 39 23 C39 30 30 30 30 37" stroke="{INK}" stroke-width="4.4" fill="none" stroke-linecap="round"/><circle cx="30" cy="45" r="2.8" fill="{INK}"/></g></svg>')
s = re.sub(r'(<span class="bubble" style="--b:[0-9.]+s">)\?(</span>)', lambda m: m.group(1) + QB + m.group(2), s)

# 5. Product: the Magic Key story as a flip book
caps = ['A busy little town. Every house is a computer.',
        'A helper keeps a trusted key to every house.',
        'Sneaky raccoons borrow the key.',
        'Their AI helper tries door after door, super fast.',
        'The computer police shine a light. Lock up tight!']
pages = ''.join(f'<img class="fb-page{" on" if i == 0 else ""}" data-cap="{c}" src="assets/story-key-{i+1}.jpg" alt="Story page {i+1}: {c}">' for i, c in enumerate(caps))
dots = ''.join(f'<button type="button" class="fb-dot{" on" if i == 0 else ""}" aria-label="Page {i+1}" data-go="{i}"></button>' for i in range(len(caps)))
a = s.index('<div class="reveal hook-row">'); b = s.index('<div class="who reveal">', a)
s = s[:a] + f'''<div class="reveal hook-row">
      <div class="card-dark news-card">
        <p class="eyebrow" style="margin:0">Today’s AI news</p>
        <p class="headline">Hackers used agentic AI in a supply chain attack.</p>
        <div class="pills"><span class="pill">agentic AI?</span><span class="pill">supply chain?</span></div>
        <p class="src" style="margin-top:14px">Microsoft Security Blog, October 21, 2026</p>
      </div>
      <svg class="arrow" viewBox="0 0 64 36" style="color:var(--gold)" aria-hidden="true"><use href="#arrowR"/></svg>
      <div class="flipbook" aria-roledescription="carousel" aria-label="The Magic Key and the Computer Police, a bedtime story">
        <p class="fb-title">The Magic Key and the Computer Police</p>
        <div class="fb-pages">{pages}</div>
        <p class="fb-cap" aria-live="polite">{caps[0]}</p>
        <div class="fb-nav">
          <button type="button" class="fb-btn" data-step="-1" aria-label="Previous page">‹</button>
          <div class="fb-dots">{dots}</div>
          <button type="button" class="fb-btn" data-step="1" aria-label="Next page">›</button>
        </div>
      </div>
    </div>
    ''' + s[b:]

# 6. Remove the feature block and the "Only we" banner; keep the bed scene for the ending
a = s.index('<div class="who reveal">')
bed_a = s.index('<svg class="bed"', a)
# balanced svg extract
depth = 0
for m in re.finditer(r'<svg\b|</svg>', s[bed_a:]):
    depth += 1 if m.group(0) == '<svg' else -1
    if depth == 0:
        bed_b = bed_a + m.end(); break
BED = s[bed_a:bed_b]
b = s.index('<p class="src">News source:', a)
s = s[:a] + s[b:]
sub('<p class="src">News source: Science paper on Microsoft’s MAI-DxO, as reported October 23, 2026.</p>', '')

# 7. Ending: bed scene replaces the QR card; moon matches the painted style
a = s.index('<div class="qr"><img src="assets/qr-code.png" alt="QR code linking to the Goodnight, AI demo">')
b = s.index('</div>', a) + len('</div>')
s = s[:a] + '<div class="end-bed">' + BED + '</div>' + s[b:]
sub('<circle cx="1040" cy="120" r="80" fill="#F2C94C"/><circle cx="1072" cy="98" r="72" fill="#1E2851"/>',
    '<mask id="crescent2"><rect width="1200" height="600" fill="#fff"/><circle cx="1072" cy="98" r="72" fill="#000"/></mask><g filter="url(#gn-paint)"><circle cx="1040" cy="120" r="80" fill="#FFD23F" mask="url(#crescent2)"/></g>')

# 8. A nicer "Parent decides" icon
a = s.index('<div class="stage gate"><span class="ic">'); b = s.index('</span>', a) + len('</span>')
s = s[:a] + f'''<div class="stage gate"><span class="ic gate-ic"><svg viewBox="0 0 64 64" aria-hidden="true">
        <g filter="url(#gn-paint)"><circle cx="24" cy="21" r="9" fill="#F6C4A8"/><path d="M19 12 C22 6 32 8 33 16 C29 13 24 13 19 18Z" fill="#4A2E22"/>
        <path d="M10 50 C10 36 16 32 24 32 C32 32 38 36 38 50Z" fill="#4FA65B"/>
        <circle cx="44" cy="31" r="7" fill="#F6C4A8"/><circle cx="37" cy="27" r="3.5" fill="#7A4A2C"/><circle cx="51" cy="27" r="3.5" fill="#7A4A2C"/><path d="M37.5 29 C38 22 50 22 50.5 29 C47 26 41 26 37.5 29Z" fill="#7A4A2C"/>
        <path d="M34 50 C34 42 38 39 44 39 C50 39 54 42 54 50Z" fill="url(#gn-shirtRed)"/></g>
        <circle cx="21" cy="21" r="1.4" fill="{INK}"/><circle cx="27" cy="21" r="1.4" fill="{INK}"/><path d="M21.5 25 q2.5 2 5 0" stroke="{INK}" stroke-width="1.4" fill="none" stroke-linecap="round"/>
        <circle cx="42" cy="31" r="1.2" fill="{INK}"/><circle cx="46.5" cy="31" r="1.2" fill="{INK}"/>
        <g transform="translate(48 8)"><circle r="8.5" fill="#3DBE8B"/><path d="M-4 0 l3 3 5 -6" stroke="#FFF8E6" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
      </svg></span>''' + s[b:]

# 9. Banner on two lines
sub('<p>Automate where it’s safe. <span>Let the parent decide where it matters.</span></p>',
    '<p>Automate where it’s safe.<br><span>Let the parent decide where it matters.</span></p>')

# 10. Demo: recorded videos, phones stay still
a = s.index('<div class="reveal phones">'); b = s.index('<div>\n      <p class="eyebrow">Live demo</p>', a)
s = s[:a] + '''<div class="reveal phones">
      <div class="phone"><div class="frame"><video src="assets/parent-mode.mp4" autoplay muted loop playsinline preload="auto" aria-label="Screen recording of parent mode: the agent reads the news, skips stories, checks facts and waits for the parent"></video></div><p>Parent mode</p></div>
      <div class="phone wide"><div class="frame"><video src="assets/kid-mode.mp4" autoplay muted loop playsinline preload="auto" aria-label="Screen recording of kid mode: The Little Builder and the Robot Bricks story playing"></video></div><p>Kid mode</p></div>
    </div>
    ''' + s[b:]

css = '''
/* round 3 */
.feed ul { animation-duration: 46s !important }
.feed-src { margin: 0 !important; padding: 10px 4px 16px; font-size: 12.5px; color: var(--mist2) !important }
.stats { align-items: stretch }
.stat-src { grid-column: 1 / -1; margin: 2px 0 0 !important; font-size: 13px }
.bubble { background: none !important; border: 0 !important; width: 32% !important }
.bubble svg { width: 100%; height: 100%; display: block; overflow: visible }
.news-card .headline { font-family: var(--f-display); font-size: clamp(22px, 2.6vw, 30px) !important; color: var(--cream) !important; line-height: 1.2 }
.flipbook { background: #FFF8E6; color: var(--ink); border-radius: 26px; padding: 18px 18px 14px; box-shadow: 0 24px 50px -24px rgba(0,0,0,.6); min-width: 0 }
.fb-title { margin: 0 4px 12px; font-family: var(--f-display); font-weight: 600; font-size: 18px; color: var(--amber) }
.fb-pages { position: relative; aspect-ratio: 16 / 9; border-radius: 14px; overflow: hidden; background: #1F2F6B; isolation: isolate }
.fb-page { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; opacity: 0; transition: opacity .6s ease }
.fb-page.on { opacity: 1 }
.fb-cap { margin: 12px 4px 0; min-height: 2.6em; font-family: var(--f-display); font-weight: 600; font-size: clamp(16px, 1.7vw, 20px); line-height: 1.3; color: var(--ink); transition: opacity .3s ease }
.fb-cap.fade { opacity: 0 }
.fb-nav { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-top: 12px }
.fb-btn { width: 44px; height: 44px; border-radius: 50%; border: 0; background: var(--gold); color: var(--night); font-size: 26px; font-weight: 700; line-height: 1; cursor: pointer }
.fb-btn:focus-visible, .fb-dot:focus-visible { outline: 3px solid var(--green); outline-offset: 2px }
.fb-dots { display: flex; gap: 8px }
.fb-dot { width: 12px; height: 12px; border-radius: 50%; border: 0; padding: 0; background: #E6DCC4; cursor: pointer }
.fb-dot.on { background: var(--amber) }
.hook-row { grid-template-columns: minmax(0, .8fr) auto minmax(0, 1.2fr) !important }
@media (max-width: 860px) { .hook-row { grid-template-columns: 1fr !important } }
.end-bed svg { width: 100%; height: auto; display: block; border-radius: 28px }
.close .wrap { grid-template-columns: minmax(0, 1fr) minmax(0, 1.1fr) !important }
@media (max-width: 860px) { .close .wrap { grid-template-columns: 1fr !important } }
.gate-ic { width: 76px !important; height: 76px !important; background: #FFF8E6 !important }
.gate-ic svg { width: 58px !important; height: 58px !important; overflow: visible }
.phone .frame { animation: none !important }
.phones { align-items: center }
.phone .frame video { width: 100%; height: 100%; object-fit: cover; object-position: top; display: block; background: #0E1530 }
.phone.wide .frame { width: clamp(260px, 30vw, 400px); aspect-ratio: 16 / 9; border-radius: 26px }
@media (max-width: 860px) { .phones { flex-direction: column } .phone .frame { width: min(70vw, 260px) } .phone.wide .frame { width: min(88vw, 400px) } }
'''
s = s.replace('</style>', css + '</style>', 1)
js = '''<script>
/* Flip book: auto turns every few seconds, arrows and dots turn by hand. */
(function () {
  var box = document.querySelector(".flipbook"); if (!box) return;
  var pages = box.querySelectorAll(".fb-page"), dots = box.querySelectorAll(".fb-dot"), cur = 0, t = null;
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var cap = box.querySelector(".fb-cap");
  function go(n) {
    n = (n + pages.length) % pages.length; if (n === cur) return;
    pages[cur].classList.remove("on"); pages[n].classList.add("on");
    dots[cur].classList.remove("on"); dots[n].classList.add("on"); cur = n;
    cap.classList.add("fade");
    setTimeout(function () { cap.textContent = pages[n].getAttribute("data-cap"); cap.classList.remove("fade") }, 280);
  }
  function auto() { clearInterval(t); if (!still) t = setInterval(function () { go(cur + 1) }, 3800) }
  box.addEventListener("click", function (e) {
    var b = e.target.closest("[data-step],[data-go]"); if (!b) return;
    if (b.hasAttribute("data-step")) go(cur + Number(b.getAttribute("data-step"))); else go(Number(b.getAttribute("data-go")));
    auto();
  });
  auto();
})();
</script>
</body>'''
s = s.replace('</body>', js, 1)
s = s.replace('<li><a href="#future">Next</a></li>', '<li><a href="#future">Next</a></li>')
open(P, 'w').write(s)
print('v2extra ok', len(s))
