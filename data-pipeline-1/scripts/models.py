import os
from datetime import datetime
import re
import pandas as pd


class Botanist:
    def __init__(self, botanist_dict_data: dict) -> None:
        if not isinstance(botanist_dict_data, dict):
            raise ValueError(
                f'The input data is not the correct type. It should be a dict but it is a {type(botanist_dict_data)}.')

        self.__email = Botanist.clean_email(botanist_dict_data.get("email"))
        self.__name = Botanist.clean_name(botanist_dict_data.get("name"))
        self.__phone = Botanist.clean_phone(botanist_dict_data.get("phone"))

    def get_values(self) -> tuple[str]:
        '''Return the botanist values to be used in SQL queries.'''
        return self.__name, self.__email, self.__phone

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
        if not name_in:
            raise ValueError(
                f"The name attribute '{name_in}' does not hold a valid value.")
        return name_in

    @staticmethod
    def clean_phone(phone_in: str) -> str:
        if phone_in is None:
            raise ValueError("Phone value is not included in the input data")

        phone_format_one = bool(re.fullmatch(
            r'\d{3}-\d{3}-\d{3}-\d{4}x\d{3}', phone_in))
        phone_format_two = bool(re.fullmatch(
            r'\(\d{3}\)\d{3}-\d{4}x\d{5}', phone_in))
        if not phone_format_one and not phone_format_two:
            raise ValueError('Phone number does not follow a correct format.')

        return phone_in


class Location:
    COUNT_OF_LOCATION_ATTRIBUTES = 5

    def __init__(self, location_data: list) -> None:
        if not isinstance(location_data, list):
            raise ValueError(
                f'The input data is not the correct type. It should be a list but it is a {type(location_data)}.')

        location_dict_data = Location.convert_location_data_to_dict(
            location_data)

        self.__latitude = Location.clean_latitude_longitude(
            location_dict_data.get('latitude'))
        self.__longitude = Location.clean_latitude_longitude(
            location_dict_data.get('longitude'))
        self.__city = Location.clean_city_name(
            location_dict_data.get('city_name'))
        self.__country = Location.convert_country_code_to_name(
            location_dict_data.get('country_code'))
        continent, capital = Location.clean_continent_capital(
            location_dict_data.get('continent_capital'))
        self.__continent = continent
        self.__capital = capital

    def get_continent_values(self) -> tuple[str]:
        return (self.__continent,)

    def get_country_values(self) -> tuple[str]:
        return (self.__country, self.__capital, self.__continent)

    def get_city_values(self) -> tuple[str]:
        return (self.__city, self.__latitude, self.__longitude, self.__country)

    @staticmethod
    def convert_location_data_to_dict(location_data_in: list) -> dict:
        if len(location_data_in) != Location.COUNT_OF_LOCATION_ATTRIBUTES:
            raise ValueError(
                f"There should be {Location.COUNT_OF_LOCATION_ATTRIBUTES} values in the location data, instead there is {len(location_data_in)}")
        return {
            "latitude": location_data_in[0],
            "longitude": location_data_in[1],
            "city_name": location_data_in[2],
            "country_code": location_data_in[3],
            "continent_capital": location_data_in[4]
        }

    @staticmethod
    def convert_country_code_to_name(country_code_in: str) -> str:
        if country_code_in is None:
            raise ValueError(
                'The country code attribute is not included in the input data.')
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(
            script_dir, './../country_code_data/code_to_name.csv')
        df_country = pd.read_csv(file_path)
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
        try:
            return float(coordinate_in)
        except ValueError:
            raise ValueError(
                f'Value {coordinate_in} is not suitable for latitude or longitude as it cant be converted to a float.')

    @staticmethod
    def clean_continent_capital(continent_capital_in: str) -> tuple[str]:
        if continent_capital_in is None:
            return ValueError('The country and capital attribute is not included in the input data.')
        continent_capital_list = continent_capital_in.split('/')
        return continent_capital_list[0], continent_capital_list[1]


