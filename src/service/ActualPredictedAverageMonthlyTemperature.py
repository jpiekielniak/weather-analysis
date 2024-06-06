import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np
import matplotlib.dates as mdates


class ActualPredictedAverageMonthlyTemperature:

    def __init__(self, latitude, longitude, start_date, end_date):
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.actual_temperatures = 'Actual Average Monthly Temperature (2m)'
        self.predicted_temperatures = 'Predicted Average Monthly Temperature (2m)'

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

    def plot_temperature(self):
        df_full = self.fetch_temperature_data()

        monthly_avg = df_full.resample('M').mean()
        predicted_temperatures = monthly_avg['Temperature'].rolling(window=12, min_periods=1).mean()

        def interpolate_data(dates, values):
            x = np.arange(len(dates))
            y = values
            spline = make_interp_spline(x, y, k=3)
            x_new = np.linspace(x.min(), x.max(), 300)
            y_new = spline(x_new)
            dates_new = pd.date_range(start=dates.min(), end=dates.max(), periods=300)
            return dates_new, y_new

        dates_new, actual_temps_smooth = interpolate_data(monthly_avg.index, monthly_avg['Temperature'])
        _, predicted_temps_smooth = interpolate_data(monthly_avg.index, predicted_temperatures)

        figure, ax = plt.subplots(figsize=(14, 10))

        ax.plot(dates_new, actual_temps_smooth, color='black', label=self.actual_temperatures)
        ax.plot(dates_new, predicted_temps_smooth, color='green', label=self.predicted_temperatures,
                linestyle='--')

        ax.legend([self.actual_temperatures, self.predicted_temperatures],
                  loc='upper left',
                  fontsize='small',
                  handlelength=0.3,
                  handletextpad=0.2,
                  labelspacing=0.2,
                  shadow=True
                  )

        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%B'))

        ax.text(0.5, -0.1, 'Month', ha='center', va='center', transform=ax.transAxes)

        ax.set_title(f'Actual vs Predicted Average Monthly Temperature in Tarnów ({datetime.datetime.strptime(self.start_date, "%Y-%m-%d").date().year})')
        ax.set_xlabel('')
        ax.set_ylabel('Temperature (°C)')
        plt.tight_layout(rect=[0, 0, 1, 0.95])

        return figure
