# Security policy

## Secrets

The following values are secrets or private identifiers and must never be committed,
pasted into issues, or shown in screenshots:

- Xiaomi Account passwords, CAPTCHA answers, and 2FA codes
- Xiaomi `serviceToken`, `ssecurity`, user IDs, and device tokens
- Home Assistant long-lived access tokens
- Home Assistant backups, `.storage` files, and `.dreame_auth_cache.json`
- private IP addresses, SMB server names, device IDs, e-mail addresses, and logs

The CLI never accepts these values in command-line options. It prompts only when a
live refresh is requested and does not persist Home Assistant API tokens or Xiaomi
Account passwords. The session cache is deliberately ignored by Git.

## Reporting a vulnerability

Do not open a public issue for a possible secret exposure or a security flaw. Open
a private GitHub security advisory for this repository and include only redacted
reproduction steps. Rotate any token that may have been exposed before reporting.

## Operational limits

This project modifies a third-party custom integration using a narrowly matched,
backed-up patch. `doctor` is read-only. `refresh --dry-run` verifies applicability
without login or file changes. A live patch refuses an unknown `protocol.py` shape.
Review HACS updates with `doctor` because upstream updates can overwrite the patch.
