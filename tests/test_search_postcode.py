import pytest
import requests
from assertpy import assert_that

from .configuration import config
from .conftest import make_headers
from .example_loader import load_example


class TestSearchPostcode:
    endpoint = "search-postcode-or-place"

    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_search_postcode(self, get_api_key):
        # Given
        expected_status_code = 200
        expected_body = load_example("search-postcode_v2.json")

        api_key = get_api_key["apikey"]
        search = "manchester"
        body = {}

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{self.endpoint}",
            params={"api-version": "2", "apikey": api_key, "search": search},
            headers=make_headers(api_key),
            json=body
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.skip(reason="returns list of places, each request gives back different size responses")
    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_place_not_found(self, get_api_key):
        # Given
        expected_status_code = 500
        expected_body = load_example("search-postcode-invalid_v2.json")

        api_key = get_api_key["apikey"]
        search = "El Dorado".lower()
        body = {}

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{self.endpoint}",
            params={"api-version": "2", "apikey": api_key, "search": search},
            headers=make_headers(api_key),
            json=body
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_not_found_api_version(self, get_api_key):
        # Given
        expected_status_code = 404
        expected_body = load_example("bad-api-version-resource-not-found.json")

        api_key = get_api_key["apikey"]
        search = "manchester"
        body = {}

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{self.endpoint}",
            params={"search": search, "apikey": api_key},
            headers=make_headers(api_key),
            json=body
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
        search = "manchester"
        invalid_api_version = 5
        body = {}

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{self.endpoint}",
            params={"search": search, "api-version": invalid_api_version, "apikey": api_key},
            headers=make_headers(api_key),
            json=body
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.integration
    def test_response_payload_urls_are_corrected(self, get_api_key):
        """
        Test that the urls returned in the response payload have been routed to the
        correct hostname for the environment used, and can be followed.
        """
        # Given
        expected_status_code = 200

        api_key = get_api_key["apikey"]
        search = "manchester"

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{self.endpoint}",
            params={"api-version": "2", "apikey": api_key, "search": search},
            headers=make_headers(api_key),
            json={},
        )

        import pdb; pdb.set_trace()

        results = response.json()['place']
        for item in results:
            url_response = requests.post(
                url=item['url'],
                headers=make_headers(api_key),
                json={},
            )
            assert_that(url_response.status_code).is_equal_to(expected_status_code)
