'''
    The main access point for running the data pipeline. The event handler for running in an 
    AWS Lambda is also defined here.
'''

import logging
from extract import RecordingAPIExtractor
from transform import PlantRecordingFactory
from load import DatabaseManager


def run_pipeline():
    '''This function runs the entire data pipeline for moving data from an API
    to an RDS.'''
    extractor = RecordingAPIExtractor(
        api_url='https://data-eng-plants-api.herokuapp.com/plants/',
        min_plant_id=1,
        max_plant_id=55,
    )
    responses = extractor.extract_api_data()
    factory = PlantRecordingFactory(responses)
    plants = factory.produce_plant_objects()
    db_manager = DatabaseManager(plants)
    db_manager.load_all()


def lambda_handler(event: None, context: None):
    '''This function is called by the AWS Lambda to run the Python scripts.'''
    logger = logging.getLogger()
    logger.setLevel("INFO")
    try:
        logger.info(f"Running...")
        run_pipeline()
        logger.info(f"Successful")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise


if __name__ == "__main__":
    run_pipeline()
