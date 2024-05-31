from passlib.context import CryptContext

from src.services.password_service.abc import AbstractCreatePasswordService


class RepositoryCreatePasswordService(AbstractCreatePasswordService):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    async def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)
