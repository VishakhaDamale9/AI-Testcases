import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import jwt
from jwt.exceptions import InvalidTokenError

from app.core import security
from app.core.config import settings


def test_create_access_token():
    """Test creating an access token."""
    # Test with default expiration
    token = security.create_access_token(subject="test@example.com")
    decoded = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
    )
    assert decoded["sub"] == "test@example.com"
    assert "exp" in decoded

    # Test with custom expiration
    expires_delta = timedelta(minutes=30)
    token = security.create_access_token(
        subject="test@example.com", expires_delta=expires_delta
    )
    decoded = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
    )
    assert decoded["sub"] == "test@example.com"
    assert "exp" in decoded


def test_verify_password():
    """Test password verification."""
    hashed_password = security.get_password_hash("password123")
    assert security.verify_password("password123", hashed_password)
    assert not security.verify_password("wrong-password", hashed_password)


def test_get_password_hash():
    """Test password hashing."""
    hashed_password = security.get_password_hash("password123")
    assert hashed_password != "password123"
    assert security.verify_password("password123", hashed_password)