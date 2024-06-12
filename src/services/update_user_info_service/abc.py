from abc import ABC, abstractmethod

from pydantic import EmailStr


class AbstractUpdateUserInfoService(ABC):
    @abstractmethod
    async def update_info(self, email: EmailStr):
        pass
