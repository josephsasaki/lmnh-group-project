
from os import environ as ENV
import pymssql
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from models import DataManager, RecordingChart, LastWateredChart


DASHBOARD_TITLE = 'LMNH Dashboard'
RECORD_QUERY = '''
    SELECT 
        p.plant_number,
        pt.plant_type_name,
        r.record_soil_moisture,
        r.record_temperature,
        r.record_timestamp,
        p.plant_last_watered,
        b.botanist_name,
        con.continent_name
    FROM record AS r
    JOIN plant AS p ON p.plant_id = r.plant_id
    JOIN plant_type AS pt ON pt.plant_type_id = p.plant_type_id
    JOIN botanist AS b ON b.botanist_id = p.botanist_id
    JOIN city AS cit ON cit.city_id = p.city_id
    JOIN country AS cou ON cou.country_id = cit.country_id
    JOIN continent AS con ON con.continent_id = cou.continent_id
'''


@st.cache_resource
def init_connection() -> pymssql.Connection:
    '''Establish connection to the RDS.'''
    load_dotenv()
    return pymssql.connect(
        server=ENV['DB_HOST'],
        user=ENV['DB_USERNAME'],
        password=ENV['DB_PASSWORD'],
        database=ENV['DB_NAME'],
        port=ENV['DB_PORT']
    )


@st.cache_data(ttl=600)
def run_query(query, _connection: pymssql.Connection) -> pd.DataFrame:
    '''Using the connection, load the required data into a dataframe.'''
    with _connection.cursor(as_dict=True) as cursor:
        cursor.execute(query)
        return pd.DataFrame(cursor.fetchall())


def main():
    '''The main function from which the dashboard is run.'''
    st.title(DASHBOARD_TITLE)
    connection = init_connection()
    dm = DataManager(full_df=run_query(RECORD_QUERY, connection))

    tab1, tab2 = st.tabs(["Recordings", "Last Watered"])
    with tab1:
        RecordingChart(dm).show()
    with tab2:
        LastWateredChart(dm).show()


if __name__ == "__main__":
    main()
