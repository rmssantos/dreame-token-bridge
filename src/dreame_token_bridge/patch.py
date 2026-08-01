"""A narrow, idempotent patch for the Dreame Xiaomi-cloud protocol."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

PATCH_MARKER = "# __DREAME_TOKEN_CACHE_PATCH__"
PATCH_ANCHOR = "    def login(self) -> bool:\n        self._session.close()"
PATCH_BODY = """    # __DREAME_TOKEN_CACHE_PATCH__
    # Read a pre-authenticated Xiaomi Account cache before attempting cloud login.
    import json as _json
    import os as _os
    _config_dir = _os.path.dirname(_os.path.abspath(__file__))
    _cache_file = None
    for _ in range(6):
        if _os.path.exists(_os.path.join(_config_dir, "configuration.yaml")):
            _cache_file = _os.path.join(_config_dir, ".dreame_auth_cache.json")
            break
        _parent = _os.path.dirname(_config_dir)
        if _parent == _config_dir:
            break
        _config_dir = _parent
    try:
        with open(_cache_file, encoding="utf-8") as _cache_handle:
            _cache = _json.load(_cache_handle)
        if _cache.get("username") == self._username:
            self._service_token = _cache["serviceToken"]
            self._userId = str(_cache["userId"])
            self._ssecurity = _cache.get("ssecurity", "")
            self._uid = str(_cache["userId"])
            self._logged_in = True
            self._fail_count = 0
            self._connected = True
            _LOGGER.info("Dreame Vacuum: using cached Xiaomi Account session")
            return True
    except Exception as _cache_error:
        _LOGGER.warning("Dreame Vacuum: cached Xiaomi Account session unavailable: %s", _cache_error)
"""


@dataclass(frozen=True)
class PatchResult:
    changed: bool
    message: str
    backup_path: Path | None = None


def apply_protocol_patch(protocol_path: Path) -> PatchResult:
    """Patch one known upstream anchor, with a one-time adjacent backup."""
    protocol_path = Path(protocol_path)
    source = protocol_path.read_text(encoding="utf-8")
    if PATCH_MARKER in source:
        return PatchResult(changed=False, message="Protocol is already patched.")
    if PATCH_ANCHOR not in source:
        return PatchResult(
            changed=False,
            message="Unsupported Dreame Vacuum protocol.py shape; no file was changed.",
        )

    backup_path = protocol_path.with_suffix(protocol_path.suffix + ".bak")
    if not backup_path.exists():
        shutil.copy2(protocol_path, backup_path)
    patched = source.replace(
        PATCH_ANCHOR,
        f"    def login(self) -> bool:\n{PATCH_BODY}        self._session.close()",
        1,
    )
    protocol_path.write_text(patched, encoding="utf-8")
    return PatchResult(changed=True, message="Protocol patch applied.", backup_path=backup_path)
