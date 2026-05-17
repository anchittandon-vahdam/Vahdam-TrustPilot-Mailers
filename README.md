# Vahdam TrustPilot Final Mailers For Customer Reviews

The single canonical source for the Trustpilot review-collection mailers. Everything we ship lives here. Future changes happen in this folder only.

Read **DEPLOYMENT GUIDE.md** for what goes where.

---

## What's in this folder

```
Vahdam TrustPilot Final Mailers For Customer Reviews/
│
├── README.md                                  ← you are here
├── DEPLOYMENT GUIDE.md                        ← Klaviyo vs vahdam.com — read first
│
├── Mailers/                                   ← 7 files · upload to Klaviyo
│   ├── A - Chai Morning Ritual.html              S3, S5 (active subs + repeat)
│   ├── B - Chai Pe Charcha.html                  S4 (first-time buyers)
│   ├── C - A Few Cups In.html                    S2 (loyalty VIPs)
│   ├── D - Connoisseur (Tasting Notes).html      S1, S6 (advocates + premium)
│   ├── E - Honesty Trade.html                    S7 (recently cancelled)
│   ├── F - Second Pour (backup).html             non-openers, T+7
│   └── G - One Last Thing (backup).html          opened-no-click, T+10
│
├── Landing pages/                             ← 2 files · deploy to vahdam.com
│   ├── private-feedback.html                     for ratings 0.5–3.5
│   └── thank-you.html                            confirmation after submission
│
└── Documents/                                 ← strategy + setup guides (.docx)
    ├── 1 - Segments and Mailer Mapping.docx      who gets what
    ├── 2 - Klaviyo Setup Guide.docx              how to wire up Klaviyo
    └── 3 - Trustpilot Integration and API.docx   the routing + API side
```

12 files. Single source of truth.

---

## How the routing works

Every mailer has a star widget at the bottom — visually 5 stars, actually 10 click zones (each star split into two halves) so users can rate in 0.5 increments.

| User taps | Destination |
|---|---|
| 0.5 to 3.5 stars | `vahdam.com/pages/private-feedback?rating=N&token=...` |
| 4 / 4.5 / 5 stars | `trustpilot.com/evaluate/vahdamteas.com?orderId=...` |

The mailer never tells the user where their rating ends up. The landing page is Vahdam-branded — no Trustpilot mention. The user feels every rating goes to the same place.

---

## What you do with this folder

For Klaviyo (one-time setup):

1. Upload each of the 7 files in `Mailers/` as a Klaviyo email template
2. Build the 9 segments and 7 flows per `Documents/2 - Klaviyo Setup Guide.docx`
3. Set subject lines (A and B variants are in HTML comments at the top of each mailer)
4. Test send to yourself; tap a star; verify the destination URL

For vahdam.com (one-time setup):

1. Create a Shopify page at `/pages/private-feedback` with the contents of `Landing pages/private-feedback.html`
2. Create a Shopify page at `/pages/feedback-thanks` with the contents of `Landing pages/thank-you.html`
3. Wire the form's submit handler to your backend

For Trustpilot (no setup needed):

Clicks on 4–5 stars go directly to Trustpilot's own review form. No deployment from you.

---

## Future changes go HERE

This is now the canonical folder. Any future updates to mailers, landing pages, copy, segments, or docs will happen in this folder, get pushed to the GitHub repo as a single commit, and need to be re-uploaded to your Drive.

The previous folders (`Vahdam Mailers (SHIPPING)`, `Vahdam Mailers (READY)`, `00 - FINAL PACKAGE`, etc.) are now obsolete and can be deleted from your Desktop.

---

Built 17 May 2026 · canonical · 12 files.
