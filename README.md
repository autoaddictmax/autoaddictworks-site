# autoaddictworks.com — website source

Static site: fast, no CMS or plugins to maintain. Lighthouse (local test): Performance 99 · SEO 100 · Accessibility 98–99 · Best Practices 100.

## Before launch — fill in `config.json`
- `phoneDisplay` / `phoneE164` → the Works phone number, then set `phoneIsPlaceholder: false`
- `hours` → real hours, then `hoursArePlaceholder: false`
  (phone and hours are left OUT of the Google schema markup until these flags are false, so placeholders never reach Google)
- `email` → the address customers should see
- `bookingUrl` → optional ShopBoss/online booking link (otherwise "Book Service" goes to /contact/)
- `formEndpoint` → where contact-form and build requests POST as JSON (GHL inbound webhook, Make.com, n8n, Formspree…). Empty = the form opens the visitor's email app instead.
- `social` → Instagram / Facebook / Google Business Profile URLs (added to schema `sameAs`)

Then run `python3 build.py` → upload the `dist/` folder.

## Hosting (pick one, all free for a site this size)
- **Cloudflare Pages** or **Netlify**: drag-and-drop `dist/`, point autoaddictworks.com DNS at it. `_headers` (caching) is already included.
- Any static host works (S3, GitHub Pages, cPanel).

## After launch — the SEO steps that matter most
1. Google Search Console: verify the domain, submit `https://autoaddictworks.com/sitemap.xml`.
2. Google Business Profile (repair): website = https://autoaddictworks.com, primary category "Auto repair shop", add "Car repair and maintenance service", "Auto tune up service", etc. Name/address/phone must match the site exactly.
3. Add real shop photos (cars on the lift, ISTA screen, the 340i) — the biggest content upgrade left.
4. Ask every happy customer for a Google review.

## Editing
- Page copy: `content.py`
- Build planner platforms, tiers, parts, prices: `static/js/builder-data.js`
- Styles: `static/css/site.css` (tokens match the brand design system)
- `python3 build.py --preview` makes a `preview/` copy with relative links (opens straight from disk).
