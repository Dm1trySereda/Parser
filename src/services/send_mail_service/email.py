import logging
import random
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from pydantic import EmailStr

from src.services.send_mail_service.abc import AbstractSendMailService


async def generate_confirmation_code():
    return random.randint(100000, 999999)


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

    async def send_mail(self, recipient_email: EmailStr):
        confirmation_code = await generate_confirmation_code()
        email_subject = "Подтверждение регистрации на сайте OZBooks"
        email_body = f"""
        <html>
        <body>
            <p style="font-size: 16px;">Здравствуйте,</p>
            <p style="font-size: 16px;">Вы указали свою электронную почту ({recipient_email}) для регистрации на сайте OZBooks.<br>
            Для завершения процесса регистрации, пожалуйста, подтвердите свою почту, введя следующий код:</p>
            <p><strong style="font-size: 18px;">Ваш код подтверждения: {confirmation_code}</strong></p>
            <p style="font-size: 16px;">Если вы не регистрировались на сайте OZBooks, пожалуйста, проигнорируйте это письмо.</p>
            <p style="font-size: 16px;">С уважением,<br>
            Команда OZBooks</p>
        </body>
        </html>
        """

        msg = MIMEText(email_body, "html", "utf-8")
        msg["Subject"] = Header(email_subject, "utf-8")

        msg["From"] = self._email_login
        msg["To"] = recipient_email
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
        return confirmation_code
