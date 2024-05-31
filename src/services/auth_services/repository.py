from src.services.auth_services.abc import AbstractAuthUserService
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.password_service.repository import RepositoryCreatePasswordService
from src.services.get_user_in_db_service.repository import RepositoryGetUserService


class RepositoryAuthUserService(AbstractAuthUserService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.verify = RepositoryCreatePasswordService()
        self.search_user = RepositoryGetUserService(session)

    async def authenticate_user(self, username: str, password: str):
        user = await self.search_user.get_current_user(username)
        if not user:
            return False
        if not self.verify.verify_password(password, user.hashed_password):
            return False
        return user
