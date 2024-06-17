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
        extended_start_date = self.get_extended_start_date(self.start_date)

        extended_data = self.fetch_wind_speed_data(extended_start_date, self.end_date)
        monthly_avg_wind_speed = extended_data.resample('M').mean()

        model_fit = self.fit_sarima_model(monthly_avg_wind_speed['WindSpeed'])
        actual_monthly_avg_wind_speed = actual_data.resample('M').mean()

        start_date = actual_monthly_avg_wind_speed.index[-1] + pd.DateOffset(months=1)
        predicted_wind_speed = self.forecast(model_fit=model_fit, start_date=start_date)

        predicted_df = pd.concat([actual_monthly_avg_wind_speed, predicted_wind_speed], axis=0)
        predicted_df.columns = ['Actual Wind Speed', 'Predicted Wind Speed']
        return predicted_df

    def plot_wind_speed_histogram(self):
        df_actual = self.fetch_wind_speed_data(self.start_date, self.end_date)
        df_predicted = self.generate_predicted_data(df_actual)

        figure, ax = plt.subplots(figsize=(14, 8))

        width = 0.4
        x = np.arange(len(df_predicted.index))

        actual_months = df_actual.resample('M').mean().index
        predicted_months = df_predicted.index[len(actual_months):]

        ax.bar(x[:len(actual_months)] - width / 2,
               df_actual.resample('M').mean()['WindSpeed'],
               width=width, edgecolor='black', label=self.actual_wind_speed_label, alpha=0.6, color='darkgreen')

        ax.bar(x[len(actual_months):] + width / 2,
               df_predicted['Predicted Wind Speed'].dropna(),
               width=width, edgecolor='black', label=self.predicted_wind_speed_label, alpha=0.6, color='lime')

        ax.set_title('Histogram of Actual and Predicted Monthly Wind Speed')
        ax.set_xlabel('Date')
        ax.set_ylabel('Monthly Wind Speed (m/s)')
        ax.set_xticks(ticks=x)
        ax.set_xticklabels([date.strftime('%Y-%m') for date in df_predicted.index], rotation=45)
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        return figure
