import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from src.services.api.WeatherDataFetcher import WeatherDataFetcher
from src.services.helpers.DateHelper import DateHelper
from src.services.models.SarimaxForecaster import SARIMAXForecaster


class ActualPredictedAverageMonthlyTemperature(SARIMAXForecaster, WeatherDataFetcher, DateHelper):

    def __init__(self, latitude, longitude, start_date, end_date):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.actual_temperatures = 'Actual Average Monthly Temperature (°C)'
        self.predicted_temperatures = 'Predicted Average Monthly Temperature (°C)'

    def plot_temperature(self):
        extended_start_date = self.get_extended_start_date(self.start_date)

        df_full = self.fetch_temperature_data(extended_start_date, self.end_date)
        monthly_avg = df_full.resample('M').mean()

        actual_start_date = self.start_date
        actual_df = self.fetch_temperature_data(actual_start_date, self.end_date)
        actual_monthly_avg = actual_df.resample('M').mean()

        if len(monthly_avg) < 2:
            raise ValueError("Not enough data to fit SARIMA model. Please provide more data.")

        model_fit = self.fit_sarima_model(monthly_avg['Temperature'])

        start_date = actual_monthly_avg.index[-1] + pd.DateOffset(months=1)
        predicted_temperatures = self.forecast(model_fit=model_fit, start_date=start_date)

        combined_df = pd.concat([actual_monthly_avg, predicted_temperatures], axis=1)
        combined_df.columns = ['Actual Temperature', 'Predicted Temperature']

        figure, ax = plt.subplots(figsize=(14, 10))

        ax.plot(combined_df.index, combined_df['Actual Temperature'], color='black', marker='o',
                label=self.actual_temperatures)
        ax.plot(combined_df.index, combined_df['Predicted Temperature'], color='green', marker='x', linestyle='--',
                label=self.predicted_temperatures)

        ax.legend(loc='upper left', fontsize='small', handlelength=0.3, handletextpad=0.2, labelspacing=0.2,
                  shadow=True)

        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

        for label in ax.get_xticklabels():
            label.set_rotation(45)
            label.set_horizontalalignment('right')

        ax.text(0.5, -0.1, 'Month', ha='center', va='center', transform=ax.transAxes)

        ax.set_title(
            f'Actual vs Predicted Average Monthly Temperature ({datetime.datetime.strptime(self.start_date, "%Y-%m-%d").date().year})')
        ax.set_xlabel('')
        ax.set_ylabel('Temperature (°C)')
        plt.tight_layout(rect=(0, 0, 1, 0.95))

        return figure
