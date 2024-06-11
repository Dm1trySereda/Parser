from fastapi import HTTPException, status

from src.request_shemas.users import UserRequest
from src.response_schemas.users import UserResponse
from src.services.get_user_service.abc import AbstractGetUserService
from src.services.registration_user_service.abc import AbstractRegistrationUserService
from src.services.send_mail_service.abc import AbstractSendMailService


class RegistrationUserFacade:
    def __init__(
        self,
        search_services: AbstractGetUserService,
        registration_services: AbstractRegistrationUserService,
        send_mail_service: AbstractSendMailService,
    ):
        self.search_services = search_services
        self.registration_services = registration_services
        self.send_mail_service = send_mail_service

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
                detail="This email address is already in use maybe you need to auth_provider",
            )
        else:
            confirmation_code = await self.send_mail_service.send_mail(
                recipient_email=new_user.email
            )
            new_user_record = await self.registration_services.create_new_user(
                new_user=new_user, confirmation_code=confirmation_code
            )
            return new_user_record


"""
1)Пользователь регистрируется - отправляем письмо на почту, регистрируем, если код с почты верный
 - делаем пользователя активным (необходимые проверки - проверить есть ли пользователь с таким именем - если да - ошибка,
 есть ли пользователь с таким email и у него нет имени пользователя и пароля - значит это пользователь с авторизацией 
 через сторонние сервисы - проверить его почту - если пароль с почты верный - обновим информацию о пользователе 
 (добавим ему логин и пароль) - теперь пользователь сможет войти и по логину с паролем и через сторонний сервис
"""
