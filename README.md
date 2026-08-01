# dreame-token-bridge

A safe-by-default local CLI for refreshing a **Xiaomi Account / Xiaomi Home**
session cache used by a patched [Dreame Vacuum](https://github.com/Tasshack/dreame-vacuum)
Home Assistant custom integration.

It helps installations where the integration cannot complete Xiaomi CAPTCHA or
two-factor authentication itself. It is not affiliated with Xiaomi, Dreame, Home
Assistant, HACS, or the upstream integrations.

<img src="assets/terminal-demo.gif" alt="Animated synthetic Xiaomi Account setup in a terminal" width="960">

_Synthetic demonstration only: all credentials, CAPTCHA and 2FA values are fictional;
session tokens are redacted._

## Safety first

- Never pass a Xiaomi Account password, Home Assistant token, or device token as a
  command-line argument.
- Use a dedicated Xiaomi Account where practical.
- Run `doctor` before changing anything.
- Review the backup created next to `protocol.py` before upgrading HACS.
- Treat `.dreame_auth_cache.json` as a password-equivalent secret. It is ignored
  by Git and must never be shared in an issue, log, or screenshot.

## Supported environments

The `--ha-config` path can point to a local Home Assistant configuration directory,
a Docker bind mount, a Linux volume, or an SMB-mounted share. Examples use only
fictional paths:

```powershell
dreame-token-bridge doctor --ha-config '\\ha-box\config'
dreame-token-bridge refresh --ha-config '\\ha-box\config' --dry-run
```

```bash
dreame-token-bridge doctor --ha-config /config
dreame-token-bridge refresh --ha-config /srv/homeassistant --restart-mode manual
```

`refresh` will prompt for the Xiaomi Account username and password. CAPTCHA and
2FA are performed by the upstream Xiaomi Cloud Tokens Extractor. The bridge does
not print the password, service token, `ssecurity`, or full account identifier.

## Home Assistant reload modes

The default is `--restart-mode manual`: the tool prints the precise reload/restart
steps without contacting Home Assistant. `--restart-mode api` is opt-in and asks
for a Home Assistant long-lived access token at runtime; it never stores that token.

## Install

```bash
python -m pip install dreame-token-bridge
```

For development:

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

See [Security](docs/SECURITY.md) and the [synthetic terminal demo](docs/DEMO.md).
