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
    def test_search_place(self, get_api_key):
        # Given
        expected_status_code = 200
        expected_body = load_example("search-place_v2.json")
        expected_place = expected_body["place"][0]["text"]

        api_key = get_api_key["apikey"]
        search = "manchester"
        body = {}

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{self.endpoint}",
            params={"api-version": "2", "apikey": api_key, "search": search},
            headers=make_headers(api_key),
            json=body,
        )

        jsonResponse = response.json()
        result = None
        for place in jsonResponse["place"]:
            if place["text"] == expected_place:
                result = place["text"]

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(result).is_equal_to(expected_place)

    @pytest.mark.sandbox
    @pytest.mark.integration
    def test_search_postcode(self, get_api_key):

        # We used ODS code since it will never change - for the given postcode, that ODS code should always appear in the results

        # Given
        expected_status_code = 200
        expected_body = load_example("search-postcode_v2.json")
        expected_ODS_code = expected_body["value"][1]["ODSCode"]

        api_key = get_api_key["apikey"]
        search = "WC1N 3JH"
        body = {}

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{self.endpoint}",
            params={"api-version": "2", "apikey": api_key, "search": search},
            headers=make_headers(api_key),
            json=body,
        )

        jsonResponse = response.json()
        result = None
        for place in jsonResponse["value"]:
            if place["ODSCode"] == expected_ODS_code:
                result = place["ODSCode"]

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(result).is_equal_to(expected_ODS_code)

    @pytest.mark.skip(
        reason="returns list of places, each request gives back different size responses"
    )
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
            json=body,
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
            json=body,
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
            params={
                "search": search,
                "api-version": invalid_api_version,
                "apikey": api_key,
            },
            headers=make_headers(api_key),
            json=body,
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    @pytest.mark.skip
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

        results = response.json()["place"]
        for item in results:
            url_response = requests.get(
                url=item["url"],
                params={"apikey": api_key},
                headers=make_headers(api_key),
            )
            assert_that(url_response.status_code).is_equal_to(expected_status_code)
