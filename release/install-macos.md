# Installing tipsofday on macOS

Tested on macOS 13–15 on Apple silicon (M-series). Intel Macs work too, but the
smaller model tier is recommended. Everything runs as **your user** — no `sudo` for
tipsofday itself.

---

## 0. What you need

| | Minimum | Comfortable |
|---|---|---|
| macOS | 13 Ventura | 14+ |
| Python | 3.11 | 3.12+ |
| RAM / unified memory | 8 GB | 16 GB |
| Disk for the model | ~4.6 GB (`gemma4:e2b`) | ~6.6 GB (`gemma4:e4b`) |

Apple silicon runs the model on the Neural Engine / GPU through Ollama's Metal backend;
no CUDA and no extra drivers are needed.

---

## 1. Homebrew, Python and pipx

```bash
# Homebrew, if you do not have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```bash
brew install python pipx
pipx ensurepath        # then open a new terminal
python3 --version      # need 3.11 or newer
```

---

## 2. Ollama (the local model runtime)

```bash
brew install --cask ollama
open -a Ollama         # starts the menu-bar app and the server
```

Or download the app from <https://ollama.com/download/mac>.

Pull the default model (Gemma 4 E4B, Apache-2.0, ~6.6 GB):

```bash
ollama pull gemma4:e4b
```

On an 8 GB Mac use the smaller tier instead:

```bash
ollama pull gemma4:e2b      # ~4.6 GB
```

---

## 3. tipsofday

```bash
pipx install "tipsofday[license] @ git+https://github.com/adalbertobrant/tipsofday"
```

`[license]` adds the `cryptography` dependency used to verify Pro keys. Drop it if you
only want the free tier.

From a clone, instead:

```bash
git clone https://github.com/adalbertobrant/tipsofday
cd tipsofday
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[license]"
```

---

## 4. First run

```bash
tipsofday init       # creates ~/.config/tipsofday/ with an editable sources.yaml
tipsofday doctor     # hardware, model, internet and feed health
tipsofday run        # writes today's briefing
```

If `doctor` says the model is missing, run `ollama pull gemma4:e4b`.

---

## 5. Run it every morning

macOS `cron` still works, but the modern approach is a `launchd` agent, which also
runs when you were asleep.

```bash
tipsofday schedule --install     # prints the exact entry for your machine
```

The printed agent looks like this:

```xml
<!-- ~/Library/LaunchAgents/dev.tipsofday.daily.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>            <string>dev.tipsofday.daily</string>
  <key>ProgramArguments</key>
  <array>
    <string>/Users/you/.local/bin/tipsofday</string>
    <string>run</string>
    <string>--refresh</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>8</integer><key>Minute</key><integer>0</integer></dict>
  <key>StandardOutPath</key>  <string>/Users/you/.local/share/tipsofday/cron.log</string>
  <key>StandardErrorPath</key><string>/Users/you/.local/share/tipsofday/cron.log</string>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/dev.tipsofday.daily.plist
```

---

## 6. Where things live

| Path | Contents |
|---|---|
| `~/.config/tipsofday/config.json` | language, model, watchlist, floors |
| `~/.config/tipsofday/sources.yaml` | your feeds and one-off links |
| `~/.local/share/tipsofday/history.db` | SQLite briefing history (Pro) |
| `~/.cache/tipsofday/` | HTTP cache |

Override them with `TIPSOFDAY_CONFIG` and `TIPSOFDAY_DATA`.

---

## 7. Troubleshooting

| Symptom | Fix |
|---|---|
| `command not found: tipsofday` | run `pipx ensurepath`, open a new terminal |
| `Cannot connect to Ollama` | open the Ollama app, or `ollama serve` |
| `model not found` | `ollama pull gemma4:e4b` |
| Mac gets hot / fans spin | use `--model gemma4:e2b`, or close other GPU apps |
| First run is slow | the model loads into memory once; later runs reuse it |
| Numbers look stripped | the grounding filter removed ungrounded numbers on purpose; see `LEGAL_NOTES.md` |

Gatekeeper may warn the first time you run a downloaded binary; launching from
Terminal avoids that entirely.
