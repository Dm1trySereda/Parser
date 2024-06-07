from fastapi import HTTPException, status

from src.request_shemas.users import UserRequest
from src.response_schemas.users import UserResponse
from src.services.get_user_service.abc import AbstractGetUserService
from src.services.registration_user_service.abc import AbstractRegistrationUserService


class RegistrationUserFacade:
    def __init__(
        self,
        search_services: AbstractGetUserService,
        registration_services: AbstractRegistrationUserService,
    ):
        self.search_services = search_services
        self.registration_services = registration_services

    async def registration_user(self, new_user: UserRequest) -> UserResponse:
        current_user_by_email = await self.search_services.get_current_user(
            email=new_user.email
        )
        current_user_by_username = await self.search_services.get_current_user(
            username=new_user.username
        )

        if current_user_by_email is None and current_user_by_username is None:
            new_user_record = await self.registration_services.create_new_user(new_user)
            return new_user_record
        if current_user_by_email and current_user_by_email.email == new_user.email:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Нужно обновить запись этого пользователя",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This user already exists",
            )
