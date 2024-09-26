import pytest
import requests
from assertpy import assert_that
from .configuration import config
# from .conftest import make_headers


@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
def test_organisation_found(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    expected_status_code = 200
    search = "ODSCode eq 'FV095'"
    response = requests.get(
        url=f"{config.BASE_URL}/{config.BASE_PATH}",
        params={"api-version": "3", "$filter": search},
        headers=nhsd_apim_auth_headers,
    )

    assert_that(response.status_code).is_equal_to(expected_status_code)


# @pytest.mark.e2e
# @pytest.mark.smoketest
# def test_ping():
#     resp = requests.get(
#         url=f"{config.BASE_URL}/{config.BASE_PATH}/_ping",
#     )
#     assert resp.status_code == 200
#     ping_data = resp.json()
#     assert "version" in ping_data


# @pytest.mark.e2e
# @pytest.mark.smoketest
# def test_status_is_secured():
#     resp = requests.get(
#         url=f"{config.BASE_URL}/{config.BASE_PATH}/_status",
#     )
#     assert resp.status_code == 401


# def test_for_status():
#     resp = requests.get(
#         url=f"{config.BASE_URL}/{config.BASE_PATH}/_status",
#         headers=make_headers(config.STATUS_ENDPOINT_API_KEY)
#     )
#     assert resp.status_code == 200
