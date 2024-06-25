from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.services.auth_services.abc import AbstractAuthUserService
from src.services.get_user_service.repository import RepositoryGetUserService
from src.services.password_service.manager import PasswordManagerService


class RepositoryAuthUserService(AbstractAuthUserService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.verify_password_service = PasswordManagerService()
        self.search_user_service = RepositoryGetUserService(session)

    async def authenticate_user(self, username: str, password: str) -> User | None:
        user = await self.search_user_service.get_current_user(username=username)
        if user and await self.verify_password_service.verify_password(
            plain_password=password, hashed_password=user.hashed_password
        ):
            return user
        else:
            return None
