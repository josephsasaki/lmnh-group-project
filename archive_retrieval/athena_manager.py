import os
from datetime import datetime
import time
import boto3
from dotenv import load_dotenv


class AthenaManager:
    """Interacts with AWS Athena"""
    BASE_QUERY = """
    SELECT * FROM c16_trenet_athena_table
    WHERE 
    record_timestamp > TIMESTAMP '{start_filter}' 
    AND 
    record_timestamp < TIMESTAMP '{end_filter}'; 
    """
    SLEEP_SECONDS = 3

    def __init__(self):
        self.client = self._get_client()

    def _get_client(self):
        load_dotenv()
        return boto3.client('athena',
                            region_name=os.environ['BUCKET_REGION'])

    def _convert_datetime_to_string(self, timestamp_in: datetime) -> str:
        return timestamp_in.strftime('%Y-%m-%d %H:%M:%S')

    def query_athena(self, start_timestamp: datetime, end_timestamp: datetime) -> None:
        load_dotenv()
        query_string_athena = self.BASE_QUERY.format(
            start_filter=self._convert_datetime_to_string(start_timestamp),
            end_filter=self._convert_datetime_to_string(end_timestamp)
        )
        response = self.client.start_query_execution(
            QueryString=query_string_athena,
            QueryExecutionContext={'Database': os.environ['DB_NAME_ATHENA']},
            ResultConfiguration={
                'OutputLocation': os.environ['S3_BUCKET_OUTPUT_LOCATION']}
        )
        # Save query id so
        self.query_id = response['QueryExecutionId']
        time.sleep(self.SLEEP_SECONDS)

    def get_query_id(self):
        return self.query_id
