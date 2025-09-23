import pytest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch
import jwt

from app.utils import (
    EmailData, 
    render_email_template, 
    send_email, 
    generate_test_email,
    generate_reset_password_email,
    generate_new_account_email,
    generate_password_reset_token,
    verify_password_reset_token
)
from app.core.config import settings
from app.core import security


def test_email_data_class():
    """Test the EmailData dataclass."""
    email_data = EmailData(html_content="<p>Test</p>", subject="Test Subject")
    assert email_data.html_content == "<p>Test</p>"
    assert email_data.subject == "Test Subject"


@patch("app.utils.Path")
def test_render_email_template(mock_path):
    """Test the render_email_template function."""
    # Setup mock
    mock_file = MagicMock()
    mock_file.read_text.return_value = "Hello {{ name }}!"
    mock_path.return_value.parent.__truediv__.return_value.__truediv__.return_value.__truediv__.return_value = mock_file

    # Call function
    result = render_email_template(template_name="test.html", context={"name": "World"})

    # Assertions
    assert result == "Hello World!"
    # Don't assert on the mock calls as the implementation may change


@patch("app.utils.emails.Message")
def test_send_email_with_tls(mock_message):
    """Test the send_email function with TLS configuration."""
    # Setup
    mock_message_instance = MagicMock()
    mock_message.return_value = mock_message_instance

    # Temporarily set EMAILS_ENABLED to True
    original_emails_enabled = settings.EMAILS_ENABLED
    settings.EMAILS_ENABLED = True

    # Save original SMTP settings
    original_smtp_tls = settings.SMTP_TLS
    original_smtp_ssl = settings.SMTP_SSL
    original_smtp_user = settings.SMTP_USER
    original_smtp_password = settings.SMTP_PASSWORD

    try:
        # Configure SMTP settings for test
        settings.SMTP_TLS = True
        settings.SMTP_SSL = False
        settings.SMTP_USER = "testuser"
        settings.SMTP_PASSWORD = "testpassword"

        # Call function
        send_email(
            email_to="test@example.com",
            subject="Test Subject",
            html_content="<p>Test Content</p>",
        )

        # Assertions
        mock_message.assert_called_once_with(
            subject="Test Subject",
            html="<p>Test Content</p>",
            mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
        )
        mock_message_instance.send.assert_called_once_with(
            to="test@example.com",
            smtp={
                "host": settings.SMTP_HOST,
                "port": settings.SMTP_PORT,
                "tls": True,
                "user": "testuser",
                "password": "testpassword"
            }
        )
    finally:
        # Restore original values
        settings.EMAILS_ENABLED = original_emails_enabled
        settings.SMTP_TLS = original_smtp_tls
        settings.SMTP_SSL = original_smtp_ssl
        settings.SMTP_USER = original_smtp_user
        settings.SMTP_PASSWORD = original_smtp_password


@patch("app.utils.emails.Message")
def test_send_email_with_ssl(mock_message):
    """Test the send_email function with SSL configuration."""
    # Setup
    mock_message_instance = MagicMock()
    mock_message.return_value = mock_message_instance

    # Temporarily set EMAILS_ENABLED to True
    original_emails_enabled = settings.EMAILS_ENABLED
    settings.EMAILS_ENABLED = True

    # Save original SMTP settings
    original_smtp_tls = settings.SMTP_TLS
    original_smtp_ssl = settings.SMTP_SSL
    original_smtp_user = settings.SMTP_USER
    original_smtp_password = settings.SMTP_PASSWORD

    try:
        # Configure SMTP settings for test
        settings.SMTP_TLS = False
        settings.SMTP_SSL = True
        settings.SMTP_USER = "testuser"
        settings.SMTP_PASSWORD = "testpassword"

        # Call function
        send_email(
            email_to="test@example.com",
            subject="Test Subject",
            html_content="<p>Test Content</p>",
        )

        # Assertions
        mock_message.assert_called_once_with(
            subject="Test Subject",
            html="<p>Test Content</p>",
            mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
        )
        mock_message_instance.send.assert_called_once_with(
            to="test@example.com",
            smtp={
                "host": settings.SMTP_HOST,
                "port": settings.SMTP_PORT,
                "ssl": True,
                "user": "testuser",
                "password": "testpassword"
            }
        )
    finally:
        # Restore original values
        settings.EMAILS_ENABLED = original_emails_enabled
        settings.SMTP_TLS = original_smtp_tls
        settings.SMTP_SSL = original_smtp_ssl
        settings.SMTP_USER = original_smtp_user
        settings.SMTP_PASSWORD = original_smtp_password


