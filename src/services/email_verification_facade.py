from fastapi import HTTPException, status

from src.services.get_user_service.abc import AbstractGetUserService
from src.services.update_user_info_service.abc import AbstractUpdateUserInfoService


class EmailVerificationFacade:
    def __init__(
        self,
        update_user_info_service: AbstractUpdateUserInfoService,
        get_user_service: AbstractGetUserService,
    ):
        self.update_user_info_service = update_user_info_service
        self.get_user_service = get_user_service

    async def verify_email(self, code, email):
        user = await self.get_user_service.get_current_user(email)
        confirmation_email = int(user.confirmation_email_code.code)
        if code == confirmation_email:
            await self.update_user_info_service.update_info(email=user.email)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid confirmation code",
                headers={"WWW-Authenticate": "Bearer"},
            )
