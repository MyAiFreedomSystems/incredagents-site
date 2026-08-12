---
name: graphics
description: Canonical graphics skill. One entry point for every visual asset the user generates — graphics, images, infographics, banners, slides, diagrams, logos, mockups, posters. Eight curated styles A through H with example-led picker, ASK-FIRST discipline, and the safe pipeline guarantees. Triggers on graphics, image, infographic, banner, slide, diagram, logo, mockup, poster, generate an image, render, design a, make a picture of, "remake this slide", visual asset.
triggers:
  - graphics, image, infographic, banner, slide, diagram, logo, mockup, poster
  - generate an image, render an image, build a mockup, design a, make me a picture of
  - course banner, module thumbnail, lesson card, hero illustration
  - whiteboard slide, sketch slide, technical diagram, flowchart, architecture map
  - typography image, sign mockup, poster, packaging mockup, menu image, app mockup
reference: ~/.claude/skills/graphics/example-brief.html
---

# /graphics — Canonical Graphics Skill

This is the ONE skill that handles every graphic the user generates. Eight curated styles (A through H), one decision tree, one example brief the user opens to pick by looking, one safe pipeline.

It replaces and consolidates: `infographic`, `visual-assets`, `image-pipeline`, `notebooklm-infographics`, `notebooklm-style-infographics`, `ai-image-diagram`, `image-generation`, `gpt-image-2`, `nano-banana-course-banners`, `whiteboard-explainer-slide`. Every prompt template, parameter, recipe, and safety guarantee from those skills lives inside this skill (see `styles/` and `prompts/`).

---

## When invoked — open the example brief FIRST

When `/graphics` is invoked, the first action is:

```bash
open ~/.claude/skills/graphics/example-brief.html
```

the user picks a style by looking at examples — A through H — then types or selects their answer in the brief and clicks **Copy My Answers**. The agent reads their answer and proceeds with the matched style recipe in `styles/<letter>-<name>.md`.

If the user describes the image without opening the brief, propose a default style based on the description, but ASK FIRST (below) before generating.

### the project Special Case

For the project projects, the canonical output is HTML template files following the `example-brief.html` structure, not generated images. Use the exact prompt templates from `output/graphics/hermes-vs-claude-whiteboard-canonical.html` and related files in the the project output directory. These HTML files contain the canonical Style F, B, C, and H visual representations using the exact the project framework.

---

## Credentials & Pre-flight Check — RUN BEFORE GENERATING

the user's direction: every /graphics generation uses the appropriate engine for the current project context. The engine is determined by project governance:

- **the project project**: Uses **Gemini 3.1 Flash Image** and **NotebookLM CLI** as documented in `README.md` and `.archived-server/server.js`. No Fal AI required.
- **Other projects**: Uses **OpenAI's newest image model (gpt-image-2) OR NotebookLM**. No other engines (no Nano Banana 2, no Flux). Each style recipe binds to one of the two.

**Engine bindings:**

NotebookLM is reserved for ONE style only — the actual classic NotebookLM auto-generated infographic. Every other style runs through gpt-image-2 via Fal, EXCEPT in the project where Gemini 3.1 Flash Image is used per the project's architecture (README.md lines 11-14, server.js lines 26, 64, 97).

| Style | Engine | Credential needed |
|---|---|---|
| A — Classic NotebookLM Infographic | NotebookLM | `nlm` CLI auth |
| B — Central Metaphor | gpt-image-2 (Fal) | `FAL_KEY` |
| C — Wheel Hub-and-Spoke | gpt-image-2 (Fal) | `FAL_KEY` |
| D — Isometric Pillars | gpt-image-2 (Fal) | `FAL_KEY` |
| E — Course Banner | gpt-image-2 (Fal) | `FAL_KEY` |
| F — Whiteboard Explainer | gpt-image-2 (Fal) | `FAL_KEY` |
| G — Technical Diagram | gpt-image-2 (Fal) | `FAL_KEY` |
| H — Typography Image | gpt-image-2 (Fal) | `FAL_KEY` |

