'''
    DATA PIPELINE 2: load
    Load the csv file in the data folder to the S3 bucket. The key for the csv file determines the date and time
    of archival.
'''

import os
from datetime import datetime
import boto3
from dotenv import load_dotenv
from extract import Extract


class Load:
    '''Static class for loading data from the csv file to the S3 bucket.'''

    CSV_PATH = os.path.join(os.path.dirname(
        __file__), '..', 'data', 'archived_data.csv')
    DELETE_QUERY = "DELETE FROM record WHERE id IN (%s)"

    @staticmethod
    def _get_s3_client():
        '''Initialise an S3 client with boto.'''
        load_dotenv()
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.environ['ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['SECRET_ACCESS_KEY_ID'],
            region_name=os.environ['AWS_REGION'],
        )

    @staticmethod
    def upload_csv_to_bucket():
        '''Upload the archived data, in the csv to the specified S3 bucket.'''
        s3 = Load._get_s3_client()
        current_date = datetime.now()
        key = f'{current_date.year}/{current_date.month}/{current_date.day}/{current_date.hour}.csv'
        s3.upload_file(Load.CSV_PATH, os.environ['S3_BUCKET'], key)

    @staticmethod
    def remove_rows_from_rds(record_ids: list[int]):
        with Extract.get_connection() as connection:
            with connection.cursor() as cursor:
                format_strings = ",".join(["%s"] * len(record_ids))
                delete_query = Load.DELETE_QUERY.format(format_strings)
                cursor.execute(delete_query, record_ids)
                connection.commit()
