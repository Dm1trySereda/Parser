from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.repository.users import CreateNewUser
from src.request_shemas.users import RemoteUserInfoRequest, UserRequest
from src.services.registration_user_service.abc import AbstractRegistrationUserService


class RepositoryRegistrationUserService(AbstractRegistrationUserService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = CreateNewUser(session)

    async def create_new_user(
        self,
        new_user: UserRequest | RemoteUserInfoRequest,
        is_active: bool = False,
    ) -> User:
        new_user_record = await self.repository.create_new(
            new_user.model_dump(by_alias=False), is_active
        )
        await self.session.flush([new_user_record])
        await self.session.refresh(new_user_record)
        return new_user_record
