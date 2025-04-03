'''
    DATA PIPELINE 2: DataHelper
    A helper class which would not fit into rds_manager or s3_manager. On method deals with saving the 24 hour
    old data in a local csv. The second method returns the primary keys (record_id) of the 24 old data
'''

import os
import pandas as pd


class DataHelper:
    '''Helper class to aid in handing of data'''

    DATA_FOLDER_PATH = os.path.join(os.path.dirname(
        __file__), '..', 'data', 'archived_data.csv')

    def __init__(self, expired_data_df: pd.DataFrame):
        self.record_ids = tuple(expired_data_df['record_id'].to_list())
        self.data_to_save = expired_data_df.drop(columns=['record_id'], axis=1)

    def convert_dataframe_to_csv(self):
        '''Saves 24 hour old data into local CSV'''
        self.data_to_save.to_csv(self.DATA_FOLDER_PATH, index=False)

    def get_primary_keys(self):
        '''returns the primary keys (record_id) of the records that will be deleted'''
        return self.record_ids
