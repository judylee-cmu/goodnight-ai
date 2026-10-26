"""Round of edits on pitch-v2.html (runs after buildv2.py)."""
import re
P = '/tmp/claude-0/-home-claude/3e881c95-6cf0-56cd-aa41-2012ca221448/scratchpad/build/pitch-v2.html'
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

# 11. Product section fits one screen: heading sits above the news card in the left column
sub("""    <p class="eyebrow">What’s our product</p>
    <h2>Real AI news, turned into a bedtime story</h2>
    <p class="lead">For parents and kids 5 to 10, together at bedtime.</p>
    <div class="reveal hook-row">
      <div class="card-dark news-card">""", """    <div class="reveal hook-row">
      <div class="prod-left">
      <p class="eyebrow">What’s our product</p>
      <h2>Real AI news, turned into a bedtime story</h2>
      <p class="lead">For parents and kids 5 to 10, together at bedtime.</p>
      <div class="card-dark news-card">""")
sub("""        <p class="src" style="margin-top:14px">Microsoft Security Blog, October 21, 2026</p>
      </div>""", """        <p class="src" style="margin-top:14px">Microsoft Security Blog, October 21, 2026</p>
      </div>
      </div>""")
s = s.replace('</style>', """
#product { padding-block: clamp(56px, 6vw, 80px) }
#product .hook-row { margin-top: 0; align-items: center; grid-template-columns: minmax(0, .95fr) auto minmax(0, 1.25fr) !important; gap: 24px }
#product .prod-left h2 { font-size: clamp(30px, 3.6vw, 48px) }
#product .prod-left .lead { margin-top: 12px; font-size: clamp(17px, 1.6vw, 20px) }
#product .news-card { margin-top: 24px; padding: 24px }
#product .news-card .headline { font-size: clamp(20px, 2vw, 26px) !important }
#product .fb-pages { max-height: 56vh; aspect-ratio: 16 / 9 }
#product .fb-cap { min-height: 1.4em } @media (max-width: 1100px) { #product .fb-cap { min-height: 2.6em } }
@media (max-width: 860px) { #product .hook-row { grid-template-columns: 1fr !important } }
</style>""", 1)

# 12. Cleaner "Try it live" column
sub("""      <ol class="steps"><li>1 Run the agent</li><li>2 Approve</li><li>3 Pip reads</li></ol>
      <div class="qr"><img src="assets/qr-code.png" alt="QR code linking to goodnight-ai-opal.vercel.app"><p>goodnight-ai-opal.vercel.app</p></div>
      <div class="btns"><a class="btn" href="index-v2.html">▶ Open the demo</a></div>""",
"""      <ol class="demo-steps">
        <li><b>1</b><span>Run tonight’s agent</span></li>
        <li><b>2</b><span>Approve a story</span></li>
        <li><b>3</b><span>Pip reads it to your kid</span></li>
      </ol>
      <div class="demo-cta">
        <img src="assets/qr-code.png" alt="QR code linking to goodnight-ai-opal.vercel.app">
        <div>
          <p class="cta-label">Scan or tap to try</p>
          <p class="cta-url">goodnight-ai-opal.vercel.app</p>
          <a class="btn" href="index-v2.html">▶ Open the demo</a>
        </div>
      </div>""")
s = s.replace('</style>', """
.demo-steps { list-style: none; margin: 28px 0 0; padding: 0; display: flex; flex-direction: column; gap: 14px }
.demo-steps li { display: flex; align-items: center; gap: 14px; font-size: clamp(17px, 1.6vw, 20px); font-weight: 600; color: var(--cream) }
.demo-steps b { flex: none; width: 34px; height: 34px; border-radius: 50%; background: var(--gold); color: var(--night); display: grid; place-items: center; font-family: var(--f-display); font-size: 17px }
.demo-cta { margin-top: 32px; display: flex; align-items: center; gap: 22px; background: var(--night2); border: 1px solid var(--night3); border-radius: 22px; padding: 18px; max-width: 520px }
.demo-cta img { flex: none; width: 128px; height: 128px; background: #FFF8E6; border-radius: 14px; padding: 8px }
.demo-cta > div { min-width: 0 }
.cta-label { margin: 0; font-size: 13px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--gold) }
.cta-url { margin: 6px 0 14px; font-size: 15px; color: var(--mist); white-space: nowrap; overflow: hidden; text-overflow: ellipsis }
.demo-cta .btn { padding: 11px 20px; font-size: 16px; min-height: 44px }
@media (max-width: 420px) { .demo-cta { flex-direction: column; align-items: flex-start } }
</style>""", 1)

