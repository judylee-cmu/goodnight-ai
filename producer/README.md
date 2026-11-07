# Producer (SEM 49772 team project)

Working folder for the Producer component. This lives here temporarily because
the Claude GitHub App is not installed on the `sem-baby-cmu` org yet. Once it is,
this folder moves to `sem-baby-cmu/goodnight-ai-news/producer/`.

Owner: Judy Lee. Pair: Madhuri Dusad.

Turns a Storyteller script into a finished bedtime story: one illustration per
page with a consistent character, warm narration with word-level timestamps,
and a packaged story file.

## Layout

- `input/` — Storyteller scripts used as test input
- `images/` — image generation test (P1, P2)
- `voice/` — text to speech test (P3, P4)
- `package/` — packaging and sync test (P5, P6, P7, P8)
- `results/` — logs, scores, cost and timing

## Status

| Test | What it needs | State |
| :-- | :-- | :-- |
| P1, P2 images | `OPENAI_API_KEY` / `GEMINI_API_KEY` | script ready, not run |
| P3, P4 voice | `OPENAI_API_KEY` / `ELEVENLABS_API_KEY` / `GEMINI_API_KEY` | script ready, not run |
| P5, P6, P7 packaging | nothing | **run, passes with placeholders** |
| P8 vertical reel | ffmpeg | **run, 1080x1920, 64s, 0.5 MB** |

## How to run

```bash
pip install openai google-genai elevenlabs
export OPENAI_API_KEY=...  ELEVENLABS_API_KEY=...  GEMINI_API_KEY=...

python images/generate.py   --script input/pip_helper_school.json --age 5to7
python voice/synthesize.py  --script input/pip_helper_school.json --age 5to7 --per-page
python package/build_story.py --script input/pip_helper_school.json --age 5to7
python package/build_reel.py  --script input/pip_helper_school.json --age 5to7
```

Then open `results/contact_sheet.html` (P1, P2), `results/voice_scoring.html`
(P3, P4) and `results/story_5to7.html` on a phone (P5, P6, P7).

The packaging step runs with no keys at all: missing images become a placeholder
and missing audio falls back to tap to advance, so the sync and interaction
logic can be checked before any API is wired up.

## Two outputs, one pipeline

The same script, images and narration feed two targets:

| Target | File | Why |
| :-- | :-- | :-- |
| In app bedtime story | `results/story_<age>.html` | narration, word highlight, tap interaction, parent approval |
| Threads / Instagram | `results/reel_<age>.mp4` | 1080x1920 H.264 + AAC, captions burned in, under 90s |

The reel is the free entry point: parents find it in a feed, the app is where
the full bedtime experience lives. Threads and Instagram are 13+, so the
audience there is parents, never the child.

## Why SVG scenes instead of generated images

The prototype does not use image generation. It hand-draws flat vector scenes
with a paper-grain filter (`feTurbulence` + `feDisplacementMap`), which is why
the character looks identical on every page and the palette never drifts.

`scene/parts.py` rebuilds that language as something a script can assemble:
sky gradient per tone, deterministic star field, moon, skyline, ground, and Pip
with breathing, blinking and a mood-driven antenna tilt. `scene/render.py`
rasterises with headless Chromium (cairosvg cannot do the filter), and
`scene/frames.py` samples one animation cycle for video.

Every animation shares a 2.0s period, so 24 frames at 12fps cover a full cycle
and ffmpeg can repeat them for any page length with no visible seam.

This makes P1 and P2 pass by construction rather than by luck:

| Test | Generated images | SVG scenes |
| :-- | :-- | :-- |
| P1 kid safe, one style | needs human review every run | guaranteed, nothing is sampled |
| P2 character consistent | the hard problem, needs seeds or references | identical by definition |
| Cost per story | about $0.30 to $0.50 | $0 |
| Time per story | minutes | 54s of rendering |

The image generation path in `images/generate.py` is kept, because a feasibility
report should show what was compared, not only what was chosen.

## Landscape flipbook

`package/build_book.py` is the phone reading experience: hold the phone
sideways, swipe left and right to turn pages. Portrait shows a rotate prompt.

Scenes are **inline SVG, not images**. All ten are mounted once at load and
cross-faded, so turning a page never re-runs the paper-grain filter, which is
the slow part on a phone. The whole book is 94 KB.

| | PNG per page | inline SVG |
| :-- | :-- | :-- |
| File size, 10 pages | 16 MB | 94 KB |
| Sharpness | fixed raster | vector, any screen |
| Still animating while reading | no | yes |

Pip is one `parts.pip()` component across all ten pages. Only x, scale and mood
change. There is no per-page redraw, so the character cannot drift: P2 is a
property of the build, not a test result.

## Carousel cards (Threads / Instagram)

`package/build_carousel.py` writes one 1080x1350 card per page, plus a
swipeable HTML preview. 4:5 is the tallest ratio a feed shows without cropping.

Format follows what works on Threads: a big headline, the character acting it
out, nothing else competing for attention.

- Headline size is picked by fitting, not by guessing. The builder tries 78px
  down to 40px and takes the largest that fits the box whole, then asserts every
  word of the page reached the card. A cut-off sentence is worse than a small one.
- `scene/pip.py` is Pip as one posable component: 8 poses (stand, point, wave,
  cheer, think, peek, read, sleep) x 5 moods (eye glow, antenna tilt, eye
  squash). A page picks a pose by its slot. The body, beak, eyes and antenna
  come from the same code every time.

| | reference feed comics | these cards |
| :-- | :-- | :-- |
| Character | drawn per panel by hand | one component, posed |
| Consistency | the artist's skill | structural |
| New page | hours | seconds |
