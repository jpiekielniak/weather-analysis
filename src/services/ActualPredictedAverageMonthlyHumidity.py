import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.services.api.WeatherDataFetcher import WeatherDataFetcher
from src.services.helpers.DateHelper import DateHelper
from src.services.models.SarimaxForecaster import SARIMAXForecaster


class ActualPredictedAverageMonthlyHumidity(SARIMAXForecaster, WeatherDataFetcher, DateHelper):
    def __init__(self, latitude, longitude, start_date, end_date):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.actual_humidity_label = 'Actual Monthly Humidity (%)'
        self.predicted_humidity_label = 'Predicted Monthly Humidity (%)'

    def generate_predicted_data(self):
        return self.generate_predicted_data_generic(
            fetch_data_func=self.fetch_humidity_data,
            value_column_name='Humidity',
            start_date=self.start_date,
            end_date=self.end_date
        )

    def plot_humidity_histogram(self):
        df_actual = self.fetch_humidity_data(self.start_date, self.end_date)
        df_predicted = self.generate_predicted_data()

        df_combined = self.combine_actual_predicted(df_actual, df_predicted, 'Humidity')

        print("Combined DataFrame:\n", df_combined)

        figure, ax = plt.subplots(figsize=(14, 8))

        width = 0.4
        x = np.arange(len(df_combined.index))

        ax.bar(x - width / 2,
               df_combined['Actual Humidity'],
               width=width, edgecolor='black', label=self.actual_humidity_label, alpha=0.6, color='red')

        ax.bar(x + width / 2,
               df_combined['Predicted Humidity'],
               width=width, edgecolor='black', label=self.predicted_humidity_label, alpha=0.6, color='green')

        ax.set_title('Histogram of Actual and Predicted Monthly Humidity')
        ax.set_xlabel('Date')
        ax.set_ylabel('Monthly Humidity (%)')
        ax.set_xticks(ticks=x)
        ax.set_xticklabels([date.strftime('%Y-%m') for date in df_combined.index], rotation=45)
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        return figure

    def combine_actual_predicted(self, actual_data, predicted_data, value_column_name):
        actual_monthly_avg = actual_data.resample('M').mean()
        predicted_monthly_avg = pd.DataFrame(predicted_data, columns=[f'Predicted {value_column_name}'])

        # Debugging: Print actual and predicted data to ensure they are correctly processed
        print("Actual Monthly Average:\n", actual_monthly_avg)
        print("Predicted Monthly Average:\n", predicted_monthly_avg)

        df_combined = pd.concat([actual_monthly_avg[value_column_name], predicted_monthly_avg], axis=1)
        df_combined.columns = [f'Actual {value_column_name}', f'Predicted {value_column_name}']
        df_combined = df_combined[self.start_date:self.end_date]
        return df_combined
