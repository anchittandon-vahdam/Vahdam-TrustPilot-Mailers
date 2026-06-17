#!/usr/bin/env python3
"""
Batch-generate VAHDAM post-purchase hero creatives with the new
Ashwagandha Coffee+ packet swapped in.

Why this script exists: the Claude Code remote environment has no
image-generation tool and its network egress is locked down, so the
creatives can't be rendered there. Run this locally (or anywhere with
internet + an API key) to generate all 21 creatives in one go.

Supported backends:
  - openai  : gpt-image-1 via the Images API (img-gen-2 family).
              Uses images.edit with the packet (+ optional source hero)
              as reference images.
  - gemini  : gemini-2.5-flash-image ("nano banana") for prompt+image
              editing. Excellent at "use this product, recreate this scene".

Usage:
  pip install openai pillow requests            # for openai backend
  pip install google-genai pillow requests      # for gemini backend

  export OPENAI_API_KEY=sk-...                  # or GEMINI_API_KEY=...

  python generate_creatives.py \
      --backend openai \
      --packet ./new-packet.png \
      --prompts ./prompts.json \
      --out ./creatives \
      --download-sources          # optional: also pull original heroes
                                  #   as composition references

  # generate just a couple to test first:
  python generate_creatives.py --backend openai --packet ./new-packet.png --only PP1 PP2
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None


# Headers that make CloudFront / Shopify CDN happy when downloading sources.
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "image/avif,image/webp,image/png,image/*,*/*;q=0.8",
    "Referer": "https://www.vahdam.co.uk/",
}


def log(msg):
    print(f"[creatives] {msg}", flush=True)


def build_full_prompt(data, item):
    """Compose the final text prompt for one creative."""
    parts = [
        "TASK: Produce a premium marketing email hero image.",
        f"PRODUCT TO FEATURE (use the attached packet image as the exact "
        f"product reference): {data['product_reference']}",
        f"SCENE: {item['prompt']}",
        f"STYLE: {data['global_style']}",
    ]
    if item.get("role") == "gift_hero_with_pouch_prop":
        parts.append(
            f"IMPORTANT: The hero subject is the gift item "
            f"({item.get('gift_item','the gift')}). The Coffee+ pouch is a "
            f"SUPPORTING prop only — do not make it the main subject."
        )
    else:
        parts.append(
            "IMPORTANT: The Coffee+ pouch is the HERO subject of the image."
        )
    parts.append(
        "Do NOT show the old/previous coffee packaging. Only the new "
        "dark forest-green Coffee+ pouch should appear."
    )
    return "\n".join(parts)


def download_sources(data, out_dir, only):
    if requests is None:
        log("requests not installed; skipping --download-sources")
        return {}
    src_dir = out_dir / "source-heroes"
    src_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for item in data["creatives"]:
        if only and item["id"] not in only:
            continue
        url = item.get("source_url")
        if not url:
            continue
        dest = src_dir / f"{item['id']}.png"
        try:
            r = requests.get(url, headers=BROWSER_HEADERS, timeout=30)
            if r.status_code == 200 and len(r.content) > 1000:
                dest.write_bytes(r.content)
                paths[item["id"]] = dest
                log(f"  downloaded source {item['id']} ({len(r.content)} bytes)")
            else:
                log(f"  source {item['id']} -> HTTP {r.status_code} "
                    f"({len(r.content)} bytes), skipping reference")
        except Exception as e:
            log(f"  source {item['id']} download failed: {e}")
    return paths


# ----------------------------- OpenAI backend -----------------------------
def run_openai(data, args, source_paths):
    from openai import OpenAI

    client = OpenAI()  # reads OPENAI_API_KEY
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    packet = Path(args.packet)

    for item in data["creatives"]:
        if args.only and item["id"] not in args.only:
            continue
        prompt = build_full_prompt(data, item)
        # Reference images: packet first, then optional source hero.
        images = [open(packet, "rb")]
        sp = source_paths.get(item["id"])
        if sp and sp.exists():
            images.append(open(sp, "rb"))
        log(f"generating {item['id']} (openai, {len(images)} ref image(s))...")
        try:
            resp = client.images.edit(
                model="gpt-image-1",
                image=images,
                prompt=prompt,
                size="1536x1024",  # closest landscape to a 2:1 email hero
            )
            b64 = resp.data[0].b64_json
            dest = out_dir / f"{item['id']}.png"
            dest.write_bytes(base64.b64decode(b64))
            log(f"  saved {dest}")
        except Exception as e:
            log(f"  ERROR on {item['id']}: {e}")
        finally:
            for fh in images:
                try:
                    fh.close()
                except Exception:
                    pass
        time.sleep(args.sleep)


# ----------------------------- Gemini backend -----------------------------
def run_gemini(data, args, source_paths):
    from google import genai
    from google.genai import types

    client = genai.Client()  # reads GEMINI_API_KEY / GOOGLE_API_KEY
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    packet_bytes = Path(args.packet).read_bytes()

    for item in data["creatives"]:
        if args.only and item["id"] not in args.only:
            continue
        prompt = build_full_prompt(data, item)
        contents = [
            prompt,
            types.Part.from_bytes(data=packet_bytes, mime_type="image/png"),
        ]
        sp = source_paths.get(item["id"])
        if sp and sp.exists():
            contents.append(
                types.Part.from_bytes(
                    data=sp.read_bytes(), mime_type="image/png"
                )
            )
        log(f"generating {item['id']} (gemini)...")
        try:
            resp = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=contents,
            )
            saved = False
            for part in resp.candidates[0].content.parts:
                if getattr(part, "inline_data", None):
                    dest = out_dir / f"{item['id']}.png"
                    dest.write_bytes(part.inline_data.data)
                    log(f"  saved {dest}")
                    saved = True
                    break
            if not saved:
                log(f"  WARNING: no image returned for {item['id']}")
        except Exception as e:
            log(f"  ERROR on {item['id']}: {e}")
        time.sleep(args.sleep)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--backend", choices=["openai", "gemini"], default="openai")
    ap.add_argument("--packet", required=True,
                    help="Path to the new VAHDAM Ashwagandha Coffee+ packet image")
    ap.add_argument("--prompts", default=str(Path(__file__).parent / "prompts.json"))
    ap.add_argument("--out", default="./creatives")
    ap.add_argument("--only", nargs="*", default=None,
                    help="Generate only these IDs, e.g. --only PP1 PP2")
    ap.add_argument("--download-sources", action="store_true",
                    help="Also download original hero images as references")
    ap.add_argument("--sleep", type=float, default=2.0,
                    help="Seconds to wait between requests")
    args = ap.parse_args()

    if not Path(args.packet).exists():
        sys.exit(f"Packet image not found: {args.packet}")

    with open(args.prompts) as f:
        data = json.load(f)

    source_paths = {}
    if args.download_sources:
        source_paths = download_sources(data, Path(args.out), args.only)

    if args.backend == "openai":
        run_openai(data, args, source_paths)
    else:
        run_gemini(data, args, source_paths)

    log("done.")


if __name__ == "__main__":
    main()