# 13. Future work: four ideas, no dates, hand drawn icons
INKC = '#1A1A2E'
PF = 'filter="url(#gn-paint)"'
IK = 'filter="url(#gn-ink)"'
icons = {
 'voice': f"""<svg viewBox="0 0 96 96" aria-hidden="true">
   <g {PF}><rect x="34" y="14" width="26" height="42" rx="13" fill="#F48FB1"/><rect x="44" y="62" width="6" height="14" rx="3" fill="#C4864F"/><rect x="32" y="76" width="30" height="7" rx="3.5" fill="#C4864F"/></g>
   <g {IK} fill="none" stroke="{INKC}" stroke-width="3" stroke-linecap="round"><path d="M26 40 C26 56 68 56 68 40"/><path d="M40 26 h14 M40 34 h14 M40 42 h14" stroke="#FFF8E6" stroke-width="2.6"/></g>
   <g {IK} fill="none" stroke="#FFD23F" stroke-width="3.6" stroke-linecap="round"><path d="M74 28 C80 34 80 44 74 50"/><path d="M82 22 C92 32 92 46 82 56"/><path d="M20 28 C14 34 14 44 20 50"/></g></svg>""",
 'ask': f"""<svg viewBox="0 0 96 96" aria-hidden="true">
   <g {PF}><path d="M14 22 C14 14 20 10 28 10 L70 10 C78 10 84 14 84 22 L84 50 C84 58 78 62 70 62 L42 62 L26 78 L28 62 C20 62 14 58 14 50Z" fill="#6C8BEF"/>
   <circle cx="72" cy="78" r="12" fill="#FFD23F"/></g>
   <g {IK}><path d="M38 28 C38 18 60 18 60 28 C60 36 49 36 49 44" stroke="#FFF8E6" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="49" cy="53" r="3.4" fill="#FFF8E6"/></g>
   <circle cx="68" cy="77" r="1.8" fill="{INKC}"/><circle cx="76" cy="77" r="1.8" fill="{INKC}"/><path d="M68 82 q4 3 8 0" stroke="{INKC}" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg>""",
 'level': f"""<svg viewBox="0 0 96 96" aria-hidden="true">
   <g {PF}><rect x="10" y="62" width="24" height="22" rx="4" fill="#4FA65B"/><rect x="36" y="44" width="24" height="40" rx="4" fill="#F7A23B"/><rect x="62" y="24" width="24" height="60" rx="4" fill="#F08A6E"/>
   <rect x="71" y="6" width="3.5" height="20" rx="1.5" fill="#C4864F"/><path d="M74.5 7 L88 11 L74.5 16Z" fill="#FFD23F"/></g>
   <g {IK} fill="{INKC}" font-family="Fredoka, Arial, sans-serif" font-weight="600" text-anchor="middle"><text x="22" y="78" font-size="13">A</text><text x="48" y="68" font-size="12">Ab</text><text x="74" y="56" font-size="10.5">Abc</text></g></svg>""",
 'world': f"""<svg viewBox="0 0 96 96" aria-hidden="true">
   <g {PF}><rect x="8" y="14" width="64" height="46" rx="6" fill="#3A7F45"/><rect x="8" y="58" width="64" height="6" rx="3" fill="#C4864F"/>
   <circle cx="70" cy="64" r="20" fill="#7FC8F8"/><path d="M58 56 C62 52 68 56 66 62 C64 68 56 66 58 56Z M74 52 C80 50 86 56 84 62 C80 64 74 60 74 52Z M68 72 C72 70 78 74 74 80 C70 82 66 76 68 72Z" fill="#4FA65B"/></g>
   <g {IK} fill="#FFF8E6" font-family="Fredoka, Arial, sans-serif" font-weight="600" text-anchor="middle"><text x="22" y="42" font-size="18">A</text><text x="40" y="44" font-size="16">文</text><text x="56" y="40" font-size="14">あ</text></g>
   <path d="M16 50 h22" stroke="#FFF8E6" stroke-width="2.4" stroke-linecap="round" {IK}/></svg>""",
}
items = [('voice', 'A warmer, more natural voice for Pip'),
         ('ask', 'Kids ask Pip questions'),
         ('level', 'Choose your level, elementary to adult'),
         ('world', 'More languages and classroom mode')]
