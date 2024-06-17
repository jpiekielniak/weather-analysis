import datetime

import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


class SARIMAXForecaster:

    @staticmethod
    def fit_sarima_model(time_series):
        model = SARIMAX(time_series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        model_fit = model.fit(disp=False)
        return model_fit

    @staticmethod
    def forecast(model_fit, forecast_steps=12, start_date=datetime.date.today()):
        forecast = model_fit.get_forecast(steps=forecast_steps)
        forecast_index = pd.date_range(start=start_date, periods=forecast_steps, freq='M')
        return pd.Series(forecast.predicted_mean, index=forecast_index)
