import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


class TemperatureFunction:

    def __init__(self):

        # import data set
        file_path = "weather_data/weather data fixed.csv"
        complete_dataset = pd.read_csv(file_path, skiprows=281, low_memory=False)
        self.df = complete_dataset[['ob_time', 'air_temperature']]
        self.df = self.df.drop(self.df.index[-1])
        self.average_temperature_year = self.df['air_temperature'].mean()
        self.parameters = self.curve_fit()

    @staticmethod
    def model_function(t, a, b, c, d, e, f, g):
        return a * np.sin(b * (t-c)) + d + e * np.sin(f * (t-g))

    def curve_fit(self):

        t_eval = np.linspace(0, 365, 8760)

        parameters, _ = curve_fit(self.model_function,
                                  t_eval, self.df['air_temperature'],
                                  p0=[20, 2*np.pi/365, 0, self.average_temperature_year, 20, 2*np.pi, 0])
        return parameters

    def exterior_temperature(self, t):
        return self.model_function(t, *self.parameters)




