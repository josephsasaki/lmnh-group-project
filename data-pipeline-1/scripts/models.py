from datetime import datetime


class Record:
    """Record class which helps store incoming data from API"""

    def __init__(self, record_dict_data: dict):
        """Initialises the Record class"""
        self.__plant_id = record_dict_data.get('plant_id')
        self.__soil_moisture = Record.clean_soil_moisture(
            record_dict_data.get('soil_moisture'))
        self.__temperature = Record.clean_temperature(
            record_dict_data.get('temperature'))
        self.__time = Record.clean_time(
            record_dict_data.get('recording_taken'))

    @staticmethod
    def clean_plant_id(plant_id_in: int) -> int:
        if plant_id_in is None:
            raise KeyError(f'Input data does not have a plant_id')

        return plant_id_in

    @staticmethod
    def clean_soil_moisture(soil_moisture_in: float) -> float:
        if soil_moisture_in is None:
            raise KeyError(f'Soil moisture not included in record data')

        if soil_moisture_in > 100 or soil_moisture_in < 0:
            raise ValueError(
                f'Soil moisture level of {soil_moisture_in} is not valid')

        return soil_moisture_in

    @staticmethod
    def clean_temperature(temperature_in: float) -> float:
        if temperature_in is None:
            raise KeyError(f'Temperature not included in record data')

        return temperature_in

    @staticmethod
    def clean_time(time_in: str) -> datetime:
        if time_in is None:
            raise KeyError(f'Time not included in record data')

        try:
            time_in = datetime.strptime(time_in, "%Y-%m-%d %H:%M:%S")
            if time_in > datetime.now():
                raise ValueError(
                    f'The time ({time_in}) is invalid as it is in the future')
            return time_in
        except ValueError:
            raise ValueError(
                f'The time ({time_in} is in an invalid format. Format should be "%Y-%m-%d %H:%M:%S")')
