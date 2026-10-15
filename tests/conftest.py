import os
import tempfile
from pathlib import Path

# Isolate the app's config/data directories before tipsofday is imported.
_TMP = Path(tempfile.mkdtemp(prefix="tipsofday-test-"))
os.environ.setdefault("TIPSOFDAY_CONFIG", str(_TMP / "config"))
os.environ.setdefault("TIPSOFDAY_DATA", str(_TMP / "data"))
os.environ.setdefault("TIPSOFDAY_ENFORCE", "0")
