from abc import ABC, abstractmethod


class AbstractGenerateOtpCodeService(ABC):

    @abstractmethod
    async def generate_code(self):
        pass
