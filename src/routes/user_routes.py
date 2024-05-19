from fastapi import APIRouter

user_routes = APIRouter(tags=['Users'])


@user_routes.get("/user/register")
async def register_user():
    return {"registered": True}
