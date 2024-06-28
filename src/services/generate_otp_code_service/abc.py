from abc import ABC, abstractmethod

from pydantic import EmailStr

from src.response_schemas.users import OneTimePassword


class AbstractGenerateOTPCodeService(ABC):

    @abstractmethod
    async def generate_qrcode(self, recipient_email: EmailStr) -> OneTimePassword:
        pass
