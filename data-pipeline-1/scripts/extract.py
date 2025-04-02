import requests
import multiprocessing as mp
import time


class Extract:
    '''Static class containing methods related to extraction.'''

    API_ENDPOINT = "https://data-eng-plants-api.herokuapp.com/plants/"
    MIN_PLANT_ID = 1
    MAX_PLANT_ID = 55

    @staticmethod
    def _make_request(plant_id: int) -> dict:
        '''Given a plant_id, make a get request to the endpoint and return the result.'''
        request = requests.get(Extract.API_ENDPOINT+str(plant_id))
        if request.status_code == 200:
            return request.json()
        return None

    @staticmethod
    def extract():
        '''Extract the endpoint data for all ids in the specified range.'''
        plant_ids = list(range(Extract.MIN_PLANT_ID, Extract.MAX_PLANT_ID+1))
        print(mp.cpu_count())
        with mp.Pool(mp.cpu_count()) as p:
            fetched_data = p.map(Extract._make_request, plant_ids)
        return [json_obj for json_obj in fetched_data if json_obj is not None]
