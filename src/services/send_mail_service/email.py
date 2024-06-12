import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from pydantic import EmailStr

from src.services.send_mail_service.abc import AbstractSendMailService


class SendMailService(AbstractSendMailService):
    def __init__(
        self,
        email_login: str,
        email_password: str,
        smtp_host: str,
        smtp_port: int,
        timeout: int,
    ):
        self._email_login = email_login
        self._email_password = email_password
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._timeout = timeout

    async def send_mail(
        self, sender_email: EmailStr, recipient_email: EmailStr, email: str
    ):
        msg = MIMEText(email, "html", "utf-8")
        email_subject = "Подтверждение регистрации на сайте OZBooks"
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = Header(email_subject, "utf-8")
        try:
            with smtplib.SMTP(
                self._smtp_host, self._smtp_port, self._timeout
            ) as server:
                server.starttls()
                server.login(self._email_login, self._email_password)
                server.sendmail(msg["From"], recipient_email, msg.as_string())
                logging.info(f"Email sent to {recipient_email}")
        except Exception as e:
            logging.error(f"Failed to send email to {recipient_email}: {e}")
