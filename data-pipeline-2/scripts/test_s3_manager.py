from datetime import datetime
from unittest.mock import patch
import pytest
import pandas as pd
from freezegun import freeze_time
from s3_manager import S3Manager


class TestS3Manager:

    @freeze_time("2025-04-02 17:47:46.000")
    @patch('s3_manager.S3Manager._get_s3_client')
    def test_s3_manager_init(self, mock_client):
        mock_client.return_value = 'FAKE CLIENT'
        s3_manager = S3Manager()
        # Assertions
        mock_client.assert_called_once()
        assert s3_manager.client_s3 == 'FAKE CLIENT'
        assert s3_manager.key_s3 == '2025/04/01/17.csv'

    @freeze_time("2025-03-02 20:47:46.000")
    @patch('s3_manager.S3Manager._get_s3_client')
    def test_get_bucket_key(self, mock_client):
        s3_manager = S3Manager()
        assert s3_manager.key_s3 == '2025/03/01/20.csv'