road = '<ol class="road road2">' + ''.join(f'<li><span class="ic2">{icons[k]}</span><span class="rt">{t}</span></li>' for k, t in items) + '</ol>'
a = s.index('<ol class="road">'); b = s.index('</ol>', a) + 5
s = s[:a] + road + s[b:]
s = s.replace('</style>', """
.road2 { grid-template-columns: repeat(4, minmax(0, 1fr)) !important; gap: 22px !important }
.road2 li { flex-direction: column !important; align-items: flex-start !important; gap: 16px !important; background: var(--night); border: 1px solid var(--night3); border-radius: 22px; padding: 22px; animation: none }
.ic2 { width: 96px; height: 96px; display: block; transition: transform .3s }
.ic2 svg { width: 100%; height: 100%; display: block; overflow: visible }
.road2 li:hover .ic2 { transform: rotate(-6deg) scale(1.05) }
.road2 .rt { font-size: clamp(17px, 1.6vw, 21px); font-weight: 600; color: var(--cream); line-height: 1.35 }
@media (max-width: 860px) { .road2 { grid-template-columns: repeat(2, minmax(0, 1fr)) !important } }
@media (max-width: 480px) { .road2 { grid-template-columns: 1fr !important } .road2 li { flex-direction: row !important; align-items: center !important } .ic2 { width: 72px; height: 72px; flex: none } }
</style>""", 1)

# 14. Calmer ending: keep the family bedtime scene only
s = re.sub(r'<mask id="crescent2">.*?</mask><g filter="url\(#gn-paint\)"><circle cx="1040" cy="120" r="80" fill="#FFD23F" mask="url\(#crescent2\)"/></g>', '', s, flags=re.S)
a = s.index('<div class="sleeper" aria-hidden="true">')
depth = 0; i = a
for m in re.finditer(r'<div\b|</div>', s[a:]):
    depth += 1 if m.group(0) == '<div' else -1
    if depth == 0:
        b = a + m.end(); break
s = s[:a] + s[b:]
sub('Goodnight, AI · by Judy Lee', 'by Goodnight, AI')
s = s.replace('</style>', """
.close .wrap { align-items: center }
.close h2 { font-size: clamp(34px, 4.6vw, 60px) !important }
</style>""", 1)

# 15. Hero eyebrow with byline
sub('<p class="eyebrow">SEM Week 1 · Agentic AI News</p>', '<p class="eyebrow">SEM Week 1 · Agentic AI News · By Judy Lee</p>')

# 16. Hand drawn wavy edges between sections, plus hanging stars
import random
def wave(seed, color):
    r = random.Random(seed)
    W, H = 1440, 48
    pts = []
    x = 0
    y = r.uniform(16, 28)
    d = f'M0 {H} L0 {y:.1f}'
    while x < W:
        nx = min(W, x + r.uniform(150, 260))
        ny = r.uniform(8, 32)
        c1x = x + (nx - x) * r.uniform(.25, .45); c1y = y + r.uniform(-14, 14)
        c2x = x + (nx - x) * r.uniform(.55, .75); c2y = ny + r.uniform(-14, 14)
        d += f' C{c1x:.1f} {c1y:.1f} {c2x:.1f} {c2y:.1f} {nx:.1f} {ny:.1f}'
        x, y = nx, ny
    d += f' L{W} {H}Z'
    return (f'<svg class="edge" viewBox="0 0 1440 48" preserveAspectRatio="none" aria-hidden="true">'
            f'<g filter="url(#gn-ink)"><path d="{d}" fill="{color}"/></g></svg>')
edges = {'problem': ('#F7F1E3', 3), 'product': ('#1C2647', 7), 'how': ('#F7F1E3', 11),
         'demo': ('#121A33', 17), 'future': ('#1C2647', 23)}
for sid, (col, seed) in edges.items():
    tag = re.search(r'<section class="[^"]*" id="%s">' % sid, s).group(0)
    s = s.replace(tag, tag + '\n  ' + wave(seed, col), 1)
# future flows down into the ending (the ending has a gradient, so the wave hangs from above)
s = s.replace('</section>\n\n<!-- 7.', wave(29, '#1C2647').replace('class="edge"', 'class="edge down"') + '\n</section>\n\n<!-- 7.', 1)
s = s.replace('<footer>', '<footer>\n  ' + wave(31, '#121A33'), 1)

