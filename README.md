# Goodnight, AI

AI news your whole family can understand, one bedtime story at a time.

Goodnight, AI is a prototype of an agentic AI news service for non tech parents and kids aged 5 to 10. Each night an AI agent picks real AI news, checks it against sources, rewrites it as a narrated picture story, and sorts it by risk. The parent is the editor: low risk stories share automatically, the rest wait for the parent to approve, revise or skip.

Built for SEM Week 1 (Option 2: Agentic AI News Portal).

## Try it

Visit https://goodnight-ai-opal.vercel.app or open the files in a browser.

- `index.html`: the one page pitch
- `demo.html`: the interactive demo (the QR code points to `/demo`)
- `system.html`: the system architecture
- `tools/v2-build/`: the scripts that generate the pages

1. **For parents:** tap "Run tonight's agent" to watch the agent's steps, see which stories it skipped and why, and approve, revise or skip each story.
2. **For kids:** only stories the parent shared appear. Tap "Start the story" and Pip reads it out loud.

## How the prototype works

Static pages, no server. The pages are plain HTML, CSS and JavaScript.

- **Story data:** each story is a JavaScript object with its lines, the scene for each line, and a note for parents.
- **Animation:** each story is an inline SVG. The page adds scene classes to the SVG, and CSS transitions and keyframes animate the characters.
- **Narration:** the browser's built in Web Speech API reads each line.
- **Agent run:** the agent's steps, skipped stories and story cards are a prerecorded replay of a real run, labeled as such on the page. A live version would run each step with an AI model.
- **Parent approval:** the kid view shows only stories with a "shared" state set by the parent view or by the green risk rule.

## News sources used in the stories

- Microsoft Security Blog, October 21, 2026: Storm-0940 and the ConnectWise supply chain compromise
- Microsoft Command Line, October 15, 2026: PRAISE, a preceptorship program with Carnegie Mellon University
- CBS News, October 23, 2026: Anthropic previews Claude Duet
