# Pricing & store setup

## Pricing table

| | **Free** | **Pro** |
|---|---|---|
| Price | $0 | **$7 / month** or **$49 / year** (2 months free) |
| Briefings per day | 1 | Unlimited (`--refresh`) |
| Assets considered | top 10 (default watchlist) | unlimited watchlist |
| Languages | pt-BR + EN | pt-BR + EN |
| Custom news sources | – | ✅ |
| Include your own article links | – | ✅ |
| History (`tipsofday history`) | – | ✅ |
| Track record (`tipsofday track`) | – | ✅ |
| JSON / Markdown export | – | ✅ |
| Scheduling helper | – | ✅ |
| Runs fully offline / local | ✅ | ✅ |
| Telemetry | none | none |

Notes for testing price: benchmark competitors at $5–15/month for market newsletters. The
$49/year tier converts better for a daily tool. Both numbers live in
`~/.config/tipsofday/config.json` under `pricing`, never hardcoded in logic.

## What to sell (and what not to)

Sell **time saved** and the **honest track record**, not predictions:
> "Two minutes instead of twenty sites, and a log of how each call actually did — not a
> promise that it will be right."

Do not market it as investment advice. The disclaimer ships in the app and must stay on
the landing page in both languages (see `LEGAL_NOTES.md`).

## Product IDs

`config.json` holds the store product IDs:

```json
{
  "product_ids": {
    "lemonsqueezy_pro_month": "REPLACE_ME",
    "lemonsqueezy_pro_year": "REPLACE_ME",
    "gumroad_pro_month": "REPLACE_ME",
    "gumroad_pro_year": "REPLACE_ME"
  },
  "license_server": ""
}
```

---

## Lemon Squeezy setup (recommended — merchant of record, VAT handled)

1. Create a store at <https://lemonsqueezy.com> and complete the tax/business details.
   Lemon Squeezy is the merchant of record: they collect and remit sales tax/VAT.
2. **Products → New product**. Create two products: *tipsofday Pro (monthly)* and
   *tipsofday Pro (yearly)*. Set a license-key "activation limit" (e.g. 3 devices).
3. Enable **License keys** on each product (Settings → Licenses, then per-product).
4. Copy each product's ID into `config.json` (`lemonsqueezy_pro_month` /
   `lemonsqueezy_pro_year`).
5. **Checkout → success**: point buyers to the install page and tell them to run
   `tipsofday activate <KEY>` with the key Lemon Squeezy emails them.
6. **Webhooks (optional):** add a webhook for `subscription_created` /
   `subscription_cancelled` only if you later add a server-side revalidation endpoint
   (`license_server`). With `license_server` empty the app is fully offline and the signed
   key plus the 14-day grace period is the whole story.

To issue a key by hand (support, refunds, friends):

```bash
tipsofday license-keygen release/vendor/private_key.pem --email user@example.com --days 365
```

Keep `release/vendor/private_key.pem` out of the repo (already in `.gitignore`) and back it
up somewhere safe — losing it means you cannot issue new keys.

## Gumroad setup (simpler, also merchant of record)

1. Create the two products at <https://gumroad.com>. Enable **"Generate a unique license
   key for each sale"** under the product's *Content/License* settings.
2. Gumroad keys are verified by Gumroad's own API, not by the embedded Ed25519 public key.
   To support Gumroad keys, set `license_server` to a tiny endpoint you run that proxies
   Gumroad's `/v2/licenses/verify`, and keep the Ed25519 path for direct sales.
3. Copy product IDs into `config.json` (`gumroad_pro_month` / `gumroad_pro_year`).

If you would rather not run any server, offer **Lemon Squeezy only**: it is the cleanest
offline story (signed key, no server, 14-day grace).

## Paddle

Same shape as Lemon Squeezy (merchant of record, license keys via API). Paddle requires
more onboarding and is aimed at larger volumes; skip it until you have sales.

## Launch checklist

- [ ] Landing page with the disclaimer in pt-BR **and** EN.
- [ ] Terms of Service + Privacy Policy ("no data leaves your machine").
- [ ] Both products live, license keys enabled, product IDs in `config.json`.
- [ ] Install guides published (see `release/install-*.md`).
- [ ] Demo video / GIF on the page (script in `release/demo-script.md`).
- [ ] A support email and a refund policy.
- [ ] Lawyer review of the wording (see `LEGAL_NOTES.md` §6).
