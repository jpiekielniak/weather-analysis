import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class ActualPredictedAverageMonthlyPrecipitation:

    def __init__(self, latitude, longitude, start_date, end_date):
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.actual_precipitation_label = 'Actual Monthly Precipitation (mm)'
        self.predicted_precipitation_label = 'Predicted Monthly Precipitation (mm)'

    def fetch_rainfall_data(self):
        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={self.latitude}&longitude={self.longitude}&start_date={self.start_date}&end_date={self.end_date}&hourly=precipitation&daily=precipitation_sum"
        response = requests.get(url)
        data = response.json()

        timestamps = data['hourly']['time']
        precipitation = data['hourly']['precipitation']

        df = pd.DataFrame({
            'Timestamp': pd.to_datetime(timestamps),
            'Precipitation': precipitation
        })

        df.set_index('Timestamp', inplace=True)
        return df

    def generate_predicted_data(self, actual_data):
        # Generate dummy predicted data based on actual data
        np.random.seed(0)  # for reproducibility
        predicted_precipitation = actual_data['Precipitation'] * np.random.uniform(0.8, 1.2, len(actual_data))
        predicted_df = actual_data.copy()
        predicted_df['Precipitation'] = predicted_precipitation
        return predicted_df

    def plot_rainfall_histogram(self):
        df_actual = self.fetch_rainfall_data()
        df_predicted = self.generate_predicted_data(df_actual)

        # Resample to monthly data and sum precipitation for each month
        monthly_actual_precipitation = df_actual.resample('M').sum()
        monthly_predicted_precipitation = df_predicted.resample('M').sum()

        # Plot histogram
        plt.figure(figsize=(14, 8))

        width = 0.4  # Width of the bars
        x = np.arange(len(monthly_actual_precipitation.index))  # label locations

        plt.bar(x - width / 2,
                monthly_actual_precipitation['Precipitation'],
                width=width, edgecolor='black', label=self.actual_precipitation_label, alpha=0.6, color='red')

        plt.bar(x + width / 2,
                monthly_predicted_precipitation['Precipitation'],
                width=width, edgecolor='black', label=self.predicted_precipitation_label, alpha=0.6, color='green')

        plt.title('Histogram of Actual and Predicted Monthly Precipitation')
        plt.xlabel('Date')
        plt.ylabel('Monthly Precipitation (mm)')
        plt.xticks(ticks=x, labels=[date.strftime('%Y-%m') for date in monthly_actual_precipitation.index], rotation=45)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        plt.show()


latitude = 50.01
longitude = 20.98
start_date = '2023-01-01'
end_date = '2023-12-31'

# plotter = ActualPredictedAverageMonthlyPrecipitation(latitude, longitude, start_date, end_date)
# plotter.plot_rainfall_histogram()