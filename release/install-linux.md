# Installing tipsofday on Linux

Tested on Ubuntu 24.04 / Debian 13 / Fedora 41 with Python 3.11–3.14.
Everything below runs as **your normal user** — no `sudo` is needed for tipsofday itself.

---

## 0. What you need

| | Minimum | Comfortable |
|---|---|---|
| Python | 3.11 | 3.12+ |
| RAM | 8 GB | 16 GB |
| Disk for the model | ~4.6 GB (`gemma4:e2b`) | ~6.6 GB (`gemma4:e4b`) |
| GPU | not required | NVIDIA 6 GB+ VRAM, or any modern iGPU |

The news and market fetches need the internet. The model runs locally.
The whole app is a CLI: one command writes one briefing to your terminal.

---

## 1. Python and pipx

Most distros ship a recent Python. Check:

```bash
python3 --version        # need 3.11 or newer
```

If it is older, install a newer one:

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install -y python3 python3-venv python3-pip pipx

# Fedora
sudo dnf install -y python3 python3-pip pipx

# Arch
sudo pacman -S --needed python python-pip python-pipx
```

`pipx` is the recommended way to install a Python CLI: it puts the app in its own
virtual environment and adds the `tipsofday` command to your `PATH`.

```bash
pipx ensurepath        # adds ~/.local/bin to PATH; open a new shell after this
```

---

## 2. Ollama (the local model runtime)

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
```

Then pull the default model (Gemma 4 E4B, Apache-2.0, ~6.6 GB):

```bash
ollama pull gemma4:e4b
```

On a low-memory machine use the smaller tier instead:

```bash
ollama pull gemma4:e2b      # ~4.6 GB
```

> If you have an NVIDIA GPU, Ollama uses it automatically once the driver is installed
> (`nvidia-smi` should print your card). No extra configuration is needed.

Start the server if your init system does not (the installer usually sets up a
`systemd` unit):

```bash
systemctl --user enable --now ollama     # or: ollama serve &
```

---

## 3. tipsofday

```bash
pipx install "tipsofday @ git+https://github.com/tipsofday/tipsofday"
```

Or, from a clone (useful if you want to hack on it):

```bash
git clone https://github.com/tipsofday/tipsofday
cd tipsofday
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

Pro license keys use Ed25519 signatures; install the optional extra so `activate` works:

```bash
pipx install "tipsofday[license] @ git+https://github.com/tipsofday/tipsofday"
```

---

## 4. First run

```bash
tipsofday init       # creates ~/.config/tipsofday/ with an editable sources.yaml
tipsofday doctor     # checks Python, hardware, model, internet and feed health
tipsofday run        # writes today's briefing
```

`tipsofday init` tells you which model to pull if it is missing. `doctor` prints a
verdict such as *"balanced: Gemma 4 E4B Q4 runs on a small GPU or CPU"*.

---

## 5. Run it every morning

**cron**

```cron
# minute hour day month weekday  — 08:00 every day
0 8 * * * /home/you/.local/bin/tipsofday run --refresh >> /home/you/.local/share/tipsofday/cron.log 2>&1
```

**systemd user timer**

```ini
# ~/.config/systemd/user/tipsofday.service
[Unit]
Description=tipsofday daily briefing
[Service]
Type=oneshot
ExecStart=%h/.local/bin/tipsofday run --refresh
```

```ini
# ~/.config/systemd/user/tipsofday.timer
[Unit]
Description=Run tipsofday every morning
[Timer]
OnCalendar=*-*-* 08:00:00
Persistent=true
[Install]
WantedBy=timers.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now tipsofday.timer
```

`tipsofday schedule --install` prints the same entry so you can paste it.

---

## 6. Where things live

| Path | Contents |
|---|---|
| `~/.config/tipsofday/config.json` | language, model, watchlist, floors |
| `~/.config/tipsofday/sources.yaml` | your feeds and one-off links |
| `~/.local/share/tipsofday/history.db` | SQLite briefing history (Pro) |
| `~/.cache/tipsofday/` | HTTP cache (delete freely) |

Override them with `TIPSOFDAY_CONFIG` and `TIPSOFDAY_DATA`.

---

## 7. Troubleshooting

| Symptom | Fix |
|---|---|
| `command not found: tipsofday` | run `pipx ensurepath`, then open a new shell |
| `Cannot connect to Ollama` | `systemctl --user start ollama` or `ollama serve &` |
| `model not found` | `ollama pull gemma4:e4b` |
| Briefing is very slow | use `--model gemma4:e2b`, or `ollama ps` to confirm the GPU is used |
| Numbers look stripped | the grounding filter removed ungrounded numbers on purpose; see `LEGAL_NOTES.md` |
| `cryptography is required` | `pipx inject tipsofday cryptography` |

Nothing works offline except the model: news and prices need the network, and the run
degrades gracefully when a feed is down (the briefing lists the failed sources).
