from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import BaseUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.async_session = session


class SearchUser(BaseRepository):
    async def get_user(self, username: str):
        select_values = list()
        if username:
            select_values.append(BaseUser.username == username)
        stmt = select(BaseUser).where(*select_values)
        return await self.async_session.execute(stmt)


class CreateNewUser(BaseRepository):
    async def create_new(self, new_user: dict):
        password = new_user.get("password")
        hashed_password = pwd_context.hash(password) if password else None
        new_user = BaseUser(
            username=new_user.get("username"),
            hashed_password=hashed_password,
            full_name=new_user.get("full_name"),
            email=new_user.get("email"),
            is_google_user=new_user.get("is_google_user", False),
        )
        self.async_session.add(new_user)
        return new_user
