# Creatives Pipeline — VAHDAM Ashwagandha Coffee+ Hero Image Regeneration

Batch-generate all 21 post-purchase email hero creatives with the **new
VAHDAM Ashwagandha Coffee+** packet (dark forest-green pouch) swapped in.

## Why this is a script and not done automatically

The Claude Code remote environment has **no image-generation tool**, and its
network egress is allowlisted (only hosts like GitHub are reachable — the
image CDNs and image APIs are blocked). So the renders can't be produced in
that environment. Run this script anywhere with internet access + an API key
(your laptop, a CI runner, a Colab notebook).

## What's here

| File | Purpose |
|------|---------|
| `prompts.json` | All 21 creatives: scene prompt, role (hero pouch vs. gift+prop), source URL, alt text |
| `generate_creatives.py` | Batch generator. OpenAI (`gpt-image-1`) or Gemini (`gemini-2.5-flash-image`) backend |
| `../Image-Regen-Prompts.md` | Human-readable Variant A / Variant B prompts for manual ChatGPT use |

PP7 is intentionally excluded (logo-only header, no hero image).

## Setup

```bash
# OpenAI backend (img-gen-2 family)
pip install openai pillow requests
export OPENAI_API_KEY=sk-...

# OR Gemini backend
pip install google-genai pillow requests
export GEMINI_API_KEY=...
```

You also need the **new packet image** saved locally (e.g. `new-packet.png`).

## Run

```bash
# Test with two first
python generate_creatives.py \
  --backend openai \
  --packet ./new-packet.png \
  --only PP1 PP2

# Full batch, also pulling the original heroes as composition references
python generate_creatives.py \
  --backend openai \
  --packet ./new-packet.png \
  --out ./creatives \
  --download-sources
```

Outputs land in `./creatives/PP1.png … PP22.png`. Downloaded source heroes (if
`--download-sources` succeeds) go to `./creatives/source-heroes/`.

## How it works

For each creative the script builds a structured prompt:
- **Product reference** — describes the new Coffee+ pouch and attaches your
  packet image as the exact visual reference.
- **Scene** — the per-email scene from `prompts.json`.
- **Style** — shared email-banner styling (2:1 landscape, warm neutrals,
  top space for headline text).
- **Role guard** — for the gift emails (PP6, PP12, PP16, PP21) it keeps the
  gift item as hero and the pouch as a supporting prop; for all others the
  pouch is the hero. It always instructs the model to drop the old packaging.

`--download-sources` additionally feeds each original hero image to the model
as a second reference so composition/lighting carry over. If a source URL
401/403s in your environment too, the script just skips that reference and
still generates from the text prompt + packet image.

## Notes / tuning

- **Aspect ratio:** OpenAI sizes are fixed (`1536x1024` used here, closest
  landscape). Crop/letterbox to the email's exact hero ratio afterward if
  needed. Gemini returns a model-chosen size.
- **Consistency:** for a uniform look across all 21, keep the same backend and
  the same packet image, and don't change `global_style` mid-batch.
- **Cost:** ~21 image generations per full run. Test with `--only` first.
- **Gift item accuracy:** the gift bottles/glass/sampler are described by name.
  For exact product fidelity, add those product photos as extra references
  (extend `run_openai` / `run_gemini` to append more images).
