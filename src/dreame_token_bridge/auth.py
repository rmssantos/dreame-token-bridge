"""Optional adapter for a locally installed Xiaomi Cloud Tokens Extractor."""

from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path


def refresh_xiaomi_session(
    extractor_dir: Path, username: str, password: str, country: str
) -> dict[str, object]:
    """Run the upstream interactive Xiaomi Account flow and return the session cache."""
    extractor_dir = Path(extractor_dir)
    extractor_file = extractor_dir / "token_extractor.py"
    if not extractor_file.is_file():
        raise RuntimeError(
            "Xiaomi Cloud Tokens Extractor was not found. Pass --extractor-dir containing "
            "token_extractor.py."
        )

    original_argv = sys.argv[:]
    sys.argv = [
        "token_extractor",
        "--username",
        username,
        "--password",
        password,
        "--server",
        country,
    ]
    sys.path.insert(0, str(extractor_dir))
    try:
        extractor = importlib.import_module("token_extractor")
        connector = extractor.PasswordXiaomiCloudConnector()
        if not connector.login():
            raise RuntimeError("Xiaomi Account login failed.")
        return {
            "username": username,
            "userId": str(connector.userId),
            "serviceToken": str(connector._serviceToken),
            "ssecurity": str(getattr(connector, "_ssecurity", "")),
            "timestamp": int(time.time()),
        }
    finally:
        sys.argv = original_argv
        try:
            sys.path.remove(str(extractor_dir))
        except ValueError:
            pass
