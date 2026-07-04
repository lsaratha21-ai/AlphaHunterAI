"""Email sender for scheduled tasks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.exceptions import ProviderError


class EmailSender:
    """Sender for email notifications with reports."""

    def __init__(
        self,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 587,
        email: str | None = None,
        password: str | None = None,
    ) -> None:
        """Initialize the EmailSender.

        Args:
            smtp_server: SMTP server address.
            smtp_port: SMTP server port.
            email: Sender email address.
            password: Email password or app password.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    def send_report_email(
        self,
        recipients: list[str],
        subject: str,
        body: str,
        attachments: list[str] | None = None,
    ) -> None:
        """Send email with report attachments.

        Args:
            recipients: List of recipient email addresses.
            subject: Email subject.
            body: Email body text.
            attachments: List of file paths to attach.

        Raises:
            ProviderError: If email sending fails.
        """
        if not self.email or not self.password:
            raise ProviderError("Email credentials not configured")

        try:
            msg = MIMEMultipart()
            msg["From"] = self.email
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            if attachments:
                for file_path in attachments:
                    path = Path(file_path)
                    if path.exists():
                        with open(path, "rb") as f:
                            part = MIMEApplication(
                                f.read(),
                                Name=path.name,
                            )
                        part["Content-Disposition"] = f'attachment; filename="{path.name}"'
                        msg.attach(part)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)

        except Exception as e:
            raise ProviderError(f"Failed to send email: {e}")

    def send_report_notification(
        self,
        recipients: list[str],
        report_date: str,
        report_files: list[str],
    ) -> None:
        """Send notification that reports are ready.

        Args:
            recipients: List of recipient email addresses.
            report_date: Date of the report.
            report_files: List of generated report file paths.
        """
        subject = f"AlphaHunter AI Report - {report_date}"
        body = f"""
AlphaHunter AI Report is ready for {report_date}.

Generated Reports:
"""
        for file_path in report_files:
            body += f"- {file_path}\n"

        body += "\nPlease find the reports attached."

        self.send_report_email(recipients, subject, body, report_files)
