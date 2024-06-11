from passlib.context import CryptContext
from sqlalchemy import select, update
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

    async def create_new(self, new_user: dict, confirmation_code: int):
        password = new_user.get("password")
        hashed_password = pwd_context.hash(password) if password else None
        user = User(
            username=new_user.get("username"),
            hashed_password=hashed_password,
            full_name=new_user.get("full_name"),
            email=new_user.get("email"),
            confirmation_code=confirmation_code,
        )
        self.async_session.add(user)
        await self.async_session.commit()
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
    async def update_info(self, email: str, code: int):
        if code:
            stmt = (
                update(User)
                .where(User.email == email)
                .values(is_active=True, confirmation_code=code)
            )
        else:
            stmt = update(User).where(User.email == email).values(is_active=True)
        await self.async_session.execute(stmt)


class GetRoleAssociation(BaseRepository):
    async def get_association(self):
        stmt = select(Role.id, Role.name)
        result = await self.async_session.execute(stmt)
        role_association = {}
        for id, name in result:
            role_association[id] = name
        return role_association
