#!/usr/bin/env python3
"""
Migrate every external image asset referenced by the Vahdam Trustpilot mailers
to Supabase Storage, then rewrite the HTML templates to point at the new,
self-hosted public URLs.

Why this is a script and not done inline by Claude Code:
  The Claude Code remote environment's network egress is allow-listed to GitHub
  only. The image CDNs (Klaviyo CloudFront `d3k81ch9hvuctc.cloudfront.net`,
  Shopify `vahdam.com` / `vahdam.co.uk`) return `403 host_not_allowed`, so the
  binaries cannot be downloaded there. Run this anywhere with open network.

What it does:
  1. Scans every .html in ../Mailers and "../Landing pages" for asset URLs.
  2. Skips destination links (instagram/x/tiktok/facebook/trustpilot/store pages)
     and inline base64 data: URIs (the star icons) -- only real CDN-hosted
     image files are migrated.
  3. Downloads each unique asset.
  4. Uploads it to your Supabase Storage bucket under a tidy folder layout
     (social/ , heroes/ , logos/).
  5. Rewrites all HTML files, swapping old URL -> new public Supabase URL.
  6. Writes asset-map.json (old -> new) and refreshes asset-manifest.json.

Modes:
  --manifest-only   Just (re)write asset-manifest.json. Works with NO network
                    and NO credentials -- useful inside the sandbox.
  --dry-run         Download + plan the rewrite, but don't upload or edit files.
  (default)         Full migrate: download, upload, rewrite.

Setup:
  pip install requests
  export SUPABASE_URL="https://<project-ref>.supabase.co"
  export SUPABASE_SERVICE_KEY="<service-role-key>"   # service role, not anon
  export SUPABASE_BUCKET="mailer-assets"             # a PUBLIC bucket

Usage:
  python migrate_to_supabase.py --manifest-only
  python migrate_to_supabase.py --dry-run
  python migrate_to_supabase.py
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    requests = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_GLOBS = [
    os.path.join(ROOT, "Mailers", "**", "*.html"),
    os.path.join(ROOT, "Landing pages", "**", "*.html"),
]

# Hosts whose image files we self-host. Anything else (social profiles,
# trustpilot, store page links, github.io landing pages) is left untouched.
ASSET_HOSTS = {
    "d3k81ch9hvuctc.cloudfront.net",
    "www.vahdam.com",
    "vahdam.com",
    "www.vahdam.co.uk",
}
IMG_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")
URL_RE = re.compile(r'https?://[^"\'\s)]+')


def is_asset(url: str) -> bool:
    p = urlparse(url)
    if p.netloc not in ASSET_HOSTS:
        return False
    path = p.path.lower()
    if path.endswith(IMG_EXTS):
        return True
    if "/cdn/shop/" in path:
        return True
    return False


def categorize(url: str) -> str:
    """Folder within the bucket: social / logos / heroes."""
    path = urlparse(url).path.lower()
    if "/assets/email/buttons/" in path:
        return "social"
    name = os.path.basename(path)
    if "logo" in name:
        return "logos"
    return "heroes"


def storage_name(url: str) -> str:
    """Deterministic object path inside the bucket. Drops the query string but
    keeps a short hash of it so e.g. ?width=400 vs ?width=800 don't collide."""
    p = urlparse(url)
    base = os.path.basename(p.path)
    if p.query:
        h = hashlib.sha1(p.query.encode()).hexdigest()[:6]
        stem, ext = os.path.splitext(base)
        base = f"{stem}-{h}{ext}"
    return f"{categorize(url)}/{base}"


def scan():
    """Return {url: [filenames...]} for every migratable asset."""
    assets = {}
    for pattern in HTML_GLOBS:
        for f in glob.glob(pattern, recursive=True):
            txt = open(f, encoding="utf-8").read()
            for m in URL_RE.findall(txt):
                url = m.replace("&amp;", "&")
                if is_asset(url):
                    assets.setdefault(url, []).append(os.path.basename(f))
    return assets


