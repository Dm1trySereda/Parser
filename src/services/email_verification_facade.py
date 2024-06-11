from fastapi import HTTPException, status

from src.services.update_user_info_service.abc import (
    AbstractUpdateUserInfoService,
)


class EmailVerificationFacade:
    def __init__(self, update_user_info_service: AbstractUpdateUserInfoService):
        self.update_user_info_service = update_user_info_service

    async def verify_email(self, confirmation_code, user):
        if confirmation_code == user.confirmation_code:
            await self.update_user_info_service.update_info(email=user.email)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid confirmation code",
                headers={"WWW-Authenticate": "Bearer"},
            )
