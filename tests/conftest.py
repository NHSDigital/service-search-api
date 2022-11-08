# flake8: noqa
import uuid

import pytest
from api_test_utils.api_test_session_config import APITestSessionConfig
from api_test_utils.fixtures import api_client  # pylint: disable=unused-import

from tests.configuration.config import ENVIRONMENT, PROXY_API_KEY


@pytest.fixture(scope='session')
def api_test_config() -> APITestSessionConfig:
    """
        this imports a 'standard' test session config,
        which builds the proxy uri

    """
    return APITestSessionConfig()


@pytest.fixture()
def get_api_key():
    print(ENVIRONMENT)
    if "sandbox" in ENVIRONMENT:
        # Sandbox environments don't need authentication. Return fake one
        return {"apikey": "not_needed"}

    return {"apikey": PROXY_API_KEY}


def make_headers(api_key):
    return {
        "apikey": api_key,
        "X-Request-Id": str(uuid.uuid4()),
        "X-Correlation-Id": str(uuid.uuid4())
    }
