# LEGAL_NOTES

> **Not legal advice.** These are engineering notes collected to make the product's
> posture deliberate. Before charging money in any jurisdiction, have a qualified lawyer
> review the product, the disclaimers and the store terms. Nothing here is a legal
> conclusion.

## 1. What the app does and does not do

It **does** summarize public news and public market data and describe which asset the
news flow points at, with a confidence level and risks.

It **does not** predict prices, recommend buying or selling, produce price targets, size
positions, or claim any return. These are enforced in the system prompt and by a
post-generation filter (`enforce_grounding`) that drops advice-like phrasing; the filter's
behaviour is measured in `eval/RESULTS.md`.

## 2. Why that framing matters

In several jurisdictions, telling the public what to buy or sell is a regulated activity:

- **Brazil (CVM).** Recommending securities/investments to the public can constitute
  activity requiring CVM authorization (e.g. the analyst/consultant regimes and the rules
  on public offering and investor communication). Crypto-asset regulation in Brazil has
  been evolving through the CVM and the central bank; a lawyer should confirm the current
  perimeter before monetising.
- **United States (SEC/CFTC).** Investment advice to others for compensation can trigger
  adviser/regulator requirements. News commentary is not investment advice, but the line
  must not be crossed by wording or by personalization.
- **European Union (MiCA + MiFID II).** MiCA covers crypto-asset service providers;
  MiFID II covers investment advice. Personalized recommendations carry the heaviest
  obligations.

The product's wording (pt-BR and EN) is written to stay on the "informational" side of
these lines, but *only a lawyer in the relevant jurisdiction can confirm* that it does.

## 3. In-app disclaimer text (shipped in every briefing)

**pt-BR**

> AVISO: conteudo apenas informativo, nao e recomendacao de investimento. Criptomoedas
> sao altamente volateis e voce pode perder todo o capital. Nao ha garantia de retorno.
> Faca sua propria pesquisa (DYOR). Este destaque e baseado em sinal de noticias, nao em
> previsao de preco.

**EN**

> DISCLAIMER: informational only, not investment advice. Crypto is highly volatile and
> you can lose all of your capital. No returns are guaranteed. Do your own research
> (DYOR). This focus asset is based on news signal, not a price prediction.

## 4. Copyright and data sources

- Only RSS/Atom excerpts and short paraphrased summaries are produced. **No full article
  is republished.** The pipeline stores excerpts locally only, does not republish article
  bodies, and links back to the source.
- `robots.txt` is respected for direct article fetches, a descriptive `User-Agent` is set,
  requests are rate-limited and cached. Users choosing unusual sources are responsible for
  those sources' terms of use.
- Market data comes from public APIs (CoinGecko, alternative.me). Each has its own terms;
  a commercial deployment should review them (rate limits, attribution, and any
  free-tier restrictions). Source names and links always appear in the output.

## 5. Open-core and licensing

- The repository is Apache-2.0. **Model weights are not bundled**: the app names a model
  and the user's own runtime downloads it. This keeps third-party weight licenses out of
  this repository.
- If you ever bundle weights: Apache-2.0 models (Gemma 4, Qwen3) can be redistributed with
  the usual Apache notices. **Gemma 1–3** require the Gemma Terms notice file, a copy of
  the agreement, and pass-through of the Prohibited Use Policy. **Llama** requires the
  "Built with Llama" attribution and has a 700M-MAU clause. Details in `DECISIONS.md`.
- Pro licensing uses a signed key with a 14-day offline grace period and no telemetry.
  No personal data is collected or transmitted by the app.

## 6. Pre-launch checklist for charging money

1. Have a lawyer review the output wording and the disclaimer for your target markets.
2. Confirm your store's (Lemon Squeezy / Gumroad / Paddle) terms and your tax setup — they
   act as merchant of record.
3. Add Terms of Service and a Privacy Policy to the product page: state clearly that no
   data leaves the user's machine.
4. Keep the "not investment advice / DYOR" disclaimer in the CLI output AND on the
   landing page, in both languages.
5. Keep a record of the model licenses and versions you ship against.
