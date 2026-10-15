---
title: tipsofday — a daily crypto briefing written on your own laptop by a local Gemma model
published: false
tags: devchallenge, hf26challenge, ai, opensource
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12)*

> **One-line pitch:** a `pipx install`-and-go CLI that turns today's crypto news into a
> short, source-linked briefing — written by an open-weight model on your machine, for
> **$0.00** a day, with your watchlist never sent to anyone.

---

## What I Built

Every morning, thousands of people who write crypto newsletters, run trading Discords, or
just hold a bag start the day the same way: opening twenty browser tabs, skimming the same
five headlines, and trying to work out *what actually matters today*.

**tipsofday** does that reading for them. You run one command:

```bash
tipsofday run --lang en
```

and it reads today's crypto feeds, pulls real prices from public APIs, and a **Gemma 4**
model running locally writes a briefing: the day's mood, the top stories with sources, one
asset with the strongest *news signal* today, **why**, a **confidence level**, the **risks**,
and **what would invalidate the call**. When the news flow is thin or contradictory it says
**"No clear signal today"** instead of inventing a pick.

**Who would pay for it?** The person who already pays with their time. A newsletter writer
who spends 45 minutes aggregating headlines before writing 400 words would pay to have that
first pass done before coffee. A small trading community that wants a private morning note
without a $50/month "AI research" seat — and, more to the point, without its watchlist,
positions, or client names leaving the laptop.

It is deliberately **not** investment advice: it never says buy or sell, never gives a price
target, and every briefing ends with a disclaimer. It is a *news summariser with guardrails*,
and the guardrails are the product.

