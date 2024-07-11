from fastapi import HTTPException, status

from src.custom_exceptions.exseptions import UsernameError, EmailError
from src.request_shemas.users import UserRequest
from src.response_schemas.users import UserResponse
from src.services.generate_otp_code_service.generate import (
    AbstractGenerateOTPCodeService,
)
from src.services.get_user_service.abc import AbstractGetUserService
from src.services.registration_user_service.abc import AbstractRegistrationUserService
from src.services.render_template_service.abc import AbstractRenderTemplateService
from src.services.send_mail_service.abc import AbstractSendMailService
from src.enums.template import RenderTemplateChoices


class RegistrationUserFacade:
    def __init__(
        self,
        search_services: AbstractGetUserService,
        registration_services: AbstractRegistrationUserService,
        send_mail_service: AbstractSendMailService,
        generate_otp_code_service: AbstractGenerateOTPCodeService,
        email_login: str,
        render_template_service: AbstractRenderTemplateService,
    ):
        self.search_services = search_services
        self.registration_services = registration_services
        self.send_mail_service = send_mail_service
        self.generate_otp_code_service = generate_otp_code_service
        self._email_login = email_login
        self.render_template_service = render_template_service

    async def registration_user(self, new_user: UserRequest) -> UserResponse:
        current_user_by_username = await self.search_services.get_current_user(
            username=new_user.username
        )
        current_user_by_email = await self.search_services.get_current_user(
            email=new_user.email
        )
        if current_user_by_username:
            raise UsernameError

        if current_user_by_email:
            raise EmailError
        else:
            generate = await self.generate_otp_code_service.generate_qrcode(
                recipient_email=new_user.email
            )
            email_content = await self.render_template_service.render_template(
                value=new_user.email,
                template=RenderTemplateChoices.registration_mail.value,
            )

            await self.send_mail_service.send_mail(
                sender_email=self._email_login,
                recipient_email=new_user.email,
                email_body=email_content,
                qrcode=generate.qrcode,
            )

            new_user_record = await self.registration_services.create_new_user(
                new_user=new_user
            )
            return new_user_record
