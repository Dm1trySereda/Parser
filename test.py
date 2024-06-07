import httpx
import asyncio
from src.request_shemas.users import RemoteUserInfoRequest


async def get_remote_user_info(access_token):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://people.googleapis.com/v1/people/me",
            params={"personFields": "names,emailAddresses"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_info = response.json()
        email_data = profile_info["emailAddresses"][0]
        remote_user_id = email_data["metadata"]["source"]["id"]
        email_value = email_data["value"]
        full_name_data = profile_info["names"][0]
        full_name = full_name_data["displayName"]
        phone_number_data = profile_info.get("phoneNumbers")

        return RemoteUserInfoRequest(remote_user_id=remote_user_id, full_name=full_name, email=email_value)


print(asyncio.run(get_remote_user_info(
    "ya29.a0AXooCgs0dCFDBWn1wDSAw7k-ZrmKIqOyMvYZ4tvDhAYmFBKfXqmjOWmBQOLMMx1FDGKceAcqZ05l325fBApeZGdzVUdKizERO5ZF-svnRCfAB_cU0UvFEDE6w-dt7ZiGud5ohu2QKwIpwbmvz81GAFXwfrs8KUxcAWutaCgYKARwSARISFQHGX2MiRppZia9M3Corhjkae2vVDg0171")))