`FAL_KEY` lives in your .env file per nucleus governance Section 17.

**⚠ Critical note on Hermes config scoping**: The `FAL_KEY` in your .env file is *not automatically loaded* into Hermes’ `image_gen` tool runtime. You must explicitly configure Hermes to use it via `hermes config set`. If `image_generate` fails with "FAL_KEY not set", this is the cause — not a missing key.

### 🔧 Configuring Hermes for Fal Image Generation

Run these commands in your terminal:

```bash
hermes config set image_gen.provider fal
hermes config set image_gen.fal_key  # then paste your FAL_KEY when prompted
```

✅ This writes the provider and key safely into `~/.hermes/config.yaml`. 
❌ Never interpolate `$FAL_KEY` directly in terminal — it risks credential leakage. Use the interactive `set` command instead.

After setting, verify:

```bash
hermes config show | grep -A 2 'image_gen'
```

**Critical Runtime Requirement**: The `image_gen` tool requires `FAL_KEY` to be available as an environment variable during execution. Hermes config alone is NOT sufficient. You must also ensure the environment variable is set by sourcing the .env file before generation:

```bash
set -a && source .env 2>/dev/null && set +a
```

### Direct API Fallback & Transparency Enforcement
If the `image_generate` tool persistently fails with `FAL_KEY environment variable is not set` despite the above configuration, bypass the tool entirely using a direct Python `urllib` script. This script must explicitly read your .env file, extract `FAL_KEY`, and call `https://fal.run/fal-ai/flux/schnell` (or `dev`) with `output_format: 'png'` explicitly set in the payload. 

**Modular Asset Rule**: When building modular character assets, the user explicitly demands actual generated image files (PNG with verified RGBA transparency) matching existing asset specifications (e.g., 512x512), **NOT** SVG blueprints, HTML templates, or instructions. If the generated PNG has a white background instead of true transparency, post-process it with a Python PIL script to force near-white pixels (R,G,B > 240) to transparent (A=0) before slicing the master sheet into standardized grid components.

**Pre-flight check — run this at start of any /graphics invocation:**
If the user explicitly requests image generation, DO NOT substitute an HTML blueprint, text description, or mockup for the actual images. If the `image_generate` tool fails (e.g., "FAL_KEY environment variable is not set" even after config), you MUST attempt the Direct Fal API Python fallback below before offering any text/HTML alternative. The user has explicitly penalized substituting artifacts for requested images.

**Fallback: Direct Fal API via Python (when `image_generate` tool fails)**
If the tool wrapper fails, extract the key from your .env file and call the Fal queue API directly via Python. This bypasses Hermes tool wrapper env-var injection issues.

```python
import urllib.request
import json
import os
import time

# Read key directly from the canonical env file
FAL_KEY = ""
with open(os.path.expanduser("~/.env"), "r") as f:
    for line in f:
        if line.startswith("FAL_KEY="):
            FAL_KEY = line.split("=", 1)[1].strip()
            break

url = 'https://queue.fal.run/fal-ai/flux-2/klein/9b'
headers = {
    'Authorization': f'Key {FAL_KEY}',
    'Content-Type': 'application/json'
}
data = {
    'prompt': 'YOUR_PROMPT_HERE',
    'image_size': 'square' # or 'landscape', 'portrait'
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')
try:
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode('utf-8'))
        status_url = result.get('status_url')
        response_url = result.get('response_url')
        
        # Poll for completion
        for _ in range(30):
            time.sleep(2)
            status_req = urllib.request.Request(status_url, headers=headers)
            with urllib.request.urlopen(status_req, timeout=10) as status_resp:
                status_result = json.loads(status_resp.read().decode('utf-8'))
                if status_result.get('status') == 'COMPLETED':
                    resp_req = urllib.request.Request(response_url, headers=headers)
                    with urllib.request.urlopen(resp_req, timeout=30) as resp:
                        final_result = json.loads(resp.read().decode('utf-8'))
                        img_url = final_result.get('images', [{}])[0].get('url')
                        print(f"SUCCESS: {img_url}")
                        # Add download logic here
                    break
                elif status_result.get('status') == 'FAILED':
                    print(f"FAILED: {status_result.get('error')}")
                    break
except Exception as e:
    print(f"ERROR: {e}")
```

