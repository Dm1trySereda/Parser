from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.users import CreateNewUser
from src.request_shemas.users import UserRequest
from src.response_schemas.users import RemoteUserInfoResponse, UserResponse
from src.services.registration_user_service.abc import AbstractRegistrationUserService
from pydantic import TypeAdapter


class RepositoryRegistrationUserService(AbstractRegistrationUserService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = CreateNewUser(session)

    async def create_new_user(
        self,
        new_user: UserRequest | RemoteUserInfoResponse,
        is_active: bool = False,
    ) -> UserResponse:
        new_user_record = await self.repository.create_new(
            new_user.model_dump(by_alias=False), is_active
        )
        return TypeAdapter(UserResponse).validate_python(new_user_record)
