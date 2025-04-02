import pytest
import unittest
from unittest.mock import patch, MagicMock
import scripts.extract as extract
from scripts.extract import Extract


class TestExtract(unittest.TestCase):

    # Ensure patching where requests.get is called
    @patch("scripts.extract.requests.get")
    def test_make_request_success(self, mock_get):
        # Create a mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = "Success"
        mock_get.return_value = mock_response

        # Call the function
        result = Extract._make_request(1)

        # Assertions
        self.assertEqual(result, "Success")
        mock_get.assert_called_once_with(Extract.API_ENDPOINT + "1")

    # Patch requests.get in correct module
    @patch("scripts.extract.requests.get")
    def test_make_request_failure(self, mock_get):
        # Simulate a 404 failure response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Call the function
        result = Extract._make_request(1)

        # Assertions
        self.assertIsNone(result)
        mock_get.assert_called_once_with(Extract.API_ENDPOINT + "1")
