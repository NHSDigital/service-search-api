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


@pytest.mark.e2e
@pytest.mark.smoketest
def test_status_is_secured():
    resp = requests.get(
        url=f"{config.BASE_URL}/{config.BASE_PATH}/_status",
    )
    assert resp.status_code == 401


def test_for_status():
    resp = requests.get(
        url=f"{config.BASE_URL}/{config.BASE_PATH}/_status",
        headers=make_headers(API_KEY)
    )
    assert resp.status_code == 200
