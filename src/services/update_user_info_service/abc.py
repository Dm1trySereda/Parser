from abc import abstractmethod, ABC

from pydantic import EmailStr


class AbstractUpdateUserInfoService(ABC):
    @abstractmethod
    async def update_info(self, email: EmailStr, code: int = None):
        pass
