# Dreame Token Bridge design

`dreame-token-bridge` is a local command-line helper for Home Assistant users whose
custom Dreame Vacuum integration needs a fresh Xiaomi Home session. It is not
affiliated with Xiaomi, Dreame, Home Assistant, HACS, or any upstream integration.

The tool deliberately does not include account details, device identifiers, network
addresses, configuration paths, or token values. Users supply their Home Assistant
configuration directory at runtime, either as a local path, a Docker bind mount, or
an SMB-mounted path. Xiaomi credentials are read interactively, never from command
line arguments. The password is handled only in memory and the tool never prints
the password, service token, `ssecurity`, user ID, or full account name.

`doctor` is read-only. It detects the integration path, reports whether the token
cache is missing or stale, and checks whether the supported protocol anchor can be
patched. `refresh` uses the upstream Xiaomi Cloud Tokens Extractor package to
complete Xiaomi Account CAPTCHA and 2FA flows, writes a private cache file, creates
a timestamped backup before modifying `protocol.py`, and applies an idempotent
cache-reading patch. A Home Assistant reload/restart is opt-in: default output is
the manual procedure; users may choose an API-assisted operation by supplying a
long-lived token through an environment variable or a prompt.

Security guardrails include restrictive cache permissions where the platform
supports them, atomic cache writes, secret redaction in exceptions, no shell command
construction from user input, `--dry-run`, and a repository secret scan in CI. The
documentation and demo use fictional placeholders only.
