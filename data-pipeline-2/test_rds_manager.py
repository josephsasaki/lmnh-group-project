from unittest.mock import patch
import pytest
import pandas as pd
from rds_manager import RDSManager


class TestRDSManager:
    @patch('rds_manager.RDSManager._initiate_connection')
    def test_connection_function_called(self, mock_conn_function):
        rds_manager = RDSManager()
        mock_conn_function.assert_called_once()

    @patch('pandas.read_sql')
    @patch('rds_manager.RDSManager._initiate_connection')
    def test_correct_read_sql_input(self, mock_conn_function, mock_read_sql):
        mock_conn_function.return_value = 'FAKE CONN'
        rds_manager = RDSManager()
        rds_manager.extract_data_to_be_archived()
        mock_read_sql.assert_called_with(rds_manager.QUERY, 'FAKE CONN')

    @pytest.mark.parametrize("test_in, expected",
                             [(1, "DELETE FROM record WHERE record_id IN (%s)"),
                              (2, "DELETE FROM record WHERE record_id IN (%s,%s)"),
                              (4, "DELETE FROM record WHERE record_id IN (%s,%s,%s,%s)")])
    @patch('rds_manager.RDSManager._initiate_connection')
    def test_correct_get_delete_query_outputs(self, mock_conn_function, test_in, expected):
        rds_manager = RDSManager()
        assert rds_manager._get_delete_query(test_in) == expected
