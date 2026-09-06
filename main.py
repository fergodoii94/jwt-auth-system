"""Minimal JWT authentication example with safer configuration and errors."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Any, Callable, TypeVar, cast

import jwt

F = TypeVar("F", bound=Callable[..., Any])


def create_access_token(subject: str, expires_minutes: int = 30) -> str:
    secret = os.getenv("JWT_SECRET_KEY")
    if not secret:
        raise RuntimeError("JWT_SECRET_KEY environment variable is required")
    now = datetime.now(timezone.utc)
    payload = {"sub": subject, "iat": now, "exp": now + timedelta(minutes=expires_minutes)}
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_access_token(token: str) -> dict[str, Any]:
    secret = os.getenv("JWT_SECRET_KEY")
    if not secret:
        raise RuntimeError("JWT_SECRET_KEY environment variable is required")
    return cast(dict[str, Any], jwt.decode(token, secret, algorithms=["HS256"]))


def require_token(function: F) -> F:
    @wraps(function)
    def wrapper(token: str, *args: Any, **kwargs: Any) -> Any:
        try:
            claims = decode_access_token(token.removeprefix("Bearer ").strip())
        except (jwt.InvalidTokenError, RuntimeError) as exc:
            raise PermissionError("Invalid or expired token") from exc
        return function(claims, *args, **kwargs)

    return cast(F, wrapper)


@require_token
def protected_resource(claims: dict[str, Any]) -> str:
    return f"Authenticated subject: {claims['sub']}"


if __name__ == "__main__":
    print("JWT authentication example")
    print("Set JWT_SECRET_KEY before creating or decoding tokens.")
