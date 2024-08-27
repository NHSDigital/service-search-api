import requests
from assertpy import assert_that

from .configuration import config
from .conftest import make_headers
from .example_loader import load_example


class TestSearchOrganisations:
    # @pytest.mark.skip(reason="Not needed at the moment")
    def test_single_organisation(self, get_api_key):
        # Given
        expected_status_code = 200
        api_key = get_api_key["apikey"]
        search = "Y02494"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "3", "search": search},
            headers=make_headers(api_key),
        )

        data = response.json()

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(len(data["value"])).is_equal_to(1)

    # @pytest.mark.skip(reason="Not needed at the moment")
    def test_organisation_not_found(self, get_api_key):
        # Given
        expected_status_code = 200
        expected_body = load_example("organisations-not-found_v3.json")

        api_key = get_api_key["apikey"]
        search = "invalid"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "3", "search": search},
            headers=make_headers(api_key),
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    # @pytest.mark.skip(reason="Not needed at the moment")
    def test_search_organisations(self, get_api_key):
        # Given
        expected_status_code = 200
        max_organisations_returned = 50

        api_key = get_api_key["apikey"]

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "3"},
            headers=make_headers(api_key),
        )
        data = response.json()

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(len(data["value"])).is_equal_to(max_organisations_returned)

    # @pytest.mark.skip(reason="Not needed at the moment")
    def test_not_found_api_version(self, get_api_key):
        # Given
        expected_status_code = 404
        expected_body = load_example("bad-api-version-resource-not-found.json")

        api_key = get_api_key["apikey"]
        search = "Y02494"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"search": search, "apikey": api_key},
            headers=make_headers(api_key),
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    # @pytest.mark.skip(reason="Not needed at the moment")
    def test_invalid_api_version(self, get_api_key):
        # Given
        expected_status_code = 404
        expected_body = load_example("bad-api-version-resource-not-found.json")

        api_key = get_api_key["apikey"]
        search = "Y02494"
        invalid_api_version = 5

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"search": search, "api-version": invalid_api_version, "apikey": api_key},
            headers=make_headers(api_key),
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_body)

    # @pytest.mark.skip(reason="Not needed at the moment")
    def test_organisation_found(self, get_api_key):
        # Given
        expected_status_code = 200
        api_key = get_api_key["apikey"]
        ods_code = "'FNC84'"
        search = f"ODSCode eq {ods_code}"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "3", "$filter": search},
            headers=make_headers(api_key),
        )
        data = response.json()

        is_code_found = False
        for item in data["value"]:
            if (item['ODSCode'] == ods_code.replace("'", "")):
                is_code_found = True

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(is_code_found).is_true()

    # @pytest.mark.skip(reason="Not needed at the moment")
    def test_organisation_found_smoke(self, get_api_key):
        # Given
        expected_status_code = 200

        api_key = get_api_key["apikey"]
        search = "ODSCode eq 'FV095'"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}",
            params={"api-version": "3", "$filter": search},
            headers=make_headers(api_key),
        )

        # Then
        assert_that(response.status_code).is_equal_to(expected_status_code)