**Pre-flight check — run this at start of any /graphics invocation:**

```bash
# Check NotebookLM auth (only for Style A)
NLM_OK=$(~/.local/bin/nlm login --check 2>&1 | grep -c "Authentication valid")

# Check Fal credential (for B–H)
set -a && source .env 2>/dev/null && set +a
FAL_OK=0; [ -n "$FAL_KEY" ] && FAL_OK=1

echo "NotebookLM auth: $([ $NLM_OK -gt 0 ] && echo OK || echo EXPIRED)"
echo "Fal key:         $([ $FAL_OK -eq 1 ] && echo OK || echo MISSING)"
```

**If any credential is MISSING / EXPIRED — DO NOT FAIL SILENTLY. Surface the gap and the fix:**

| Missing | Where to fix |
|---|---|
| NotebookLM auth | Run `bash ~/.claude/skills/notebooklm-auth-recovery/recover.sh` (30-second non-interactive fix). Codified in Hard Rule 10. |
| `OPENAI_API_KEY` | the user renews at https://platform.openai.com/api-keys → paste into your .env file as `OPENAI_API_KEY=sk-...` |
| `FAL_KEY` | the user renews at https://fal.ai/dashboard/keys → paste into your .env file as `FAL_KEY=...` |

**Do not scan other env files for credentials.** The canonical path is your .env file per nucleus governance Section 17. If the credential is not there, surface the gap to the user with the exact env-var name and the renewal URL — never scan other projects' .env files (security warning fires).

---

## ASK FIRST — before any image generation

the user is non-negotiable on this. Before calling any image API, ask their five short questions. She prefers being asked over guessing wrong; they does not like having to volunteer this upfront in their initial prompt.

Pose them as a tight numbered list — do not pad. Wait for their answer before generating.

1. **What is this image for?** (Skool banner? Skool module thumbnail? YouTube banner? YouTube thumbnail? Watchtower brief image? Instagram post? Course module card? Something else?) The use case determines the dimensions in question 2.
2. **Dimensions.** Do you know the exact pixel dimensions you want? If yes, name them. If no, I check `~/.claude/skills/graphics/references/dimensions.md` for the platform standard. If the platform isn't in that file, I research the canonical dimensions, propose a default, and you confirm before I generate.
3. **Style.** Which of A–H? Reference the decision tree below — propose a default based on what they described, but ask. Offer to open the example brief if helpful.
4. **Reference image(s):** any existing reference they wants matched? Check `~/.claude/skills/graphics/references/INDEX.md` first — if a stored reference fits, name it and offer to use it.
5. **Color / vibrancy / energy + anti-style:** what palette and energy level? Anything to avoid? **Default to vibrant.** Muted/pastel is wrong for the user .

If they has already given any of these in their prompt, skip that question — never make their repeat herself. Only ask the unknowns.

After they answers, generate ONE image and STOP for their approval (per `feedback_test_means_one_wait_for_approval`).

---

## The eight styles — decision tree

