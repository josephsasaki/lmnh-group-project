'''
    DATA PIPELINE 2: transform
    Take the extracted rows (in the form of a pandas dataframe) and convert to a csv file, 
    stored locally in the data folder.
'''

import os
import pandas as pd


class ExpiredDataHelper:
    '''Class that helps Extract and Load, by saving data and finding IDs to remove Data'''

    DATA_FOLDER_PATH = os.path.join(os.path.dirname(
        __file__), '..', 'data', 'archived_data.csv')

    def __init__(self, expired_data_df: pd.DataFrame):
        self.record_ids = tuple(expired_data_df['record_id'].to_list())
        self.data_to_save = expired_data_df.drop(columns=['record_id'], axis=1)

    def convert_dataframe_to_csv(self):
        '''Saves the data in data_to_save attribute'''
        self.data_to_save.to_csv(self.DATA_FOLDER_PATH, index=False)

    def get_primary_keys(self):
        '''Extract the primary keys (record_id) from the data. 
        This will be used to remove the rows from the RDS'''
        return self.record_ids
