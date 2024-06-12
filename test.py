# import logging
# import os
# import smtplib
# from email.header import Header
# from email.mime.text import MIMEText
#
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
# )
#
#
# def send_email(recipients_mail: list, msg_text: str):
#
#     email_login = os.getenv("EMAIL_LOGIN", "ll-O-E-Xa-l-i@yandex.by")
#     email_password = os.getenv("EMAIL_PASSWORD", "instczoubunjqjwi")
#
#     msg = MIMEText(f"{msg_text}", "plain", "utf-8")
#     msg["Subject"] = Header("OZ Books", "utf-8")
#     msg["From"] = email_login
#     msg["To"] = ",".join(recipients_mail)
#
#     smtp_server = "smtp.yandex.ru"
#     smtp_port = 587
#
#     try:
#         with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
#             server.starttls()
#             server.login(email_login, email_password)
#             server.sendmail(msg["From"], recipients_mail, msg.as_string())
#             logging.info(f"Email sent to {', '.join(recipients_mail)}")
#     except Exception as e:
#         logging.error(f"Failed to send email to {', '.join(recipients_mail)}: {e}")
#
#
# def main():
#     code = 345896
#     send_email(
#         recipients_mail=["dima.sereda.d@gmail.com", "dmitry.sereda.d@gmail.com"],
#         msg_text=f"Ваш код: {code}",
#     )
#
#
# if __name__ == "__main__":
#     main()
