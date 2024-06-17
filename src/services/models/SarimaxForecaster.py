import datetime

import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

from src.services.helpers.DateHelper import DateHelper


class SARIMAXForecaster(DateHelper):

    @staticmethod
    def fit_sarima_model(self):
        model = SARIMAX(self, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        model_fit = model.fit(disp=False)
        return model_fit

    @staticmethod
    def forecast(model_fit, forecast_steps=12, start_date=datetime.date.today()):
        forecast = model_fit.get_forecast(steps=forecast_steps)
        forecast_index = pd.date_range(start=start_date, periods=forecast_steps, freq='M')
        return pd.Series(forecast.predicted_mean, index=forecast_index)

    @staticmethod
    def generate_predicted_data_generic(actual_data, fetch_data_func, value_column_name, start_date, end_date):
        extended_start_date = DateHelper.get_extended_start_date(start_date)

        extended_data = fetch_data_func(extended_start_date, end_date)
        monthly_sum = extended_data.resample('M').sum()

        model_fit = SARIMAXForecaster.fit_sarima_model(monthly_sum[value_column_name])

        forecast_start_date = actual_data.resample('M').sum().index[-1] + pd.DateOffset(months=1)
        forecast_end_date = pd.to_datetime(end_date) + pd.DateOffset(months=12)
        forecast_index = pd.date_range(start=forecast_start_date, end=forecast_end_date, freq='M')

        predicted_values = SARIMAXForecaster.forecast(model_fit=model_fit, start_date=forecast_start_date)
        predicted_values.index = forecast_index
        predicted_values.name = f'Predicted {value_column_name}'

        return predicted_values
