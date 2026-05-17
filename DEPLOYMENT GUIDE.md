# Deployment Guide — what goes where

Two surfaces. Two deployment paths. The mailer is the inbox; the landing page is the website.

---

## TL;DR

| File | Where it goes | How |
|---|---|---|
| `Mailers/A - Chai Morning Ritual.html` | Klaviyo | Upload as an email template |
| `Mailers/B - Chai Pe Charcha.html` | Klaviyo | Upload as an email template |
| `Mailers/C - A Few Cups In.html` | Klaviyo | Upload as an email template |
| `Mailers/D - Connoisseur (Tasting Notes).html` | Klaviyo | Upload as an email template |
| `Mailers/E - Honesty Trade.html` | Klaviyo | Upload as an email template |
| `Mailers/F - Second Pour (backup, non-openers).html` | Klaviyo | Upload as an email template |
| `Mailers/G - One Last Thing (backup, openers no-click).html` | Klaviyo | Upload as an email template |
| `Landing pages/private-feedback.html` | vahdam.com | Shopify page at /pages/private-feedback |
| `Landing pages/thank-you.html` | vahdam.com | Shopify page at /pages/feedback-thanks |

7 files into Klaviyo. 2 files into your Shopify (or wherever vahdam.com is hosted).

---

## Why two different places — short version

The mailer is what the customer sees inside Gmail / Outlook / Apple Mail. Email is a **read-only sandbox** — it can't run JavaScript, most CSS is stripped, forms can't submit. So the mailer can only contain:

- Static HTML
- Inline images (the hero photos + star halves are all base64-embedded — confirmed self-contained)
- Links that go somewhere else

The landing page is what the customer sees **after they click a star in the email**. That's a real web page on `vahdam.com` — JavaScript runs, forms submit, the rating widget shows live hover preview, the customer can type a note. None of that works inside an inbox.

Trying to put the landing page inside the mailer would mean:
- The hover-to-preview rating widget would stop working (no `:hover` reliable in email)
- The form would never submit (Gmail blocks form actions from email)
- The live rating display would never update (no JavaScript in email)

So the architectural split is forced by how email clients work, not by anything I can change.

---

## What's in each mailer file (everything you need for Klaviyo)

Each of the 7 HTML files in `Mailers/` is **a single self-contained file** with:

- The full email HTML body
- All images embedded as base64 data URIs — no CDN dependency, no broken-image risk
  - Hero photos for A, C, D
  - Star half-icons (10 of them per mailer — the 5-star rating widget)
- One Google Fonts CSS `<link>` for Cormorant Garamond + Montserrat (Klaviyo handles this; the fallbacks `Georgia` + `Helvetica` cover any client that strips it)
- All merge tags Klaviyo expects: `{{ first_name|default:'there' }}`, `{{ last_product_purchased }}`, `{{ token }}`, `{{ order_id }}`, `{{ email }}`, etc.
- A/B subject lines as HTML comments at the top — copy these into Klaviyo's split test config

That's it. Each file is 30–80 KB total. Open one in a browser to preview it. Drag it into Klaviyo's template editor and you're done.

---

## What's in each landing page file

`Landing pages/private-feedback.html` — the page customers arrive at when they tap a star rated 0.5–3.5. It contains:

- The rating widget (10 hit zones across 5 visual stars, with live hover preview)
- A pre-fill — when the URL has `?rating=2.5`, the page initializes with 2.5 stars locked in
- A free-text box and an opt-in checkbox
- A submit handler that posts to your backend (currently stubbed; production needs to wire to your actual `/v1/feedback/private` endpoint or whatever Vahdam's stack uses)

`Landing pages/thank-you.html` — what they see after submitting the private feedback form.

---

## How to upload mailers to Klaviyo

1. Klaviyo → Email Templates → Create new template → "Drag & drop editor" → switch to "HTML editor" view.
2. Copy-paste the entire contents of `Mailers/A - Chai Morning Ritual.html` (or whichever).
3. Save with a name matching the file (e.g., "TP Funnel — A Chai Morning Ritual").
4. Set up the flow that triggers this template (see Klaviyo Setup Guide.docx in Documents/).
5. Set the subject line — pick A or B from the HTML comments at the top of the file.
6. Send yourself a test.
7. Repeat for B through G.

---

## How to deploy landing pages to vahdam.com

On Shopify (which is most likely where vahdam.com lives):

1. Shopify Admin → Online Store → Pages → Add page.
2. Title: "Tell us about your last order".
3. Click "Show HTML" (the `<>` icon in the editor toolbar).
4. Paste the entire contents of `Landing pages/private-feedback.html`.
5. URL handle: `private-feedback` (so the final URL is `vahdam.com/pages/private-feedback`).
6. Save and publish.
7. Repeat for `thank-you.html` at handle `feedback-thanks` (URL: `vahdam.com/pages/feedback-thanks`).

If you're using a different platform, the principle is the same — these are plain HTML pages with a JavaScript form. Drop them onto any page hosting that accepts custom HTML.

**The mailer URLs point to these exact paths:**
- `https://vahdam.com/pages/private-feedback?rating=...` ← for ratings 0.5–3.5
- `https://vahdam.com/pages/feedback-thanks` ← after submission

If your Shopify URL structure differs (e.g., `/pages/feedback` instead of `/pages/private-feedback`), you'll need to update the 7 private-feedback URLs in each mailer to match. The find-and-replace is straightforward — search for `vahdam.com/pages/private-feedback` and swap.

---

## What's NOT a deployment concern

**The Trustpilot URL.** Ratings 4, 4.5, 5 link to `https://www.trustpilot.com/evaluate/vahdamteas.com?orderId=...` — this is Trustpilot's standard review form for the vahdamteas.com business unit. No deployment needed; the page already exists on Trustpilot's side.

**Hero images for mailers A, C, D.** Base64-embedded in each mailer file. No CDN to set up.

**The star half-images.** Also base64-embedded.

**Web fonts.** The Google Fonts `<link>` in the `<head>` of each file fetches Cormorant Garamond + Montserrat from Google's CDN. Klaviyo and most email clients handle this fine. If your sender domain blocks fonts.googleapis.com (uncommon), the fallback stack — `Georgia, 'Times New Roman', serif` and `Helvetica, Arial, sans-serif` — kicks in automatically.

---

## Final pre-launch checklist

For each of the 7 mailers in Klaviyo:

- [ ] Subject lines A and B set as a 50/50 split test
- [ ] Merge tags substituting correctly in test sends (no `{{first_name}}` literals leaking)
- [ ] Tested in Litmus or Email on Acid across Gmail, Outlook, Apple Mail, mobile
- [ ] Star widget renders as 5 stars (not 10 stars in a row — that means the base64 images failed to load)
- [ ] Each star is independently clickable (tap one in the actual sent email, confirm the URL has the expected `rating=` value)
- [ ] Suppression segments (S8, S9) excluded from the flow
- [ ] Throttling (`last_funnel_send`) configured per the Klaviyo Setup Guide

For the landing pages on vahdam.com:

- [ ] `/pages/private-feedback` returns the rating widget page
- [ ] URL with `?rating=2.5` pre-fills the rating correctly
- [ ] Hover preview works (move cursor across stars, verify the big "2.5 stars" updates live)
- [ ] Form submission posts to your backend successfully
- [ ] `/pages/feedback-thanks` displays the confirmation
- [ ] Page tested on mobile (cursor-hover doesn't exist on mobile — tapping should still work for setting rating)

When all the above pass, you're ready to send the first campaign.
