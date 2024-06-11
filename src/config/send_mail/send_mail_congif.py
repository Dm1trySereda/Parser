from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class ConfigSendEmail(BaseSettings):
    EMAIL_ADDRESS: str
    APPLICATION_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int
    TIMEOUT: int


load_dotenv()
settings_send_mail = ConfigSendEmail()