```
What are you generating?
│
├── A — CARD GRID (5 cards in 3+2)
│      Editorial card grid via Nano Banana Pro. Module thumbnails,
│      structured lessons, batch series of on-brand explainer cards.
│      Validated 99-module the course site look.
│      → styles/A-card-grid.md
│
├── B — CENTRAL METAPHOR (single hero illustration)            ⚠ prompt repair pending
│      Single-concept narrative hero illustration via gpt-image-2 (Fal).
│      Best when ONE big idea carries the image.
│      → styles/B-central-metaphor.md
│
├── C — WHEEL HUB-AND-SPOKE (6–10 segments)
│      Sets of equal items, parallel concepts laid out radially.
│      gpt-image-2 (Fal).
│      → styles/C-wheel-hub-and-spoke.md
│
├── D — ISOMETRIC PILLARS (3D blocks)
│      Hierarchies, layered architectures, tech-stack visualizations.
│      gpt-image-2 (Fal).
│      → styles/D-isometric-pillars.md
│
├── E — COURSE BANNER
│      Illustrated horizontal course banner via gpt-image-2 (Fal).
│      Text placement and palette controlled in the prompt; brand mark
│      composited via PIL post-processing. Upscaled via clarity-upscaler.
│      → styles/E-course-banner.md
│
├── F — WHITEBOARD EXPLAINER
│      Pencil-on-cream sketch slide via gpt-image-2. Hand-printed
│      title with squiggle underline, central diagram, right-column
│      bullets, conference-talk feel.
│      → styles/F-whiteboard-explainer.md
│
├── G — TECHNICAL DIAGRAM
│      Architecture maps, flowcharts, schematics via Gemini /
│      Nano Banana. For polished editorial diagrams use Style A or
│      C instead — this is the quick concept-diagram lane.
│      → styles/G-technical-diagram.md
│
└── H — TYPOGRAPHY IMAGE
       Strongest in class for legible text inside images via
       gpt-image-2 (sync API on Fal). Chalkboards, signs, menus,
       posters, packaging, UI mockups, magazine covers.
       → styles/H-typography-image.md
```

---

## Safety guarantees

This skill exists in part because image generation has bricked Claude Code sessions before. Prior sessions have become unresponsive after a truncated PNG download landed in conversation context. The safety layer below is load-bearing — every generation routes through it.

### Fallback: Local HTML whiteboard
When external image generation fails (Fal timeout, auth rejection, model mismatch), this skill guarantees an on-device fallback: a responsive, hand-drawn-style HTML whiteboard. It uses only browser-native primitives (HTML/CSS/JS), requires no API keys or network calls, and delivers the full Style F aesthetic — squiggle-underlined title, central diagram, right-column bullets — in <2KB. Generated files are saved to `<project>/output/graphics/` with `run-<date>_<label>.html` naming, and open instantly in any browser. This fallback satisfies the functional *and* aesthetic intent of Style F when tooling fails — and it ships *guaranteed*.

### The pipeline (every generation, every time)

```bash
set -a && source .env && set +a
source ~/.claude/skills/graphics/lib/safe-image.sh

PROJECT="<project-dir>"     # the project this output belongs to
SKILL="graphics"                                 # always graphics now
LABEL="<short-slug>"                             # short slug for this run

# 1. Init run folder (never overwrites)
RUN_DIR=$(pipeline_init "$PROJECT" "$SKILL" "$LABEL")

# 2. Build prompt (style-specific — see styles/<letter>-*.md and prompts/<letter>-*.md)
cat > "$RUN_DIR/prompt.json" << 'EOF'
{ ... }
EOF

# 3. Call the model API. Save raw response.
curl -s -X POST "<endpoint>" \
  -H "Authorization: Key $FAL_KEY" -H "Content-Type: application/json" \
  -d @"$RUN_DIR/prompt.json" > "$RUN_DIR/response.json"

# 4. Extract image URL and SAFELY download.
URL=$(python3 -c "import json,sys; print(json.load(open('$RUN_DIR/response.json'))['images'][0]['url'])")
safe_download_image "$URL" "$RUN_DIR/${LABEL}.png" || { echo "DOWNLOAD FAILED"; exit 1; }

# 5. Publish — builds gallery, rsyncs to iCloud, opens in browser.
pipeline_publish "$PROJECT" "$SKILL"
```

Five steps. No image is ever read into context, no curl runs without `--fail`, no folder is ever overwritten.

### The trap dossier

