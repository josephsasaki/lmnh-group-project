'''
    DATA PIPELINE 2: pipeline
    This script combines each part of the pipeline: extract, transform and load.
'''

from extract import ExpiredDataFinder
from transform import ExpiredDataHelper
from load import DataArchiverAndDeleter


if __name__ == "__main__":
    # Get data to archive
    data_finder = ExpiredDataFinder()
    df_to_archive = data_finder.extract_data_to_be_archived()
    # Initiate archive data helper
    data_helper = ExpiredDataHelper(df_to_archive)
    data_helper.convert_dataframe_to_csv()
    # Delete from RDS and save csv
    archiver_deleter = DataArchiverAndDeleter()
    archiver_deleter.upload_csv_to_bucket()
    archiver_deleter(data_finder.get_connection(),
                     data_helper.get_primary_keys())
