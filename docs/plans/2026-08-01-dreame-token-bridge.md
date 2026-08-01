# Dreame Token Bridge Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a portable, safe-by-default CLI that refreshes a Xiaomi Account
session cache and reapplies a narrow Dreame Vacuum integration patch.

**Architecture:** A Python package separates path validation, cache serialization,
patch generation/application, and the CLI. The CLI delegates Xiaomi authentication
to the upstream extractor only after interactive confirmation. No credentials are
accepted in CLI arguments or committed files.

**Tech Stack:** Python 3.10+, standard library, `requests`, `pytest`, Ruff.

---

### Task 1: Establish public-repository guardrails

**Files:**
- Create: `README.md`, `LICENSE`, `.gitignore`, `.gitleaks.toml`, `.github/workflows/ci.yml`
- Test: `.github/workflows/ci.yml`

**Step 1:** Add a README with only fictional examples and a clear Xiaomi Account
scope.

**Step 2:** Add ignore rules and CI secret scanning before adding source code.

### Task 2: Add cache and patch tests

**Files:**
- Create: `tests/test_cache.py`, `tests/test_patch.py`
- Create: `src/dreame_token_bridge/cache.py`, `src/dreame_token_bridge/patch.py`

**Step 1:** Write tests for atomic cache serialization, redacted errors, idempotent
patching, unsupported anchors, and backup creation.

**Step 2:** Run `pytest` and confirm the tests fail because the package is absent.

**Step 3:** Implement the minimal cache and patch helpers.

**Step 4:** Re-run `pytest` and confirm the tests pass.

### Task 3: Add the safe CLI

**Files:**
- Create: `tests/test_cli.py`
- Create: `src/dreame_token_bridge/cli.py`, `src/dreame_token_bridge/__main__.py`
- Modify: `pyproject.toml`

**Step 1:** Write tests that `doctor` is read-only and that `refresh` requires an
explicit configuration path and interactive account input.

**Step 2:** Run the focused tests and confirm failure.

**Step 3:** Implement `doctor`, `refresh --dry-run`, and restart guidance. Keep
the extractor adapter behind an interface so tests never make live Xiaomi calls.

**Step 4:** Run the complete suite and linting.

### Task 4: Publish-ready documentation and demo

**Files:**
- Create: `docs/SECURITY.md`, `docs/DEMO.md`, `assets/terminal-demo.cast`
- Modify: `README.md`

**Step 1:** Add a fictional terminal recording source; no live terminal capture is
permitted.

**Step 2:** Document Xiaomi Account CAPTCHA/2FA, SMB/Docker/Linux paths, manual
and API-assisted reload modes, HACS-update behaviour, and secret-reporting policy.

### Task 5: Verify and publish

**Step 1:** Run `pytest`, Ruff, packaging metadata validation, and the secret scan.

**Step 2:** Inspect `git diff --check` and scan tracked content for private network
identifiers, real names, e-mail addresses, and tokens.

**Step 3:** Commit the clean repository, create a public GitHub repository, push,
and provide the URL.