class Record:
    """Record class which helps store incoming data from API"""
    MAX_SOIL_MOISTURE = 100
    MIN_SOIL_MOISTURE = -10

    def __init__(self, record_dict_data: dict) -> None:
        """Initialises the Record class"""
        self.__soil_moisture = Record.clean_soil_moisture(
            record_dict_data.get('soil_moisture'))
        self.__temperature = Record.clean_temperature(
            record_dict_data.get('temperature'))
        self.__taken = Record.clean_taken_time(
            record_dict_data.get('recording_taken'))

    @staticmethod
    def clean_soil_moisture(soil_moisture_in: float) -> float:
        if soil_moisture_in is None:
            raise ValueError('Soil moisture not included in record data')

        if soil_moisture_in > Record.MAX_SOIL_MOISTURE or soil_moisture_in < Record.MIN_SOIL_MOISTURE:
            raise ValueError(
                f'Soil moisture level of {soil_moisture_in} is not valid')

        return round(soil_moisture_in, 2)

    @staticmethod
    def clean_temperature(temperature_in: float) -> float:
        if temperature_in is None:
            raise ValueError(f'Temperature not included in record data')

        return round(temperature_in, 2)

    @staticmethod
    def clean_taken_time(timestamp_in: str) -> datetime:
        if timestamp_in is None:
            raise ValueError(f'Time not included in record data')

        try:
            timestamp_in = datetime.strptime(timestamp_in, "%Y-%m-%d %H:%M:%S")
            if timestamp_in > datetime.now():
                raise ValueError(
                    f'The time ({timestamp_in}) is invalid as it is in the future')
            return timestamp_in
        except ValueError:
            raise ValueError(
                f'The time ({timestamp_in} is in an invalid format. Format should be "%Y-%m-%d %H:%M:%S")')


class PlantType:
    def __init__(self, plant_type_dict_data: dict) -> None:
        self.__name = PlantType.clean_plant_type_name(
            plant_type_dict_data.get('name'))
        self.__scientific_name = PlantType.clean_plant_type_scientific_name(
            plant_type_dict_data.get('scientific_name'))
        self.__image_url = PlantType.clean_image_url(
            plant_type_dict_data.get('images'))

    def get_values(self) -> tuple[str]:
        return (self.__name, self.__scientific_name, self.__image_url)

    @staticmethod
    def clean_plant_type_name(plant_type_name_in: str) -> str:
        if plant_type_name_in is None:
            raise ValueError(
                "The plant type name attribute is not included in the input data.")
        if not plant_type_name_in:
            raise ValueError(
                f'Plant type name value: "{plant_type_name_in}", is not valid')
        return plant_type_name_in

    @staticmethod
    def clean_plant_type_scientific_name(plant_type_scientific_name_in: list[str]) -> str | None:
        if not plant_type_scientific_name_in:
            return None
        if not isinstance(plant_type_scientific_name_in, list):
            raise ValueError(
                'The scientific name for the plant should be input as a list')
        return plant_type_scientific_name_in[0]

    @staticmethod
    def clean_image_url(images_url_in: dict | None) -> str | None:
        if images_url_in is None:
            return None
        image_url = images_url_in.get('original_url')
        if image_url is None:
            return None
        if image_url[0:8] == "https://" and image_url[-3:] == "jpg":
            return image_url
        return None


class Plant:
    # Plant should take in all data, make all the objects it needs, and put them in an attribute itself.
    def __init__(self, response_data: dict) -> None:
        self.__last_watered = Plant.clean_last_watered(
            response_data.get('last_watered'))
        self.__plant_number = Plant.clean_plant_number(
            response_data.get('plant_id'))
        # object instantiation
        self.__botanist = Botanist(response_data.get('botanist'))
        self.__location = Location(response_data.get('origin_location'))
        self.__record = Record({
            "soil_moisture": response_data.get('soil_moisture'),
            "temperature": response_data.get('temperature'),
            "recording_taken": response_data.get('recording_taken'),
        })
        self.__plant_type = PlantType({
            "name": response_data.get('name'),
            "scientific_name": response_data.get("scientific_name"),
            "images": response_data.get("images")
        })

    def get_botanist(self) -> Botanist:
        return self.__botanist

    def get_location(self) -> Location:
        return self.__location

    def get_plant_type(self) -> PlantType:
        return self.__plant_type

    def get_values(self) -> tuple[str]:
        return (
            self.__plant_number,
            self.__plant_type.get_values()[0],
            self.__botanist.get_values()[0],
            self.__location.get_city_values()[0],
            self.__last_watered,
        )

    @staticmethod
    def clean_plant_number(plant_number_in: int) -> int:
        if plant_number_in is None:
            raise ValueError(
                'There is no plant number in the response object.')
        return plant_number_in

    @staticmethod
    def clean_last_watered(last_watered_in: str) -> datetime:
        if last_watered_in is None:
            raise ValueError(f'The last_watered attribute is not included')
        try:
            last_watered_in = datetime.strptime(
                last_watered_in, "%a, %d %b %Y %H:%M:%S %Z")
            if last_watered_in > datetime.now():
                raise ValueError(
                    f'The time ({last_watered_in}) is invalid as it is in the future')
            return last_watered_in
        except ValueError:
            raise ValueError(
                f'The time ({last_watered_in} is in an invalid format. Format should be "%Y-%m-%d %H:%M:%S")')
