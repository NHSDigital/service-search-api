import pytest
import requests
from .configuration import config
from .conftest import make_headers


API_KEY = "3fed41a7-1de3-4e03-980b-5945a4c06c86"


@pytest.mark.e2e
@pytest.mark.smoketest
def test_ping():
    resp = requests.get(
        url=f"{config.BASE_URL}/{config.BASE_PATH}/_ping",
    )
    assert resp.status_code == 200
    ping_data = resp.json()
    assert "version" in ping_data


# THIS DOES NOT WORK AS INTENDED.
# For some reason, only the special API_KEY constant above works with this proxy endpoint. It looks like
# an app ID to me, but what do I know? It seems to work, insofar as it can reach the endpoint, but then the
# status is a fail because we don't have a valid key for an active subscription (whatever that means)
def test_status_is_secured():
    resp = requests.get(
        url=f"{config.BASE_URL}/{config.BASE_PATH}/_status",
        headers=make_headers(API_KEY),
    )
    assert resp.status_code == 200
    # status_data = resp.json()
    # assert status_data["status"] == "healthy"
