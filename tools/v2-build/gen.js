// Emits the new cast as static SVG strings (JSON) for pitch-v2.html and index-v2.html.
const fs = require('fs');
const src = fs.readFileSync(__dirname + '/eyes.html', 'utf8');
const lines = src.split('\n');
const start = lines.findIndex(l => l.startsWith("const INK"));
const end = lines.findIndex(l => l.startsWith("const fig"));
let code = lines.slice(start, end).join('\n');
let defs = src.slice(src.indexOf('<defs>') + 6, src.indexOf('</defs>'));
global.window = {};
code += `
function eyesSVG(e){
 const [lx,ly,lr,rx,ry,rr,dx,dy,pr]=e;
 return '<g class="p-eyes"><g filter="url(#ink)"><circle cx="'+lx+'" cy="'+ly+'" r="'+lr+'" fill="#FFFDF6"/><circle cx="'+rx+'" cy="'+ry+'" r="'+rr+'" fill="#FFFDF6"/></g>'+
  '<circle cx="'+(lx+dx)+'" cy="'+(ly+dy)+'" r="'+pr+'" fill="'+INK+'"/><circle cx="'+(rx+dx)+'" cy="'+(ry+dy)+'" r="'+pr+'" fill="'+INK+'"/></g>';
}
module.exports = {pip, luna, person, kid, boot, INK};`;
const m = { exports: {} };
new Function('module', 'window', code)(m, global.window);
const C = m.exports;

const A = [106,131,14,158,126,14,1,-6,5.8];
const D = [106,131,14,158,126,14,-3,-5,5.8];

