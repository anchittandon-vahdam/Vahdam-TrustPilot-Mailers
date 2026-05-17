# Vahdam Trustpilot Gated Review Funnel — Final Package

This is the cleaned, structured deliverable folder. Everything below this README is what you actually need; the two folders at the parent level (`Output Variant 1/` and `Outout Variant 2/`) are the unsorted working state and can be deleted once you've reviewed this folder.

## Folder structure

```
00 - FINAL PACKAGE/
│
├── 00 - START HERE.html                     ← open this first
├── README.md                                ← you are here
│
├── 01 - Reference Mailers (original)/       ← the high-quality reference you shared
│   ├── 01-mailers-minimal/                  7 mailers, minimal density + preview PNGs
│   ├── 02-mailers-lean/                     7 mailers, lean density + preview PNGs
│   ├── 03-review-flow-pages/                review-choice / private-feedback / thanks
│   ├── 04-supporting-docs/                  subject lines, structure-per-mailer, compliance
│   ├── assets/                              hero images (base64-embedded in HTML)
│   └── README.md                            the reference's own README
│
├── 02 - Final Package v4 (USE THIS)/        ← the new build, matching reference quality
│   ├── index.html                           main hub — open in browser to navigate
│   ├── interactive_flow_prototype.html      clickable end-to-end prototype
│   │
│   ├── mailers/                             28 production HTML mailers
│   │   ├── 01 - minimal · direct-to-Trustpilot/    Variant 1 CTA (loyal cohorts)
│   │   ├── 02 - minimal · in-mailer rating/        Variant 2 CTA (broader cohorts)
│   │   ├── 03 - lean · direct-to-Trustpilot/       Variant 1, lean density
│   │   └── 04 - lean · in-mailer rating/           Variant 2, lean density
│   │
│   ├── review-flow-pages/                   landing pages users see after CTA click
│   ├── landing-pages/                       alt landing pages (Variant A & B engineering)
│   ├── backend/                             OpenAPI spec + Node/Express reference stub
│   ├── briefs/                              the two strategic briefs (.docx)
│   ├── supporting-docs/                     reader's guide, mailer ideation, Trustpilot
│   │                                        setup, Klaviyo setup (all .docx)
│   └── reference-docs/                      compliance guides from the reference
│
├── 03 - Version Archive/                    ← every iteration kept safely
│   ├── v2 - initial M1-M9 mailers.zip       very first build
│   ├── v3 - 4-strategy version.zip          gated × ungated × discount × no-discount
│   └── v4 - current (reference quality).zip the version inside "02 - Final Package v4"
│
└── 04 - Build Scripts (optional)/           ← only if you ever need to regenerate
    ├── build_briefs.js                      regenerates the two .docx briefs
    ├── build_docs.js                        regenerates the 4 supporting docs
    ├── transform_mailers.js                 produces the 28 mailers from reference
    ├── build_landing.js                     produces landing pages
    └── mailers_build_all_M1-M9.js           the older M1-M9 mailer generator
```

## What changed vs the old folder

**Removed (safe to delete from the unsorted folders):**
- `node_modules/` — 8.7 MB of npm dependencies, regenerable via `npm install docx`
- `Vahdam_Trustpilot_Funnel_Package/` — old uncompressed copy, superseded by v3/v4 zips
- Empty `.zip` files (`Vahdam_Trustpilot_Funnel.zip`, `Vahdam_Trustpilot_Funnel_Package.zip` — both 0 bytes)
- Temp zip leftovers (`ziKuCubF`, `zicZni4T`)
- `audit.jsonl` — 1.7 MB Claude session log, not your content
- `.claude/` — session metadata
- `uploads/` — was empty
- `package.json` / `package-lock.json` — only needed for re-running build scripts

**Kept and reorganized:**
- The original reference mailers (folder 01) — untouched, just renamed and copied
- The full v4 deliverable (folder 02) — restructured into self-explanatory subfolders
- All version zips (folder 03) — nothing lost, every iteration archived
- Build scripts (folder 04) — moved out of the root, kept for reproducibility

## Where to start by role

- **First-time reader** → `00 - START HERE.html`, then `02 - Final Package v4/index.html`
- **Lifecycle marketer** → `02 - Final Package v4/mailers/` + `supporting-docs/Klaviyo_ESP_Setup_Guide.docx`
- **Engineer** → `02 - Final Package v4/briefs/` + `backend/` + `supporting-docs/Trustpilot_Setup_Guide.docx`
- **Designer / brand** → `01 - Reference Mailers/` + `02 - Final Package v4/supporting-docs/Mailer_Ideation_and_Structure.docx`
- **CX / legal** → `02 - Final Package v4/reference-docs/gated-review-flow-guide.md` (compliance posture)

## Compliance note (important)

The v4 mailers include two CTA variants:
1. **Direct-to-Trustpilot** — fully compliant. Use freely.
2. **In-mailer star rating** — the pattern the reference's own `gated-review-flow-guide.md` calls *banned* under Trustpilot guidelines, FTC CRFA (US), and the UK DMCC Act 2025. Use only after legal sign-off.

Built it because the May 16 strategy session asked for it. Read `reference-docs/gated-review-flow-guide.md` before launching Variant 2.

## How to delete the old unsorted folders

After confirming everything you need is in this `00 - FINAL PACKAGE/` folder, you can safely delete:
- `Outout Variant 2/` (the unsorted original reference — its contents are in `01 - Reference Mailers`)
- `Output Variant 1/` (the unsorted working state — everything useful is in `02 - Final Package v4`)

That'll reclaim ~24 MB and leave you with a clean folder.
