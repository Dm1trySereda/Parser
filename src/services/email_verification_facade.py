from pydantic import EmailStr

from src.custom_exceptions.exseptions import OTPCodeError
from src.services.generate_otp_code_service.abc import AbstractGenerateOTPCodeService
from src.services.update_user_info_service.abc import AbstractUpdateUserInfoService


class EmailVerificationFacade:
    def __init__(
        self,
        update_user_info_service: AbstractUpdateUserInfoService,
        generate_otp_code_service: AbstractGenerateOTPCodeService,
    ):
        self.update_user_info_service = update_user_info_service
        self.generate_otp_code_service = generate_otp_code_service

    async def verify_email(
        self,
        user_confirmation_code: int,
        recipient_email: EmailStr,
    ):
        generate = await self.generate_otp_code_service.generate_qrcode(recipient_email)
        if user_confirmation_code == generate.otp_code:
            await self.update_user_info_service.update_info(email=recipient_email)
        else:
            raise OTPCodeError
