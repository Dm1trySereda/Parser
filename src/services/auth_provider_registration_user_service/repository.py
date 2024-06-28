from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users import AddAuthProvider
from src.response_schemas.users import RemoteUserInfoResponse
from src.services.auth_provider_registration_user_service.abc import (
    AbstractAuthProviderRegistrationUserService,
)


class RepositoryAuthProviderRegistrationUserService(
    AbstractAuthProviderRegistrationUserService
):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = AddAuthProvider(session)

    async def create_new_auth_provider(
        self, user: RemoteUserInfoResponse, provider: str
    ):
        await self.repository.create_new_auth_provider(
            user.model_dump(by_alias=False), provider
        )
