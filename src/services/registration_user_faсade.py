from fastapi import HTTPException, status

from src.request_shemas.users import UserRequest
from src.response_schemas.users import UserResponse
from src.services.generate_otp_code_service.generate import (
    AbstractGenerateOtpCodeService,
)
from src.services.get_user_service.abc import AbstractGetUserService
from src.services.registration_user_service.abc import AbstractRegistrationUserService
from src.services.send_mail_service.abc import AbstractSendMailService


class RegistrationUserFacade:
    def __init__(
        self,
        search_services: AbstractGetUserService,
        registration_services: AbstractRegistrationUserService,
        send_mail_service: AbstractSendMailService,
        generate_otp_code_service: AbstractGenerateOtpCodeService,
        email_login: str,
    ):
        self.search_services = search_services
        self.registration_services = registration_services
        self.send_mail_service = send_mail_service
        self.generate_otp_code_service = generate_otp_code_service
        self._email_login = email_login

    async def registration_user(self, new_user: UserRequest) -> UserResponse:
        current_user_by_username = await self.search_services.get_current_user(
            username=new_user.username
        )
        current_user_by_email = await self.search_services.get_current_user(
            email=new_user.email
        )
        if current_user_by_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already exists",
            )
        if current_user_by_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email address is already in use maybe you need to auth",
            )
        else:
            confirmation_code = await self.generate_otp_code_service.generate_code()
            with open("src/templates/registration_mail.html", "r") as file:
                registration_mail = file.read()
                email_content = registration_mail.format(
                    confirmation_code=confirmation_code, recipient_email=new_user.email
                )
                await self.send_mail_service.send_mail(
                    sender_email=self._email_login,
                    recipient_email=new_user.email,
                    email=email_content,
                )
            new_user_record = await self.registration_services.create_new_user(
                new_user=new_user, confirmation_code=confirmation_code
            )
            return new_user_record
