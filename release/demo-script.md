# tipsofday — 60–90 second demo script

Goal: prove, on camera, that the *thinking* is local, the numbers are grounded, and the
app refuses to invent a pick. Everything below runs on the presenter's laptop.

**Pre-flight (do this before recording):**

```bash
# model is pulled and the server is warm
ollama pull gemma4:e4b
tipsofday doctor          # should end with "ok" for model + feeds
tipsofday run --refresh   # warm up once so the demo is not the cold-load run
```

Have two terminals open, both at the project root, with a large font.
Have a screenshot of the checkout/pricing page ready in case you cut for time.

---

## Shot list

### 0:00 — 0:08 · What it is (talking head or title card)

> "tipsofday writes a daily crypto briefing with a local, open-weight model. Nothing about
> your watchlist leaves this laptop."

Show the terminal with `tipsofday doctor` output still on screen (hardware + model lines).

### 0:08 — 0:18 · Prove the AI is local: airplane mode

Turn on airplane mode (or disable Wi‑Fi/Ethernet) **on camera**.

```bash
ollama ps         # the model is running locally
```

> "The model is on this machine. The internet is off."

*Do not run the briefing yet* — the news and price fetch still needs the network; that is
the honest framing. The point being shown is that the *model* is local.

### 0:18 — 0:30 · Turn the network back on and run it

Re-enable the network, then:

```bash
tipsofday run --refresh --lang en
```

Let it stream; ~10–25 s on a small GPU (longer on CPU). While it runs, say:

> "It reads today's feeds, fetches prices from CoinGecko, and a Gemma 4 model on this
> machine writes the briefing — one sentence at a time."

### 0:30 — 0:52 · Read the briefing on screen

Walk the rendered panel:

- **market mood** — one or two sentences, no advice;
- **top stories** — with the source and a link;
- **asset in focus** — the ticker, *why*, the **confidence**, the **risks**, and
  **what would invalidate it**;
- point at the footer **disclaimer**.

> "It never says buy or sell, never gives a price target. Every number you see comes from
> the market API, not from the model — anything the model makes up is stripped before it
> reaches the screen."

### 0:52 — 1:04 · Show the guardrail *and* the "no signal" honesty

```bash
python eval/replay.py --backend mock --all     # instant, deterministic
```

Highlight in the summary: `injection_hits_total: 0`, `banned_after_filter_total: 0`,
`no_signal_correct_rate: 1.0`.

> "The test set includes a prompt-injection article that says 'ignore all previous
> instructions' and a sponsored '100x' shill post. Neither survives. And when there is not
> enough signal — thin news, negative news — it says 'no clear signal' instead of picking."

If you have a day where the model returned no signal, show it here.

### 1:04 — 1:16 · Show the track record (the honest part)

```bash
tipsofday track
```

> "It keeps a local SQLite history and compares the focus asset with just holding BTC —
> including when it loses. Right now the record has only a few closed days, so it prints a
> warning that the sample is too small to mean anything. That honesty is the feature."

### 1:16 — 1:25 · Price and close

Show the pricing page / `tipsofday status`.

> "Free gives you one briefing a day; Pro is $7 a month for the custom watchlist, history,
> export and scheduling. The core is Apache-2.0 on GitHub — link below."

---

## 90-second compressed variant

If you only get 90 seconds total, drop shots 0:52 and 1:04 to five seconds each and cut
the talking-head sections to one line:

1. Airplane mode + `ollama ps` — 10 s
2. Network on, `tipsofday run --lang en` — 25 s
3. Read the briefing, point at confidence/risks/invalidation/disclaimer — 25 s
4. `python eval/replay.py --backend mock --all` → `injection_hits_total: 0` — 10 s
5. `tipsofday track` → the small-sample warning — 10 s
6. Price + "Apache-2.0 on GitHub" — 10 s

---

## Audio/quiet alternative (30–45 s, no voice)

A silent loop for a DEV post or README: record only the terminal, with on-screen captions:

1. "model runs on this laptop →" (`ollama ps`)
2. "one command →" (`tipsofday run --lang en`)
3. "numbers come from the API, not the model →" (briefing panel)
4. "injection + shill test set → 0 hits →" (`eval/replay.py` summary)
5. "it says 'no clear signal' when honest →" (briefing or results table)

Export as GIF/MP4 at 12–15 fps and keep it under 8 MB for a README embed.
