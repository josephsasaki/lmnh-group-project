"""
This script takes in a list of responses in the form of dictionaries. It passes this to
the Plant object which cleans and instantiates a Plant and related objects. This object is then
stored in a list.
"""
from models import Plant


class Transform:
    """Transform class used to clean json data and instantiate objects"""
    @staticmethod
    def create_plant_objects(plant_responses: list[dict]) -> list[Plant]:
        """Creates a list of Plant objects, one object for each json response"""
        plant_list = []
        for response in plant_responses:
            plant_list.append(Plant(response))

        return plant_list
