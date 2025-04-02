
from extract import PlantAPIExtractor
from transform import PlantFactory
from load import DatabaseManager
from models import Plant


def run_pipeline():
    extractor = PlantAPIExtractor(
        api_url='https://data-eng-plants-api.herokuapp.com/plants/',
        min_plant_id=1,
        max_plant_id=55,
    )
    responses = extractor.extract_api_data()
    plant_factory = PlantFactory(responses)
    plants = plant_factory.produce_plant_objects()
    db_manager = DatabaseManager(plants)
    db_manager.load_all()


if __name__ == "__main__":
    run_pipeline()
