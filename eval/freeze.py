#!/usr/bin/env python3
"""Capture today's real inputs into a frozen corpus for deterministic replay.

Run it once a day; each run writes one day to eval/corpus/<day>.json. Nothing
is sent anywhere: it fetches the same public feeds/APIs the app uses and saves
the raw bodies so eval/replay.py can re-run without touching the network.

Usage:
    python eval/freeze.py                     # capture today
    python eval/freeze.py --day 2026-10-15
    python eval/freeze.py --synthetic         # also derive labelled stress days
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness as H  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", default=dt.datetime.now(dt.timezone.utc).date().isoformat())
    ap.add_argument("--synthetic", action="store_true",
                    help="also write labelled stress days derived from the capture")
    ap.add_argument("--max-articles", type=int, default=40)
    ap.add_argument("--lookback-hours", type=int, default=30)
    ap.add_argument("--no-compact", dest="compact", action="store_false",
                    help="keep raw HTML bodies (default: strip script/style blocks)")
    ap.set_defaults(compact=True)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    H.bootstrap()
    T = sys.modules["tipsofday"]
    T.ensure_dirs()
    cfg = T.Config.load()

    corpus = H.empty_corpus(args.day)

    def log(msg: str) -> None:
        if not args.quiet:
            print(msg)

    with T.HttpClient() as live:
        rec = H.RecordingClient(live)

        # --- market data -------------------------------------------------- #
        try:
            snap = T.fetch_market_data(list(T.ASSET_IDS), rec)
            corpus["market"] = {
                "assets": {s: {
                    "symbol": a.symbol, "coingecko_id": a.coingecko_id,
                    "price_usd": a.price_usd, "change_24h": a.change_24h,
                    "change_7d": a.change_7d, "volume_24h": a.volume_24h,
                    "market_cap": a.market_cap,
                } for s, a in snap.assets.items()},
                "fear_greed": snap.fear_greed,
                "fear_greed_label": snap.fear_greed_label,
                "btc_dominance": snap.btc_dominance,
            }
            log(f"market: {len(snap.assets)} assets, fear&greed={snap.fear_greed}")
        except Exception as exc:  # noqa: BLE001
            log(f"market FAILED: {exc}")

        # --- news feeds ---------------------------------------------------- #
        sources = T.load_sources(cfg.sources_file)
        corpus["sources"] = [{"name": s.name, "url": s.url, "lang": s.lang,
                              "reliability": s.reliability, "enabled": s.enabled}
                             for s in sources]
        ingest = T.ingest_news(sources, rec, lookback_hours=args.lookback_hours,
                               custom_urls=[], max_articles=args.max_articles)
        log(f"articles: {len(ingest.articles)} (failed sources: {len(ingest.failed)})")

        for art in ingest.articles:
            corpus["articles"].append({
                "title": art.title, "url": art.url, "source": art.source,
                "lang": art.lang, "reliability": art.reliability,
                "age_hours": round(art.age_hours(), 2),
            })
            # capture the article body when the pipeline would fetch it
            if art.url not in corpus["bodies"]:
                try:
                    corpus["bodies"][art.url] = rec.get_text(art.url, check_robots=True)[:200_000]
                except Exception:  # noqa: BLE001
                    pass

    corpus["bodies"] = rec.bodies
    corpus["failed"] = [[n, e] for n, e in ingest.failed]

    if args.compact:
        before = sum(len(v) for v in corpus["bodies"].values())
        H.compact_corpus(corpus)
        after = sum(len(v) for v in corpus["bodies"].values())
        log(f"compacted bodies: {before / 1e6:.1f}MB -> {after / 1e6:.1f}MB "
            f"(extracted text unchanged)")

    out = H.save_corpus(corpus, H.CORPUS_DIR / f"{args.day}.json")
    log(f"wrote {out}  ({len(corpus['bodies'])} bodies, "
        f"{len(corpus['articles'])} articles)")

    if args.synthetic:
        for name, day in H.synth_days(corpus).items():
            p = H.save_corpus(day, H.SYNTH_DIR / f"{args.day}-{name}.json")
            log(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
