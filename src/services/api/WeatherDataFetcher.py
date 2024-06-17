import pandas as pd
import requests


class WeatherDataFetcher:

    def __init__(self):
        self.latitude = None
        self.longitude = None

    def fetch_temperature_data(self, start_date, end_date):
        url = f"https://archive-api.open-meteo.com/v1/era5?latitude={self.latitude}&longitude={self.longitude}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m"
        response = requests.get(url)
        data = response.json()

        timestamps = data['hourly']['time']
        temperatures = data['hourly']['temperature_2m']

        df = pd.DataFrame({
            'Timestamp': pd.to_datetime(timestamps),
            'Temperature': temperatures
        })

        df.set_index('Timestamp', inplace=True)
        return df

    def fetch_wind_speed_data(self, start_date, end_date):
        url = f"https://archive-api.open-meteo.com/v1/era5?latitude={self.latitude}&longitude={self.longitude}&start_date={start_date}&end_date={end_date}&hourly=windspeed_10m"
        response = requests.get(url)
        data = response.json()

        timestamps = data['hourly']['time']
        wind_speeds = data['hourly']['windspeed_10m']

        df = pd.DataFrame({
            'Timestamp': pd.to_datetime(timestamps),
            'WindSpeed': wind_speeds
        })

        df.set_index('Timestamp', inplace=True)
        return df

    def fetch_humidity_data(self, start_date, end_date):
        url = f"https://archive-api.open-meteo.com/v1/era5?latitude={self.latitude}&longitude={self.longitude}&start_date={start_date}&end_date={end_date}&hourly=relative_humidity_2m"
        response = requests.get(url)
        data = response.json()

        timestamps = data['hourly']['time']
        humidity = data['hourly']['relative_humidity_2m']

        df = pd.DataFrame({
            'Timestamp': pd.to_datetime(timestamps),
            'Humidity': humidity
        })

        df.set_index('Timestamp', inplace=True)
        return df

    def fetch_rainfall_data(self, start_date, end_date):
        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={self.latitude}&longitude={self.longitude}&start_date={start_date}&end_date={end_date}&hourly=precipitation"
        response = requests.get(url)
        data = response.json()

        timestamps = data['hourly']['time']
        precipitation = data['hourly']['precipitation']

        df = pd.DataFrame({
            'Timestamp': pd.to_datetime(timestamps),
            'Precipitation': precipitation
        })

        df.set_index('Timestamp', inplace=True)
        return df
