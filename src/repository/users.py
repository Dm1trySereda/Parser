from datetime import datetime, timedelta

from passlib.context import CryptContext
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

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
        query = query.options(joinedload(User.confirmation_email_code))
        return await self.async_session.execute(query)


class CreateNewUser(BaseRepository):

    async def create_new(self, new_user: dict, is_active: bool = False):
        password = new_user.get("password")
        hashed_password = pwd_context.hash(password) if password else None
        user = User(
            username=new_user.get("username"),
            hashed_password=hashed_password,
            full_name=new_user.get("full_name"),
            email=new_user.get("email"),
            is_active=is_active,
        )
        self.async_session.add(user)
        return user


class AddAuthProvider(BaseRepository):
    async def create_new_auth_provider(self, user: dict, provider: str):
        stmt = select(User.id).where(User.email == user.get("email"))
        result = await self.async_session.execute(stmt)
        user_id = result.scalar_one()

        auth_provider = AuthProvider(
            provider=provider,
            remote_user_id=user.get("remote_user_id"),
            full_name=user.get("full_name"),
            email=user.get("email"),
            user_id=user_id,
        )

        self.async_session.add(auth_provider)


class UpdateUserInformation(BaseRepository):
    async def update_info(self, email: str):
        stmt = update(User).where(User.email == email).values(is_active=True)
        await self.async_session.execute(stmt)


class DeleteInactiveUser(BaseRepository):
    async def delete_inactive_user(self, current_time: datetime):
        query = delete(User)
        query = query.filter(
            User.is_active.is_(False),
            User.created_at < current_time - timedelta(hours=1),
        )
        await self.async_session.execute(query)


class GetRoleAssociation(BaseRepository):
    async def get_association(self):
        stmt = select(Role.id, Role.name)
        result = await self.async_session.execute(stmt)
        role_association = {}
        for id, name in result:
            role_association[id] = name
        return role_association
