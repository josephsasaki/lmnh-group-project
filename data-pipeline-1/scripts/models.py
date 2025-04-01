from datetime import datetime


class Botanist:
    def __init__(self, botanist_dict_data: dict):
        self.__email = Botanist.clean_email(botanist_dict_data.get("email"))
        self.__name = Botanist.clean_name(botanist_dict_data.get("name"))
        self.__phone = Botanist.clean_phone(botanist_dict_data.get("phone"))

    @staticmethod
    def clean_email(email_in: str):
        if email_in is None:
            raise ValueError("Email value is not included in the input data")
        if '@' not in email_in:
            raise ValueError(
                f"The email is not valid as it does'nt have an '@' symbol.")
        return email_in

    @staticmethod
    def clean_name(name_in: str):
        if name_in is None:
            raise ValueError("Name value is not included in the input data")
        return name_in

    @staticmethod
    def clean_phone(phone_in: str):
        if phone_in is None:
            raise ValueError("Phone value is not included in the input data")

        phone_in = list(phone_in)
        clean_phone = []
        for char in phone_in:
            if char.isnumeric():
                clean_phone.append(char)

        return ''.join(clean_phone)


class Record:
    """Record class which helps store incoming data from API"""

    def __init__(self, record_dict_data: dict):
        """Initialises the Record class"""
        self.__soil_moisture = Record.clean_soil_moisture(
            record_dict_data.get('soil_moisture'))
        self.__temperature = Record.clean_temperature(
            record_dict_data.get('temperature'))
        self.__time = Record.clean_time(
            record_dict_data.get('recording_taken'))

    @staticmethod
    def clean_soil_moisture(soil_moisture_in: float) -> float:
        if soil_moisture_in is None:
            raise ValueError(f'Soil moisture not included in record data')

        if soil_moisture_in > 100 or soil_moisture_in < 0:
            raise ValueError(
                f'Soil moisture level of {soil_moisture_in} is not valid')

        return soil_moisture_in

    @staticmethod
    def clean_temperature(temperature_in: float) -> float:
        if temperature_in is None:
            raise ValueError(f'Temperature not included in record data')

        return temperature_in

    @staticmethod
    def clean_time(time_in: str) -> datetime:
        if time_in is None:
            raise ValueError(f'Time not included in record data')

        try:
            time_in = datetime.strptime(time_in, "%Y-%m-%d %H:%M:%S")
            if time_in > datetime.now():
                raise ValueError(
                    f'The time ({time_in}) is invalid as it is in the future')
            return time_in
        except ValueError:
            raise ValueError(
                f'The time ({time_in} is in an invalid format. Format should be "%Y-%m-%d %H:%M:%S")')


class Plant:
    # plabnt should take in all data and make all th eobjects its needs and put themin an attribute itself.
    def __init__(self, all_data: dict):
        self.__last_watered = Plant.clean_last_watered(
            plant_dict_data.get('last_watered'))

    @staticmethod
    def clean_last_watered(last_watered_in: str) -> datetime:
        if last_watered_in is None:
            raise ValueError(f'The last_watered attribute is not included')
        try:
            last_watered_in = datetime.strptime(
                last_watered_in, "%Y-%m-%d %H:%M:%S")
            if last_watered_in > datetime.now():
                raise ValueError(
                    f'The time ({last_watered_in}) is invalid as it is in the future')
            return last_watered_in
        except ValueError:
            raise ValueError(
                f'The time ({last_watered_in} is in an invalid format. Format should be "%Y-%m-%d %H:%M:%S")')

    @staticmethod
    def id_checker(id_in: int, id_name: str) -> None:
        if not isinstance(id_in, int):
            raise TypeError(f'{id_name} is not an integer')

    def set_plant_type_id(self, plant_type_id_in: int):
        Plant.id_checker(plant_type_id_in)
        self.__plant_type_id = plant_type_id_in

    def set_botanist_id(self, botanist_id_in: int):
        Plant.id_checker(botanist_id_in)
        self.__botanist_id = botanist_id_in

    def set_city_id(self, city_id_in: int):
        Plant.id_checker(city_id_in)
        self.__city_id = city_id_in
