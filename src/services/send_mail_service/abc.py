from abc import ABC, abstractmethod

from pydantic import EmailStr


class AbstractSendMailService(ABC):
    @abstractmethod
    async def send_mail(
        self, sender_email: EmailStr, recipient_email: EmailStr, email: str
    ):
        pass
