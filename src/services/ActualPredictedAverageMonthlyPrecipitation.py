import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from src.services.api.WeatherDataFetcher import WeatherDataFetcher
from src.services.models.SarimaxForecaster import SARIMAXForecaster


class ActualPredictedAverageMonthlyPrecipitation(SARIMAXForecaster, WeatherDataFetcher):

    def __init__(self, latitude, longitude, start_date, end_date):
        super().__init__()
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.actual_precipitation_label = 'Actual Monthly Precipitation (mm)'
        self.predicted_precipitation_label = 'Predicted Monthly Precipitation (mm)'

    def generate_predicted_data(self, actual_data):
        monthly_sum_precipitation = actual_data.resample('M').sum()

        model_fit = self.fit_sarima_model(monthly_sum_precipitation['Precipitation'])

        forecast_steps = 12
        forecast = model_fit.get_forecast(steps=forecast_steps)
        forecast_index = pd.date_range(start=monthly_sum_precipitation.index[-1] + pd.DateOffset(months=1),
                                       periods=forecast_steps,
                                       freq='M')
        predicted_precipitation = pd.Series(forecast.predicted_mean, index=forecast_index)

        predicted_df = pd.concat([monthly_sum_precipitation, predicted_precipitation], axis=0)
        return predicted_df

    def plot_rainfall_histogram(self):
        df_actual = self.fetch_rainfall_data()
        df_predicted = self.generate_predicted_data(df_actual)

        df_actual_monthly = df_actual.resample('M').sum()
        df_predicted_monthly = df_predicted.resample('M').sum()

        df_combined = pd.concat([df_actual_monthly['Precipitation'], df_predicted_monthly['Precipitation']], axis=1)
        df_combined.columns = ['Actual Precipitation', 'Predicted Precipitation']

        df_combined = df_combined[self.start_date:self.end_date]

        figure, ax = plt.subplots(figsize=(14, 8))

        width = 0.4
        x = np.arange(len(df_combined.index))

        ax.bar(x - width / 2,
               df_combined['Actual Precipitation'],
               width=width, edgecolor='black', label=self.actual_precipitation_label, alpha=0.6, color='red')

        ax.bar(x + width / 2,
               df_combined['Predicted Precipitation'],
               width=width, edgecolor='black', label=self.predicted_precipitation_label, alpha=0.6, color='green')

        ax.set_title('Histogram of Actual and Predicted Monthly Precipitation')
        ax.set_xlabel('Date')
        ax.set_ylabel('Monthly Precipitation (mm)')
        ax.set_xticks(ticks=x)
        ax.set_xticklabels([date.strftime('%Y-%m') for date in df_combined.index], rotation=45)
        ax.legend()
        ax.grid(True)
        plt.tight_layout()

        return figure


