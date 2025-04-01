import requests
import multiprocessing as mp
import time


class Extract:
    '''Static class containing methods related to extraction.'''

    API_ENDPOINT = "https://data-eng-plants-api.herokuapp.com/plants/"
    MIN_PLANT_ID = 1
    MAX_PLANT_ID = 10

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
        with mp.Pool(mp.cpu_count()) as p:
            fetched_data = p.map(Extract._make_request, plant_ids)
        return [json_obj for json_obj in fetched_data if not None]

    @staticmethod
    def extract_slow():
        '''Extract the endpoint data for all ids in the specified range.'''
        plant_ids = list(range(Extract.MIN_PLANT_ID, Extract.MAX_PLANT_ID+1))
        fetched_data = []
        for plant_id in plant_ids:
            fetched_data.append(Extract._make_request(plant_id))
        return [json_obj for json_obj in fetched_data if not None]


if __name__ == "__main__":
    end = time.time()
    x = Extract.extract_slow()
    print(x)
