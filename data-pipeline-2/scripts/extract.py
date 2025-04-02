'''
    DATA PIPELINE 2: extract
    The following script takes data from the RDS (short-term storage) and loads the data into a pandas dataframe.
    It specifically extracts data outside a 24 hour window from the current time.
'''

import os
import datetime as datetime
import pandas as pd
import pymysql
from dotenv import load_dotenv


class Extract:
    '''A static class from which extract methods are called.'''

    QUERY = '''
        WITH outside_24_hour AS (
            SELECT * FROM record
            WHERE record_taken < NOW() - INTERVAL 24 HOUR
        )
        SELECT 
            o24h.record_id,
            p.plant_number, 
            o24h.soil_moisture, 
            o24h.temperature,
            o24h.record_taken
        FROM outside_24_hour AS o24h
        JOIN plant AS p ON p.plant_id = o24h.plant_id
        JOIN plant_type AS pt ON pt.plant_type_id = p.plant_type_id
        JOIN botanist AS b ON b.botanist_id = p.botanist_id
        JOIN city AS cit ON cit.city_id = p.city_id
        JOIN country AS cou ON cou.country_id = cit.country_id
        JOIN continent AS con ON con.continent_id = cou.continent_id
    '''

    @staticmethod
    def _get_connection():
        '''Get the connection to the RDS, using credentials from the .env file.'''
        load_dotenv()
        return pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME'],
        )

    def extract_data_to_be_archived(self) -> pd.DataFrame:
        '''Extract the rows from the RDS which are outside the 24 hour window.'''
        with Extract._get_connection() as connection:
            return pd.read_sql(Extract.QUERY, connection)
