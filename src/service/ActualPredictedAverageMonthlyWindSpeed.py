import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class ActualPredictedAverageMonthlyWindSpeed:
    def __init__(self, latitude, longitude, start_date, end_date):
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.actual_wind_speed_label = 'Actual Monthly Wind Speed (m/s)'
        self.predicted_wind_speed_label = 'Predicted Monthly Wind Speed (m/s)'

    def fetch_wind_speed_data(self):
        url = f"https://archive-api.open-meteo.com/v1/era5?latitude={self.latitude}&longitude={self.longitude}&start_date={self.start_date}&end_date={self.end_date}&hourly=windspeed_10m"
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

    def generate_predicted_data(self, actual_data):
        np.random.seed(0)
        predicted_wind_speed = actual_data['WindSpeed'] * np.random.uniform(0.8, 1.2, len(actual_data))
        predicted_df = actual_data.copy()
        predicted_df['WindSpeed'] = predicted_wind_speed
        return predicted_df

    def plot_wind_speed_histogram(self):
        df_actual = self.fetch_wind_speed_data()
        df_predicted = self.generate_predicted_data(df_actual)

        monthly_actual_wind_speed = df_actual.resample('M').mean()
        monthly_predicted_wind_speed = df_predicted.resample('M').mean()

        figure, ax = plt.subplots(figsize=(14, 8))

        width = 0.4
        x = np.arange(len(monthly_actual_wind_speed.index))

        ax.bar(x - width / 2,
               monthly_actual_wind_speed['WindSpeed'],
               width=width, edgecolor='black', label=self.actual_wind_speed_label, alpha=0.6, color='darkgreen')

        ax.bar(x + width / 2,
               monthly_predicted_wind_speed['WindSpeed'],
               width=width, edgecolor='black', label=self.predicted_wind_speed_label, alpha=0.6, color='lime')

        ax.set_title('Histogram of Actual and Predicted Monthly Wind Speed')
        ax.set_xlabel('Date')
        ax.set_ylabel('Monthly Wind Speed (m/s)')
        ax.set_xticks(ticks=x)
        ax.set_xticklabels([date.strftime('%Y-%m') for date in monthly_actual_wind_speed.index], rotation=45)
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        return figure
