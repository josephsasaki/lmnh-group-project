'''
    The extraction part of the first data pipeline. The source of data is an API, 
    which provided readings from on around 50 different plants. The data for each 
    plant is read and stored in a Python list.
'''

import multiprocessing as mp
import requests


class RecordingAPIExtractor:
    '''The APIExtractor class extracts data recorded from the plants API across 
    all specified plant ids.'''

    def __init__(self, api_url: str, min_plant_id: int = 1, max_plant_id: int = 55):
        '''The minimum and maximum values represent the range of plant ids checked to have data.'''
        self.api_url = api_url
        self.min_plant_id = min_plant_id
        self.max_plant_id = max_plant_id

    def _make_request(self, plant_id: int) -> dict:
        '''Given a plant_id, make a get request to the endpoint and return the result.
        If the request returns anything other than a success code, None is returned; this
        can happen if the plant_id is invalid, or if a faulty reading is made.'''
        request = requests.get(f"{self.api_url}{plant_id}", timeout=4)
        if request.status_code == 200:
            return request.json()
        return None

    def extract_api_data(self):
        '''Extract the endpoint data for all ids in the specified range. Multiprocessing
        is used since the API can be quite slow. None results are filtered out the final result.'''
        plant_ids = list(range(self.min_plant_id, self.max_plant_id+1))
        with mp.Pool(mp.cpu_count()) as p:
            fetched_data = p.map(self._make_request, plant_ids)
        return [json_obj for json_obj in fetched_data if json_obj is not None]
