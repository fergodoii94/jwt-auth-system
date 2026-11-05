from __future__ import annotations

import os
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from functools import wraps
from typing import Any, TypeVar, cast

import jwt

F = TypeVar("F", bound=Callable[..., Any])


def _get_secret() -> str:
    secret = os.getenv("JWT_SECRET_KEY")
    if not secret:
        raise RuntimeError("JWT_SECRET_KEY environment variable is required")
    if len(secret.encode("utf-8")) < 32:
        raise RuntimeError("JWT_SECRET_KEY must contain at least 32 bytes")
    return secret


def create_access_token(subject: str, expires_minutes: int = 30) -> str:
    normalized_subject = subject.strip()
    if not normalized_subject:
        raise ValueError("Token subject cannot be empty")
    if expires_minutes <= 0:
        raise ValueError("Token expiration must be greater than zero")

    now = datetime.now(UTC)
    payload = {
        "sub": normalized_subject,
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, _get_secret(), algorithm="HS256")


def decode_access_token(token: str) -> dict[str, Any]:
    claims = jwt.decode(
        token,
        _get_secret(),
        algorithms=["HS256"],
        options={"require": ["sub", "iat", "exp"]},
    )
    if not isinstance(claims.get("sub"), str) or not claims["sub"].strip():
        raise jwt.InvalidTokenError("Token subject is missing or empty")
    return cast(dict[str, Any], claims)


def require_token(function: F) -> F:
    @wraps(function)
    def wrapper(token: str, *args: Any, **kwargs: Any) -> Any:
        scheme, separator, credentials = token.strip().partition(" ")
        if not separator or scheme.lower() != "bearer" or not credentials.strip():
            raise PermissionError("Authorization must use the Bearer scheme")

        try:
            claims = decode_access_token(credentials.strip())
        except (jwt.InvalidTokenError, RuntimeError) as exc:
            raise PermissionError("Invalid or expired token") from exc
        return function(claims, *args, **kwargs)

    return cast(F, wrapper)


@require_token
def protected_resource(claims: dict[str, Any]) -> str:
    return f"Authenticated subject: {claims['sub']}"


if __name__ == "__main__":
    print("JWT authentication example")
    print("Set a random JWT_SECRET_KEY of at least 32 bytes before use.")
