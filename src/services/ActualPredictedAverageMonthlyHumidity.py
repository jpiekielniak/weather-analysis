import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

    def generate_predicted_data(self, actual_data):
        extended_start_date = self.get_extended_start_date(self.start_date)

        extended_data = self.fetch_humidity_data(extended_start_date, self.end_date)
        monthly_avg_humidity = extended_data.resample('M').mean()

        model_fit = self.fit_sarima_model(monthly_avg_humidity['Humidity'])

        start_date = monthly_avg_humidity.index[-1] + pd.DateOffset(months=1)
        predicted_humidity = self.forecast(model_fit=model_fit, start_date=start_date)

        actual_monthly_avg_humidity = actual_data.resample('M').mean()
        predicted_df = pd.concat([actual_monthly_avg_humidity, predicted_humidity], axis=0)
        predicted_df.columns = ['Actual Humidity', 'Predicted Humidity']
        return predicted_df

    def plot_humidity_histogram(self):
        df_actual = self.fetch_humidity_data(self.start_date, self.end_date)
        df_predicted = self.generate_predicted_data(df_actual)

        figure, ax = plt.subplots(figsize=(14, 8))

        width = 0.4
        x = np.arange(len(df_predicted.index))

        actual_monthly_avg = df_actual.resample('M').mean()

        ax.bar(x[:len(actual_monthly_avg.index)] - width / 2,
               actual_monthly_avg['Humidity'],
               width=width, edgecolor='black', label=self.actual_humidity_label, alpha=0.6, color='blue')

        ax.bar(x[len(actual_monthly_avg.index):] + width / 2,
               df_predicted['Predicted Humidity'].dropna(),
               width=width, edgecolor='black', label=self.predicted_humidity_label, alpha=0.6, color='lightblue')

        ax.set_title('Histogram of Actual and Predicted Monthly Humidity')
        ax.set_xlabel('Date')
        ax.set_ylabel('Monthly Humidity (%)')
        ax.set_xticks(ticks=x)
        ax.set_xticklabels([date.strftime('%Y-%m') for date in df_predicted.index], rotation=45)
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        return figure
