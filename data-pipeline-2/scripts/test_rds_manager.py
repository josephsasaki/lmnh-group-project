from unittest.mock import patch
import pytest
import pandas as pd
from rds_manager import RDSManager


class TestRDSManager:
    @patch('rds_manager.RDSManager._initiate_connection')
    def test_connection_function_called_on_instantiation(self, mock_conn_function):
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
                             [(1, "DELETE FROM record WHERE record_id IN (?)"),
                              (2, "DELETE FROM record WHERE record_id IN (?,?)"),
                              (4, "DELETE FROM record WHERE record_id IN (?,?,?,?)")])
    @patch('rds_manager.RDSManager._initiate_connection')
    def test_correct_get_delete_query_inputs(self, mock_conn_function, test_in, expected):
        rds_manager = RDSManager()
        assert rds_manager.get_delete_query(test_in) == expected

    @patch('rds_manager.RDSManager._initiate_connection')
    def test_get_delete_query_input_0(self, mock_conn_function, capsys):
        rds_manager = RDSManager()
        with pytest.raises(SystemExit):
            query_test = rds_manager.get_delete_query(0)
            captured = capsys.readouterr()
            assert 'No 24 hour old data...\nQuitting' == captured.out

    @pytest.mark.parametrize("test_in",
                             [(-1),
                              (-2),
                              (-4)])
    @patch('rds_manager.RDSManager._initiate_connection')
    def test_get_delete_query_input_negative(self, mock_conn_function, test_in, capsys):
        rds_manager = RDSManager()
        with pytest.raises(ValueError):
            query_test = rds_manager.get_delete_query(test_in)
            captured = capsys.readouterr()
            assert f'The number of ids cant be {test_in} as this is negative' == captured.out
