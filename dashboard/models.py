
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import altair as alt


class DataManager():

    TEMPERATURE = 'temperature'
    SOIL_MOISTURE = 'soil_moisture'

    def __init__(self, full_df: pd.DataFrame):
        self.__full_df = self._clean(full_df)

    @staticmethod
    def mad_outlier_detection(group, column: str, threshold=3.5):
        '''Identifies outliers in a group using the MAD method.'''
        median = np.median(group[column])
        mad = np.median(np.abs(group[column] - median))
        # Avoid division by zero
        if mad == 0:
            group[f'is_anomalous_{column}'] = False
            return group
        modified_z_score = 0.6745 * (group[column] - median) / mad
        group[f'is_anomalous_{column}'] = np.abs(modified_z_score) > threshold
        return group

    @staticmethod
    def find_percentile_values(group, column: str):
        """
        Finds values in the bottom 10% and top 10% among non-outliers.
        """
        non_outliers = group[~group[f'is_anomalous_{column}']].copy()
        if len(non_outliers) < 2:  # Avoid issues with small groups
            group[f'is_extreme_{column}'] = False
            return group
        lower_bound = np.percentile(non_outliers[column], 5)
        upper_bound = np.percentile(non_outliers[column], 95)
        group[f'is_extreme_{column}'] = (group[column] >= upper_bound) | (
            group[column] <= lower_bound)
        return group

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
        # Find anomalies
        df = df.groupby('plant_number', group_keys=False).apply(
            DataManager.mad_outlier_detection, column='temperature')
        df = df.groupby('plant_number', group_keys=False).apply(
            DataManager.find_percentile_values, column='temperature')
        # st.write(df)
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

    def get_recordings_temperature_data(self, plant_number: int, time_frame: int) -> pd.DataFrame:
        '''Reformat the data into a format ready for visualising temperature 
        data in the recordings chart.'''
        temp_df = self.__full_df[self.__full_df['plant_number'] == plant_number][[
            'timestamp', 'temperature', 'is_anomalous_temperature', 'is_extreme_temperature']].copy()
        temp_df = temp_df[temp_df['timestamp'] >
                          datetime.now() - timedelta(hours=time_frame)].copy()
        return temp_df

    def get_recordings_soil_moisture_data(self, plant_number: int, time_frame: int) -> pd.DataFrame:
        '''Reformat the data into a format ready for visualising soil moisture 
        data in the recordings chart.'''
        sm_df = self.__full_df[self.__full_df['plant_number'] == plant_number][[
            'timestamp', 'soil_moisture']].copy()
        sm_df = sm_df[sm_df['timestamp'] >
                      datetime.now() - timedelta(hours=time_frame)].copy()
        return sm_df

    def get_last_watered_data(self, botanist: str) -> pd.DataFrame:
        '''Reformat the data into a format ready for visualisation in the last watered chart.'''
        lw_df = self.__full_df[self.__full_df['botanist'] == botanist].copy()
        lw_df = lw_df[['plant_number', 'last_watered']].drop_duplicates()
        lw_df["now"] = pd.Timestamp.now()
        lw_df["hours_since"] = round((lw_df['now'] - lw_df['last_watered']
                                      ).dt.total_seconds() / 3600, 2)
        return lw_df

    def get_alerts_data(self) -> pd.DataFrame:
        '''Create the table shown on the alerts page.'''
        # Find the most recent row for each plant
        latest_rows = self.__full_df.loc[self.__full_df.groupby('plant_number')[
            'timestamp'].idxmax()]
        # Determine whether watering is needed (using alert emoji)
        latest_rows["Needs Watering"] = latest_rows['soil_moisture'].apply(
            lambda x: '💧' if x < 30 else '')
        # Extreme temperature detection (using alert emoji)
        latest_rows["Extreme Temp. Detected"] = latest_rows['is_extreme_temperature'].apply(
            lambda x: '⚠️' if x else '')
        # Select relevant columns and rename for clarity
        latest_rows = latest_rows[['plant_number', 'plant_type',
                                   'Needs Watering', 'Extreme Temp. Detected']]
        latest_rows = latest_rows.rename(columns={
            'plant_number': 'Plant No.',
            'plant_type': 'Name',
        })
        latest_rows.set_index('Plant No.', inplace=True)
        return latest_rows


