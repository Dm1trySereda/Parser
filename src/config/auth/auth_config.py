from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class ConfigAuth(BaseSettings):
    SIGNATURE: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


load_dotenv()
settings_auth = ConfigAuth()
