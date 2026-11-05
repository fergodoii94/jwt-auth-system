import pytest

from main import create_access_token, protected_resource


def test_create_token_requires_configured_secret(monkeypatch):
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    with pytest.raises(RuntimeError, match="JWT_SECRET_KEY"):
        create_access_token("user-123")


def test_bearer_scheme_is_case_insensitive(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "x" * 48)
    token = create_access_token("user-123")

    assert protected_resource(token=f"bearer {token}") == "Authenticated subject: user-123"


def test_protected_resource_rejects_token_without_bearer_scheme(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "x" * 48)
    token = create_access_token("user-123")

    with pytest.raises(PermissionError, match="Bearer"):
        protected_resource(token=token)
