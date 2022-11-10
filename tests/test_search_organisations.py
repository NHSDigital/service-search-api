import pytest
import requests
from assertpy import assert_that

from .configuration import config
from .conftest import make_headers
from .example_loader import load_example


class TestSearchOrganisations:
    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_single_organisation(self, get_api_key):
        # Given
        expected_status_code = 200
        expected_body = load_example("organisations-single_v2.json")

        api_key = get_api_key["apikey"]
        search = "DN601"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "2", "search": search},
            headers=make_headers(api_key),
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_organisation_not_found(self, get_api_key):
        # Given
        expected_status_code = 200
        expected_body = load_example("organisations-not-found_v2.json")

        api_key = get_api_key["apikey"]
        search = "a-search-query"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "2", "search": search},
            headers=make_headers(api_key),
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_search_organisations(self, get_api_key):
        # Given
        expected_status_code = 200
        expected_body = load_example("organisations_v2.json")

        api_key = get_api_key["apikey"]

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "2"},
            headers=make_headers(api_key),
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_not_found(self, get_api_key):
        # Given
        expected_status_code = 404
        expected_body = load_example("bad-api-version-resource-not-found.json")

        api_key = get_api_key["apikey"]
        bad_api_version = "1"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": bad_api_version, "apikey": api_key},
            headers=make_headers(api_key),
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)
