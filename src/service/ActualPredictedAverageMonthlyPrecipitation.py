import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class ActualPredictedAverageMonthlyPrecipitation:

    def __init__(self, latitude, longitude, start_date, end_date):
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.actual_precipitation_label = 'Actual Monthly Precipitation (mm)'
        self.predicted_precipitation_label = 'Predicted Monthly Precipitation (mm)'

    def fetch_rainfall_data(self):
        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={self.latitude}&longitude={self.longitude}&start_date={self.start_date}&end_date={self.end_date}&hourly=precipitation&daily=precipitation_sum"
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

    def generate_predicted_data(self, actual_data):
        window_size = 7
        predicted_precipitation = actual_data['Precipitation'].rolling(window=window_size, min_periods=1).mean()
        predicted_df = actual_data.copy()
        predicted_df['Precipitation'] = predicted_precipitation
        return predicted_df

    def plot_rainfall_histogram(self):
        df_actual = self.fetch_rainfall_data()
        df_predicted = self.generate_predicted_data(df_actual)

        monthly_actual_precipitation = df_actual.resample('M').sum()
        monthly_predicted_precipitation = df_predicted.resample('M').sum()

        figure, ax = plt.subplots(figsize=(14, 8))

        width = 0.4
        x = np.arange(len(monthly_actual_precipitation.index))

        ax.bar(x - width / 2,
               monthly_actual_precipitation['Precipitation'],
               width=width, edgecolor='black', label=self.actual_precipitation_label, alpha=0.6, color='red')

        ax.bar(x + width / 2,
               monthly_predicted_precipitation['Precipitation'],
               width=width, edgecolor='black', label=self.predicted_precipitation_label, alpha=0.6, color='green')

        ax.set_title('Histogram of Actual and Predicted Monthly Precipitation')
        ax.set_xlabel('Date')
        ax.set_ylabel('Monthly Precipitation (mm)')
        ax.set_xticks(ticks=x)
        ax.set_xticklabels([date.strftime('%Y-%m') for date in monthly_actual_precipitation.index], rotation=45)
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        return figure