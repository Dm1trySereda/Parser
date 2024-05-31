from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.async_session = session


class SearchUser(BaseRepository):
    async def get_user(self, username: str):
        select_values = list()
        if username:
            select_values.append(User.username == username)
        stmt = select(User).where(*select_values)
        return await self.async_session.execute(stmt)


class CreateNewUser(BaseRepository):
    async def create_new(self, new_user: dict):
        new_user = User(
            username=new_user.get("username"),
            hashed_password=pwd_context.hash(new_user.get("hashed_password")),
            full_name=new_user.get("full_name"),
            email=new_user.get("email"),
        )
        self.async_session.add(new_user)
        return new_user
