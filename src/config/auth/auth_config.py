from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class ConfigAuth(BaseSettings):
    SIGNATURE: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


load_dotenv()
settings_auth = ConfigAuth()


