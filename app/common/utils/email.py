"""Simple SMTP text email utility configured for Gmail by default.

Usage:
    from app.common.utils.email import send_email
    await send_email(to_email="user@example.com", subject="Hello", body="Hi")
"""

from __future__ import annotations

import asyncio
import smtplib

from app.core.config import SETTINGS


def _send_email_sync(
    to_email: str,
    subject: str,
    body: str,
) -> None:
    host = SETTINGS.SMTP_HOST
    port = SETTINGS.SMTP_PORT
    username = SETTINGS.SMTP_USERNAME
    password = SETTINGS.SMTP_PASSWORD
    use_tls = SETTINGS.SMTP_USE_TLS
    from_email = SETTINGS.SMTP_FROM_EMAIL or (username or "")
    from_name = SETTINGS.SMTP_FROM_NAME

    if not host or not port or not from_email:
        raise RuntimeError("SMTP settings are not configured properly.")

    # Minimal RFC2822 text message with headers
    from_header = f"{from_name} <{from_email}>" if from_name else from_email
    headers = [
        f"From: {from_header}",
        f"To: {to_email}",
        f"Subject: {subject}",
        "MIME-Version: 1.0",
        "Content-Type: text/plain; charset=utf-8",
        "Content-Transfer-Encoding: 8bit",
    ]
    message = "\r\n".join(headers) + "\r\n\r\n" + (body or "")

    with smtplib.SMTP(host, port) as server:
        server.ehlo()
        if use_tls:
            server.starttls()
            server.ehlo()
        if username and password:
            server.login(username, password)
        server.sendmail(from_email, [to_email], message)


async def send_email(
    to_email: str,
    subject: str,
    body: str,
) -> None:
    """Send a plain text email using SMTP (runs in a thread)."""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(
        None,
        _send_email_sync,
        to_email,
        subject,
        body,
    )
