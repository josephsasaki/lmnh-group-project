import pytest
import pandas as pd
from scripts.transform import Transform


class TestTransform:

    def test_correct_df_input(self):
        df_test = pd.DataFrame({
            'record_id': [1, 2, 3, 4, 12, 15],
            'plant_type_name': ['a', 'an', 'ant', 'anta', 'antar', 'antari']
        })
        record_id_list = Transform.get_primary_keys(df_test)
        assert len(record_id_list) == 6
        assert record_id_list == [1, 2, 3, 4, 12, 15]
        assert isinstance(record_id_list, list) == True

    def test_no_record_id(self):
        df_test = pd.DataFrame({
            'plant_type_name': ['a', 'an', 'ant', 'anta', 'antar', 'antari']
        })
        with pytest.raises(KeyError):
            record_id_list = Transform.get_primary_keys(df_test)
