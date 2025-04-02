from unittest.mock import patch
import pytest
import pandas as pd
from extract import Extract


class TestExtract():

    @patch('extract.Extract._get_connection')
    @patch('pandas.read_sql')
    def test_functions_called_once(self, read_sql_mock, conn_mock):
        read_sql_return = pd.DataFrame({
            'id': [1, 2],
            'test': [1, 2]})
        read_sql_mock.return_value = read_sql_return
        response = Extract.extract_data_to_be_archived()
        # Assertions
        conn_mock.assert_called_once()
        read_sql_mock.assert_called_once()
        assert isinstance(response, pd.DataFrame) == True
        assert response.equals(read_sql_return) == True

    @patch('pyodbc.connect')
    def test_only_one_connection(self, pyodbc_conn_mock):
        pyodbc_conn_mock.return_value = 'This is a fake connection'
        conn = Extract._get_connection()
        pyodbc_conn_mock.assert_called_once()
        assert conn == 'This is a fake connection'
