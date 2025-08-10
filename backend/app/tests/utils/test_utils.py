import pytest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.utils import EmailData, render_email_template, send_email
from app.core.config import settings


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
    mock_path.return_value.__truediv__.return_value.__truediv__.return_value.__truediv__.return_value = mock_file

    # Call function
    result = render_email_template(template_name="test.html", context={"name": "World"})

    # Assertions
    assert result == "Hello World!"
    mock_path.assert_called_once_with(__file__)
    mock_path.return_value.__truediv__.assert_called_once_with("email-templates")


@patch("app.utils.emails.Message")
def test_send_email(mock_message):
    """Test the send_email function."""
    # Setup
    mock_message_instance = MagicMock()
    mock_message.return_value = mock_message_instance

    # Temporarily set emails_enabled to True
    original_emails_enabled = settings.emails_enabled
    settings.emails_enabled = True

    try:
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
        mock_message_instance.send.assert_called_once()
    finally:
        # Restore original value
        settings.emails_enabled = original_emails_enabled


def test_send_email_disabled():
    """Test the send_email function when emails are disabled."""
    # Temporarily set emails_enabled to False
    original_emails_enabled = settings.emails_enabled
    settings.emails_enabled = False

    try:
        # Call function should raise an assertion error
        with pytest.raises(AssertionError):
            send_email(
                email_to="test@example.com",
                subject="Test Subject",
                html_content="<p>Test Content</p>",
            )
    finally:
        # Restore original value
        settings.emails_enabled = original_emails_enabled