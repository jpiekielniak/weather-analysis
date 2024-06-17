import pandas as pd
import requests


class WeatherDataFetcher:

    def __init__(self):
        self.latitude = None
        self.longitude = None

    def fetch_weather_data(self, start_date, end_date, parameter, data_frame_column_name):
        url = f"https://archive-api.open-meteo.com/v1/era5?latitude={self.latitude}&longitude={self.longitude}&start_date={start_date}&end_date={end_date}&hourly={parameter}"
        response = requests.get(url)
        data = response.json()

        timestamps = data['hourly']['time']
        temperatures = data['hourly'][parameter]

        df = pd.DataFrame({
            'Timestamp': pd.to_datetime(timestamps),
            data_frame_column_name: temperatures
        })

        df.set_index('Timestamp', inplace=True)
        return df

    def fetch_temperature_data(self, start_date, end_date):
        return self.fetch_weather_data(
            start_date=start_date,
            end_date=end_date,
            parameter='temperature_2m',
            data_frame_column_name='Temperature'
        )

    def fetch_wind_speed_data(self, start_date, end_date):
        return self.fetch_weather_data(
            start_date=start_date,
            end_date=end_date,
            parameter='windspeed_10m',
            data_frame_column_name='WindSpeed'
        )

    def fetch_humidity_data(self, start_date, end_date):
        return self.fetch_weather_data(
            start_date=start_date,
            end_date=end_date,
            parameter='relative_humidity_2m',
            data_frame_column_name='Humidity'
        )

    def fetch_rainfall_data(self, start_date, end_date):
        return self.fetch_weather_data(
            start_date=start_date,
            end_date=end_date,
            parameter='precipitation',
            data_frame_column_name='Precipitation'
        )
