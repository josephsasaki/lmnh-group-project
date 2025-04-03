'''
    DATA PIPELINE 2: DataHelper
    This script defines a helper class which contains functions outside the scope of RDSManager and S3Manager. 
    On method deals with saving the 24 hour old data in a local csv. The second method returns the primary 
    keys (record_id) of the 24 old data.
'''

import pandas as pd


class DataHelper:
    '''Helper class to aid in handing of data'''
    DATA_FOLDER_PATH = '/tmp/' + 'archived_data.csv'

    def __init__(self, expired_data_df: pd.DataFrame):
        if not isinstance(expired_data_df, pd.DataFrame):
            raise TypeError('The input to this class is not a dataframe!')
        self.record_ids = tuple(expired_data_df['record_id'].to_list())
        self.data_to_save = expired_data_df.drop(columns=['record_id'], axis=1)

    def convert_dataframe_to_csv(self):
        '''Saves 24 hour old data into local CSV'''
        self.data_to_save.to_csv(self.DATA_FOLDER_PATH, index=False)

    def get_primary_keys(self):
        '''Returns the primary keys (record_id) of the records that will be deleted'''
        return self.record_ids