@patch("app.utils.emails.Message")
def test_send_email_without_tls_ssl(mock_message):
    """Test the send_email function without TLS or SSL configuration."""
    # Setup
    mock_message_instance = MagicMock()
    mock_message.return_value = mock_message_instance

    # Temporarily set EMAILS_ENABLED to True
    original_emails_enabled = settings.EMAILS_ENABLED
    settings.EMAILS_ENABLED = True

    # Save original SMTP settings
    original_smtp_tls = settings.SMTP_TLS
    original_smtp_ssl = settings.SMTP_SSL
    original_smtp_user = settings.SMTP_USER
    original_smtp_password = settings.SMTP_PASSWORD

    try:
        # Configure SMTP settings for test
        settings.SMTP_TLS = False
        settings.SMTP_SSL = False
        settings.SMTP_USER = ""
        settings.SMTP_PASSWORD = ""

        # Call function
        send_email(
            email_to="test@example.com",
            subject="Test Subject",
            html_content="<p>Test Content</p>",
        )

        # Assertions
        mock_message.assert_called_once_with(
            subject="Test Subject",
            html="<p>Test Content</p>",
            mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
        )
        mock_message_instance.send.assert_called_once_with(
            to="test@example.com",
            smtp={
                "host": settings.SMTP_HOST,
                "port": settings.SMTP_PORT
            }
        )
    finally:
        # Restore original values
        settings.EMAILS_ENABLED = original_emails_enabled
        settings.SMTP_TLS = original_smtp_tls
        settings.SMTP_SSL = original_smtp_ssl
        settings.SMTP_USER = original_smtp_user
        settings.SMTP_PASSWORD = original_smtp_password


def test_send_email_disabled():
    """Test the send_email function when emails are disabled."""
    # Temporarily set EMAILS_ENABLED to False
    original_emails_enabled = settings.EMAILS_ENABLED
    settings.EMAILS_ENABLED = False

    try:
        # Call function with emails disabled
        send_email(
            email_to="test@example.com",
            subject="Test Subject",
            html_content="<p>Test Content</p>",
        )
    finally:
        # Restore original value
        settings.EMAILS_ENABLED = original_emails_enabled


def test_generate_password_reset_token():
    """Test the generate_password_reset_token function."""
    # Setup
    email = "test@example.com"
    
    # Call function
    token = generate_password_reset_token(email=email)
    
    # Assertions
    assert token is not None
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
    assert decoded["sub"] == email
    
    # Check expiration time
    now = datetime.now(timezone.utc).timestamp()
    expected_exp = now + timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS).total_seconds()
    assert abs(decoded["exp"] - expected_exp) < 10  # Allow for small time differences


def test_verify_password_reset_token_valid():
    """Test the verify_password_reset_token function with a valid token."""
    # Setup
    email = "test@example.com"
    token = generate_password_reset_token(email=email)
    
    # Call function
    result = verify_password_reset_token(token=token)
    
    # Assertions
    assert result == email


def test_verify_password_reset_token_invalid():
    """Test the verify_password_reset_token function with an invalid token."""
    # Call function with invalid token
    result = verify_password_reset_token(token="invalid-token")
    
    # Assertions
    assert result is None


def test_verify_password_reset_token_expired():
    """Test the verify_password_reset_token function with an expired token."""
    # Setup - create an expired token
    email = "test@example.com"
    now = datetime.now(timezone.utc)
    expired_time = now - timedelta(hours=1)  # Token expired 1 hour ago
    exp = expired_time.timestamp()
    
    expired_token = jwt.encode(
        {"exp": exp, "nbf": expired_time, "sub": email},
        settings.SECRET_KEY,
        algorithm=security.ALGORITHM,
    )
    
    # Call function
    result = verify_password_reset_token(token=expired_token)
    
    # Assertions
    assert result is None


@patch("app.utils.render_email_template")
def test_generate_test_email(mock_render):
    """Test the generate_test_email function."""
    # Setup
    mock_render.return_value = "<p>Test Email Content</p>"
    email_to = "test@example.com"
    
    # Call function
    result = generate_test_email(email_to=email_to)
    
    # Assertions
    assert isinstance(result, EmailData)
    assert result.subject == f"{settings.PROJECT_NAME} - Test email"
    assert result.html_content == "<p>Test Email Content</p>"
    mock_render.assert_called_once_with(
        template_name="test_email.html",
        context={"project_name": settings.PROJECT_NAME, "email": email_to}
    )


@patch("app.utils.render_email_template")
def test_generate_reset_password_email(mock_render):
    """Test the generate_reset_password_email function."""
    # Setup
    mock_render.return_value = "<p>Reset Password Email Content</p>"
    email_to = "test@example.com"
    email = "user@example.com"
    token = "test-token"
    
    # Call function
    result = generate_reset_password_email(email_to=email_to, email=email, token=token)
    
    # Assertions
    assert isinstance(result, EmailData)
    assert result.subject == f"{settings.PROJECT_NAME} - Password recovery for user {email}"
    assert result.html_content == "<p>Reset Password Email Content</p>"
    mock_render.assert_called_once_with(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": f"{settings.FRONTEND_HOST}/reset-password?token={token}",
        }
    )


@patch("app.utils.render_email_template")
def test_generate_new_account_email(mock_render):
    """Test the generate_new_account_email function."""
    # Setup
    mock_render.return_value = "<p>New Account Email Content</p>"
    email_to = "test@example.com"
    username = "testuser"
    password = "testpassword"
    
    # Call function
    result = generate_new_account_email(email_to=email_to, username=username, password=password)
    
    # Assertions
    assert isinstance(result, EmailData)
    assert result.subject == f"{settings.PROJECT_NAME} - New account for user {username}"
    assert result.html_content == "<p>New Account Email Content</p>"
    mock_render.assert_called_once_with(
        template_name="new_account.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": settings.FRONTEND_HOST,
        }
    )