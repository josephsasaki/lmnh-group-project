from datetime import datetime
import pandas as pd


class Botanist:
    def __init__(self, botanist_dict_data: dict):
        self.__email = Botanist.clean_email(botanist_dict_data.get("email"))
        self.__name = Botanist.clean_name(botanist_dict_data.get("name"))
        self.__phone = Botanist.clean_phone(botanist_dict_data.get("phone"))

    @staticmethod
    def clean_email(email_in: str) -> str:
        if email_in is None:
            raise ValueError("Email value is not included in the input data")
        if '@' not in email_in:
            raise ValueError(
                f"The email is not valid as it doesn't have an '@' symbol.")
        return email_in

    @staticmethod
    def clean_name(name_in: str) -> str:
        if name_in is None:
            raise ValueError("Name value is not included in the input data")
        return name_in

    @staticmethod
    def clean_phone(phone_in: str) -> str:
        if phone_in is None:
            raise ValueError("Phone value is not included in the input data")

        phone_in = list(phone_in)
        clean_phone = []
        for char in phone_in:
            if char.isnumeric():
                clean_phone.append(char)

        return ''.join(clean_phone)


class Location:
    def __init__(self, location_dict_data: dict):
        self.__latitude = Location.clean_latitude_longitude(
            location_dict_data.get('latitude'))
        self.__longitude = Location.clean_latitude_longitude(
            location_dict_data.get('longitude'))
        self.__city_name = Location.clean_city_name(
            location_dict_data.get('latitude'))
        self.__country_name = Location.convert_country_code_to_name(
            location_dict_data.get('country_code'))
        continent, capital = location_dict_data.get('continent_capital')
        self.__continent = continent
        self.__capital = capital

    @staticmethod
    def convert_country_code_to_name(country_code_in: str) -> str:
        if country_code_in is None:
            raise ValueError(
                'The country code attribute is not included in the input data.')
        df_country = pd.read_csv('country_code_data/code_to_name.csv')
        df_country = df_country[df_country['alpha-2']
                                == country_code_in.upper()]
        country = df_country['name'].iloc[0]
        return country

    @staticmethod
    def clean_city_name(city_name_in: str) -> str:
        if city_name_in is None:
            raise ValueError(
                'The city name attribute is not included in the input data.')
        return city_name_in

    @staticmethod
    def clean_latitude_longitude(coordinate_in: float) -> float:
        if coordinate_in is None:
            raise ValueError(
                'The latitude or longitude attribute is not included in the input data.')
        if not isinstance(coordinate_in, float):
            raise ValueError(
                f'Value {coordinate_in} is not suitable for latitude or longitude as its not a float.')
        return coordinate_in

    @staticmethod
    def clean_continent_capital(continent_capital_in: str) -> tuple[str]:
        if continent_capital_in is None:
            return ValueError('The country and capital attribute is not included in the input data.')
        continent_capital_list = continent_capital_in.split('/')
        return continent_capital_list[0], continent_capital_list[1]


class Record:
    """Record class which helps store incoming data from API"""
    MAX_SOIL_MOISTURE = 100
    MIN_SOIL_MOISTURE = 0

    def __init__(self, record_dict_data: dict):
        """Initialises the Record class"""
        self.__soil_moisture = Record.clean_soil_moisture(
            record_dict_data.get('soil_moisture'))
        self.__temperature = Record.clean_temperature(
            record_dict_data.get('temperature'))
        self.__timestamp = Record.clean_time(
            record_dict_data.get('recording_taken'))

    @staticmethod
    def clean_soil_moisture(soil_moisture_in: float) -> float:
        if soil_moisture_in is None:
            raise ValueError('Soil moisture not included in record data')

        if soil_moisture_in > Record.MAX_SOIL_MOISTURE or soil_moisture_in < Record.MIN_SOIL_MOISTURE:
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
    # Plant should take in all data, make all the objects it needs, and put them in an attribute itself.
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


if __name__ == '__main__':
    Location.convert_country_code_to_name('AU')
