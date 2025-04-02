

from os import environ as ENV
from dotenv import load_dotenv
import pyodbc
from models import Plant, Botanist, Location


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
            AND target.plant_type_name = source.plant_type_name
            AND target.plant_type_scientific_name = source.plant_type_scientific_name
            AND target.plant_type_image_url = source.plant_type_image_url
        WHEN NOT MATCHED THEN
            INSERT (plant_type_name, plant_type_scientific_name, plant_type_image_url)
            VALUES (source.plant_type_name, source.plant_type_scientific_name, source.plant_type_image_url);
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
                cursor.execute(Load.TEST, botanist.get_values())
                cursor.commit()


if __name__ == "__main__":
    connection = Load.get_connection()
    try:
        botanists = [
            Botanist({"name": "Testing", "email": "test.test@test.com",
                      "phone": "001-481-273-3691x127"}),
            Botanist({"name": "Joe", "email": "Joe.s@test.com",
                      "phone": "001-481-273-3691x128"}),
        ]
        Load.add_new_botanists(botanists, connection)
    except Exception as e:
        print("here??/")
        raise (e)
    finally:
        connection.close()