class RecordingChart():

    def __init__(self, data_manager: DataManager):
        self.__dm = data_manager

    def _get_widget_inputs(self) -> tuple[str]:
        '''Get user inputs from the widgets.'''
        left_column, mid_column, right_column = st.columns(3)
        with left_column:
            user_plant_option = st.selectbox(
                "Plant No.", self.__dm.get_user_option_plant_numbers()
            )
            plant_number = DataManager.get_plant_id_from_user_option(
                user_plant_option)
        with mid_column:
            recording_type = st.radio(
                "Recording type",
                [self.__dm.TEMPERATURE, self.__dm.SOIL_MOISTURE],
                format_func=DataManager.titlize
            )
        with right_column:
            time_frame = st.slider(
                label="Time frame",
                min_value=1,
                max_value=24,
                step=1,
                value=12
            )
        return plant_number, recording_type, time_frame

    def _show_temperature_chart(self, plant_number: int, time_frame: int) -> None:
        '''Show the temperature chart.'''
        # Organise dataframe
        df = self.__dm.get_recordings_temperature_data(
            plant_number, time_frame)
        # Separate anomalies from normal points
        df_normal = df[~df["is_anomalous_temperature"]].copy()
        df_anomalies = df[df["is_anomalous_temperature"]]
        # Get temperature limits
        padding = 0.005
        min_temp = df_normal['temperature'].min()
        max_temp = df_normal['temperature'].max()
        temp_diff = max_temp - min_temp
        min_scale = min_temp - temp_diff * (1 - padding)
        max_scale = max_temp + temp_diff * (1 + padding)
        # Base line chart for normal points
        line_chart = alt.Chart(df_normal).mark_line().encode(
            x="timestamp:T",
            y=alt.Y("temperature:Q").scale(domain=(min_scale, max_scale))
        )
        # Add points, coloring extreme values
        points = alt.Chart(df_normal).mark_point(size=60).encode(
            x=alt.X("timestamp:T", title="Time"),
            y=alt.Y("temperature:Q", title="Temperature (°C)"),
            color=alt.condition(
                alt.datum.is_extreme_temperature,
                alt.value("red"),
                alt.value("steelblue")
            ),
            tooltip=["timestamp", "temperature"]
        )
        # Anomaly vertical lines
        anomaly_lines = alt.Chart(df_anomalies).mark_rule(
            color="red",
            strokeWidth=0.5,
        ).encode(
            x="timestamp:T"
        )
        # Combine everything
        final_chart = line_chart + points + anomaly_lines
        st.altair_chart(final_chart, use_container_width=True)

    def _show_temperature_info(self):
        st.info(
            'Red horizontal lines refer to anomalous temperature readings.', icon="🔺")
        st.info(
            "Red points refer to 'extreme' readings, in the top and bottom 5% percentile.", icon="🔴")
        st.info(
            "Blue points are 'normal' temperature readings.", icon="🔵")

    def _show_soil_moisture_chart(self, plant_number: int, time_frame: int) -> None:
        '''Show the soil moisture chart.'''
        df = self.__dm.get_recordings_soil_moisture_data(
            plant_number, time_frame)
        line_chart = alt.Chart(df).mark_line(point=True).encode(
            x=alt.X("timestamp:T", title="Time"),
            y=alt.Y("soil_moisture:Q", title="Soil Moisture (%)"),
            tooltip=["timestamp", "soil_moisture"]
        )
        st.altair_chart(line_chart, use_container_width=True)

    def show(self):
        '''Show the entire chart, with necessary widgets.'''
        plant_number, recording_type, time_frame = self._get_widget_inputs()
        if recording_type == DataManager.TEMPERATURE:
            self._show_temperature_chart(plant_number, time_frame)
            self._show_temperature_info()
        else:
            self._show_soil_moisture_chart(plant_number, time_frame)


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
        # Create the chart with circles and lines
        chart = (
            alt.Chart(df)
            .mark_point(filled=True)  # Use points (circles)
            .encode(
                x=alt.X("last_watered:T", title="Last Watered Time"),
                y=alt.Y("plant_number:O", title="Plant No."),
                color=alt.Color("hours_since:Q", scale=alt.Scale(
                    scheme="redyellowgreen", reverse=True), title="Hours since"),
                size=alt.Size("hours_since:Q",
                              scale=alt.Scale(range=[100, 300]), legend=None)
            )
            + alt.Chart(df)
            .mark_rule(strokeWidth=2)  # Use horizontal lines
            .encode(
                # The starting point of the line (time of last watered)
                x="last_watered:T",
                x2="now:T",  # The ending point (now)
                y=alt.Y("plant_number:O"),
                color=alt.Color("hours_since:Q", scale=alt.Scale(
                    scheme="redyellowgreen", reverse=True), title="Hours since")
            )
        )
        # Display the chart
        st.altair_chart(chart, use_container_width=True)

    def show(self):
        '''Entire process for showing recordings graph.'''
        botanist = self._get_widget_inputs()
        self._show_last_watered_chart(botanist)


class AlertsChart():

    def __init__(self, data_manager: DataManager):
        self.__dm = data_manager

    def _show_alert_info(self):
        st.info(
            'A plant needs watering is soil moisture is below 30%.', icon="💧")
        st.info(
            'Extreme temperatures are above or below the 5% percentile for each plant.', icon="⚠️")

    def show(self):
        '''Entire process for showing the alerts graph.'''
        self._show_alert_info()
        st.table(self.__dm.get_alerts_data())
