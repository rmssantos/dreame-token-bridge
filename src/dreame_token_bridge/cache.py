"""Private, atomic storage for Xiaomi Account session data."""

from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Mapping
from pathlib import Path


REQUIRED_TOKEN_FIELDS = {"username", "userId", "serviceToken", "ssecurity", "timestamp"}


def write_token_cache(cache_path: Path, tokens: Mapping[str, object]) -> Path:
    """Atomically write a complete token cache and restrict its permissions when possible."""
    missing = REQUIRED_TOKEN_FIELDS.difference(tokens)
    if missing:
        raise ValueError(f"Token cache is missing required fields: {', '.join(sorted(missing))}")

    cache_path = Path(cache_path)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(dict(tokens), indent=2, sort_keys=True) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{cache_path.name}.", dir=cache_path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as temporary_file:
            temporary_file.write(payload)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        try:
            os.chmod(temporary_path, 0o600)
        except OSError:
            # Windows and network shares may not support POSIX permissions.
            pass
        os.replace(temporary_path, cache_path)
    finally:
        temporary_path.unlink(missing_ok=True)
    return cache_path
