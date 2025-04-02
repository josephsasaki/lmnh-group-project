
from extract import Extract
from transform import Transform
from load import Load
from models import Plant

import time


class Pipeline():

    @staticmethod
    def _extract() -> list[dict]:
        return Extract.extract_api_data()

    @staticmethod
    def _transform(api_data: list[dict]) -> list['Plant']:
        return Transform.create_plant_objects(api_data)

    @staticmethod
    def _load(plants: list['Plant']) -> None:
        with Load.get_connection() as connection:
            with connection.cursor() as cursor:
                # botanists
                botanists = [plant.get_botanist() for plant in plants]
                Load.add_new_botanists(botanists, cursor)
                print("   -> Botanists")
                # locations
                locations = [plant.get_location() for plant in plants]
                Load.add_new_continents(locations, cursor)
                Load.add_new_countries(locations, cursor)
                Load.add_new_cities(locations, cursor)
                print("   -> Locations")
                # plant types
                plant_types = [plant.get_plant_type() for plant in plants]
                Load.add_new_plant_type(plant_types, cursor)
                print("   -> Plant types")
                # Add any new plants
                Load.add_new_plants(plants, cursor)
                print("   -> Plants")
                # Add new records
                Load.add_new_records(plants, cursor)
                print("   -> Records")
                cursor.commit()

    @staticmethod
    def run():
        api_data = Pipeline._extract()
        print("Extracted")
        plants = Pipeline._transform(api_data)
        print("Transformed")
        Pipeline._load(plants)
        print("Loaded")


if __name__ == "__main__":
    Pipeline.run()
