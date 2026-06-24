"""
Security utilities: JWT token creation/verification and password hashing.
"""

from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import TokenExpiredException, TokenInvalidException

# ── Password hashing ──────────────────────────────────────────────────────────

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Return bcrypt hash of a plain-text password."""
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return True if the plain-text password matches the hash."""
    return _pwd_context.verify(plain_password, hashed_password)


# ── JWT ───────────────────────────────────────────────────────────────────────

def create_access_token(subject: str | UUID, extra_claims: dict[str, Any] | None = None) -> str:
    """Create a signed JWT access token."""
    now = datetime.now(tz=timezone.utc)
    expires = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": now,
        "exp": expires,
        "type": "access",
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(subject: str | UUID) -> str:
    """Create a signed JWT refresh token."""
    now = datetime.now(tz=timezone.utc)
    expires = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": now,
        "exp": expires,
        "type": "refresh",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT token.

    Raises:
        TokenExpiredException: if the token is expired.
        TokenInvalidException: if the token is malformed or signature is wrong.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as exc:
        if "expired" in str(exc).lower():
            raise TokenExpiredException() from exc
        raise TokenInvalidException() from exc


def get_subject_from_token(token: str) -> str:
    """Return the `sub` claim from a valid JWT token."""
    payload = decode_token(token)
    sub = payload.get("sub")
    if not sub:
        raise TokenInvalidException()
    return str(sub)
