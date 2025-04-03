import pytest
from unittest.mock import patch
from extract import RecordingAPIExtractor


@pytest.fixture
def api_extractor():
    return RecordingAPIExtractor(api_url="http://mock-api.com/")


def test_make_request_success(api_extractor):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "valid response"}

        response = api_extractor._make_request(1)
        assert response == {"data": "valid response"}


def test_make_request_failure(api_extractor):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404

        response = api_extractor._make_request(1)
        assert response is None
