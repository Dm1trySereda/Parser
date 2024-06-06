from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.repository.users import CreateNewUser, SearchUser
from src.request_shemas.users import GoogleUserRequest, UserRequest
from src.services.registration_user_service.abc import AbstractRegistrationUserService


class RepositoryRegistrationUserService(AbstractRegistrationUserService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.searcher = SearchUser(session)
        self.inserter = CreateNewUser(session)

    async def create_new_user(
        self, new_user: UserRequest | GoogleUserRequest
    ) -> User | None:
        new_user_record = await self.inserter.create_new(
            new_user=new_user.model_dump(by_alias=False)
        )
        await self.session.flush([new_user_record])
        await self.session.refresh(new_user_record)
        return new_user_record
