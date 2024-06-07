from typing import Dict

from passlib.context import CryptContext
from sqlalchemy import and_, exists, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import AuthProvider, Role, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.async_session = session


class SearchUser(BaseRepository):
    async def get_user(self, **kwargs):
        query = select(User)
        if kwargs.get("email"):
            query = query.filter(User.email == kwargs.get("email"))
        if kwargs.get("username"):
            query = query.filter(User.username == kwargs.get("username"))
        remote_user_id = kwargs.get("remote_user_id")
        if remote_user_id:
            # query = query.filter(User.external_user_relationship.any(remote_user_id=remote_user_id))
            query = query.filter(
                User.id == AuthProvider.user_id,
                AuthProvider.remote_user_id == remote_user_id,
            )
        return await self.async_session.execute(query)


class CreateNewUser(BaseRepository):
    async def create_new(self, new_user: dict, provider: str):
        password = new_user.get("password")
        hashed_password = pwd_context.hash(password) if password else None
        user = User(
            username=new_user.get("username"),
            hashed_password=hashed_password,
            full_name=new_user.get("full_name"),
            email=new_user.get("email"),
        )
        self.async_session.add(user)
        await self.async_session.commit()
        if provider:
            auth_provider = AuthProvider(
                provider=provider,
                remote_user_id=new_user.get("remote_user_id"),
                full_name=new_user.get("full_name"),
                email=new_user.get("email"),
                user_id=user.id,
            )
            self.async_session.add(auth_provider)
        return user


class GetRoleAssociation(BaseRepository):
    async def get_association(self):
        stmt = select(Role.id, Role.name)
        result = await self.async_session.execute(stmt)
        role_association = {}
        for id, name in result:
            role_association[id] = name
        return role_association