def write_manifest(assets):
    manifest = {
        "asset_count": len(assets),
        "asset_hosts": sorted(ASSET_HOSTS),
        "assets": [
            {
                "url": url,
                "category": categorize(url),
                "storage_path": storage_name(url),
                "used_in": sorted(set(files)),
                "uses": len(files),
            }
            for url, files in sorted(assets.items())
        ],
    }
    out = os.path.join(os.path.dirname(__file__), "asset-manifest.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    print(f"Wrote {out} ({len(assets)} assets)")
    return manifest


def public_url(supabase_url, bucket, path):
    return f"{supabase_url.rstrip('/')}/storage/v1/object/public/{bucket}/{path}"


def upload(supabase_url, service_key, bucket, path, data, content_type):
    endpoint = f"{supabase_url.rstrip('/')}/storage/v1/object/{bucket}/{path}"
    headers = {
        "Authorization": f"Bearer {service_key}",
        "Content-Type": content_type,
        "x-upsert": "true",
    }
    r = requests.post(endpoint, headers=headers, data=data, timeout=60)
    if r.status_code not in (200, 201):
        raise RuntimeError(f"upload failed {r.status_code}: {r.text[:200]}")


CONTENT_TYPES = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp", ".svg": "image/svg+xml",
}


def migrate(dry_run=False):
    if requests is None:
        sys.exit("requests not installed: pip install requests")

    supabase_url = os.environ.get("SUPABASE_URL")
    service_key = os.environ.get("SUPABASE_SERVICE_KEY")
    bucket = os.environ.get("SUPABASE_BUCKET", "mailer-assets")
    if not dry_run and not (supabase_url and service_key):
        sys.exit("Set SUPABASE_URL and SUPABASE_SERVICE_KEY env vars (or use --dry-run).")

    assets = scan()
    write_manifest(assets)
    url_map = {}

    for url in sorted(assets):
        path = storage_name(url)
        print(f"\n{url}\n  -> {path}")
        try:
            resp = requests.get(url, timeout=60)
            resp.raise_for_status()
        except Exception as e:
            print(f"  !! download failed, leaving as-is: {e}")
            continue
        ext = os.path.splitext(path)[1].lower()
        ctype = CONTENT_TYPES.get(ext, "application/octet-stream")
        if dry_run:
            print(f"  [dry-run] would upload {len(resp.content)} bytes ({ctype})")
            url_map[url] = public_url(supabase_url or "https://<project>.supabase.co", bucket, path)
            continue
        try:
            upload(supabase_url, service_key, bucket, path, resp.content, ctype)
        except Exception as e:
            print(f"  !! upload failed, leaving as-is: {e}")
            continue
        new = public_url(supabase_url, bucket, path)
        url_map[url] = new
        print(f"  uploaded -> {new}")

    # Rewrite HTML (skip in dry-run).
    if not dry_run and url_map:
        rewrite_html(url_map)

    out = os.path.join(os.path.dirname(__file__), "asset-map.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(url_map, fh, indent=2)
    print(f"\nWrote {out} ({len(url_map)} mappings)")
    if dry_run:
        print("Dry run -- no files uploaded or rewritten.")


def rewrite_html(url_map):
    files = []
    for pattern in HTML_GLOBS:
        files.extend(glob.glob(pattern, recursive=True))
    changed = 0
    for f in files:
        txt = open(f, encoding="utf-8").read()
        orig = txt
        for old, new in url_map.items():
            # match both raw and &amp;-encoded forms of the query string
            txt = txt.replace(old, new).replace(old.replace("&", "&amp;"), new)
        if txt != orig:
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(txt)
            changed += 1
            print(f"  rewrote {os.path.basename(f)}")
    print(f"Rewrote {changed} HTML file(s).")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest-only", action="store_true", help="Only (re)write asset-manifest.json (no network).")
    ap.add_argument("--dry-run", action="store_true", help="Download + plan, but don't upload or edit files.")
    args = ap.parse_args()

    if args.manifest_only:
        write_manifest(scan())
    else:
        migrate(dry_run=args.dry_run)
