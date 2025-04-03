'''
    The models related to the plants object are defined here. 
'''

import os
from datetime import datetime
import re
import pandas as pd


class Botanist:
    '''Class representing a botanist, with a name, email and phone number.'''

    def __init__(self, botanist_dict_data: dict) -> None:
        '''Initialise the botanist with data extracted directly from the API.'''
        if not isinstance(botanist_dict_data, dict):
            raise ValueError(
                f'The input data is not the correct type. \
                      It should be a dict but it is a {type(botanist_dict_data)}.')
        self.__email = self.clean_email(botanist_dict_data.get("email"))
        self.__name = self.clean_name(botanist_dict_data.get("name"))
        self.__phone = self.clean_phone(botanist_dict_data.get("phone"))

    def get_values(self) -> tuple[str]:
        '''Return the botanist values to be used in SQL queries.'''
        return self.__name, self.__email, self.__phone

    def clean_email(self, email_in: str) -> str:
        '''Clean the email field. Raises error if invalid.'''
        if email_in is None:
            raise ValueError("Email value is not included in the input data")
        if '@' not in email_in:
            raise ValueError(
                "The email is not valid as it doesn't have an '@' symbol.")
        return email_in

    def clean_name(self, name_in: str) -> str:
        '''Clean the name field. Raises error if invalid.'''
        if name_in is None:
            raise ValueError("Name value is not included in the input data")
        if not name_in:
            raise ValueError(
                f"The name attribute '{name_in}' does not hold a valid value.")
        return name_in

    def clean_phone(self, phone_in: str) -> str:
        '''Clean the phone field. Raises error if invalid.'''
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
    '''Class representing a plant's origin location. Contained is the continent, country
    and city data.'''

    COUNT_OF_LOCATION_ATTRIBUTES = 5

    def __init__(self, location_data: list) -> None:
        '''Initialise the location object with data passed directly from the API.'''
        if not isinstance(location_data, list):
            raise ValueError(
                f'The input data is not the correct type. \
                    It should be a list but it is a {type(location_data)}.')
        location_dict_data = self.convert_location_data_to_dict(
            location_data)
        self.__latitude = self.clean_coordinate(
            location_dict_data.get('latitude'))
        self.__longitude = self.clean_coordinate(
            location_dict_data.get('longitude'))
        self.__city = self.clean_city_name(
            location_dict_data.get('city_name'))
        self.__country = self.convert_country_code_to_name(
            location_dict_data.get('country_code'))
        continent, capital = self.clean_continent_capital(
            location_dict_data.get('continent_capital'))
        self.__continent = continent
        self.__capital = capital

    def get_continent_values(self) -> tuple[str]:
        '''Get a tuple of values related to continents for loading.
        return: (continent_name)'''
        return (self.__continent,)

    def get_country_values(self) -> tuple[str]:
        '''Get a tuple of values related to countries for loading.
        return: (country_name, country_capital, continent_name)'''
        return (self.__country, self.__capital, self.__continent)

    def get_city_values(self) -> tuple[str]:
        '''Get a tuple of values related to cities for loading.
        return: (city_name, city_latitude, city_longitude, country_name)'''
        return (self.__city, self.__latitude, self.__longitude, self.__country)

    def convert_location_data_to_dict(self, location_data_in: list) -> dict:
        '''The location data is received as a list, so it first converted to a dictionary 
        for easier manipulation.'''
        if len(location_data_in) != self.COUNT_OF_LOCATION_ATTRIBUTES:
            raise ValueError(
                f"There should be {self.COUNT_OF_LOCATION_ATTRIBUTES} values in the \
                    location data, instead there is {len(location_data_in)}")
        return {
            "latitude": location_data_in[0],
            "longitude": location_data_in[1],
            "city_name": location_data_in[2],
            "country_code": location_data_in[3],
            "continent_capital": location_data_in[4]
        }

    def convert_country_code_to_name(self, country_code: str) -> str:
        '''Convert the country code to the full country name.'''
        if country_code is None:
            raise ValueError(
                'The country code attribute is not included in the input data.')
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(
            script_dir, './../country_code_data/code_to_name.csv')
        df_country = pd.read_csv(file_path)
        df_country = df_country[df_country['alpha-2']
                                == country_code.upper()]
        return df_country['name'].iloc[0]

    def clean_city_name(self, city_name_in: str) -> str:
        '''Clean the city name field. Raises error if invalid.'''
        if city_name_in is None:
            raise ValueError(
                'The city name attribute is not included in the input data.')
        return city_name_in

    def clean_coordinate(self, coordinate_in: float) -> float:
        '''Clean an inputted latitude or longitude. Raises error if invalid.'''
        if coordinate_in is None:
            raise ValueError(
                'The latitude or longitude attribute is not included in the input data.')
        try:
            return float(coordinate_in)
        except ValueError as exc:
            raise ValueError(
                f'Value {coordinate_in} is not suitable for latitude or \
                    longitude as it cant be converted to a float.') from exc

    def clean_continent_capital(self, continent_capital_in: str) -> tuple[str]:
        '''Clean the continent and capital field. Raises error if invalid.'''
        if continent_capital_in is None:
            return ValueError(
                'The country and capital attribute is not included in the input data.')
        continent_capital_list = continent_capital_in.split('/')
        return continent_capital_list[0], continent_capital_list[1]


