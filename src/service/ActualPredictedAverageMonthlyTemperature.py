import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
import itertools


class ActualPredictedAverageMonthlyTemperature:

    def __init__(self, latitude, longitude, start_date, end_date):
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.actual_temperatures = 'Actual Average Monthly Temperature (°C)'
        self.predicted_temperatures = 'Predicted Average Monthly Temperature (°C)'

    def fetch_temperature_data(self):
        url = f"https://archive-api.open-meteo.com/v1/era5?latitude={self.latitude}&longitude={self.longitude}&start_date={self.start_date}&end_date={self.end_date}&hourly=temperature_2m"
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

    @staticmethod
    def adf_test(series):
        result = adfuller(series, autolag='AIC')
        return result[1]

    @staticmethod
    def fit_sarima_model(time_series):
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in pdq]

        best_aic = float("inf")
        best_pdq = None
        best_seasonal_pdq = None
        best_model = None

        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    temp_model = SARIMAX(time_series,
                                         order=param,
                                         seasonal_order=param_seasonal,
                                         enforce_stationarity=False,
                                         enforce_invertibility=False)
                    temp_model_fit = temp_model.fit(disp=False)
                    if temp_model_fit.aic < best_aic:
                        best_aic = temp_model_fit.aic
                        best_pdq = param
                        best_seasonal_pdq = param_seasonal
                        best_model = temp_model_fit
                except:
                    continue

        return best_model

    def plot_temperature(self):
        df_full = self.fetch_temperature_data()
        monthly_avg = df_full.resample('M').mean()

        model_fit = self.fit_sarima_model(monthly_avg['Temperature'])

        forecast_steps = 12
        forecast = model_fit.get_forecast(steps=forecast_steps)
        forecast_index = pd.date_range(start=monthly_avg.index[-1] + pd.DateOffset(months=1), periods=forecast_steps,
                                       freq='M')
        predicted_temperatures = pd.Series(forecast.predicted_mean, index=forecast_index)

        combined_df = pd.concat([monthly_avg, predicted_temperatures], axis=1)
        combined_df.columns = ['Actual Temperature', 'Predicted Temperature']

        figure, ax = plt.subplots(figsize=(14, 10))

        ax.plot(combined_df.index, combined_df['Actual Temperature'], color='black', marker='o',
                label=self.actual_temperatures)
        ax.plot(combined_df.index, combined_df['Predicted Temperature'], color='green', marker='x', linestyle='--',
                label=self.predicted_temperatures)

        ax.legend([self.actual_temperatures, self.predicted_temperatures],
                  loc='upper left',
                  fontsize='small',
                  handlelength=0.3,
                  handletextpad=0.2,
                  labelspacing=0.2,
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
        plt.tight_layout(rect=[0, 0, 1, 0.95])

        return figure
