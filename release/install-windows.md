# Installing tipsofday on Windows

Tested on Windows 11 (and Windows 10 22H2) with Python 3.11–3.14.
Everything below runs in **PowerShell**. No administrator rights are required for the
normal install; only the optional "every morning" scheduled task asks for elevation.

---

## 0. What you need

| | Minimum | Comfortable |
|---|---|---|
| Windows | 10 (22H2) | 11 |
| Python | 3.11 | 3.12+ |
| RAM | 8 GB | 16 GB |
| Disk for the model | ~4.6 GB (`gemma4:e2b`) | ~6.6 GB (`gemma4:e4b`) |
| GPU | not required | NVIDIA 6 GB+ VRAM, or a modern iGPU |

The news and market fetches need the internet. The model runs locally on your PC.

---

## 1. Python

```powershell
winget install --id Python.Python.3.12 -e
```

Then open a **new** PowerShell window and check:

```powershell
python --version      # need 3.11 or newer
```

If `python` opens the Microsoft Store, install "Python 3.12" from the Store instead, or
disable the `python.exe` app alias in *Settings → Apps → Advanced app settings → App
execution aliases*.

---

## 2. pipx (isolated installs)

```powershell
python -m pip install --user pipx
python -m pipx ensurepath
```

Close and reopen PowerShell so the updated `PATH` takes effect.

---

## 3. Ollama (the local model runtime)

```powershell
winget install --id Ollama.Ollama -e
```

Or download the installer from <https://ollama.com/download/windows>. Ollama starts a
background server (look for the llama icon in the system tray).

Pull the default model (Gemma 4 E4B, Apache-2.0, ~6.6 GB):

```powershell
ollama pull gemma4:e4b
```

On a low-memory PC use the smaller tier instead:

```powershell
ollama pull gemma4:e2b      # ~4.6 GB
```

> With an NVIDIA GPU, Ollama uses it automatically once the driver is installed.
> Check with `nvidia-smi`. AMD/Intel GPUs fall back to CPU, which still works, just slower.

---

## 4. tipsofday

```powershell
pipx install "tipsofday[license] @ git+https://github.com/adalbertobrant/tipsofday"
```

`[license]` adds the `cryptography` dependency used to verify Pro keys; drop it for the
free tier only.

If `git` is missing, install it first: `winget install --id Git.Git -e`.
Alternatively, download the repository ZIP, unzip it, and run

```powershell
cd C:\path\to\tipsofday
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[license]"
```

---

## 5. First run

```powershell
tipsofday init       # creates %APPDATA%\tipsofday\ with an editable sources.yaml
tipsofday doctor     # hardware, model, internet and feed health
tipsofday run        # writes today's briefing
```

`doctor` will tell you if the model is missing or if Ollama is not reachable.

---

## 6. Run it every morning

```powershell
tipsofday schedule --install
```

That prints the exact command. Paste it into an **elevated** (Administrator) PowerShell:

```powershell
schtasks /Create /SC DAILY /TN tipsofday /TR "tipsofday run --refresh" /ST 08:00
```

Make sure `tipsofday` resolves for the task's account; if not, use the full path:

```powershell
schtasks /Create /SC DAILY /TN tipsofday /TR "$env:USERPROFILE\.local\bin\tipsofday.exe run --refresh" /ST 08:00
```

Remove it later with `schtasks /Delete /TN tipsofday /F`.

---

## 7. Where things live

| Path | Contents |
|---|---|
| `%APPDATA%\tipsofday\config.json` | language, model, watchlist, floors |
| `%APPDATA%\tipsofday\sources.yaml` | your feeds and one-off links |
| `%LOCALAPPDATA%\tipsofday\history.db` | SQLite briefing history (Pro) |
| `%LOCALAPPDATA%\tipsofday\` | HTTP cache |

Override them with the `TIPSOFDAY_CONFIG` and `TIPSOFDAY_DATA` environment variables.

---

## 8. Troubleshooting

| Symptom | Fix |
|---|---|
| `tipsofday is not recognized` | run `python -m pipx ensurepath`, reopen PowerShell |
| Execution policy blocks the venv | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `Cannot connect to Ollama` | start Ollama from the Start menu; check the tray icon |
| `model not found` | `ollama pull gemma4:e4b` |
| Briefing is slow | `--model gemma4:e2b`, or check that the GPU is used (`ollama ps`) |
| Console shows `?` instead of accents | run `chcp 65001` once, or use Windows Terminal |
| Numbers look stripped | the grounding filter removed ungrounded numbers on purpose; see `LEGAL_NOTES.md` |
| `cryptography is required` | `pipx inject tipsofday cryptography` |

Windows Terminal (or the new PowerShell 7) renders the Rich output best; the legacy
console works but with a plainer look.