def charm(x, length, kind, delay, color='#FFD23F'):
    if kind == 'star':
        shape = f'<path d="M0 {length} l5 11 12 2 -9 8 2 12 -10 -6 -10 6 2 -12 -9 -8 12 -2z" fill="{color}"/>'
    else:
        shape = f'<path d="M6 {length-2} C-12 {length+6} -12 {length+34} 8 {length+40} C-2 {length+30} -2 {length+12} 6 {length-2}Z" fill="{color}"/>'
    return (f'<g transform="translate({x} 0)"><g class="charm" style="animation-delay:{delay}s">'
            f'<path d="M0 0 L0 {length}" stroke="#B7791F" stroke-width="2" stroke-linecap="round" opacity=".7"/>'
            f'<g filter="url(#gn-paint)">{shape}</g></g></g>')
hang = ('<svg class="charms" viewBox="0 0 1440 170" preserveAspectRatio="xMidYMin slice" aria-hidden="true">'
        + charm(170, 74, 'star', 0) + charm(250, 120, 'moon', .8) + charm(322, 56, 'star', 1.6, '#F7A23B')
        + charm(1120, 96, 'star', .4, '#F7A23B') + charm(1195, 62, 'moon', 1.2) + charm(1270, 84, 'star', 2) + '</svg>')
tag = '<section class="cream" id="problem">'
s = s.replace(tag, tag + '\n  ' + hang, 1)
s = s.replace('</style>', """
#problem, #product, #how, #demo, #future, .close { position: relative }
.edge.down { top: auto; bottom: -46px; transform: scaleY(-1) }
footer { position: relative; border-top: 0 !important }
.close { z-index: 0 } #future { z-index: 1 }
.edge { position: absolute; left: 0; top: -46px; width: 100%; height: 48px; display: block; pointer-events: none; z-index: 2 }
.charms { position: absolute; left: 0; top: -40px; width: 100%; height: 170px; pointer-events: none; z-index: 3; overflow: visible }
.charm { animation: sway 5s ease-in-out infinite; transform-box: fill-box; transform-origin: 50% 0 }
@keyframes sway { 0%, 100% { transform: rotate(0) } 50% { transform: rotate(4deg) } }
@media (max-width: 760px) { .charms { display: none } }
@media (prefers-reduced-motion: reduce) { .charm { animation: none } }
</style>""", 1)

# 18. Tinker Pip invites people to see the system behind the product
import json as _json, re as _re
_c = _json.load(open('/tmp/claude-0/-home-claude/3e881c95-6cf0-56cd-aa41-2012ca221448/scratchpad/cast.json'))
_names = _re.findall(r'id="([A-Za-z]+)"', _c['defs'] + '<radialGradient id="mglow">')
_t = _c['tinker']
for _n in _names:
    _t = _t.replace(f'url(#{_n})', f'url(#gn-{_n})')
old = '<div class="reveal banner"><p>Automate where it’s safe.<br><span>Let the parent decide where it matters.</span></p></div>'
assert old in s
new = ('<div class="reveal banner"><p>Automate where it’s safe.<br><span>Let the parent decide where it matters.</span></p>'
       '<a class="tinker-link" href="system.html" aria-label="See the system behind it">'
       '<span class="tk-bubble">Curious how I’m built?<b>See the system behind it →</b></span>' + _t + '</a></div>')
s = s.replace(old, new, 1)
s = s.replace('</style>', """
.banner { display: flex; align-items: center; justify-content: space-between; gap: 24px; flex-wrap: wrap; overflow: visible }
.tinker-link { display: flex; align-items: flex-end; gap: 6px; text-decoration: none; color: var(--cream); margin: -30px -6px -26px auto }
.tinker-link svg.tinker { width: 128px; height: auto; overflow: visible; flex: none }
.banner .tk-bubble { color: #121A33 }
.tk-bubble { position: relative; background: #FFF8E6; color: #121A33; border-radius: 18px 18px 4px 18px; padding: 10px 14px; font-size: 14px; line-height: 1.35; margin-bottom: 64px; max-width: 190px }
.tk-bubble b { display: block; font-family: var(--f-display); font-weight: 600; font-size: 16px; color: #121A33 }
.tinker-link:hover .tk-bubble, .tinker-link:focus-visible .tk-bubble { background: var(--gold) }
.tinker-link:focus-visible { outline: 3px solid var(--gold); outline-offset: 6px; border-radius: 16px }
.tinker-link:hover svg.tinker .p-arm-r.wave { animation: wave 1.3s ease-in-out 1 !important }
@media (max-width: 760px) { .tinker-link { margin: 0 auto 0 0 } .tinker-link svg.tinker { width: 104px } }
</style>""", 1)

open(P, 'w').write(s)
print('v2extra ok', len(s))