function decorate(svg){
  // bob group around everything except the ground shadow, and a waving arm group
  svg = svg.replace(/(<ellipse cx="134" cy="286"[^>]*\/>)/, '$1<g class="p-bob">').replace(/<\/svg>\s*$/, '</g></svg>');
  svg = svg.replace('<path d="M192 150 C212 140 222 120 222 96" stroke="#6C8BEF" stroke-width="12" fill="none" stroke-linecap="round"/><circle cx="222" cy="88" r="8.5" fill="#6C8BEF"/>',
    '<g class="p-arm-r wave"><path d="M192 150 C212 140 222 120 222 96" stroke="#6C8BEF" stroke-width="12" fill="none" stroke-linecap="round"/><circle cx="222" cy="88" r="8.5" fill="#6C8BEF"/></g>');
  // soft glow behind the moon
  svg = svg.replace('<g filter="url(#paint)"><path d="M172 14', '<circle class="p-glow" cx="150" cy="0" r="30" fill="url(#mglow)"/><g filter="url(#paint)"><path d="M172 14');
  return svg;
}
function pipSVG(pose, eyes, attrs){
  window.EYE = eyes;
  let s = decorate(C.pip(pose));
  if (pose === 'sleep') s = s.replace(/<g fill="#FFF1C9" font-family[\s\S]*?<\/g>/, '');
  return s.replace('<svg viewBox="0 -24 270 324">', `<svg viewBox="0 -24 270 324" ${attrs||''}>`);
}
function inner(svg){ return svg.replace(/^<svg[^>]*>/, '').replace(/<\/svg>\s*$/, ''); }
const stripQ = s => s.replace(/<g filter="url\(#ink\)"><path d="M1(58 44|68 36)[\s\S]*?<\/g>/, '');

// Parent for the bedtime scene: same people style
function parent(){
  const skin = '#E9B394', hair = '#4A2E22';
  return `<svg viewBox="0 0 210 220">
  <g filter="url(#paint)">
   <path d="M44 220 C46 186 66 168 104 166 C142 168 162 186 164 220Z" fill="#4FA65B"/>
   <rect x="92" y="146" width="24" height="26" rx="4" fill="${skin}"/>
   <circle cx="56" cy="116" r="9" fill="${skin}"/><circle cx="150" cy="114" r="9" fill="${skin}"/>
   <path d="M58 104 C58 70 80 58 104 58 C130 58 150 72 150 104 C150 138 130 156 104 156 C78 156 58 138 58 104Z" fill="${skin}"/>
   <path d="M54 104 C50 62 80 46 106 46 C134 46 158 62 152 104 C146 84 126 76 112 70 C100 80 76 88 54 104Z" fill="${hair}"/>
  </g>
  <path d="M78 112 q7 6 14 0 M112 110 q7 6 14 0" stroke="${C.INK}" stroke-width="2.8" fill="none" stroke-linecap="round" filter="url(#ink)"/>
  <path d="M103 116 c-4 4 -3 8 2 8" stroke="#C97C66" stroke-width="2.2" fill="none" stroke-linecap="round"/>
  <path d="M93 132 C97 140 109 140 113 131" stroke="${C.INK}" stroke-width="2.8" fill="none" stroke-linecap="round" filter="url(#ink)"/>
  <circle cx="74" cy="128" r="8" fill="#F48FB1" opacity=".55" filter="url(#fuzz)"/><circle cx="134" cy="126" r="8" fill="#F48FB1" opacity=".55" filter="url(#fuzz)"/>
 </svg>`;
}

// Bedtime scene: parent and kid in bed, Pip on the tablet, Luna in the window.
function bed(){
  const kidS = stripQ(C.kid()).replace('<svg viewBox="0 0 210 220">', '<svg x="520" y="168" width="210" height="220" viewBox="0 0 210 220">');
  const parS = parent().replace('<svg viewBox="0 0 210 220">', '<svg x="230" y="128" width="240" height="252" viewBox="0 0 210 220">');
  window.EYE = A;
  const tabPip = inner(C.pip('wave'));
  return `<svg class="bed" role="img" aria-label="A parent and child in bed watching Pip on a tablet, with a sleepy moon in the window" viewBox="0 0 960 560">
  <rect width="960" height="560" rx="32" fill="#1F2F6B"/>
  <g fill="#FFF1C9"><circle cx="90" cy="70" r="3"/><circle cx="280" cy="44" r="2.5"/><circle cx="520" cy="80" r="3"/><circle cx="430" cy="140" r="2"/></g>
  <g filter="url(#paint)"><rect x="690" y="44" width="210" height="160" rx="18" fill="#2B3F86"/></g>
  <path d="M795 44 V204 M690 124 H900" stroke="#1F2F6B" stroke-width="8"/>
  <svg x="720" y="40" width="150" height="170" viewBox="0 -24 270 324">${inner(C.luna()).replace(/<ellipse cx="134" cy="286"[^>]*\/>/, '')}</svg>
  <g filter="url(#paint)">
   <path d="M90 228 C92 182 140 170 200 172 L760 168 C820 168 868 184 870 230 L870 300 L90 300Z" fill="#F08A6E"/>
   <rect x="250" y="250" width="200" height="70" rx="34" fill="#FFF1C9"/><rect x="520" y="262" width="200" height="66" rx="32" fill="#FFF1C9"/>
  </g>
  ${parS}${kidS}
  <g filter="url(#paint)">
   <path d="M70 352 C200 330 420 344 520 336 C640 328 800 330 892 350 L900 520 C700 540 260 540 62 520Z" fill="url(#dotCream)"/>
   <path d="M62 506 C260 526 700 526 900 506 L900 530 C700 548 260 548 62 530Z" fill="#F7A23B"/>
  </g>
  <g filter="url(#paint)"><rect x="410" y="300" width="150" height="104" rx="14" fill="#2B2F3A" transform="rotate(-3 485 352)"/></g>
  <rect x="420" y="310" width="130" height="84" rx="8" fill="#16204A" transform="rotate(-3 485 352)"/>
  <svg x="452" y="306" width="66" height="80" viewBox="0 -24 270 324">${tabPip}</svg>
  <path d="M342 330 C370 344 396 346 414 342 M600 340 C584 352 566 358 552 356" stroke="#E9B394" stroke-width="16" fill="none" stroke-linecap="round" filter="url(#paint)"/>
 </svg>`;
}

// Detective card for the product section
function detective(){
  const p = pipSVG('detective', A, '').replace('<svg viewBox="0 -24 270 324" >', '<svg x="210" y="-6" width="250" height="300" viewBox="0 -24 270 324">');
  return `<svg role="img" aria-label="Pip the robot detective holding a magnifying glass next to a doctor’s clipboard" viewBox="0 0 480 300" style="width:100%;max-width:400px;height:auto;overflow:visible">
  <g filter="url(#paint)" transform="rotate(-6 100 180)"><rect x="40" y="100" width="110" height="150" rx="14" fill="#C4864F"/><rect x="52" y="116" width="86" height="124" rx="8" fill="#FFFCF5"/><rect x="74" y="90" width="42" height="20" rx="7" fill="#9AA6C4"/>
  <rect x="85" y="134" width="20" height="46" rx="4" fill="#4FA65B"/><rect x="72" y="147" width="46" height="20" rx="4" fill="#4FA65B"/>
  <path d="M66 198 h58 M66 212 h40 M66 224 h50" stroke="#E6DCC4" stroke-width="5" stroke-linecap="round"/></g>
  ${p}
 </svg>`;
}


// Hero: Pip tucked into bed, leaning on a pillow, reading a glowing storybook.
function readHero(){
  window.EYE = [106,131,14,158,126,14,0,4,5.8];
  let pip = inner(C.pip('stand')).replace(/<ellipse cx="134" cy="286"[^>]*\/>/, '');
  const BX = 300;                       // book center
  const L = `M${BX} 300 C${BX-28} 286 ${BX-66} 286 ${BX-98} 296 L${BX-104} 360 C${BX-72} 350 ${BX-32} 350 ${BX} 364Z`;
  const R = `M${BX} 300 C${BX+28} 286 ${BX+66} 286 ${BX+98} 296 L${BX+104} 360 C${BX+72} 350 ${BX+32} 350 ${BX} 364Z`;
  const floaters = [[196,286,0,'#FFD23F'],[404,282,1.4,'#FFF1C9'],[214,274,2.6,'#F48FB1'],[388,290,3.6,'#FFD23F']]
    .map(([x,y,d,c]) => `<path class="floaty" style="animation-delay:${d}s" d="M${x} ${y} l3 7 7 3 -7 3 -3 7 -3 -7 -7 -3 7 -3z" fill="${c}"/>`).join('');
  return `<svg viewBox="0 0 640 500" class="pip reader" role="img" aria-label="Pip, a small blue robot, tucked into bed under a blanket, reading a glowing storybook next to a night lamp">
  <defs>
   <radialGradient id="bookglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFE08A" stop-opacity=".75"/><stop offset=".45" stop-color="#FFD23F" stop-opacity=".2"/><stop offset="1" stop-color="#FFD23F" stop-opacity="0"/></radialGradient>
   <radialGradient id="lampglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFD9A0" stop-opacity=".6"/><stop offset="1" stop-color="#FFD9A0" stop-opacity="0"/></radialGradient>
  </defs>
  <circle class="lamp-glow" cx="572" cy="250" r="130" fill="url(#lampglow)"/>
  <circle class="book-glow" cx="${BX}" cy="300" r="240" fill="url(#bookglow)"/>
  <g filter="url(#paint)">
   <!-- headboard -->
   <path d="M150 330 L150 140 C150 96 200 84 300 84 C400 84 450 96 450 140 L450 330Z" fill="#C4864F"/>
   <path d="M174 330 L174 152 C174 118 214 110 300 110 C386 110 426 118 426 152 L426 330Z" fill="#D99A5E"/>
   <!-- pillow -->
   <path d="M188 240 C182 196 230 184 300 186 C372 184 420 196 414 240 C420 278 372 290 300 288 C230 290 182 278 188 240Z" fill="#FFF8E6"/>
   <!-- nightstand + lamp -->
   <rect x="524" y="352" width="96" height="104" rx="10" fill="#7A4E2D"/><rect x="536" y="396" width="72" height="8" rx="4" fill="#5A3A22"/>
   <path d="M572 352 C570 320 574 300 572 280" stroke="#FFF1C9" stroke-width="7" fill="none" stroke-linecap="round"/>
   <path d="M536 284 C540 248 552 230 572 228 C592 230 604 248 608 284Z" fill="#FFD23F"/>
  </g>
  <circle cx="572" cy="288" r="9" fill="#FFF8E6"/>
  <!-- Pip leaning back on the pillow -->
  <g transform="rotate(-4 300 330)"><svg x="185" y="112" width="230" height="276" viewBox="0 -24 270 324" overflow="visible">${pip}</svg></g>
  <g filter="url(#paint)">
   <!-- blanket over Pip, with a folded cream edge -->
   <path d="M120 330 C150 312 220 318 300 314 C380 318 450 312 480 330 L500 452 C400 470 200 470 100 452Z" fill="url(#dotPink)"/>
   <path d="M118 332 C160 314 230 320 300 316 C372 320 442 314 482 332 L486 352 C440 336 372 342 300 338 C228 342 160 336 114 352Z" fill="#FFF1C9"/>
   <!-- bed frame -->
   <rect x="92" y="446" width="416" height="26" rx="10" fill="#C4864F"/>
   <rect x="104" y="468" width="20" height="26" rx="5" fill="#7A4E2D"/><rect x="476" y="468" width="20" height="26" rx="5" fill="#7A4E2D"/>
   <!-- book resting on the blanket -->
   <path d="M${BX} 306 C${BX-30} 292 ${BX-70} 292 ${BX-108} 302 L${BX-114} 372 C${BX-76} 362 ${BX-34} 362 ${BX} 378 C${BX+34} 362 ${BX+76} 362 ${BX+114} 372 L${BX+108} 302 C${BX+70} 292 ${BX+30} 292 ${BX} 306Z" fill="#E8483A"/>
   <path d="${L}" fill="#FFF8E6"/><path d="${R}" fill="#FFF8E6"/>
  </g>
  <g stroke="#D9C9A6" stroke-width="3.5" stroke-linecap="round"><path d="M${BX-86} 312 q36 -9 72 -2 M${BX-86} 326 q34 -8 70 -1 M${BX-84} 340 q32 -7 66 0"/><path d="M${BX+14} 310 q36 -8 72 1 M${BX+16} 324 q34 -7 70 2 M${BX+18} 338 q30 -6 64 2"/></g>
  <path class="flip-page" d="${R}" fill="#FFF1D6"/>
  <path d="M${BX} 300 V364" stroke="#D9C9A6" stroke-width="3"/>
  <!-- little hands holding the book -->
  <circle cx="${BX-108}" cy="330" r="11" fill="#6C8BEF"/><circle cx="${BX+108}" cy="330" r="11" fill="#6C8BEF"/>
  
 </svg>`;
}

const out = {
  readHero: readHero(),
  defs,
  hero: pipSVG('wave', D, 'class="pip" role="img" aria-label="Pip, a small blue robot with a moon antenna, waving"'),
  mini: pipSVG('stand', D, 'class="mini-pip" aria-hidden="true" style="width:96px;height:116px;overflow:visible"'),
  sleep: pipSVG('sleep', A, 'class="sleep-pip" aria-hidden="true"'),
  detective: detective(),
  bed: bed(),
  kid: stripQ(C.kid()),
  grandma: stripQ(C.person('grandma')),
  friend: stripQ(C.person('mom')),
  luna: C.luna(),
  indexPip: inner(pipSVG('wave', A, '')),
};
fs.writeFileSync(__dirname + '/cast.json', JSON.stringify(out));
console.log(Object.keys(out).map(k => k + ':' + out[k].length).join(' '));