class Recording:
    '''Object representing a reading made about a plant's condition.'''

    MAX_SOIL_MOISTURE = 100
    MIN_SOIL_MOISTURE = 0

    def __init__(self, record_dict_data: dict) -> None:
        '''Initialises the Record class.'''
        self.__soil_moisture = self.clean_soil_moisture(
            record_dict_data.get('soil_moisture'))
        self.__temperature = self.clean_temperature(
            record_dict_data.get('temperature'))
        self.__taken = self.clean_taken_time(
            record_dict_data.get('recording_taken'))

    def get_values(self):
        '''Get a tuple of values related to a record for loading.
        return: (soil_moisture, temperature, taken)'''
        return self.__soil_moisture, self.__temperature, self.__taken

    def clean_soil_moisture(self, soil_moisture_in: float) -> float:
        '''Clean the soil moisture field. Raises error if invalid.'''
        if soil_moisture_in is None:
            raise ValueError('Soil moisture not included in record data')
        if soil_moisture_in > self.MAX_SOIL_MOISTURE or soil_moisture_in < self.MIN_SOIL_MOISTURE:
            raise ValueError(
                f'Soil moisture level of {soil_moisture_in} is not valid')
        return round(soil_moisture_in, 2)

    def clean_temperature(self, temperature_in: float) -> float:
        '''Clean the temperature field. Raises error if invalid.'''
        if temperature_in is None:
            raise ValueError('Temperature not included in record data')
        return round(temperature_in, 2)

    def clean_taken_time(self, timestamp_in: str) -> datetime:
        '''Clean the time taken field. Raises error if invalid.'''
        if timestamp_in is None:
            raise ValueError('Time not included in record data')
        try:
            timestamp_in = datetime.strptime(timestamp_in, "%Y-%m-%d %H:%M:%S")
            if timestamp_in > datetime.now():
                raise ValueError(
                    f'The time ({timestamp_in}) is invalid as it is in the future')
            return timestamp_in
        except ValueError as exc:
            raise ValueError(
                f'The time ({timestamp_in} is in an invalid format. \
                    Format should be "%Y-%m-%d %H:%M:%S")') from exc


