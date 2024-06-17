from statsmodels.tsa.statespace.sarimax import SARIMAX
import itertools


class SARIMAXForecaster:

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
