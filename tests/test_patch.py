from dreame_token_bridge.patch import PATCH_MARKER, apply_protocol_patch


def test_apply_protocol_patch_creates_backup_and_is_idempotent(tmp_path):
    protocol = tmp_path / "protocol.py"
    original = "class Protocol:\n    def login(self) -> bool:\n        self._session.close()\n"
    protocol.write_text(original, encoding="utf-8")

    first = apply_protocol_patch(protocol)
    second = apply_protocol_patch(protocol)

    assert first.changed is True
    assert second.changed is False
    assert PATCH_MARKER in protocol.read_text(encoding="utf-8")
    assert protocol.with_suffix(".py.bak").read_text(encoding="utf-8") == original


def test_apply_protocol_patch_rejects_unknown_login_shape(tmp_path):
    protocol = tmp_path / "protocol.py"
    protocol.write_text("class Protocol:\n    def login(self):\n        pass\n", encoding="utf-8")

    result = apply_protocol_patch(protocol)

    assert result.changed is False
    assert "unsupported" in result.message.lower()
