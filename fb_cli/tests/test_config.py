from __future__ import annotations

import os
import stat

import pytest

from fbcli.config import Profile, Store, mask
from fbcli.errors import ConfigError


def test_save_and_load_roundtrip(store: Store) -> None:
    store.save(Profile(name="work", access_token="abc", app_id="1", app_secret="s"))
    loaded = store.load("work")
    assert loaded.access_token == "abc"
    assert loaded.app_id == "1"
    assert store.current_name() == "work"


def test_credentials_file_is_private(store: Store) -> None:
    store.save(Profile(name="default", access_token="abc"))
    mode = stat.S_IMODE(os.stat(store.path).st_mode)
    assert mode == 0o600


def test_env_overrides_stored_token(store: Store, monkeypatch) -> None:
    store.save(Profile(name="default", access_token="stored"))
    monkeypatch.setenv("FB_ACCESS_TOKEN", "from-env")
    assert store.load("default").access_token == "from-env"


def test_require_token_error(store: Store) -> None:
    with pytest.raises(ConfigError, match="No access token"):
        Profile(name="empty").require_token()


def test_require_app_error() -> None:
    with pytest.raises(ConfigError, match="App credentials"):
        Profile(name="x", access_token="t").require_app()


def test_token_for_page_prefers_page_token() -> None:
    profile = Profile(name="x", access_token="user", pages={"42": "page-token"})
    assert profile.token_for_page("42") == ("42", "page-token")


def test_token_for_page_falls_back_to_user_token() -> None:
    profile = Profile(name="x", access_token="user", default_page_id="7")
    assert profile.token_for_page(None) == ("7", "user")


def test_token_for_page_requires_a_page() -> None:
    with pytest.raises(ConfigError, match="No page selected"):
        Profile(name="x", access_token="t").token_for_page(None)


def test_delete_profile_switches_current(store: Store) -> None:
    store.save(Profile(name="a", access_token="1"))
    store.save(Profile(name="b", access_token="2"))
    assert store.delete("b") is True
    assert store.current_name() == "a"
    assert store.delete("missing") is False


def test_mask_hides_secret() -> None:
    assert mask("abcdefghijklmnop").startswith("abcd")
    assert "efghijkl" not in mask("abcdefghijklmnop")
    assert mask(None) == "—"
    assert mask("short") == "*****"
