'''
    DATA PIPELINE 2: load
    Load the csv file in the data folder to the S3 bucket. The key for the csv file determines the date and time
    of archival.
'''

import os
from datetime import datetime, timedelta
import boto3
import pyodbc
from dotenv import load_dotenv
from extract import ExpiredDataFinder
from transform import ExpiredDataHelper


class DataArchiverAndDeleter:
    '''Static class for loading data from the csv file to the S3 bucket.'''

    CSV_PATH = os.path.join(os.path.dirname(
        __file__), '..', 'data', 'archived_data.csv')
    BASE_DELETE_QUERY = "DELETE FROM record WHERE record_id IN ({wildcards})"

    def __init__(self):
        load_dotenv()
        self.client_s3 = self._get_s3_client()
        self.key_s3 = self.get_bucket_key()

    def _get_s3_client(self):
        '''Initialise an S3 client with boto.'''
        load_dotenv()
        client = boto3.client(
            "s3",
            aws_access_key_id=os.environ['ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['SECRET_ACCESS_KEY_ID'],
            region_name=os.environ['AWS_REGION'])
        return client

    def get_delete_query(self, number_of_ids):
        return self.BASE_DELETE_QUERY.format(wildcards=','.join(['?']*number_of_ids))

    def get_bucket_key(self) -> str:
        # storing the previous days data so timedelta is -1 day
        yesterday_date = datetime.now()-timedelta(days=1)
        return f'{yesterday_date.year}/{yesterday_date.month}/{yesterday_date.day}/{yesterday_date.hour}.csv'

    def upload_csv_to_bucket(self):
        '''Upload the archived data, in the csv to the specified S3 bucket.'''
        with open(self.CSV_PATH, 'rb') as file:
            self.client_s3.put_object(
                Bucket=os.environ['S3_BUCKET'], Key=self.key_s3, Body=file)

    def remove_rows_from_rds(self, conn: pyodbc.Connection, record_ids: tuple[int]):
        with conn.cursor() as cursor:
            delete_query = self.get_delete_query(len(record_ids))
            cursor.execute(delete_query, record_ids)
            conn.commit()
