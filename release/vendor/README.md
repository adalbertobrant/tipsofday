# Vendor signing keys (never commit the private key)

This folder is **not** part of the open-source distribution.

| File | Committed? | Purpose |
|---|---|---|
| `private_key.pem` | ❌ never (git-ignored) | Ed25519 key that signs Pro license keys |
| `README.md` | ✅ | this file |

## How licensing works

- Pro license keys are Ed25519-signed tokens: `base64url(payload).base64url(signature)`.
- The payload is JSON: `{"email": "...", "plan": "pro", "iat": "...", "exp": "..."}`.
- The **public** key is embedded in the app (`LICENSE_PUBLIC_KEY_B64` in `tipsofday.py`),
  so every install can verify a key offline with a 14-day grace period.
- `license_server` in `~/.config/tipsofday/config.json` is optional; when set, the app can
  additionally ask it whether a key was revoked.

## Issuing a key (vendor only)

```bash
python tipsofday.py license-keygen release/vendor/private_key.pem \
    --email buyer@example.com --plan pro --days 365
```

Keep `private_key.pem` on a machine you control, back it up somewhere offline, and rotate
it (which invalidates old keys) if it ever leaks. Losing it means you can no longer issue
keys for the embedded public key; you would ship a new public key in a new release.

## Verifying the public key matches the private key

```bash
python - <<'PY'
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from pathlib import Path
import tipsofday as T

priv = serialization.load_pem_private_key(Path("release/vendor/private_key.pem").read_bytes(), password=None)
pub = priv.public_key().public_bytes(
    serialization.Encoding.Raw, serialization.PublicFormat.Raw)
print("embedded :", T.LICENSE_PUBLIC_KEY_B64)
print("private  :", base64.b64encode(pub).decode())
print("match    :", base64.b64encode(pub).decode() == T.LICENSE_PUBLIC_KEY_B64)
PY
```

> Keys issued from this folder only unlock **Pro features**. The core briefing, the
> guardrails and the report format are Apache-2.0 and never gated.