**[→ Read the full README](https://github.com/tipsofday/tipsofday#readme)** ·
**[→ The honest eval report](https://github.com/tipsofday/tipsofday/blob/main/eval/RESULTS.md)**
<!-- Replace the repo URL with your own once the repository is public. -->

---

## Demo

There is no hosted link, and that is the point — the model runs on *your* hardware, so a
"deployed demo" would be a different product. The demo is a 60–90 second screen recording
following [`release/demo-script.md`](https://github.com/tipsofday/tipsofday/blob/main/release/demo-script.md):
airplane mode on, `ollama ps` proves the model is local, network back on, `tipsofday run`
streams a briefing, then `eval/replay.py` shows the guardrails firing.

A text stand-in for the video — the real render, pt-BR by default, English with `--lang en`:

```
╭──────────────────── Destaque do dia ──────────────────────────╮
│ BNB   confianca: media                                        │
│                                                               │
│ Por que                                                       │
│  · Fluxo de noticias positivo nas ultimas 24h.                │
│  · Volume 24h de $1.9B acima do piso de liquidez.             │
│                                                               │
│ Riscos                                                        │
│  · Movimento puxado por noticia pode ja estar precificado.    │
│                                                               │
│ O que invalidaria isto                                        │
│  · Virada na narrativa dominante ou dados que contradigam.    │
╰───────────────────────────────────────────────────────────────╯
```

Reproduce it yourself in three commands: `ollama pull gemma4:e4b`, `pipx install .`,
`tipsofday run --refresh --lang en`.

<!-- TODO before publishing: paste the video/GIF link here and embed it. -->

---

## Code

Apache-2.0. The whole application is one readable Python file
(`tipsofday.py`, ~2,300 lines) so it can be audited in one sitting and split later. Tests,
the replay harness, and the release copy are in the same repo.

```text
{% embed https://github.com/tipsofday/tipsofday %}
```

- `tests/` — **21 offline unit + integration tests** (no network, no model). CI on GitHub
  Actions, Python 3.11–3.14.
- `eval/` — `freeze.py` (capture a day), `replay.py` (serves frozen HTTP bodies back through
  the *real* pipeline), `backtest.py`, and `RESULTS.md`.
- `DECISIONS.md` — every notable choice, with the benchmark behind it.
- `LEGAL_NOTES.md` — why this is an information tool and where the regulatory lines are.

---

## How I Built It

**The open-source AI is the core, not a garnish.** Every sentence the user reads is written
by an open-weight model running through **Ollama**, defaulting to **`gemma4:e4b`**
(Apache-2.0, ~6.6 GB Q4). The entire model layer sits behind one `LLMBackend` interface, so
Ollama, a `llama.cpp` GGUF, or an offline `MockBackend` are drop-in swaps — and the tests use
the mock so CI never needs a GPU.

The pipeline is **map–reduce**: each article is mapped to a structured insight (assets,
event, sentiment, one-line summary), then reduced in plain Python into a weighted sentiment
per asset (source reliability × recency), and one final call writes the briefing JSON.

Five design rules hold it together, and each one exists because something broke without it:

1. **Numbers come from APIs, never from the model.** Every number in the output is checked
   against the market snapshot; sentences with ungrounded numbers are dropped.
2. **Web text is data, never instructions.** Article text is sanitised and wrapped in
   delimiters before it reaches the model.
3. **The pick is capped.** No micro-caps or illiquid tokens can become the focus asset.
4. **"No clear signal today" is a valid answer** — and the correct one when news is thin.
5. **Local SQLite history** makes a track record possible, and the track record refuses to
   publish a percentage until the sample is big enough.

### What the measurements actually said

I built a replay harness that feeds *frozen* HTTP bodies back through the real pipeline, so
the numbers are reproducible offline. Full detail, including everything that went wrong, is
in [`eval/RESULTS.md`](https://github.com/tipsofday/tipsofday/blob/main/eval/RESULTS.md).
The short version, on an RTX 5050 (8 GB):

| | English | pt-BR |
|---|---:|---:|
| Valid JSON, per call | **1.00** | **1.00** |
| Prompt-injection artefacts that reached the output | **0** | **0** |
| Advice-like phrases that survived the filter | **0** | **0** |
| Correctly declined on the thin-news day | **yes** | **yes** |
| Mean latency per briefing | 22.9 s | 24.3 s |
| Cost in API spend | **$0.00** | **$0.00** |

Two findings I would rather not print, but a review that hides them is not a review:

- **A guardrail silently disabled the product.** The model kept naming BTC (negative news ⇒
  ineligible), so the app returned "no clear signal" on **6 of 6 days**. Safe, and useless.
  I added a single eligibility retry; it now picks on 4 of 6 in English. In Portuguese it
  barely fires and still declines on 5 of 6. That instability is itself the finding: a 4B
  model's judgement is language-dependent, so the output is framed as a **news summary**, not
  a signal.
- **It is honestly measured on n = 1 real day.** One captured day plus five derived stress
  probes (red/bull, injection, shill, thin) — the probes test guardrails, not accuracy, and
  the report says so in its own "threats to validity" section. The backtest prints
  *"nothing honest to report"* while it has zero closed outcomes.

I also found and fixed a **bug in my own metric** (it counted numbers in fields the pipeline
throws away) and a **bug in my own corpus** (the "thin day" was also wiping market data).
Both are documented in `RESULTS.md` rather than quietly corrected.

---

## Why Does Open Innovation Matter?

Because this specific product does not work as a closed one.

- **The economics only work at zero.** A briefing costs **$0.00** in API spend; the
  cloud-equivalent is ≈ **$0.003**. That is a rounding error *per call* and a business
  decision *per user per day*. An open-weight model on hardware the user already owns is the
  difference between "a nice side project" and "a $7/month tool with a margin".
- **The promise is privacy, and only local inference can keep it.** tipsofday's whole pitch
  is that a writer's watchlist, positions and client names *never leave the laptop*. The
  fetch needs the internet; the **thinking does not**. You cannot promise that with a hosted
  API.
- **No lock-in, by construction.** The model is one interface away. Fork it, swap Gemma for
  Qwen or Llama, fine-tune for a niche, run it on a Raspberry Pi — the code does not care.
  When a vendor changes its price or its policy, no one's workflow breaks.
- **Auditable beats trust-me.** Open weights plus open code means the guardrails are
  reviewable, the prompt is readable, and the eval harness can be re-run on your machine —
  which is exactly why I could report the failure above instead of hiding it.
- **Open weights are the reason a Dutch-angle niche is even possible.** A 4B model on a
  gaming laptop can be shaped with a prompt and a filter into something dependable for one
  narrow job. That is open innovation working: not a bigger model, a *smaller, owned* one.

---

## My Agent Session

<!-- Optional, but judges love it. Save your session with DevRelay and embed it with the
     agent_session tag, or link to it. TODO: attach the DevRelay agent session for this build. -->

The build was done agent-first: the whole app was written against a written spec
(`PROMPT.md`), the model layer and guardrails were benchmarked before being trusted, and the
evaluation harness was built to try to *falsify* the product rather than flatter it. The
session is being saved with DevRelay; I will embed it here before publishing.

---

## My First User

I do not have a paying user yet, and I would rather say that than dress up a user test as
one. Here is the honest state and the plan:

- The tool is installable today (`pipx install .`) and runs on an 8 GB laptop GPU.
- The first real test is scheduled with a friend who writes a small paid crypto newsletter —
  the exact person in "What I Built". The question I want to ask them is not "do you like
  it?" but *"does this replace the 45 minutes you spend before you write?"*
- The Pro tier ($7/month: custom watchlist, history, JSON/Markdown export, scheduling) is
  already implemented, so if the answer is yes, the conversion path exists — no rebuild
  required.

If that changes before the deadline, this section changes with it.

---

## Prize Categories

- **Best Use of Gemma** — the briefings are written entirely by
  **`gemma4:e4b`** (Google's open-weight Gemma 4, Apache-2.0), served locally through
  Ollama. Gemma is not a helper here; it is the writer. Everything else in the pipeline
  exists to keep Gemma honest: verified numbers, sanitised inputs, and a filter that drops
  anything the model invents.

No other partner technology is used, so no other category is claimed.

---

*Information tool only — not financial advice. tipsofday does not predict prices and does
not tell anyone what to buy or sell. It reports which asset today's news flow points at, and
shows its work.*

---

*This article was written by me with help from an AI coding agent, and I have checked every
number in it against the committed files in the repository (`eval/RESULTS.md` and the raw
JSON in `eval/`).*
