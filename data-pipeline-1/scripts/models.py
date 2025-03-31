class Record:
    """Record class which helps store incoming data from API"""

    def __init__(self, record_dict_data: dict):
        """Initialises the Record class"""
        self.__plant_id = record_dict_data.get('plant_id')
        self.__soil_moisture = Record.clean_soil_moisture(
            record_dict_data.get('soil_moisture'))
        self.__temperature = record_dict_data.get('temperature')
        self.__time = record_dict_data.get('recording_taken')

    @staticmethod
    def clean_soil_moisture(soil_moisture_data_in: float):
        if soil_moisture_data_in is None:
            raise ValueError(f'Soil moisture not included in record data')

        if soil_moisture_data_in > 100 or soil_moisture_data_in < 0:
            raise ValueError(
                f'Soil moisture level of {soil_moisture_data_in} is not valid')

        return soil_moisture_data_in
