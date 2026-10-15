#!/usr/bin/env python3
"""Backtest the "asset in focus" against BTC buy-and-hold and a random pick.

Two modes:

  --live-history        read the app's own SQLite history (what really happened
                        on this machine) and compare each day's focus return
                        with BTC over the same window.
  --replay FILE...      for each corpus day with a `forward` block (close prices
                        N days later, captured by `eval/freeze.py --forward`),
                        compare focus vs BTC vs a deterministic random pick.

Honesty rules baked in:
  * prints the sample size and a warning when n < 30
  * reports the result even when it loses to BTC (and says so plainly)
  * the random baseline is deterministic per day (hash of the day string), so
    it cannot be cherry-picked after the fact

Usage:
    python eval/backtest.py --live-history
    python eval/backtest.py --replay eval/corpus/*.json
"""
from __future__ import annotations

import argparse
import glob as globmod
import json
import statistics as stats
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness as H  # noqa: E402


def _ret(p0: float, p1: float) -> float:
    return (p1 / p0 - 1.0) * 100.0


def random_pick(day: str, watchlist: list[str]) -> str:
    return watchlist[sum(ord(c) for c in day) % len(watchlist)]


def report(pairs: list[dict], label: str, watchlist: list[str]) -> dict:
    n = len(pairs)
    if not n:
        print(f"\n{label}: no closed outcomes yet (n=0). Nothing honest to report.")
        return {"label": label, "n": 0}

    focus = [p["focus_ret"] for p in pairs]
    btc = [p["btc_ret"] for p in pairs]
    rnd = [p["rand_ret"] for p in pairs]
    wins_btc = sum(1 for f, b in zip(focus, btc) if f > b)
    out = {
        "label": label,
        "n": n,
        "avg_focus_pct": round(stats.fmean(focus), 3),
        "avg_btc_pct": round(stats.fmean(btc), 3),
        "avg_random_pct": round(stats.fmean(rnd), 3),
        "median_focus_pct": round(stats.median(focus), 3),
        "median_btc_pct": round(stats.median(btc), 3),
        "focus_hit_rate_pct": round(sum(1 for f in focus if f > 0) / n * 100, 2),
        "btc_hit_rate_pct": round(sum(1 for b in btc if b > 0) / n * 100, 2),
        "days_focus_beat_btc": wins_btc,
        "pct_days_focus_beat_btc": round(wins_btc / n * 100, 2),
        "beats_btc": (stats.fmean(focus) > stats.fmean(btc)),
        "sample_warning": n < 30,
    }
    print(f"\n== {label} (n={n}) ==")
    print(f"  avg return  focus {out['avg_focus_pct']:+.2f}%  |  "
          f"BTC {out['avg_btc_pct']:+.2f}%  |  random {out['avg_random_pct']:+.2f}%")
    print(f"  hit rate    focus {out['focus_hit_rate_pct']:.1f}%  |  BTC {out['btc_hit_rate_pct']:.1f}%")
    print(f"  focus beat BTC on {wins_btc}/{n} days ({out['pct_days_focus_beat_btc']:.1f}%)")
    if out["beats_btc"]:
        print("  verdict: focus beat BTC on average in this sample.")
    else:
        print("  verdict: focus did NOT beat BTC in this sample. Reported as-is.")
    if out["sample_warning"]:
        print("  WARNING: n < 30. This is not statistically meaningful; treat as a smoke test.")
    return out


def from_live_history() -> dict:
    H.bootstrap()
    T = sys.modules["tipsofday"]
    rows, st = T.build_track_record()
    pairs = []
    for r in rows:
        if r.ret is None or r.btc_ret is None:
            continue
        day = r.day
        # random baseline needs the price of a random watchlist asset: not stored,
        # so we only report focus vs BTC here and say so.
        pairs.append({"day": day, "focus_ret": r.ret, "btc_ret": r.btc_ret, "rand_ret": 0.0})
    if not pairs:
        print("Live history has no closed outcomes yet (the track record needs 24h+).")
        return {"label": "live history", "n": 0, "note": "no closed outcomes"}
    return report(pairs, "live history (focus vs BTC)", list(T.DEFAULT_WATCHLIST))


def from_replay(paths: list[Path]) -> list[dict]:
    H.bootstrap()
    T = sys.modules["tipsofday"]
    watch = list(T.DEFAULT_WATCHLIST)
    out = []
    for p in paths:
        c = H.load_corpus(p)
        fwd = c.get("forward") or {}
        pick = c.get("focus_from_replay") or c.get("focus")
        entry = fwd.get("entry") or {}
        later = fwd.get("close") or {}
        if not (pick and entry.get(pick) and later.get(pick)):
            continue
        btc_entry, btc_later = entry.get("BTC"), later.get("BTC")
        rp = random_pick(c.get("day", ""), watch)
        if not (btc_entry and btc_later and entry.get(rp) and later.get(rp)):
            continue
        out.append({
            "day": c["day"],
            "focus": pick,
            "focus_ret": _ret(entry[pick], later[pick]),
            "btc_ret": _ret(btc_entry, btc_later),
            "rand_ret": _ret(entry[rp], later[rp]),
            "random_pick": rp,
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live-history", action="store_true")
    ap.add_argument("--replay", nargs="*", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    results: dict = {}
    if args.live_history:
        results["live_history"] = from_live_history()

    if args.replay is not None:
        paths: list[Path] = []
        for pat in (args.replay or ["eval/corpus/*.json"]):
            paths += [Path(x) for x in sorted(globmod.glob(pat))]
        pairs = from_replay(paths)
        results["replay"] = report(pairs, "frozen replay (focus vs BTC vs random)",
                                   list(sys.modules["tipsofday"].DEFAULT_WATCHLIST)
                                   if "tipsofday" in sys.modules else ["BTC"])
        results["replay"]["pairs"] = pairs

    if not (args.live_history or args.replay is not None):
        print(__doc__)
        return 1

    if args.out:
        Path(args.out).write_text(json.dumps(results, indent=1, ensure_ascii=False), "utf-8")
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
