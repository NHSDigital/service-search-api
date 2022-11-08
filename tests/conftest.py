# flake8: noqa
import asyncio
import uuid

import pytest
from api_test_utils.api_test_session_config import APITestSessionConfig
from api_test_utils.apigee_api_apps import ApigeeApiDeveloperApps

from tests.configuration.config import ENVIRONMENT, PROXY_API_KEY


@pytest.fixture(scope='session')
def api_test_config() -> APITestSessionConfig:
    """
        this imports a 'standard' test session config,
        which builds the proxy uri

    """
    return APITestSessionConfig()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def default_apigee_app():
    apigee_app = ApigeeApiDeveloperApps()
    await apigee_app.create_new_app()

    yield apigee_app

    # Teardown
    print("\nDestroying Default App..")
    await apigee_app.destroy_app()


@pytest.fixture()
async def get_api_key(default_apigee_app):
    if "sandbox" in ENVIRONMENT:
        # Sandbox environments don't need authentication. Return fake one
        return {"apikey": "not_needed"}

    return {"apikey": default_apigee_app.client_id}


def make_headers(api_key):
    return {
        "apikey": api_key,
        "X-Request-Id": str(uuid.uuid4()),
        "X-Correlation-Id": str(uuid.uuid4())
    }
