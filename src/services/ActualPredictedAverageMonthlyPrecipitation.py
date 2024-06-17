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
        extended_start_date = self.get_extended_start_date(self.start_date)

        extended_data = self.fetch_rainfall_data(extended_start_date, self.end_date)
        monthly_sum_precipitation = extended_data.resample('M').sum()

        model_fit = self.fit_sarima_model(monthly_sum_precipitation['Precipitation'])

        start_date = monthly_sum_precipitation.index[-1] + pd.DateOffset(months=1)
        predicted_precipitation = self.forecast(model_fit=model_fit, start_date=start_date)

        actual_monthly_sum_precipitation = actual_data.resample('M').sum()
        predicted_df = pd.concat([actual_monthly_sum_precipitation, predicted_precipitation], axis=0)
        predicted_df.columns = ['Actual Precipitation', 'Predicted Precipitation']
        return predicted_df

    def plot_rainfall_histogram(self):
        df_actual = self.fetch_rainfall_data(self.start_date, self.end_date)
        df_predicted = self.generate_predicted_data(df_actual)

        figure, ax = plt.subplots(figsize=(14, 8))

        width = 0.4
        x = np.arange(len(df_predicted.index))

        actual_months = df_actual.resample('M').sum().index
        predicted_months = df_predicted.index[len(actual_months):]

        ax.bar(x[:len(actual_months)] - width / 2,
               df_actual.resample('M').sum()['Precipitation'],
               width=width, edgecolor='black', label=self.actual_precipitation_label, alpha=0.6, color='red')

        ax.bar(x[len(actual_months):] + width / 2,
               df_predicted['Predicted Precipitation'].dropna(),
               width=width, edgecolor='black', label=self.predicted_precipitation_label, alpha=0.6, color='green')

        ax.set_title('Histogram of Actual and Predicted Monthly Precipitation')
        ax.set_xlabel('Date')
        ax.set_ylabel('Monthly Precipitation (mm)')
        ax.set_xticks(ticks=x)
        ax.set_xticklabels([date.strftime('%Y-%m') for date in df_predicted.index], rotation=45)
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        return figure
