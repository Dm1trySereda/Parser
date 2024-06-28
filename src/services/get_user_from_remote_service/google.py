import httpx

from src.response_schemas.users import RemoteUserInfoResponse
from src.response_schemas.users import RemoteToken
from src.services.get_user_from_remote_service.abc import (
    AbstractGetUserInfoFromRemoteService,
)


class GetGoogleUserInfoService(AbstractGetUserInfoFromRemoteService):

    async def get_user_info(self, remote_token: RemoteToken) -> RemoteUserInfoResponse:
        access_token = remote_token.access_token
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://people.googleapis.com/v1/people/me",
                params={"personFields": "names,emailAddresses"},
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if response.status_code != 200:
                raise Exception(
                    "Error: Received an unexpected status from Google: %s"
                    % response.status_code
                )
            profile_info = response.json()
            email_data = profile_info["emailAddresses"][0]
            remote_user_id = email_data["metadata"]["source"]["id"]
            email_value = email_data["value"]
            full_name_data = profile_info["names"][0]
            full_name = full_name_data["displayName"]
            return RemoteUserInfoResponse(
                remote_user_id=remote_user_id, full_name=full_name, email=email_value
            )
