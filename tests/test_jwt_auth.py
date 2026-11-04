from datetime import UTC, datetime, timedelta

import jwt
import pytest

from main import create_access_token, decode_access_token, protected_resource


def test_create_and_decode_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "x" * 48)
    token = create_access_token(" user-123 ")
    claims = decode_access_token(token)
    assert claims["sub"] == "user-123"
    assert "iat" in claims
    assert "exp" in claims


def test_create_token_rejects_empty_subject(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "x" * 48)
    with pytest.raises(ValueError):
        create_access_token("   ")


def test_create_token_rejects_non_positive_expiration(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "x" * 48)
    with pytest.raises(ValueError):
        create_access_token("user-123", expires_minutes=0)


def test_decode_rejects_short_secret(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "short")
    with pytest.raises(RuntimeError):
        decode_access_token("not-a-token")


def test_decode_rejects_expired_token(monkeypatch):
    secret = "x" * 48
    monkeypatch.setenv("JWT_SECRET_KEY", secret)
    now = datetime.now(UTC)
    token = jwt.encode(
        {
            "sub": "user-123",
            "iat": now - timedelta(minutes=2),
            "exp": now - timedelta(minutes=1),
        },
        secret,
        algorithm="HS256",
    )
    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token)


def test_decode_rejects_invalid_signature(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "x" * 48)
    token = jwt.encode(
        {
            "sub": "user-123",
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        },
        "y" * 48,
        algorithm="HS256",
    )

    with pytest.raises(jwt.InvalidSignatureError):
        decode_access_token(token)


def test_decode_requires_standard_claims(monkeypatch):
    secret = "x" * 48
    monkeypatch.setenv("JWT_SECRET_KEY", secret)
    token = jwt.encode(
        {"sub": "user-123", "iat": datetime.now(UTC)},
        secret,
        algorithm="HS256",
    )

    with pytest.raises(jwt.MissingRequiredClaimError):
        decode_access_token(token)


def test_protected_resource_accepts_bearer_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "x" * 48)
    token = create_access_token("user-123")
    assert protected_resource(token=f"Bearer {token}") == "Authenticated subject: user-123"


def test_protected_resource_rejects_invalid_token(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "x" * 48)
    with pytest.raises(PermissionError):
        protected_resource(token="invalid")
