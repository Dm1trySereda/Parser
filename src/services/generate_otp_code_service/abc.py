from abc import ABC, abstractmethod

from src.response_schemas.users import OneTimePassword


class AbstractGenerateOTPCodeService(ABC):

    @abstractmethod
    async def generate_qrcode(self, recipient_email) -> OneTimePassword:
        pass
