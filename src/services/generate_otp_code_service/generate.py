import random

from src.services.generate_otp_code_service.abc import AbstractGenerateOtpCodeService


class GenerateOtpCodeService(AbstractGenerateOtpCodeService):

    async def generate_code(self):
        return random.randint(100000, 999999)
