import datetime
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from src.services.helpers.DateHelper import DateHelper


class SARIMAXForecaster(DateHelper):

    @staticmethod
    def fit_sarima_model(data):
        model = SARIMAX(data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        model_fit = model.fit(disp=False)
        return model_fit

    @staticmethod
    def forecast(model_fit, forecast_steps=12, start_date=datetime.datetime.now()):
        forecast = model_fit.get_forecast(steps=forecast_steps)
        forecast_index = pd.date_range(start=start_date, periods=forecast_steps, freq='M')
        return pd.Series(forecast.predicted_mean, index=forecast_index)

    @staticmethod
    def generate_predicted_data_generic(fetch_data_func, value_column_name, start_date, end_date):
        extended_start_date = DateHelper.get_extended_start_date(start_date, years=10)

        historical_end_date = (pd.to_datetime(start_date) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')
        extended_data = fetch_data_func(extended_start_date, historical_end_date)
        monthly_mean = extended_data.resample('M').mean()

        model_fit = SARIMAXForecaster.fit_sarima_model(monthly_mean[value_column_name])

        forecast_start_date = pd.to_datetime(start_date)
        forecast_end_date = pd.to_datetime(end_date) + pd.DateOffset(years=1)
        forecast_steps = len(pd.date_range(start=forecast_start_date, end=forecast_end_date, freq='M'))

        predicted_values = SARIMAXForecaster.forecast(model_fit=model_fit, forecast_steps=forecast_steps, start_date=forecast_start_date)
        predicted_values.name = f'Predicted {value_column_name}'

        print(f'PREDICTION: {predicted_values}')
        return predicted_values
