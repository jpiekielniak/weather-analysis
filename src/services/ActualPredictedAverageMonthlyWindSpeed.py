import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.services.api.WeatherDataFetcher import WeatherDataFetcher
from src.services.helpers.DateHelper import DateHelper
from src.services.models.SarimaxForecaster import SARIMAXForecaster


class ActualPredictedAverageMonthlyWindSpeed(SARIMAXForecaster, WeatherDataFetcher, DateHelper):
    def __init__(self, latitude, longitude, start_date, end_date):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.actual_wind_speed_label = 'Actual Monthly Wind Speed (m/s)'
        self.predicted_wind_speed_label = 'Predicted Monthly Wind Speed (m/s)'

    def generate_predicted_data(self, actual_data):
        return self.generate_predicted_data_generic(
            actual_data=actual_data,
            fetch_data_func=self.fetch_wind_speed_data,
            value_column_name='WindSpeed',
            start_date=self.start_date,
            end_date=self.end_date
        )

    def plot_wind_speed_histogram(self):
        df_actual = self.fetch_wind_speed_data(self.start_date, self.end_date)
        combined_df = self.generate_predicted_data(df_actual)

        figure, ax = plt.subplots(figsize=(14, 8))

        width = 0.4
        x = np.arange(len(combined_df.index))

        actual_months = df_actual.resample('M').mean().index
        predicted_months = combined_df.index[len(actual_months):]

        ax.bar(x[:len(actual_months)] - width / 2,
               combined_df['Actual WindSpeed'].dropna(),
               width=width, edgecolor='black', label=self.actual_wind_speed_label, alpha=0.6, color='darkgreen')

        ax.bar(x[len(actual_months):] + width / 2,
               combined_df['Predicted WindSpeed'].dropna(),
               width=width, edgecolor='black', label=self.predicted_wind_speed_label, alpha=0.6, color='lime')

        ax.set_title('Histogram of Actual and Predicted Monthly Wind Speed')
        ax.set_xlabel('Date')
        ax.set_ylabel('Monthly Wind Speed (m/s)')
        ax.set_xticks(ticks=x)
        ax.set_xticklabels([date.strftime('%Y-%m') for date in combined_df.index], rotation=45)
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        return figure
