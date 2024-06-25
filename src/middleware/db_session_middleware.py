from fastapi import Request

from src.config.database.db_helpers import db_helper


async def db_session_middleware(request: Request, call_next):
    async with db_helper.get_db_session() as session:
        request.state.db = session
        response = await call_next(request)
    return response
