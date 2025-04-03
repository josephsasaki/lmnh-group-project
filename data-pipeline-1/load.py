'''
    The loading part of the first data pipeline. This script takes the plant data and 
    loads it to the short-term storage solution (RDS). Reference tables are added first, 
    then the recording data.
'''

from os import environ as ENV
from dotenv import load_dotenv
import pymssql
from models import Plant


class DatabaseManager:
    '''Load class used to load plant data to the RDS.'''

    CONTINENT_UPSERT = '''
        MERGE INTO continent AS target
        USING (SELECT %s AS continent_name) AS source
        ON target.continent_name = source.continent_name
        WHEN NOT MATCHED THEN
            INSERT (continent_name)
            VALUES (source.continent_name);
    '''
    COUNTRY_UPSERT = '''
        MERGE INTO country AS target
        USING (
            SELECT 
                %s AS country_name, 
                %s AS country_capital, 
                (SELECT continent_id FROM continent WHERE continent_name = %s) AS continent_id
        ) AS source
        ON target.country_name = source.country_name
        WHEN NOT MATCHED AND source.continent_id IS NOT NULL THEN
            INSERT (country_name, country_capital, continent_id)
            VALUES (source.country_name, source.country_capital, source.continent_id);
    '''
    CITY_UPSERT = '''
        MERGE INTO city AS target
        USING (
            SELECT 
                %s AS city_name, 
                %s AS city_latitude, 
                %s AS city_longitude, 
                (SELECT country_id FROM country WHERE country_name = %s) AS country_id
        ) AS source
        ON target.city_name = source.city_name
        WHEN NOT MATCHED AND source.country_id IS NOT NULL THEN
            INSERT (city_name, city_latitude, city_longitude, country_id)
            VALUES (source.city_name, source.city_latitude, source.city_longitude, source.country_id);
    '''
    BOTANIST_UPSERT = '''
        MERGE INTO botanist AS target
        USING (SELECT %s AS botanist_name, %s AS botanist_email, %s AS botanist_phone) AS source
        ON target.botanist_name = source.botanist_name
            AND target.botanist_email = source.botanist_email
            AND target.botanist_phone = source.botanist_phone
        WHEN NOT MATCHED THEN
            INSERT (botanist_name, botanist_email, botanist_phone)
            VALUES (source.botanist_name, source.botanist_email, source.botanist_phone);
    '''
    PLANT_TYPE_UPSERT = '''
        MERGE INTO plant_type AS target
        USING (SELECT %s AS plant_type_name, %s AS plant_type_scientific_name, %s AS plant_type_image_url) AS SOURCE
        ON target.plant_type_name = source.plant_type_name
        WHEN NOT MATCHED THEN
            INSERT (plant_type_name, plant_type_scientific_name, plant_type_image_url)
            VALUES (source.plant_type_name, source.plant_type_scientific_name, source.plant_type_image_url);
    '''
    PLANT_UPSERT = '''
        MERGE INTO plant AS target
        USING (
            SELECT 
                %s AS plant_number, 
                (SELECT plant_type_id FROM plant_type WHERE plant_type_name = %s) AS plant_type_id, 
                (SELECT botanist_id FROM botanist WHERE botanist_name = %s) AS botanist_id,
                (SELECT city_id FROM city WHERE city_name = %s) AS city_id,
                %s AS plant_last_watered
        ) AS source
        ON target.plant_number = source.plant_number
        WHEN MATCHED THEN
            UPDATE SET target.plant_last_watered = source.plant_last_watered
        WHEN NOT MATCHED THEN
            INSERT (plant_type_id, plant_number, botanist_id, city_id, plant_last_watered)
            VALUES (source.plant_type_id, source.plant_number, source.botanist_id, source.city_id, source.plant_last_watered);
    '''
    RECORDING_INSERT = '''
        INSERT INTO record (plant_id, record_soil_moisture, record_temperature, record_timestamp)
        SELECT plant_id, %s, %s, %s FROM plant
        WHERE plant_number = %s;
    '''

    def __init__(self, plants: list[Plant]):
        self.plants = plants
        self.connection = self._make_connection()
        self.cursor = self.connection.cursor()

    def _make_connection(self):
        '''Get the connection to the RDS, using credentials from the .env file.'''
        load_dotenv()
        return pymssql.connect(
            server=ENV['DB_HOST'],
            user=ENV['DB_USERNAME'],
            password=ENV['DB_PASSWORD'],
            database=ENV['DB_NAME'],
            port=ENV['DB_PORT']
        )

    def _add_new_locations(self):
        '''Merge any new locations to the database. A continent is considered new
        if the continent name doesn't already exist. A country is considered new
        if the country name doesn't already exist.A city is considered new
        if the city name doesn't already exist.
        Note, the cursor commits must be done externally.'''
        locations = [plant.get_location() for plant in self.plants]
        # Continents
        continent_values = [location.get_continent_values()
                            for location in locations]
        self.cursor.executemany(self.CONTINENT_UPSERT, continent_values)
        # Countries
        country_values = [location.get_country_values()
                          for location in locations]
        self.cursor.executemany(self.COUNTRY_UPSERT, country_values)
        # City
        city_values = [location.get_city_values() for location in locations]
        self.cursor.executemany(self.CITY_UPSERT, city_values)

    def _add_new_botanists(self):
        '''Merge any new botanists to the database. A botanist is considered new
        if their name, email and phone number do not exist.
        Note, the cursor commits must be done externally.'''
        botanist_values = [plant.get_botanist().get_values()
                           for plant in self.plants]
        self.cursor.executemany(self.BOTANIST_UPSERT, botanist_values)

    def _add_new_plant_type(self):
        '''Merge any new plant types to the database. A plant type is considered new
        if the plant name (not scientific name)
        Note, the cursor commits must be done externally.'''
        plant_type_values = [plant.get_plant_type().get_values()
                             for plant in self.plants]
        self.cursor.executemany(self.PLANT_TYPE_UPSERT, plant_type_values)

    def _add_new_plants(self):
        '''Merge any new plants to the database. A plant is considered new is the 
        plant_number does not yet exist. If the plant_number does already exist in the database,
        update the last_watered field.
        Note, the cursor commits must be done externally.'''
        plant_values = [plant.get_values() for plant in self.plants]
        self.cursor.executemany(self.PLANT_UPSERT, plant_values)

    def _add_new_recordings(self):
        '''Insert the new recordings to the database. 
        Note, the cursor commits must be done externally.'''
        recording_values = [plant.get_record_values() for plant in self.plants]
        self.cursor.executemany(self.RECORDING_INSERT, recording_values)

    def load_all(self) -> None:
        '''Connect to the database and load the plant data passed at instantiation.'''
        try:
            self._add_new_botanists()
            self._add_new_locations()
            self._add_new_plant_type()
            self._add_new_plants()
            self._add_new_recordings()
            self.connection.commit()
        except Exception as e:
            print(f"Error in load_all: {e}")
        finally:
            self.cursor.close()
            self.connection.close()
