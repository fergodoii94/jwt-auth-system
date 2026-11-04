# JWT Authentication Example

A compact Python example demonstrating JSON Web Token creation, verification and decorator-based protection of a Python function.

## Implemented features

- Creates HS256 access tokens with subject, issued-at and expiration claims.
- Requires a non-empty subject and a positive token lifetime.
- Reads the signing key from `JWT_SECRET_KEY` and requires at least 32 bytes.
- Verifies the signature and requires `sub`, `iat` and `exp` claims.
- Provides a `require_token` decorator that passes verified claims to a protected function.
- Includes pytest coverage for token creation, expiration, key validation and protected access.

## Run locally

Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
export JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
pytest -q
```

Do not commit the generated key or use a development key in production.

## Example usage

```python
from main import create_access_token, protected_resource

token = create_access_token("user-123")
print(protected_resource(token=f"Bearer {token}"))
```

The protected function receives verified claims after the decorator validates the bearer token.

## Security scope and limitations

This is an educational token-handling example, not a complete authentication service. It does not implement user registration, password hashing, refresh-token rotation/revocation, key rotation, issuer/audience validation, role-based authorization, HTTP middleware or a FastAPI bearer-auth integration. The decorator expects a token argument directly.

Before production use, add a managed secret/key lifecycle, strict issuer/audience policy, framework-level authentication/authorization and a broader security test suite.
