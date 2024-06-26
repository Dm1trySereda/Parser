from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users import UpdateUserInformation
from src.services.update_user_info_service.abc import AbstractUpdateUserInfoService


class RepositoryUpdateUserInfoService(AbstractUpdateUserInfoService):
    def __init__(self, session: AsyncSession):
        self.updater = UpdateUserInformation(session)

    async def update_info(self, email: EmailStr):
        await self.updater.update_info(email)
