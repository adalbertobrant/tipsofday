#!/usr/bin/env python3
"""Strip <script>/<style>/<noscript> from captured corpus bodies, in place.

The corpus stores whole web pages so a replay is byte-for-byte deterministic,
but the model never sees raw HTML: the pipeline hands it the *extracted* text,
and both extractors (trafilatura and the built-in fallback) skip script/style.
Dropping those blocks makes each capture ~7x smaller while leaving the text the
model sees identical.

Run once to shrink an existing corpus (e.g. before committing it):

    python eval/compact_corpus.py                 # rewrite all corpus files
    python eval/compact_corpus.py --verify        # assert extraction is unchanged
    python eval/compact_corpus.py --dry-run       # report sizes, write nothing
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness as H  # noqa: E402


def iter_corpus_files() -> list[Path]:
    paths = sorted(glob.glob(str(H.CORPUS_DIR / "*.json")))
    paths += sorted(glob.glob(str(H.SYNTH_DIR / "*.json")))
    return [Path(p) for p in paths]


def verify(path: Path, before: dict, after: dict) -> int:
    """Assert extract_text_from_html is unchanged for every body. Returns diffs."""
    T = sys.modules["tipsofday"]
    diffs = 0
    for url, old in (before.get("bodies") or {}).items():
        new = (after.get("bodies") or {}).get(url)
        if not isinstance(old, str) or not isinstance(new, str):
            continue
        if "<" not in old:
            continue  # JSON API bodies are not touched
        if T.extract_text_from_html(old, url) != T.extract_text_from_html(new, url):
            diffs += 1
            print(f"  EXTRACTION DIFF {path.name}: {url[:90]}")
    return diffs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true",
                    help="assert the extracted text is identical before writing")
    ap.add_argument("--dry-run", action="store_true", help="report only, write nothing")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if args.verify:
        H.bootstrap()
    if not args.verify and not args.quiet:
        print("(run with --verify to check extraction identity with the app's parser)")

    files = iter_corpus_files()
    if not files:
        print("no corpus files found (eval/corpus, eval/corpus_synth)", file=sys.stderr)
        return 2

    total_before = total_after = 0
    total_diffs = 0
    for path in files:
        raw = path.read_text("utf-8")
        before = json.loads(raw)
        total_before += len(raw)

        after = H.compact_corpus(json.loads(raw))
        if args.verify:
            total_diffs += verify(path, before, after)

        new = json.dumps(after, ensure_ascii=False, indent=1)
        total_after += len(new)
        if not args.dry_run:
            path.write_text(new, "utf-8")
        if not args.quiet:
            pct = 100 * (1 - len(new) / max(1, len(raw)))
            print(f"{path.name:<34} {len(raw)/1e6:6.1f}MB -> {len(new)/1e6:5.1f}MB (-{pct:.0f}%)")

    verb = "would write" if args.dry_run else "wrote"
    print(f"\n{verb} {len(files)} files: {total_before/1e6:.1f}MB -> {total_after/1e6:.1f}MB")
    if args.verify:
        print(f"extraction diffs: {total_diffs}")
        return 1 if total_diffs else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
