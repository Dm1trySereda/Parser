from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.users import AddAuthProvider
from src.request_shemas.users import RemoteUserInfoRequest
from src.services.auth_provider_registration_user_service.abc import (
    AbstractAuthProviderRegistrationUserService,
)


class RepositoryAuthProviderRegistrationUserService(
    AbstractAuthProviderRegistrationUserService
):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.inserter = AddAuthProvider(session)

    async def create_new_auth_provider(
        self, user: RemoteUserInfoRequest, provider: str
    ):
        await self.inserter.create_new_auth_provider(
            user.model_dump(by_alias=False), provider
        )
