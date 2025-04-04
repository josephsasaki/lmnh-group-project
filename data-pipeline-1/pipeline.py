'''
    The main access point for running the data pipeline. The event handler for running in an 
    AWS Lambda is also defined here.
'''

from extract import RecordingAPIExtractor
from transform import PlantRecordingFactory
from load import DatabaseManager


def run_api_pipeline():
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
