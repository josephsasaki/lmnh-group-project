import pytest
import pandas as pd
from data_helper import DataHelper


class TestDataHelper:

    @pytest.fixture
    def df_test(self):
        return pd.DataFrame({
            'record_id': [1, 2, 3, 4, 12, 15],
            'plant_type_name': ['a', 'an', 'ant', 'anta', 'antar', 'antari']
        })

    def test_valid_init(self, df_test):
        data_helper = DataHelper(df_test)
        assert data_helper.record_ids == (1, 2, 3, 4, 12, 15)
        assert pd.DataFrame(
            {'plant_type_name': ['a', 'an', 'ant', 'anta', 'antar', 'antari']}).equals(data_helper.data_to_save)

    def test_invalid_init_type(self):
        with pytest.raises(TypeError):
            data_helper = DataHelper(0)

    def test_primary_keys(self, df_test):
        data_helper = DataHelper(df_test)
        assert data_helper.get_primary_keys() == (1, 2, 3, 4, 12, 15)
