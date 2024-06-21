from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import Role
from src.repositories.users import GetRoleAssociation
from src.services.role_association_service.abc import AbstractRoleAssociationService


class RepositoryRoleAssociationService(AbstractRoleAssociationService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.role_association = GetRoleAssociation(session)

    async def get_role_association(self) -> dict[int:str]:
        return await self.role_association.get_association()
