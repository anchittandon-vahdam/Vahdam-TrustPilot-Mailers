# Vahdam Mailers — FINAL DELIVERABLE

The complete, final mailer package. Every mailer routes the same way: tap a star → 4+ goes to Trustpilot, 1–3 saves to our side.

---

## Folder map

```
Vahdam Mailers (FINAL DELIVERABLE)/
│
├── README.md                                ← you are here
│
├── Mailers - Minimal density/               ← 7 themes (A through G)
│   ├── A - Chai Morning Ritual.html
│   ├── B - Chai Pe Charcha.html
│   ├── C - A Few Cups In.html
│   ├── D - Connoisseur (Tasting Notes).html
│   ├── E - Honesty Trade.html
│   ├── F - Second Pour (backup, non-openers).html
│   └── G - One Last Thing (backup, openers no-click).html
│
├── Mailers - Lean density/                  ← same 7 themes, lean visual treatment
│
└── Documents/
    ├── 1 - Segments and Mailer Mapping.docx
    ├── 2 - Klaviyo Setup Guide.docx
    └── 3 - Trustpilot Integration and API.docx
```

**17 files total · 1 MB · no code, no extras.**

---

## How every mailer works

Each mailer has two sections:

**Top section (varies by theme A–G)** — the visual centerpiece that signals the cohort identity: hero image for the default mailer, speech bubble for the social mailer, three stat cards for the loyalty mailer, tasting-note card for the premium mailer, etc. This is where you signal *who this email is for*.

**Bottom section (identical across every mailer)** — five tappable stars under "Tap your rating". Each star is a tracked link to the backend.

When the customer taps a star:

| Rating | Where they go | What happens |
|---|---|---|
| **5 ★** | Trustpilot review page | Order metadata pre-filled. They write a public review. |
| **4 ★** | Trustpilot review page | Same as 5 — public review. |
| **3 ★** | Private feedback form on Vahdam | Rating saved on our side. They can add a note. |
| **2 ★** | Private feedback form + auto Zendesk ticket | We follow up within 24 hours. |
| **1 ★** | Private feedback form + auto Zendesk ticket | Same — human reaches out. |

The user only sees stars and the destination they arrive at — the gating happens server-side. They never see "you'd be routed differently if your rating were higher".

---

## The 7 themes (the "different mailer types")

Same 7 themes appear in both density folders. Same content, different visual treatments.

| Theme | Best for | Visual centerpiece |
|---|---|---|
| **A — Chai Morning Ritual** | Default — most customers | Hero image of steaming cup + light callout |
| **B — Chai Pe Charcha** | Conversational / social cohorts | Speech bubble showing an example review |
| **C — A Few Cups In** | Loyal repeat buyers | Three stat cards (cups in / months / reviews so far) |
| **D — Connoisseur** | Premium SKU buyers, brand advocates | Tasting note card (Aroma / Body / Finish / Verdict) |
| **E — Honesty Trade** | Customers who value directness | Two-sided callout (Our side + Your side) |
| **F — Second Pour** | Backup for non-openers (T+7 days) | Single pill badge — shortest mailer |
| **G — One Last Thing** | Backup for opened-no-click (T+10 days) | Acknowledgment box before the headline |

See **Document 1** for the segment-to-theme mapping (which customer segment receives which theme).

---

## Density choice

Every theme ships in both Minimal and Lean density. Content is identical; only the visual treatment differs.

**Minimal density** — clean white card on grey background. Subdued, the default.

**Lean density** — adds top/bottom black film-strip bars ("A QUICK NOTE" / "THAT'S THE WHOLE THING"), dark callout boxes, small cream accent notes. More crafted, slightly heavier.

A/B-test minimal vs lean within a cohort to find which density your audience responds to.

---

## The three documents

**1. Segments and Mailer Mapping** — Who gets which mailer theme, and why. Covers all 9 customer segments (S1 brand advocates through S9 refund/damage), send timing, frequency caps, suppression rules.

**2. Klaviyo Setup Guide** — Building the segments and flows in Klaviyo. Step-by-step segment conditions, the 7 flows with triggers and delays, throttling, A/B test setup, go-live phasing, testing checklist.

**3. Trustpilot Integration and API** — The technical guide. Trustpilot Business account setup, OAuth, the exact routing logic for each star (1 through 5), the backend API spec, code reference for the routing endpoint, reconciliation patterns, environment variables, and the compliance flag worth knowing before launch.

---

## Compliance flag

The in-mailer rating pattern (Variant 2 from earlier work) is the pattern Trustpilot's own Business Guidelines call banned. Same pattern is flagged by FTC CRFA (US) and UK DMCC Act 2025. **Document 3, Section 10** spells out the risk and mitigations.

This is a deliberate strategic choice — the meeting decision was to ship this pattern despite the risk. Mitigation: use Variant A (direct redirect, no Invitation API) initially, scope to small cohorts first, monitor for any Trustpilot communication and be ready to fall back to the compliant pattern within 24 hours of any signal.

---

Built 16 May 2026 · 17 files · 1 MB
