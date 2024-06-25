from abc import ABC, abstractmethod


class AbstractRoleAssociationService(ABC):
    @abstractmethod
    async def get_role_association(self) -> dict[int:str]:
        pass
