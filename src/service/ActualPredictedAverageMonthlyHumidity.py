import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

    def generate_predicted_data(self, actual_data):
        np.random.seed(0)
        predicted_humidity = actual_data['Humidity'] * np.random.uniform(0.8, 1.2, len(actual_data))
        predicted_df = actual_data.copy()
        predicted_df['Humidity'] = predicted_humidity
        return predicted_df

    def plot_humidity_histogram(self):
        df_actual = self.fetch_humidity_data()
        df_predicted = self.generate_predicted_data(df_actual)

        monthly_actual_humidity = df_actual.resample('M').mean()
        monthly_predicted_humidity = df_predicted.resample('M').mean()

        figure, ax = plt.subplots(figsize=(14, 8))

        width = 0.4
        x = np.arange(len(monthly_actual_humidity.index))

        ax.bar(x - width / 2,
               monthly_actual_humidity['Humidity'],
               width=width, edgecolor='black', label=self.actual_humidity_label, alpha=0.6, color='blue')

        ax.bar(x + width / 2,
               monthly_predicted_humidity['Humidity'],
               width=width, edgecolor='black', label=self.predicted_humidity_label, alpha=0.6, color='lightblue')

        ax.set_title('Histogram of Actual and Predicted Monthly Humidity')
        ax.set_xlabel('Date')
        ax.set_ylabel('Monthly Humidity (%)')
        ax.set_xticks(ticks=x)
        ax.set_xticklabels([date.strftime('%Y-%m') for date in monthly_actual_humidity.index], rotation=45)
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        return figure
