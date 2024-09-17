# flake8: noqa
import asyncio
import os
import uuid
import pytest
from pytest_nhsd_apim.apigee_apis import ApigeeNonProdCredentials, ApigeeClient, DeveloperAppsAPI
from tests.configuration.config import ENVIRONMENT


@pytest.fixture(scope="session")
def client():
    # Can I check environment and use particular env variables depending on that?
    # How do I check the environment?
    config = ApigeeNonProdCredentials(
        apigee_nhsd_nonprod_password=os.environ["APIGEE_PASSWORD"],
        apigee_nhsd_nonprod_username=os.environ["APIGEE_USERNAME"],
        apigee_nhsd_nonprod_otp_key=os.environ["APIGEE_OTP_KEY"]
        ) # should use exported token
    client = ApigeeClient(config=config)
    return client


@pytest.fixture(scope="session")
def default_apigee_app(client):
    apigee_app = DeveloperAppsAPI(client=client)
    body = {
        "apiProducts": ["service-search-api-internal-dev"],
        "attributes": [],
        "callbackUrl": "example.com",
        "name": "myapp_test",
        "scopes": [],
        "status": "approved"
    }

    response = apigee_app.create_app(email="andrew.littlewood1@nhs.net", body=body)
    yield response

    print("\nDestroying Default app")
    apigee_app.delete_app_by_name(email="andrew.littlewood1@nhs.net", app_name="myapp_test")


@pytest.fixture(scope="session")
async def get_api_key(default_apigee_app):
    # print("response is:")
    # print(default_apigee_app_reponse)
    if "sandbox" in ENVIRONMENT:
        # Sandbox environments don't need authentication. Return fake one
        return {"apikey": "not_needed"}

    return {"apikey": default_apigee_app["credentials"][0]["consumerKey"]}


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def make_headers(api_key):
    return {
        "apikey": api_key,
        "X-Request-Id": str(uuid.uuid4()),
        "X-Correlation-Id": str(uuid.uuid4())
    }
