from fastapi import HTTPException, status

from src.request_shemas.users import GoogleUserRequest, UserRequest
from src.response_schemas.users import UserResponse
from src.services.get_user_in_db_service.abc import AbstractGeUserInDbService
from src.services.registration_user_service.abc import AbstractRegistrationUserService


class RegistrationUserFacade:
    def __init__(
        self,
        search_services: AbstractGeUserInDbService,
        registration_services: AbstractRegistrationUserService,
    ):
        self.search_services = search_services
        self.registration_services = registration_services

    async def registration_user(
        self, new_user: UserRequest | GoogleUserRequest
    ) -> UserResponse:
        current_user = await self.search_services.get_current_user(
            username=new_user.username
        )
        if current_user is None:
            new_user_record = await self.registration_services.create_new_user(new_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this username already exist",
            )
        return new_user_record