class PlantType:
    '''Object representing a plant type.'''

    def __init__(self, plant_type_dict_data: dict) -> None:
        '''Initialise a plant type.'''
        self.__name = self.clean_plant_type_name(
            plant_type_dict_data.get('name'))
        self.__scientific_name = self.clean_plant_type_scientific_name(
            plant_type_dict_data.get('scientific_name'))
        self.__image_url = self.clean_image_url(
            plant_type_dict_data.get('images'))

    def get_values(self) -> tuple[str]:
        '''Get values related to the plant type used for loading.
        return: (name, scientific_name, image_url)'''
        return (self.__name, self.__scientific_name, self.__image_url)

    def clean_plant_type_name(self, plant_type_name_in: str) -> str:
        '''Clean the plant type name field. Raises error if invalid.'''
        if plant_type_name_in is None:
            raise ValueError(
                "The plant type name attribute is not included in the input data.")
        if not plant_type_name_in:
            raise ValueError(
                f'Plant type name value: "{plant_type_name_in}", is not valid')
        return plant_type_name_in

    def clean_plant_type_scientific_name(self,
                                         plant_type_scientific_name_in: list[str]) -> str | None:
        '''Clean the plant type scientific name. Raises error if invalid.'''
        if not plant_type_scientific_name_in:
            return None
        if not isinstance(plant_type_scientific_name_in, list):
            raise ValueError(
                'The scientific name for the plant should be input as a list')
        return plant_type_scientific_name_in[0]

    def clean_image_url(self, images_url_in: dict | None) -> str | None:
        '''Clean the image url. Raises error if invalid.'''
        if images_url_in is None:
            return None
        image_url = images_url_in.get('original_url')
        if image_url is None:
            return None
        if image_url[0:8] == "https://" and image_url[-3:] == "jpg":
            return image_url
        return None


class Plant:
    '''Object representing a plant object. Plant should take in all data, 
    make all the objects it needs, and put them in an attribute itself.'''

    def __init__(self, response_data: dict) -> None:
        '''Instantiate a plant object.'''
        self.__last_watered = self.clean_last_watered(
            response_data.get('last_watered'))
        self.__plant_number = self.clean_plant_number(
            response_data.get('plant_id'))
        self.__botanist = Botanist(response_data.get('botanist'))
        self.__location = Location(response_data.get('origin_location'))
        self.__record = Recording({
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
        '''Get the botanist object.'''
        return self.__botanist

    def get_location(self) -> Location:
        '''Get the location object.'''
        return self.__location

    def get_plant_type(self) -> PlantType:
        '''Get the plant type object.'''
        return self.__plant_type

    def get_values(self) -> tuple[str]:
        '''Get values related to the plant used for loading.
        return: (plant_number, plant_type_name, botanist_name, city_name, last_watered)'''
        return (
            self.__plant_number,
            self.__plant_type.get_values()[0],
            self.__botanist.get_values()[0],
            self.__location.get_city_values()[0],
            self.__last_watered,
        )

    def get_record_values(self) -> tuple[str]:
        '''Get the values related to a record, used for loading.
        return: (soil_moisture, temperature, taken, plant_number)'''
        return (
            *self.__record.get_values(),
            self.__plant_number,
        )

    def clean_plant_number(self, plant_number_in: int) -> int:
        '''Clean the plant_number. Raises error if invalid.'''
        if plant_number_in is None:
            raise ValueError(
                'There is no plant number in the response object.')
        return plant_number_in

    def clean_last_watered(self, last_watered_in: str) -> datetime:
        '''Clean the last_watered field. Raises error if invalid.'''
        if last_watered_in is None:
            raise ValueError('The last_watered attribute is not included')
        try:
            last_watered_in = datetime.strptime(
                last_watered_in, "%a, %d %b %Y %H:%M:%S %Z")
            if last_watered_in > datetime.now():
                raise ValueError(
                    f'The time ({last_watered_in}) is invalid as it is in the future')
            return last_watered_in
        except ValueError as exc:
            raise ValueError(
                f'The time ({last_watered_in} is in an invalid format. \
                    Format should be "%Y-%m-%d %H:%M:%S")') from exc
