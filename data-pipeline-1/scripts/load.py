

from os import environ as ENV
from dotenv import load_dotenv
import pyodbc
from models import Plant, Botanist, Location, PlantType


class Load:

    CONTINENT_UPSERT = '''
        MERGE INTO continent AS target
        USING (SELECT ? AS continent_name) AS source
        ON target.continent_name = source.continent_name
        WHEN NOT MATCHED THEN
            INSERT (continent_name)
            VALUES (source.continent_name);
    '''
    COUNTRY_UPSERT = '''
        MERGE INTO country AS target
        USING (
            SELECT 
                ? AS country_name, 
                ? AS country_capital, 
                (SELECT continent_id FROM continent WHERE continent_name = ?) AS continent_id
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
                ? AS city_name, 
                ? AS city_latitude, 
                ? AS city_longitude, 
                (SELECT country_id FROM country WHERE country_name = ?) AS country_id
        ) AS source
        ON target.city_name = source.city_name
        WHEN NOT MATCHED AND source.country_id IS NOT NULL THEN
            INSERT (city_name, city_latitude, city_longitude, country_id)
            VALUES (source.city_name, source.city_latitude, source.city_longitude, source.country_id);
    '''
    BOTANIST_UPSERT = '''
        MERGE INTO botanist AS target
        USING (SELECT ? AS botanist_name, ? AS botanist_email, ? AS botanist_phone) AS source
        ON target.botanist_name = source.botanist_name
            AND target.botanist_email = source.botanist_email
            AND target.botanist_phone = source.botanist_phone
        WHEN NOT MATCHED THEN
            INSERT (botanist_name, botanist_email, botanist_phone)
            VALUES (source.botanist_name, source.botanist_email, source.botanist_phone);
    '''
    PLANT_TYPE_UPSERT = '''
        MERGE INTO plant_type AS target
        USING (SELECT ? AS plant_type_name, ? AS plant_type_scientific_name, ? AS plant_type_image_url) AS SOURCE
        ON target.plant_type_name = source.plant_type_name
        WHEN NOT MATCHED THEN
            INSERT (plant_type_name, plant_type_scientific_name, plant_type_image_url)
            VALUES (source.plant_type_name, source.plant_type_scientific_name, source.plant_type_image_url);
    '''
    PLANT_UPSERT = '''
        MERGE INTO plant AS target
        USING (
            SELECT 
                ? AS plant_number, 
                (SELECT plant_type_id FROM plant_type WHERE plant_type_name = ?) AS plant_type_id, 
                (SELECT botanist_id FROM botanist WHERE botanist_name = ?) AS botanist_id,
                (SELECT city_id FROM city WHERE city_name = ?) AS city_id,
                ? AS plant_last_watered
        ) AS source
        ON target.plant_number = source.plant_number
        WHEN MATCHED THEN
            UPDATE SET target.plant_last_watered = source.plant_last_watered
        WHEN NOT MATCHED THEN
            INSERT (plant_type_id, plant_number, botanist_id, city_id, plant_last_watered)
            VALUES (source.plant_type_id, source.plant_number, source.botanist_id, source.city_id, source.plant_last_watered);
    '''

    @staticmethod
    def get_connection():
        '''Get the connection to the RDS, using credentials from the .env file.'''
        load_dotenv()
        conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                    f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                    f"UID={ENV['DB_USERNAME']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")
        conn = pyodbc.connect(conn_str)
        return conn

    @staticmethod
    def add_new_continents(locations: list[Location], connection):
        with connection.cursor() as cursor:
            for location in locations:
                cursor.execute(Load.CONTINENT_UPSERT,
                               location.get_continent_values())
                cursor.commit()

    @staticmethod
    def add_new_countries(locations: list[Location], connection):
        with connection.cursor() as cursor:
            for location in locations:
                cursor.execute(Load.COUNTRY_UPSERT,
                               location.get_country_values())
                cursor.commit()

    @staticmethod
    def add_new_cities(locations: list[Location], connection):
        with connection.cursor() as cursor:
            for location in locations:
                cursor.execute(Load.CITY_UPSERT, location.get_city_values())
                cursor.commit()

    @staticmethod
    def add_new_botanists(botanists: list[Botanist], connection):
        with connection.cursor() as cursor:
            for botanist in botanists:
                cursor.execute(Load.BOTANIST_UPSERT, botanist.get_values())
                cursor.commit()

    @staticmethod
    def add_new_plant_type(plant_types: list[PlantType], connection):
        with connection.cursor() as cursor:
            for plant_type in plant_types:
                cursor.execute(Load.PLANT_TYPE_UPSERT, plant_type.get_values())
                cursor.commit()

    @staticmethod
    def add_new_plants(plants: list[Plant], connection):
        '''Insert plants only if plant_number doesn't exist, update last_watered if it does.'''
        with connection.cursor() as cursor:
            for plant in plants:
                cursor.execute(Load.PLANT_UPSERT, plant.get_values())
                cursor.commit()
