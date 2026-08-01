# Contributing

All changes go through a pull request; direct pushes to `main` are blocked.

Before opening a PR, run:

```bash
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m build --wheel --sdist
```

Never include real Xiaomi Account details, Home Assistant credentials, token caches,
private network identifiers, or copied Home Assistant logs. Use fictional values in
tests, documentation, screenshots, and recordings.
