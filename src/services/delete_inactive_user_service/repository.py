from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users import DeleteInactiveUser
from src.services.delete_inactive_user_service.abc import (
    AbstractDeleteInactiveUserService,
)


class RepositoryDeleteInactiveUserService(AbstractDeleteInactiveUserService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.deleter = DeleteInactiveUser(session)

    async def delete_inactive_user(self, current_time: datetime):
        await self.deleter.delete_inactive_user(current_time)
