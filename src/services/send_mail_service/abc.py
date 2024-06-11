from abc import abstractmethod, ABC

from pydantic import EmailStr


class AbstractSendMailService(ABC):
    @abstractmethod
    async def send_mail(self, recipient_email: EmailStr):
        pass
