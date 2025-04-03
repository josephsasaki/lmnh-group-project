'''
    The transformation part of the first data pipeline. The aim of this script is to 
    transform the raw plant data into objects, with cleaned and connected attributes.
'''

from models import Plant


class PlantRecordingFactory:
    '''Class which takes a list of json objects containing plant data and transforms them into
    a list of actual plant objects.'''

    def __init__(self, responses: list[dict]):
        '''Initialise with the list of responses'''
        self.responses = responses

    def produce_plant_objects(self) -> list[Plant]:
        '''Creates a list of Plant objects, one object for each json response. If an error is raised
        in the process of making the plant object, the response is deemed invalid and skipped.'''
        plants = []
        for response in self.responses:
            try:
                plants.append(Plant(response))
            except ValueError:
                continue
        return plants
