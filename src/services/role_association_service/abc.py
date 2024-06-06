from abc import ABC, abstractmethod

from src.models.users import Role


class AbstractRoleAssociationService(ABC):
    @abstractmethod
    async def get_role_association(self) -> dict[int:str]:
        pass
