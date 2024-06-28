from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users import GetRoleAssociation
from src.services.role_association_service.abc import AbstractRoleAssociationService


class RepositoryRoleAssociationService(AbstractRoleAssociationService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = GetRoleAssociation(session)

    async def get_role_association(self) -> dict[int:str]:
        roles = await self.repository.get_association()
        role_association = {}
        for role_id, role_name in roles:
            role_association[role_id] = role_name
        return role_association
