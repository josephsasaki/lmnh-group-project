from datetime import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo
import pytest
import pandas as pd
from freezegun import freeze_time
from s3_manager import S3Manager


class TestS3Manager:
    # "2025-04-02 17:47:46.000",

    @freeze_time(datetime(year=2025, month=4, day=2, hour=17, minute=47, second=46).astimezone(ZoneInfo("Europe/London")))
    @patch('s3_manager.S3Manager._get_s3_client')
    def test_s3_manager_init(self, mock_client):
        mock_client.return_value = 'FAKE CLIENT'
        s3_manager = S3Manager()
        # Assertions
        mock_client.assert_called_once()
        assert s3_manager.client_s3 == 'FAKE CLIENT'
        assert s3_manager.key_s3 == '2025/04/01/17.csv'

    @freeze_time(datetime(year=2025, month=3, day=2, hour=20, minute=47, second=46).astimezone(ZoneInfo("Europe/London")))
    @patch('s3_manager.S3Manager._get_s3_client')
    def test_get_bucket_key(self, mock_client):
        s3_manager = S3Manager()
        assert s3_manager.key_s3 == '2025/03/01/20.csv'
