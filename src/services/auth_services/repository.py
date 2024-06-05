from sqlalchemy.ext.asyncio import AsyncSession

from src.services.auth_services.abc import AbstractAuthUserService
from src.services.get_user_in_db_service.repository import RepositoryGetUserService
from src.services.password_service.repository import RepositoryCreatePasswordService


class RepositoryAuthUserService(AbstractAuthUserService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.verify = RepositoryCreatePasswordService()
        self.search_user = RepositoryGetUserService(session)

    async def authenticate_user(self, username: str, password: str):
        user = await self.search_user.get_current_user(username)
        if user and await self.verify.verify_password(
            plain_password=password, hashed_password=user.hashed_password
        ):
            return user
        else:
            return None
