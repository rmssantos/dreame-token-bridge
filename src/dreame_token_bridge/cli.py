"""Command-line interface for local, opt-in Dreame token recovery."""

from __future__ import annotations

import argparse
import getpass
import sys
from pathlib import Path
from typing import Sequence

import requests

from .auth import refresh_xiaomi_session
from .cache import write_token_cache
from .patch import PATCH_ANCHOR, PATCH_MARKER, apply_protocol_patch


def _paths(config_dir: Path) -> tuple[Path, Path]:
    protocol = config_dir / "custom_components" / "dreame_vacuum" / "dreame" / "protocol.py"
    return protocol, config_dir / ".dreame_auth_cache.json"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dreame-token-bridge")
    subcommands = parser.add_subparsers(dest="command", required=True)
    for command in ("doctor", "refresh"):
        subcommand = subcommands.add_parser(command)
        subcommand.add_argument("--ha-config", required=True, type=Path)
    refresh = subcommands.choices["refresh"]
    refresh.add_argument("--dry-run", action="store_true")
    refresh.add_argument("--extractor-dir", type=Path)
    refresh.add_argument("--country", default="de")
    refresh.add_argument("--restart-mode", choices=("manual", "api"), default="manual")
    refresh.add_argument("--confirm-restart", action="store_true")
    refresh.add_argument("--ha-url", default="http://homeassistant.local:8123")
    return parser


def _doctor(config_dir: Path) -> int:
    protocol, cache = _paths(config_dir)
    print("Doctor runs read-only; no files will be created or changed.")
    if not config_dir.is_dir():
        print("Home Assistant configuration directory does not exist.")
        return 1
    if not protocol.is_file():
        print("Dreame Vacuum protocol.py was not found at the supported location.")
        return 1
    source = protocol.read_text(encoding="utf-8")
    patch_status = (
        "already patched"
        if PATCH_MARKER in source
        else "patchable"
        if PATCH_ANCHOR in source
        else "unsupported"
    )
    print(f"Protocol: {patch_status}")
    print(f"Cache: {'present' if cache.is_file() else 'missing'}")
    return 0 if patch_status != "unsupported" else 1


def _restart_via_api(base_url: str) -> int:
    token = getpass.getpass("Home Assistant long-lived access token: ")
    try:
        response = requests.post(
            f"{base_url.rstrip('/')}/api/services/homeassistant/restart",
            headers={"Authorization": f"Bearer {token}"},
            timeout=15,
        )
    except requests.RequestException as error:
        print(f"Home Assistant restart request failed: {error}", file=sys.stderr)
        return 1
    if response.status_code not in (200, 202):
        print(
            f"Home Assistant restart request was rejected ({response.status_code}).",
            file=sys.stderr,
        )
        return 1
    print("Home Assistant restart requested.")
    return 0


def _manual_restart_guidance() -> None:
    print("Next: Home Assistant → Settings → Devices & services → Dreame Vacuum → Reload.")
    print(
        "If reload does not recover the integration, restart Home Assistant from Settings → System."
    )


def _refresh(arguments: argparse.Namespace) -> int:
    protocol, cache = _paths(arguments.ha_config)
    if not arguments.ha_config.is_dir() or not protocol.is_file():
        print(
            "Run doctor first: the supported Home Assistant and protocol paths were not found.",
            file=sys.stderr,
        )
        return 1
    if arguments.dry_run:
        source = protocol.read_text(encoding="utf-8")
        status = (
            "already patched"
            if PATCH_MARKER in source
            else "patchable"
            if PATCH_ANCHOR in source
            else "unsupported"
        )
        print(f"Dry run: cache would be written to {cache.name}; protocol is {status}.")
        return 0 if status != "unsupported" else 1
    if arguments.extractor_dir is None:
        print("--extractor-dir is required for a live Xiaomi Account refresh.", file=sys.stderr)
        return 2

    username = input("Xiaomi Account username: ").strip()
    if not username:
        print("A Xiaomi Account username is required.", file=sys.stderr)
        return 2
    password = getpass.getpass("Xiaomi Account password: ")
    try:
        tokens = refresh_xiaomi_session(
            arguments.extractor_dir, username, password, arguments.country
        )
        write_token_cache(cache, tokens)
        patch = apply_protocol_patch(protocol)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Refresh failed: {error}", file=sys.stderr)
        return 1

    print("Xiaomi Account session cache updated.")
    print(patch.message)
    if arguments.restart_mode == "manual":
        _manual_restart_guidance()
        return 0
    if not arguments.confirm_restart:
        print("API restart requires --confirm-restart; no restart was requested.", file=sys.stderr)
        return 2
    return _restart_via_api(arguments.ha_url)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.command == "doctor":
        return _doctor(arguments.ha_config)
    return _refresh(arguments)
