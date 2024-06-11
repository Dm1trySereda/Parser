from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class ConfigAuth(BaseSettings):
    SIGNATURE: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URL: str


load_dotenv()
settings_auth = ConfigAuth()
