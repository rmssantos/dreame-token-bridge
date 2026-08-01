import json

from dreame_token_bridge.cache import write_token_cache


def test_write_token_cache_creates_private_json_without_exposing_secrets(tmp_path):
    cache_path = tmp_path / ".dreame_auth_cache.json"
    tokens = {
        "username": "demo@example.com",
        "userId": "12345",
        "serviceToken": "example-token",
        "ssecurity": "REDACTED",
        "timestamp": 1,
    }

    result = write_token_cache(cache_path, tokens)

    assert result == cache_path
    assert json.loads(cache_path.read_text(encoding="utf-8")) == tokens
    assert not list(tmp_path.glob("*.tmp"))
