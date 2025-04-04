
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import altair as alt


class DataManager():

    TEMPERATURE = 'temperature'
    SOIL_MOISTURE = 'soil_moisture'

    def __init__(self, full_df: pd.DataFrame):
        self.__full_df = self._clean(full_df)

    def _clean(self, df: pd.DataFrame) -> pd.DataFrame:
        '''Clean the data received from the SQL query.'''
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

    def get_user_option_plant_numbers(self) -> list[str]:
        '''Extract the different plants from the dataframe, and produce
        user friendly strings to choose plants.'''
        pt = self.__full_df[['plant_number', 'plant_type']].drop_duplicates()
        pt['user_option'] = pt['plant_number'].astype(
            str) + ' - ' + pt['plant_type']
        return pt['user_option'].to_list()

    def get_botanists(self) -> list[str]:
        '''Get the list of botanist names from the full dataframe.'''
        return self.__full_df['botanist'].drop_duplicates().to_list()

    @staticmethod
    def get_plant_id_from_user_option(user_option: str) -> int:
        '''From a user option of a plant, extract the plant number'''
        return int(user_option.split(' - ')[0])

    @staticmethod
    def titlize(recording_type: str) -> str:
        '''Convert an ugly recording type string into a nice looking string.'''
        return recording_type.title().replace('_', ' ')

    def get_recordings_temperature_data(self, plant_number: int) -> pd.DataFrame:
        '''Reformat the data into a format ready for visualising temperature 
        data in the recordings chart.'''
        temp_df = self.__full_df[self.__full_df['plant_number'] == plant_number][[
            'timestamp', 'temperature', f'is_anomalous_temperature']].copy()
        temp_df = temp_df[temp_df['timestamp'] >
                          datetime.now() - timedelta(hours=12)].copy()
        return temp_df

    def get_last_watered_data(self, botanist: str) -> pd.DataFrame:
        '''Reformat the data into a format ready for visualisation in the last watered chart.'''
        lw_df = self.__full_df[self.__full_df['botanist'] == botanist].copy()
        lw_df = lw_df[['plant_number', 'last_watered']].drop_duplicates()
        lw_df["now"] = pd.Timestamp.now()
        lw_df["hours_since"] = round((lw_df['now'] - lw_df['last_watered']
                                      ).dt.total_seconds() / 3600, 2)
        return lw_df


class RecordingChart():

    def __init__(self, data_manager: DataManager):
        self.__dm = data_manager

    def _get_widget_inputs(self) -> tuple[str]:
        '''Get user inputs from the widgets.'''
        left_column, right_column = st.columns(2)
        with left_column:
            user_plant_option = st.selectbox(
                "Plant No.", self.__dm.get_user_option_plant_numbers()
            )
            plant_number = DataManager.get_plant_id_from_user_option(
                user_plant_option)
        with right_column:
            recording_type = st.radio(
                "Recording type",
                [self.__dm.TEMPERATURE, self.__dm.SOIL_MOISTURE],
                format_func=DataManager.titlize
            )
        return plant_number, recording_type

    def _show_temperature_chart(self, plant_number: int) -> None:
        '''Show the temperature chart.'''
        df = self.__dm.get_recordings_temperature_data(plant_number)
        df_normal = df[~df["is_anomalous_temperature"]]
        df_anomalies = df[df["is_anomalous_temperature"]]
        line_chart = alt.Chart(df_normal).mark_line(point=True).encode(
            x="timestamp:T",
            y="temperature:Q",
            tooltip=["timestamp", "temperature"]
        )
        anomaly_lines = alt.Chart(df_anomalies).mark_rule(color="red").encode(
            x="timestamp:T"
        )
        final_chart = line_chart + anomaly_lines
        st.altair_chart(final_chart, use_container_width=True)

    def show(self):
        '''Show the entire chart, with necessary widgets.'''
        plant_number, recording_type = self._get_widget_inputs()
        if recording_type == DataManager.TEMPERATURE:
            self._show_temperature_chart(plant_number)


class LastWateredChart():

    def __init__(self, data_manager: DataManager):
        self.__dm = data_manager

    def _get_widget_inputs(self) -> str:
        '''Get user inputs from the widgets.'''
        left_column, _ = st.columns(2)
        with left_column:
            botanist = st.selectbox(
                "Botanist", self.__dm.get_botanists()
            )
        return botanist

    def _show_last_watered_chart(self, botanist: str) -> None:
        df = self.__dm.get_last_watered_data(botanist)
        chart = (
            alt.Chart(df)
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

    def show(self):
        '''Entire process for showing recordings graph.'''
        botanist = self._get_widget_inputs()
        self._show_last_watered_chart(botanist)

# @st.dialog("Anomalies Detected")
# def alert():
#     st.write("ALERT!")


# def detect_issues(df: pd.DataFrame):
#     '''Entire process for alerts. Find any extreme readings from plants which should be addressed.'''
#     # Compute IQR per plant
#     pass
