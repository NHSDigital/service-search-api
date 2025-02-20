import pytest
import requests
from .configuration import config


@pytest.mark.integration
@pytest.mark.e2e
@pytest.mark.smoketest
def test_ping():
    resp = requests.get(
        url=f"{config.BASE_URL}/{config.BASE_PATH}/_ping",
    )
    assert resp.status_code == 200
    ping_data = resp.json()
    assert "version" in ping_data


@pytest.mark.integration
@pytest.mark.e2e
@pytest.mark.smoketest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
def test_status_is_secured():
    resp = requests.get(
        url=f"{config.BASE_URL}/{config.BASE_PATH}/_status",
    )
    print(resp.status_code)
    assert resp.status_code == 401


@pytest.mark.integration
@pytest.mark.e2e
@pytest.mark.smoketest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
def test_for_status(status_endpoint_auth_headers):
    resp = requests.get(
        url=f"{config.BASE_URL}/{config.BASE_PATH}/_status",
        headers=status_endpoint_auth_headers
    )

    status_data = resp.json()
    apim_responde_code = status_data["checks"]["healthcheck"]["responseCode"]
    apigee_status_code = resp.status_code
    
    assert apigee_status_code == 200
    assert apim_responde_code == 200
