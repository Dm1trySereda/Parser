from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.repository.users import SearchUser
from src.services.get_user_service.abc import AbstractGetUserService


class RepositoryGetUserService(AbstractGetUserService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = SearchUser(session)

    async def get_current_user(
        self,
        email: str = None,
        remote_user_id: int = None,
        username: str = None,
    ) -> User | None:
        search_user = await self.repository.get_user(
            email=email, remote_user_id=remote_user_id, username=username
        )
        return search_user.scalar_one_or_none()
