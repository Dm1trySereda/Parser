from typing import Dict

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import Role, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.async_session = session


class SearchUser(BaseRepository):
    async def get_user(self, username: str):
        stmt = select(User).where(User.username == username)
        return await self.async_session.execute(stmt)


class CreateNewUser(BaseRepository):
    async def create_new(self, new_user: dict):
        password = new_user.get("password")
        hashed_password = pwd_context.hash(password) if password else None
        new_user = User(
            username=new_user.get("username"),
            hashed_password=hashed_password,
            full_name=new_user.get("full_name"),
            email=new_user.get("email"),
        )
        self.async_session.add(new_user)
        return new_user


class GetRoleAssociation(BaseRepository):
    async def get_association(self):
        stmt = select(Role.id, Role.name)
        result = await self.async_session.execute(stmt)
        role_association = {}
        for id, name in result:
            role_association[id] = name
        return role_association
