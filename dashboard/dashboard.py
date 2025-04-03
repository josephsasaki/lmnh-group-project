
from os import environ as ENV
import pymssql
import streamlit as st
import pandas as pd
from pandas import DataFrame
import altair as alt
from dotenv import load_dotenv
from datetime import datetime, timedelta
from scipy.stats import zscore


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
TEMPERATURE = 'temperature'
SOIL_MOISTURE = 'soil_moisture'


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
        df = pd.DataFrame(cursor.fetchall())
        df.columns = [
            'plant_number',
            'plant_type',
            'soil_moisture',
            'temperature',
            'timestamp',
            'last_watered',
            'botanist',
            'continent',
        ]
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # Compute Z-scores for each plant individually
        df["soil_moisture_z_score"] = df.groupby("plant_number")["soil_moisture"].transform(
            lambda x: (x - x.mean()) / x.std())
        df["temperature_z_score"] = df.groupby("plant_number")["temperature"].transform(
            lambda x: (x - x.mean()) / x.std())
        # Mark anomalies
        df["is_anomalous_soil_moisture"] = (
            df["soil_moisture_z_score"].abs() > 3)
        df["is_anomalous_temperature"] = (
            df["temperature_z_score"].abs() > 0.8)
        return df


def titlize(recording_type: str):
    '''Convert an ugly recording type string into a nice looking string.'''
    return recording_type.title().replace('_', ' ')


def get_user_option_plant_numbers(data: pd.DataFrame) -> list[str]:
    '''Extract the different plants from the dataframe, and produce
    user friendly strings to choose plants.'''
    pt = data[['plant_number', 'plant_type']].drop_duplicates()
    pt['user_option'] = pt['plant_number'].astype(
        str) + ' - ' + pt['plant_type']
    return pt['user_option'].to_list()


def get_plant_id_from_user_option(user_option: str) -> int:
    '''From a user option of a plant, extract the plant number'''
    return int(user_option.split(' - ')[0])


def get_botanists(data: pd.DataFrame) -> list[str]:
    '''Get the list of botanist names from the full dataframe.'''
    return data['botanist'].drop_duplicates().to_list()


def recordings_widgets(data: pd.DataFrame):
    '''Get user inputs from the widgets.'''
    left_column, right_column = st.columns(2)
    with left_column:
        user_plant_option = st.selectbox(
            "Plant No.", get_user_option_plant_numbers(data)
        )
        plant_number = get_plant_id_from_user_option(user_plant_option)
    with right_column:
        recording_type = st.radio(
            "Recording type",
            [TEMPERATURE, SOIL_MOISTURE],
            format_func=titlize
        )
    return plant_number, recording_type


def recordings_transform(df: pd.DataFrame, plant_number: int, recording_type: str) -> pd.DataFrame:
    '''Reformat the data into a format ready for visualisation in the recordings graph.'''
    df = df[df['plant_number'] == plant_number][[
        'timestamp', recording_type, f'is_anomalous_{recording_type}']].copy()
    df = df[df['timestamp'] > datetime.now() - timedelta(hours=12)].copy()
    return df


def recordings_chart(data: pd.DataFrame, plant_number: int, recording_type: str):
    '''Produce the chart for recordings.'''
    if recording_type == TEMPERATURE:
        df_normal = data[~data["is_anomalous_temperature"]]
        df_anomalies = data[data["is_anomalous_temperature"]]
        line_chart = alt.Chart(df_normal).mark_line().encode(
            x="timestamp:T",
            y="temperature:Q",
            tooltip=["timestamp", "temperature"]
        )
        anomaly_lines = alt.Chart(df_anomalies).mark_rule(color="red").encode(
            x="timestamp:T"
        )
        final_chart = line_chart + anomaly_lines
        # Display in Streamlit
        st.altair_chart(final_chart, use_container_width=True)


def recordings(data: pd.DataFrame):
    '''Entire process for showing recordings graph.'''
    plant_number, recording_type = recordings_widgets(data)
    data = recordings_transform(data, plant_number, recording_type)
    recordings_chart(data, plant_number, recording_type)


def last_watered_widgets(data: pd.DataFrame):
    '''Get user inputs from the widgets.'''
    left_column, right_column = st.columns(2)
    with left_column:
        botanist = st.selectbox(
            "Botanist", get_botanists(data)
        )
    with right_column:
        pass
    return botanist, None


def last_watered_transform(df: pd.DataFrame, botanist: str) -> pd.DataFrame:
    '''Reformat the data into a format ready for visualisation in the last watered graph.'''
    df = df[df['botanist'] == botanist].copy()
    df = df[['plant_number', 'last_watered']].drop_duplicates()
    df["now"] = pd.Timestamp.now()
    df["hours_since"] = round((df['now'] - df['last_watered']
                               ).dt.total_seconds() / 3600, 2)
    return df


def last_watered_chart(data: pd.DataFrame):
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("last_watered:T", title="Last Watered Time"),
            x2="now:T",  # Bars extend to "now"
            y=alt.Y("plant_number:O", title="Plant No."),
            color=alt.Color("hours_since:Q", scale=alt.Scale(
                scheme="redyellowgreen", reverse=True), title="Hours since")
        )
    )
    st.altair_chart(chart, use_container_width=True)


def last_watered(data: pd.DataFrame):
    '''Entire process for showing recordings graph.'''
    botanist, _ = last_watered_widgets(data)
    data = last_watered_transform(data, botanist)
    last_watered_chart(data)


@st.dialog("Anomalies Detected")
def alert():
    st.write("ALERT!")


def detect_issues(df: pd.DataFrame):
    '''Entire process for alerts. Find any extreme readings from plants which should be addressed.'''
    # Compute IQR per plant
    Q1 = df.groupby("plant_number")["temperature"].transform(
        lambda x: x.quantile(0.25))
    Q3 = df.groupby("plant_number")["temperature"].transform(
        lambda x: x.quantile(0.75))
    IQR = Q3 - Q1
    # Define anomaly thresholds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    # Mark anomalies
    df["is_anomalous"] = (df["temperature"] < lower_bound) | (
        df["temperature"] > upper_bound)
    df_anomalies = df[df["is_anomalous"]]
    st.write(df_anomalies)


def main():
    '''The main function from which the dashboard is run.'''
    st.title(DASHBOARD_TITLE)
    connection = init_connection()
    data = run_query(RECORD_QUERY, connection)
    tab1, tab2 = st.tabs(["Recordings", "Last Watered"])
    with tab1:
        recordings(data)
    with tab2:
        last_watered(data)
    # detect_issues(data)


if __name__ == "__main__":
    main()
