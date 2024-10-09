import pytest
import requests
from assertpy import assert_that
from .example_loader import load_example
from .configuration import config


class TestSearchOrganisations:
    @pytest.mark.integration
    @pytest.mark.smoketest
    @pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
    def test_organisation_found(self, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 200
        search = "ODSCode eq 'FV095'"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "3", "$filter": search},
            headers=nhsd_apim_auth_headers,
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)

    @pytest.mark.integration
    @pytest.mark.smoketest
    @pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
    def test_single_organisation(self, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 200
        search = "Y02494"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "3", "search": search},
            headers=nhsd_apim_auth_headers
        )

        data = response.json()

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(len(data["value"])).is_equal_to(1)

    @pytest.mark.integration
    @pytest.mark.smoketest
    @pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
    def test_organisation_not_found(self, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 200
        expected_body = load_example("organisations-not-found_v3.json")
        search = "invalid"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "3", "search": search},
            headers=nhsd_apim_auth_headers
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.integration
    @pytest.mark.smoketest
    @pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
    def test_search_organisations_get(self, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 200
        max_organisations_returned = 50

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "3"},
            headers=nhsd_apim_auth_headers
        )
        data = response.json()

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(len(data["value"])).is_equal_to(max_organisations_returned)

    @pytest.mark.integration
    @pytest.mark.smoketest
    @pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
    def test_search_organisations_post(self, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 200
        max_organisations_returned = 50

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "3"},
            json={"search": "*"},
            headers=nhsd_apim_auth_headers
        )
        data = response.json()

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(len(data["value"])).is_equal_to(max_organisations_returned)

    @pytest.mark.integration
    @pytest.mark.smoketest
    @pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
    def test_not_found_api_version(self, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 404
        expected_body = load_example("bad-api-version-resource-not-found.json")
        search = "Y02494"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"search": search},
            headers=nhsd_apim_auth_headers
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.integration
    @pytest.mark.smoketest
    @pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
    def test_invalid_api_version(self, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 404
        expected_body = load_example("bad-api-version-resource-not-found.json")
        search = "Y02494"
        invalid_api_version = 5

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"search": search, "api-version": invalid_api_version},
            headers=nhsd_apim_auth_headers,
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.integration
    @pytest.mark.smoketest
    @pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
    def test_organisation_found_smoke_get(self, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 200
        search = "ODSCode eq 'FV095'"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "3", "$filter": search},
            headers=nhsd_apim_auth_headers
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)

    @pytest.mark.integration
    @pytest.mark.smoketest
    @pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level0"})
    def test_organisation_found_smoke_post(self, nhsd_apim_auth_headers):
        # Given
        expected_status_code = 200

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "3"},
            json={"search": "FV095"},
            headers=nhsd_apim_auth_headers
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
