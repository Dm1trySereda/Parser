from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.async_session = session


class GetCurrentUser(BaseRepository):
    async def get_user(self, **kwargs):
        select_values = list()
        if kwargs.get("username"):
            select_values.append(User.username == kwargs.get("username"))
        if kwargs.get("full_name"):
            select_values.append((User.full_name == kwargs.get("full_name")))
        stmt = select(User).where(*select_values)
        return await self.async_session.execute(stmt)


class CreateNewUser(BaseRepository):
    async def create_new(self, new_user: dict):
        new_user = User(
            username=new_user.get("username"),
            full_name=new_user.get("full_name"),
            email=new_user.get("email"),
            hashed_password=pwd_context.hash(new_user.get("hashed_password")),
            is_active=new_user.get("is_active"),
        )
        self.async_session.add(new_user)
        return new_user
