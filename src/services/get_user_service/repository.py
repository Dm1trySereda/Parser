from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users import SearchUser
from src.response_schemas.users import UserResponse
from src.services.get_user_service.abc import AbstractGetUserService
from pydantic import TypeAdapter


class RepositoryGetUserService(AbstractGetUserService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = SearchUser(session)

    async def get_current_user(
        self,
        email: str = None,
        remote_user_id: int = None,
        username: str = None,
    ) -> UserResponse | None:
        search_user = await self.repository.get_user(
            email=email, remote_user_id=remote_user_id, username=username
        )
        current_user = search_user.scalar_one_or_none()
        if current_user:
            return TypeAdapter(UserResponse).validate_python(current_user)
