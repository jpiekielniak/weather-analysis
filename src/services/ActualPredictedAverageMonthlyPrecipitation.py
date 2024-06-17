import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.services.api.WeatherDataFetcher import WeatherDataFetcher
from src.services.helpers.DateHelper import DateHelper
from src.services.models.SarimaxForecaster import SARIMAXForecaster


class ActualPredictedAverageMonthlyPrecipitation(SARIMAXForecaster, WeatherDataFetcher, DateHelper):

    def __init__(self, latitude, longitude, start_date, end_date):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.actual_precipitation_label = 'Actual Monthly Precipitation (mm)'
        self.predicted_precipitation_label = 'Predicted Monthly Precipitation (mm)'

    def generate_predicted_data(self, actual_data):
        return self.generate_predicted_data_generic(
            actual_data=actual_data,
            fetch_data_func=self.fetch_rainfall_data,
            value_column_name='Precipitation',
            start_date=self.start_date,
            end_date=self.end_date
        )

    def plot_rainfall_histogram(self):
        df_actual = self.fetch_rainfall_data(self.start_date, self.end_date)
        df_predicted = self.generate_predicted_data(df_actual)

        df_combined = self.combine_actual_predicted(df_actual, df_predicted, 'Precipitation')

        figure, ax = plt.subplots(figsize=(14, 8))

        width = 0.4
        x = np.arange(len(df_combined.index))

        ax.bar(x - width / 2,
               df_combined['Actual Precipitation'],
               width=width, edgecolor='black', label=self.actual_precipitation_label, alpha=0.6, color='red')

        ax.bar(x + width / 2,
               df_predicted,
               width=width, edgecolor='black', label=self.predicted_precipitation_label, alpha=0.6, color='green')

        ax.set_title('Histogram of Actual and Predicted Monthly Precipitation')
        ax.set_xlabel('Date')
        ax.set_ylabel('Monthly Precipitation (mm)')
        ax.set_xticks(ticks=x)
        ax.set_xticklabels([date.strftime('%Y-%m') for date in df_combined.index], rotation=45)
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        return figure

    def combine_actual_predicted(self, actual_data, predicted_data, value_column_name):
        actual_monthly_sum = actual_data.resample('M').sum()
        df_combined = pd.concat([actual_monthly_sum[value_column_name], predicted_data], axis=1)
        df_combined.columns = [f'Actual {value_column_name}', f'Predicted {value_column_name}']
        df_combined = df_combined[self.start_date:self.end_date]
        return df_combined