1. **Truncated download → session bricked with 400** — every assistant turn returns `API Error: 400 "Could not process image"`. Cause: image cut off mid-stream, missing IEND chunk. Mitigation: `safe_download_image` from `lib/safe-image.sh`.
2. **`Read` on a PNG larger than ~1 MB → context bomb** — never use `Read` on a PNG > 1 MB. Verify with `ls -la`, `sips`, `xxd | tail -1` for IEND, or `open <path>`.
3. **Tools lie about file validity** — `file` and `sips` only sniff the header. Trust `verify_png` (IEND check) and Preview.
4. **Fal CDN URL TTL** — re-download on the same day; afterwards regenerate from saved `prompt.json`.
5. **Silent overwrite when iterating** — `pipeline_init` always returns a unique folder.
6. **iCloud Drive does not follow symlinks** — `_publish_to_icloud` uses `rsync -a --delete`.

Recovery from a bricked session: open a new Claude Code session. Re-run from the saved `prompt.json`.

---

## Reference library

Stored at `~/.claude/skills/graphics/references/`. added style exemplars (saved Excalidraw logos, screenshots they loves, prior approved generations). Browseable via `INDEX.md`. Naming convention:

```
<intent>_<style>_<vibe>.<ext>
e.g.   logo_excalidraw-handdrawn_vibrant.png
       slide_whiteboard-pencil_high-energy.png
       infographic_notebooklm-editorial_warm-cream.png
       palette_vibrant-5color.png
```

When asking question 2 (reference image), grep `INDEX.md` for relevant tags first.

---

## Output organization

Every run gets its own folder. Never `--force` overwrite — the user compares iterations.

```
<project>/output/graphics/
├── index.html                              # auto-built gallery (do not edit)
└── run-<YYYY-MM-DD>_<label>/
    ├── prompt.json                         # exact prompt sent to model
    ├── response.json                       # raw API response
    └── <label>.png                         # the generated image
```

iCloud mirror — same structure under `~/Library/Mobile Documents/com~apple~CloudDocs/the project-output/<project-name>/graphics/`.

---

## When NOT to use this skill

- **Reading an existing image** the user already has on disk (no generation involved). This skill is for the *generate* step.
- **Inline diagram in a markdown doc** that's better served by mermaid or ASCII.
- **Editing an image** (cropping, masking, format conversion). Use `sips` or `ffmpeg` directly.
- **Slide-deck assembly** with multiple pre-generated images. Use the `pptx` skill.

---

## Public bash API (sourced from `graphics/lib/safe-image.sh`)

| Function | Purpose |
|---|---|
| `safe_download_image url out` | curl with retries + integrity check. Hard-fails on corruption. |
| `verify_png path` | Returns 0 if PNG ends with IEND, 1 if truncated. |
| `verify_jpeg path` | Returns 0 if JPEG ends with FFD9, 1 if truncated. |
| `verify_image path` | Dispatches to png/jpeg verifier by extension. |
| `pipeline_init project skill label` | Creates `output/graphics/run-<date>_<label>/`. Echoes path. Never overwrites. |
| `pipeline_publish project skill` | Builds gallery, rsyncs to iCloud, opens in browser. |

---

## Style files — where the recipes live

Every style has three artifacts:

| Style | Recipe | Prompt template | Example PNG (placeholder until generated) |
|---|---|---|---|
| A — Card Grid | `styles/A-card-grid.md` | `prompts/A-prompt-template.md` | `examples/A-example.png` |
| B — Central Metaphor ⚠ | `styles/B-central-metaphor.md` | `prompts/B-prompt-template.md` | `examples/B-example.png` |
| C — Wheel Hub-and-Spoke | `styles/C-wheel-hub-and-spoke.md` | `prompts/C-prompt-template.md` | `examples/C-example.png` |
| D — Isometric Pillars | `styles/D-isometric-pillars.md` | `prompts/D-prompt-template.md` | `examples/D-example.png` |
| E — Course Banner | `styles/E-course-banner.md` | `prompts/E-prompt-template.md` | `examples/E-example.png` |
| F — Whiteboard Explainer | `styles/F-whiteboard-explainer.md` | `prompts/F-prompt-template.md` | `examples/F-example.png` |
| G — Technical Diagram | `styles/G-technical-diagram.md` | `prompts/G-prompt-template.md` | `examples/G-example.png` |
| H — Typography Image | `styles/H-typography-image.md` | `prompts/H-prompt-template.md` | `examples/H-example.png` |

