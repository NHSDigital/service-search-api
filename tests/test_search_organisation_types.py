import pytest
import requests
from assertpy import assert_that

from .configuration import config
from .conftest import make_headers
from .example_loader import load_example


class TestSearchPostcode:
    endpoint = "organisationtypes"
    api_version = "1"

    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_search_organisation_types(self, get_api_key):
        # Given
        expected_status_code = 200
        expected_body = load_example("organisation-types_v1.json")

        api_key = get_api_key["apikey"]

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{self.endpoint}",
            params={"api-version": self.api_version, "apikey": api_key},
            headers=make_headers(api_key),
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_search_single_organisation_type(self, get_api_key):
        # Given
        expected_status_code = 200
        expected_body = load_example("organisation-types-single-item_v1.json")

        api_key = get_api_key["apikey"]
        search = "pharmacy"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{self.endpoint}",
            params={"api-version": self.api_version, "apikey": api_key, "search": search},
            headers=make_headers(api_key),
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_organisation_type_not_found(self, get_api_key):
        # Given
        expected_status_code = 200
        expected_body = load_example("organisation-types-not-found_v1.json")

        api_key = get_api_key["apikey"]
        search = "an_org_type"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{self.endpoint}",
            params={"api-version": self.api_version, "apikey": api_key, "search": search},
            headers=make_headers(api_key),
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_invalid_api_version(self, get_api_key):
        # Given
        expected_status_code = 404
        expected_body = load_example("bad-api-version-resource-not-found.json")

        api_key = get_api_key["apikey"]
        bad_api_version = "2"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{self.endpoint}",
            params={"api-version": bad_api_version, "apikey": api_key},
            headers=make_headers(api_key),
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)
