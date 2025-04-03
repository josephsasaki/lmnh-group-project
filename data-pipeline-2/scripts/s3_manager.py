'''
    DATA PIPELINE 2: s3_manager
    Deals with interacting with AWS S3 bucket
'''

import os
from datetime import datetime, timedelta
import boto3
from dotenv import load_dotenv


class S3Manager:
    '''Class that interacts with AWS S3 bucket'''

    CSV_PATH = os.path.join(os.path.dirname(
        __file__), '..', 'data', 'archived_data.csv')

    def __init__(self):
        load_dotenv()
        self.client_s3 = self._get_s3_client()
        self.key_s3 = self._create_bucket_key()

    def _get_s3_client(self):
        '''Initialise an S3 client with boto3.'''
        load_dotenv()
        client = boto3.client(
            "s3",
            aws_access_key_id=os.environ['ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['SECRET_ACCESS_KEY_ID'],
            region_name=os.environ['AWS_REGION'])
        return client

    def _create_bucket_key(self) -> str:
        """Returns the key of the object (csv) to be stored on S3."""
        # storing the previous days data so timedelta is -1 day
        yesterday_date = datetime.now()-timedelta(days=1)
        return f'{yesterday_date.year}/{yesterday_date.month}/{yesterday_date.day}/{yesterday_date.hour}.csv'

    def upload_csv_to_bucket(self):
        '''Upload the archived data, in the csv to the specified S3 bucket.'''
        with open(self.CSV_PATH, 'rb') as file:
            self.client_s3.put_object(
                Bucket=os.environ['S3_BUCKET'], Key=self.key_s3, Body=file)
