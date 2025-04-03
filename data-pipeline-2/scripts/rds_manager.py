'''
    DATA PIPELINE 2: RDS manager
    This script defines the class that interacts with the remote RDS on AWS. It has methods to
    get old data, delete rows of data and close the connection.
'''

from os import environ as ENV
import pandas as pd
import pyodbc
from dotenv import load_dotenv


class RDSManager:
    '''A class for interacting with a remote RDS on AWS'''

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
    BASE_DELETE_QUERY = "DELETE FROM record WHERE record_id IN ({wildcards})"

    def __init__(self) -> None:
        self.conn = self._initiate_connection()

    def _initiate_connection(self) -> pyodbc.Connection:
        '''Function called in init to initiate a connection to RDS in RDSManager'''
        load_dotenv()
        conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                    f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                    f"UID={ENV['DB_USERNAME']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")
        conn = pyodbc.connect(conn_str)
        return conn

    def close_connection(self) -> None:
        '''Closes a connection to the RDS'''
        self.conn.close()

    def extract_data_to_be_archived(self) -> pd.DataFrame:
        '''Extract the rows from the RDS which are outside the 24 hour window.'''
        return pd.read_sql(self.QUERY, self.conn)

    def _get_delete_query(self, number_of_ids: int) -> str:
        '''Creates delete query from a base query'''
        return self.BASE_DELETE_QUERY.format(wildcards=','.join(['?']*number_of_ids))

    def remove_rows_from_rds(self, record_ids: tuple[int]) -> None:
        """Removes rows from record table using input record_id's"""
        with self.conn.cursor() as cursor:
            delete_query = self._get_delete_query(len(record_ids))
            cursor.execute(delete_query, record_ids)
            self.conn.commit()
