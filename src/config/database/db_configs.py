from typing import Optional

from dotenv import load_dotenv
from pydantic import MySQLDsn
from pydantic_settings import BaseSettings


class ConfigDataBase(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DATABASE: str
    DB_ECHO_LOG: bool = False
    # AUTH_SERVICE_URL: str
    # AUTH_SERVICE_API_KEY: str

    @property
    def database_url(self) -> Optional[MySQLDsn]:
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
            f"localhost:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )

    @property
    def async_database_url(self) -> Optional[MySQLDsn]:
        return (
            f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@"
            f"{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        )

    class Config:
        extra = "ignore"


load_dotenv()
setting_db = ConfigDataBase()
