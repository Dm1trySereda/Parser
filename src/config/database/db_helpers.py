from asyncio import current_task
from contextlib import asynccontextmanager

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    async_sessionmaker, create_async_engine)

from .db_configs import setting_db


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url, echo=echo)
        self.session_manager = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    def get_scoped_session(self):
        return async_scoped_session(self.session_manager, scopefunc=current_task)

    @asynccontextmanager
    async def get_db_session(self):
        session: AsyncSession = self.session_manager()
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise error
        finally:
            await session.close()


db_helper = DatabaseHelper(setting_db.async_database_url, setting_db.DB_ECHO_LOG)