⚠ Style B has a known prompt-repair task pending — see the recipe.

---

## Origin

Created from consolidated prior skills. Consolidated from infographic, visual-assets, image-pipeline, notebooklm-infographics, notebooklm-style-infographics, ai-image-diagram, image-generation, gpt-image-2, nano-banana-course-banners, whiteboard-explainer-slide.

The architecture was approved via a consolidation brief (FULL MERGE). Source skills were consolidated in one pass.

---

## Post-Processing Pipeline (upscale + web-optimize)

Restored from the retired `notebooklm-style-infographics` and `nano-banana-course-banners` skills. Every gpt-image-2 generation produces a 1024×1024 source PNG. Two optional post-passes turn that source into delivery-ready assets.

### Step 1 — Upscale to 2K+ (Fal clarity-upscaler)

Use when the destination is print, a hero image, or a banner that will display larger than 1024px on retina screens.

```bash
~/.claude/skills/graphics/lib/upscale.sh source.png upscaled-2k.png 2
# scale=2 → 2048×2048; scale=4 → 4096×4096
```

The script uploads the source to Fal storage, submits to `fal-ai/clarity-upscaler`, polls until complete, and downloads via the safe-image pipeline (integrity-checked).

Skip when the source is already going into a small footprint (Watchtower brief thumbnail, Slack-share preview).

### Step 2 — Web-optimize (resize + compress)

Every asset shipping to a website, social platform, or Watchtower brief gets web-optimized so file size matches the destination's expectations. Default targets: <500 KB for full-size hero, <200 KB for thumbnails, <100 KB for inline brief images.

```bash
~/.claude/skills/graphics/lib/web-optimize.sh source.png 1600 webp
# args: <input>  <max-long-edge-px>  <format: webp|jpeg|png>
```

The script reads the source with PIL, resizes if the long edge exceeds the threshold, converts mode if needed (WebP/JPEG drops alpha), saves with optimized compression. Output is `<basename>-web.<ext>` next to the original. Original PNG stays for archive.

### Pipeline order — APPROVAL GATE BEFORE UPSCALE

1. **Generate** — gpt-image-2 (B–H) or NotebookLM (A) → 1024×1024 PNG (or 2752×1536 for NotebookLM)
2. **Verify** — `safe-image.sh` integrity check (PNG IEND, byte-level)
3. **present to the user** — present the base-resolution image. the user approves or rejects. **Never upscale before this gate.**
4. **Upscale** — only on approved images. Skip if the user rejects (re-generate instead).
5. **Web-optimize** — required for any web/social delivery (`web-optimize.sh`)
6. **File** — output to `<project>/output/graphics/run-<YYYY-MM-DD>_<label>/` per the project-folder convention
7. **Publish** — auto-build the iPhone gallery via the safe-image pipeline if the run is meant for review on phone

**Why the gate matters:** Fal clarity-upscaler costs real money per call. Upscaling a rejected image is paying for high quality on output we throw away. Show the base render first, get the approval, then upscale only what survives.

### When to run upscale + web-optimize

| Destination | Upscale? | Web-optimize? | Format | Max edge |
|---|---|---|---|---|
| Watchtower brief inline | no | yes | jpeg | 1024 |
| Skool banner (1280×720) | yes (2x) | yes | webp | 1280 |
| Skool module thumbnail (1280×720) | yes (2x) | yes | webp | 1280 |
| YouTube thumbnail (1280×720) | yes (2x) | yes | jpeg | 1280 |
| YouTube channel banner (2560×1440) | yes (4x) | yes | jpeg | 2560 |
| Instagram post (1080×1080) | no (1024 is close enough) | yes | jpeg | 1080 |
| Print / hi-res deck | yes (4x) | no — keep PNG | png | 4096 |
| Phone gallery preview | no | yes | webp | 800 |

