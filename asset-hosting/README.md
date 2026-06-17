# Asset Hosting — Migrate mailer images to Supabase Storage

Self-host every image referenced by the 22 mailers + 2 landing pages on
**Supabase Storage**, so the templates no longer depend on Klaviyo's CloudFront
CDN or Shopify's CDN. After migration every `<img>` and CSS `url()` points at a
stable, public Supabase URL you control.

## Why a script (and not done by Claude Code directly)

The Claude Code remote environment's network egress is **allow-listed to GitHub
only**. The source CDNs return `403 host_not_allowed`:

| Host | Status from sandbox |
|------|--------------------|
| `d3k81ch9hvuctc.cloudfront.net` (Klaviyo) | ❌ `403 host_not_allowed` |
| `www.vahdam.com` / `vahdam.co.uk` (Shopify) | ❌ blocked |
| `raw.githubusercontent.com` | ✅ `200` |

So the image binaries can't be downloaded in-session. Run this script anywhere
with open network (your laptop, CI, Colab).

## What gets migrated (27 unique assets)

See [`asset-manifest.json`](./asset-manifest.json) for the full list. Summary:

| Category | Count | Source |
|----------|-------|--------|
| `heroes/` | 22 | Klaviyo-uploaded hero/product images + one Shopify product shot |
| `social/` | 4 | Klaviyo's facebook / instagram / tiktok / x icons |
| `logos/` | 1 | `logo-website.png` (Shopify CDN) |

**Left untouched** (correctly external — not assets to self-host): social
profile links (instagram/x/tiktok/facebook), Trustpilot review links,
vahdam.com store links, the `anchittandon-vahdam.github.io` landing-page links,
and the star-rating icons (already inlined as base64 `data:` URIs).

## Setup

```bash
pip install requests

export SUPABASE_URL="https://<project-ref>.supabase.co"
export SUPABASE_SERVICE_KEY="<service-role-key>"   # service role key, NOT anon
export SUPABASE_BUCKET="mailer-assets"             # must be a PUBLIC bucket
```

Create the bucket once (Supabase dashboard → Storage → New bucket → name it
`mailer-assets`, toggle **Public** on). Public buckets serve files at
`{SUPABASE_URL}/storage/v1/object/public/{bucket}/{path}` with CDN caching —
ideal for email image hotlinking.

## Run

```bash
# 1. (Optional) refresh the manifest only — no network, no creds needed:
python migrate_to_supabase.py --manifest-only

# 2. Dry run — downloads + plans the rewrite, uploads/edits nothing:
python migrate_to_supabase.py --dry-run

# 3. Full migration — download → upload to Supabase → rewrite all HTML:
python migrate_to_supabase.py
```

After a full run:
- All 24 HTML files are rewritten in place with the new Supabase URLs.
- `asset-map.json` records every `old → new` URL mapping.
- Re-run is safe (idempotent): uploads use `x-upsert`, and once HTML is
  rewritten the old URLs are gone so nothing double-maps.

## After migrating

1. `git diff` to review the URL swaps.
2. Test-render a couple of mailers (open in a browser / send a Klaviyo test).
3. Commit & push.
4. Re-upload the templates to Klaviyo / your Drive as usual.
