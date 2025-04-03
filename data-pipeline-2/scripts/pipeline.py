'''
    DATA PIPELINE 2: pipeline
    This script calls the classes in rds_manager, data_helper and s3_manager to archive
    data in s3 and delete the archived data from the RDS
'''

from rds_manager import RDSManager
from data_helper import DataHelper
from s3_manager import S3Manager


def run_archive_pipeline():
    # Get data to archive
    rds_manager = RDSManager()
    df_to_archive = rds_manager.extract_data_to_be_archived()
    # Initiate archive data helper
    data_helper = DataHelper(df_to_archive)
    # Save to csv
    data_helper.convert_dataframe_to_csv()
    # Instantiate S3Manager and upload to bucket
    s3_manager = S3Manager()
    s3_manager.upload_csv_to_bucket()
    # Delete from RDS
    rds_manager.remove_rows_from_rds(data_helper.get_primary_keys())
    # Close connection
    rds_manager.close_connection()
