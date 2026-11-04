# JWT Authentication Example

A compact Python example demonstrating JSON Web Token creation, verification and decorator-based protection of a Python function.

## Current implementation

- Creates HS256 access tokens with a subject, issued-at time and expiration.
- Verifies token signatures and expiration with PyJWT.
- Reads the signing key from the `JWT_SECRET_KEY` environment variable.
- Provides a `require_token` decorator that passes verified claims to a protected function.
- Raises a permission error for invalid or expired tokens.

## Requirements

Python 3.10+ and PyJWT.

```bash
python -m venv .venv
source .venv/bin/activate
pip install PyJWT
export JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
python main.py
```

Do not commit the generated key or use a development key in production.

## Example usage

```python
from main import create_access_token, protected_resource

token = create_access_token("user-123")
print(protected_resource(token=token))
```

The protected function receives verified claims after the decorator validates the bearer token.

## Security scope and limitations

This is an educational token-handling example, not a complete authentication service. It does not implement user registration, password hashing, refresh-token rotation/revocation, key rotation, issuer/audience validation, role-based authorization, HTTP middleware or a FastAPI dependency. The decorator expects a token argument directly and is not an HTTP bearer-auth integration.

Before production use, add a managed secret/key lifecycle, strict token claim validation, tests for invalid/expired tokens, and framework-level authentication/authorization.

