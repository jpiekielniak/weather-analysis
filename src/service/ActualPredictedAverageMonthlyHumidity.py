import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import itertools
import matplotlib.dates as mdates


class ActualPredictedAverageMonthlyHumidity:
    def __init__(self, latitude, longitude, start_date, end_date):
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.actual_humidity_label = 'Actual Monthly Humidity (%)'
        self.predicted_humidity_label = 'Predicted Monthly Humidity (%)'

    def fetch_humidity_data(self):
        url = f"https://archive-api.open-meteo.com/v1/era5?latitude={self.latitude}&longitude={self.longitude}&start_date={self.start_date}&end_date={self.end_date}&hourly=relative_humidity_2m"
        response = requests.get(url)
        data = response.json()

        timestamps = data['hourly']['time']
        humidity = data['hourly']['relative_humidity_2m']

        df = pd.DataFrame({
            'Timestamp': pd.to_datetime(timestamps),
            'Humidity': humidity
        })

        df.set_index('Timestamp', inplace=True)
        return df

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

    def generate_predicted_data(self, actual_data):
        monthly_avg_humidity = actual_data.resample('M').mean()

        model_fit = self.fit_sarima_model(monthly_avg_humidity['Humidity'])

        forecast_steps = 12
        forecast = model_fit.get_forecast(steps=forecast_steps)
        forecast_index = pd.date_range(start=monthly_avg_humidity.index[-1] + pd.DateOffset(months=1), periods=forecast_steps,
                                       freq='M')
        predicted_humidity = pd.Series(forecast.predicted_mean, index=forecast_index)

        predicted_df = pd.concat([monthly_avg_humidity, predicted_humidity], axis=0)
        predicted_df.columns = ['Actual Humidity', 'Predicted Humidity']
        return predicted_df

    def plot_humidity_histogram(self):
        df_actual = self.fetch_humidity_data()
        df_predicted = self.generate_predicted_data(df_actual)

        figure, ax = plt.subplots(figsize=(14, 8))

        width = 0.4
        x = np.arange(len(df_predicted.index))

        ax.bar(x[:len(df_actual.resample('M').mean().index)] - width / 2,
               df_actual.resample('M').mean()['Humidity'],
               width=width, edgecolor='black', label=self.actual_humidity_label, alpha=0.6, color='blue')

        ax.bar(x[len(df_actual.resample('M').mean().index):] + width / 2,
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
