from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.repository.users import SearchUser
from src.services.get_user_in_db_service.abc import AbstractGeUserInDbService


class RepositoryGetUserService(AbstractGeUserInDbService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.searcher = SearchUser(session)

    async def get_current_user(self, username: str) -> User:
        search_user = await self.searcher.get_user(username)
        return search_user.scalar_one_or_none()
