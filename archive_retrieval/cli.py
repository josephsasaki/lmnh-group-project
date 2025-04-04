import argparse
from datetime import datetime
from athena_manager import AthenaManager
from s3_athena_manager import S3AthenaManager


def parse_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-st', '--start_timestamp',
                        description="start timestamp for filtering format: '%Y-%m-%d %H:%M:%S'")
    parser.add_argument('-et', '--end_timestamp',
                        description="end timestamp for filtering format: '%Y-%m-%d %H:%M:%S'")
    args = parser.parse_args()
    return args.start_timestamp, args.end_timestamp


def convert_to_datetime(timestamp_in: str):
    return datetime.strptime(timestamp_in, '%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    # Parse and format inputs
    start_timestamp, end_timestamp = parse_inputs()
    start_timestamp = convert_to_datetime(start_timestamp)
    end_timestamp = convert_to_datetime(end_timestamp)
    # Instantiate AthenaManager and query Athena
    athena = AthenaManager()
    athena.query_athena(start_timestamp, end_timestamp)
    # Download CSV from the S3
    s3 = S3AthenaManager()
    s3.download_athena_data(athena.get_query_id())
