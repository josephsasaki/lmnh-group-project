'''
    DATA PIPELINE 2: extract
    The following script takes data from the RDS (short-term storage) and loads the data into a pandas dataframe.
    It specifically extracts data outside a 24 hour window from the current time.
'''

from os import environ as ENV
import datetime as datetime
import pandas as pd
import pyodbc
from dotenv import load_dotenv


class ExpiredDataFinder:
    '''A static class from which extract methods are called.'''

    QUERY = '''
    WITH outside_24_hour AS (
            SELECT * FROM record
            WHERE record_timestamp < DATEADD(hour, -24, CONVERT(datetime, SYSDATETIMEOFFSET() AT TIME ZONE 'GMT Standard Time'))
    )
    SELECT 
        o24h.record_id,
        p.plant_number,
        p.plant_last_watered,
        o24h.record_soil_moisture, 
        o24h.record_temperature,
        o24h.record_timestamp,
        pt.plant_type_name,
        pt.plant_type_scientific_name,
        pt.plant_type_image_url,
        b.botanist_name,
        b.botanist_email,
        b.botanist_phone,
        cit.city_name,
        cit.city_latitude,
        cit.city_longitude,
        cou.country_name,
        cou.country_capital,
        con.continent_name
    FROM outside_24_hour AS o24h
    JOIN plant AS p ON p.plant_id = o24h.plant_id
    JOIN plant_type AS pt ON pt.plant_type_id = p.plant_type_id
    JOIN botanist AS b ON b.botanist_id = p.botanist_id
    JOIN city AS cit ON cit.city_id = p.city_id
    JOIN country AS cou ON cou.country_id = cit.country_id
    JOIN continent AS con ON con.continent_id = cou.continent_id
    '''

    def __init__(self):
        self.conn = self._initiate_connection()

    def _initiate_connection(self) -> pyodbc.Connection:
        '''Get the connection to the RDS, using credentials from the .env file.'''
        load_dotenv()
        conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                    f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                    f"UID={ENV['DB_USERNAME']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")
        conn = pyodbc.connect(conn_str)
        return conn

    def get_connection(self):
        return self.conn

    def close_connection(self):
        self.conn.close()

    def extract_data_to_be_archived(self) -> pd.DataFrame:
        '''Extract the rows from the RDS which are outside the 24 hour window.'''
        return pd.read_sql(self.QUERY, self.conn)
