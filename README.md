<div align="center">

# JWT Authentication Example

**A focused Python example of JSON Web Token creation and verification.**

[![CI](https://github.com/fergodoii94/jwt-auth-system/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/fergodoii94/jwt-auth-system/actions/workflows/ci-cd.yml)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-Pytest-0A9EDC?logo=pytest&logoColor=white)

</div>

A compact Python example demonstrating JSON Web Token creation, verification and decorator-based protection of a Python function.

## Implemented features

- Creates HS256 access tokens with subject, issued-at and expiration claims.
- Requires a non-empty subject and a positive token lifetime.
- Reads the signing key from `JWT_SECRET_KEY` and requires at least 32 bytes.
- Verifies the signature and requires `sub`, `iat` and `exp` claims.
- Provides a `require_token` decorator that passes verified claims to a protected function.
- Includes pytest coverage for token creation, expiration, invalid signatures, required claims, key validation and protected access.

## Security design choices

- **Pinned algorithm:** the decoder accepts only HS256 rather than trusting the token header to choose an algorithm.
- **Required claims:** tokens must contain `sub`, `iat` and `exp`; expired tokens and invalid signatures are rejected.
- **Managed secret input:** `JWT_SECRET_KEY` is read from the environment and must contain at least 32 bytes. There is no hard-coded fallback.
- **Small integration surface:** `require_token` demonstrates function-level protection and passes verified claims to the wrapped function. It is not a FastAPI dependency or a complete user-authentication system.

## Tech stack

- Python 3.11+
- JSON Web Tokens (HS256)
- Pytest
- Ruff

## Run locally

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

## Quality checks

```bash
ruff check main.py tests
pytest -q
```

GitHub Actions runs these checks on pushes and pull requests to `main`. Check the Actions tab for the result associated with each commit.

## Security scope and limitations

> **Portfolio scope:** This is an educational token-handling example, not a complete authentication service.

It does not implement user registration, password hashing, refresh-token rotation/revocation, key rotation, issuer/audience validation, role-based authorization, HTTP middleware or a FastAPI bearer-auth integration. The decorator expects a token argument directly.

Before production use, add a managed secret/key lifecycle, strict issuer/audience policy, framework-level authentication/authorization and a broader security test suite.

---

<div align="center">
  <sub>Part of my Python backend engineering portfolio.</sub>
</div>
