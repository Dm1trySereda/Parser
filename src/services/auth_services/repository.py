from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.repository.users import CreateNewUser, GetCurrentUser
from src.response_schemas.users import UserInDBResponse
from src.services.auth_services.abc import AbstractGetCurrentUserService


class RepositoryGetCurrentUserService(AbstractGetCurrentUserService):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_current_user(self, **kwargs: dict) -> User:
        searcher = GetCurrentUser(self.session)
        search_user = await searcher.get_user(**kwargs)
        return search_user.scalar_one_or_none()

    async def create_user(self, new_user: UserInDBResponse) -> User | Any:
        current_user = await self.get_current_user(username=new_user.username)
        if current_user is None:
            inserter = CreateNewUser(self.session)
            new_user_record = await inserter.create_new(
                new_user=new_user.model_dump(by_alias=False)
            )
            await self.session.flush([new_user_record])
            await self.session.refresh(new_user_record)
            return new_user_record
        return None
