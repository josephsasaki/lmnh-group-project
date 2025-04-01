'''
    DATA PIPELINE 2: transform
    Take the extracted rows (in the form of a pandas dataframe) and convert to a csv file, 
    stored locally in the data folder.
'''

import os
import pandas as pd
from pandas import DataFrame


class Transform:
    '''Static class for transforming data to a csv file.'''

    DATA_FOLDER_PATH = os.path.join(os.path.dirname(
        __file__), '..', 'data', 'archived_data.csv')

    @staticmethod
    def convert_dataframe_to_csv(data: DataFrame):
        '''Take a dataframe containing rows to be archived, and produce a csv file.'''
        data.to_csv(Transform.DATA_FOLDER_PATH, index=False)
