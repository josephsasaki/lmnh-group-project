'''
    DATA PIPELINE 2: pipeline
    This script combines each part of the pipeline: extract, transform and load.
'''

from extract import Extract
from transform import Transform
from load import Load


if __name__ == "__main__":
    data_to_be_archived = Extract.extract_data_to_be_archived()
    record_ids_to_remove = Transform.get_primary_keys(data_to_be_archived)
    Transform.convert_dataframe_to_csv(data_to_be_archived)
    Load.upload_csv_to_bucket()
    Load.remove_rows_from_rds(record_ids_to_remove)
