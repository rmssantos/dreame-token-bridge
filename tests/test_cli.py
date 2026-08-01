from dreame_token_bridge.cli import main


def test_doctor_reports_missing_files_without_writing(tmp_path, capsys):
    exit_code = main(["doctor", "--ha-config", str(tmp_path)])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "read-only" in output.lower()
    assert not list(tmp_path.iterdir())


def test_refresh_dry_run_requires_no_credentials_and_changes_nothing(tmp_path, capsys):
    protocol = tmp_path / "custom_components" / "dreame_vacuum" / "dreame" / "protocol.py"
    protocol.parent.mkdir(parents=True)
    protocol.write_text(
        "class Protocol:\n    def login(self) -> bool:\n        self._session.close()\n",
        encoding="utf-8",
    )

    exit_code = main(["refresh", "--ha-config", str(tmp_path), "--dry-run"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "dry run" in output.lower()
    assert ".dreame_auth_cache.json" not in {path.name for path in tmp_path.iterdir()}
    assert "__DREAME_TOKEN_CACHE_PATCH__" not in protocol.read_text(encoding="utf-8")
