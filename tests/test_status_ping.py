# from functools import partial

# import pytest
# from aiohttp import ClientResponse
# from api_test_utils import poll_until, env
# from api_test_utils.api_session_client import APISessionClient
# from api_test_utils.api_test_session_config import APITestSessionConfig


import json
import requests
from .configuration import config
from .conftest import make_headers


def test_ping(get_api_key):
    # need a poll until - something to keep doing it til a timeout, success or error.
    # also, is this the url I need to be pinging? I would suppose so, right?
    api_key = get_api_key["apikey"]
    resp = requests.get(
        url=f"{config.BASE_URL}/{config.BASE_PATH}/_ping",
        headers=make_headers(api_key),
    )
    assert resp.status_code == 200
    ping_data = json.loads(resp.text)
    assert "version" in ping_data


# async def _is_deployed(resp: ClientResponse, api_test_config: APITestSessionConfig) -> bool:
#     if resp.status != 200:
#         return False
#     body = await resp.json()

#     return body.get("commitId") == api_test_config.commit_id


# async def is_401(resp: ClientResponse) -> bool:
#     return resp.status == 401


# @pytest.mark.e2e
# @pytest.mark.smoketest
# def test_output_test_config(api_test_config: APITestSessionConfig):
#     print(api_test_config)


# # api_client not available as a fixture. Will have to port everything over somehow.
# # there's a function called "test_ping_endpoint" in pytest_nhsd_apim
# @pytest.mark.e2e
# @pytest.mark.smoketest
# @pytest.mark.asyncio
# async def test_wait_for_ping(api_client: APISessionClient, api_test_config: APITestSessionConfig):
#     """
#         test for _ping ..  this uses poll_until to wait until the correct SOURCE_COMMIT_ID ( from env var )
#         is available
#     """

#     is_deployed = partial(_is_deployed, api_test_config=api_test_config)

#     await poll_until(
#         make_request=lambda: api_client.get('_ping'),
#         until=is_deployed,
#         timeout=120
#     )


# @pytest.mark.e2e
# @pytest.mark.smoketest
# @pytest.mark.asyncio
# async def test_check_status_is_secured(api_client: APISessionClient):

#     await poll_until(
#         make_request=lambda: api_client.get('_status'),
#         until=is_401,
#         timeout=120
#     )


# @pytest.mark.e2e
# @pytest.mark.smoketest
# @pytest.mark.asyncio
# async def test_wait_for_status(api_client: APISessionClient, api_test_config: APITestSessionConfig):

#     """
#         test for _status ..  this uses poll_until to wait until the correct SOURCE_COMMIT_ID ( from env var )
#         is available
#     """

#     is_deployed = partial(_is_deployed, api_test_config=api_test_config)

#     await poll_until(
#         make_request=lambda: api_client.get('_status', headers={'apikey': env.status_endpoint_api_key()}),
#         until=is_deployed,
#         timeout=120
#     )
