import os
from datetime import datetime
import boto3
from dotenv import load_dotenv


class S3AthenaManager:
    def __init__(self):
        load_dotenv()
        self.client = self._get_s3_client()

    def _get_s3_client(self):
        '''Initialise an S3 client with boto3.'''
        client = boto3.client(
            "s3",
            aws_access_key_id=os.environ['ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['SECRET_ACCESS_KEY_ID'],
            region_name=os.environ['BUCKET_REGION'])
        return client

    def download_athena_data(self, athena_query_id: str) -> None:
        self.client.download_file(Bucket=os.environ['S3_ATHENA_BUCKET_NAME'],
                                  Key=f'{athena_query_id}'+'.csv',
                                  Filename='requested_data.csv')
