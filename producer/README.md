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
