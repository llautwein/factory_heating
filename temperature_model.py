import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

# This class generates the temperature function from the weather data


class TemperatureFunction:

    def __init__(self):

        # import data set
        file_path = "weather_data/weather data.csv"
        complete_dataset = pd.read_csv(file_path, skiprows=281, low_memory=False)
        self.df = complete_dataset[['ob_time', 'air_temperature']]
        self.df = self.df.drop(self.df.index[-1])
        self.average_temperature_year = self.df['air_temperature'].mean()
        t_0 = 90 * 24
        shift_part = self.df.iloc[:t_0]
        rest_of_data = self.df.iloc[t_0:]

        # Concatenate `rest_of_data` with `first_100`
        self.df = pd.concat([rest_of_data, shift_part], ignore_index=True)
        self.parameters = self.curve_fit()
        print(self.parameters)

    @staticmethod
    def model_function(t, x_1, x_2, x_3, x_4, x_5):
        return x_1 * np.sin(2*np.pi * (t-x_2)) + x_3 * np.sin(2*np.pi/365 * (t-x_4)) + x_5

    def curve_fit(self):

        t_eval = np.linspace(0, 365, 8760)

        parameters, _ = curve_fit(self.model_function,
                                  t_eval, self.df['air_temperature'], method="lm",
                                  p0=[20, 0, 20, 0, 12])
        return parameters

    def plot_datapoints_and_function(self):
        params = {'legend.fontsize': 'xx-large',
                  'axes.labelsize': 'xx-large',
                  'axes.titlesize': 'xx-large',
                  'xtick.labelsize': 'xx-large',
                  'ytick.labelsize': 'xx-large'}
        pylab.rcParams.update(params)
        t_eval = np.linspace(0, 365, 365*24)
        plt.figure()
        plt.scatter(t_eval, self.df['air_temperature'], s=1, label="Air Temperature (London Heathrow)")
        plt.xlabel("Time t [days]")
        plt.ylabel('Temperature T [°C]')
        plt.legend()

        fig, ax = plt.subplots()
        ax.plot(t_eval, self.exterior_temperature(t_eval), label="Temperature Function", color="gray", alpha=0.7)
        plt.scatter(t_eval, self.df['air_temperature'], s=1, label="Air Temperature (London Heathrow)")

        # Extract one week of data for zoom-in
        t_extract = np.linspace(0, 31, 31*24)
        y_extract = self.exterior_temperature(t_extract)
        data_points_extract = self.df["air_temperature"].iloc[0:31*24]

        # Create zoomed inset with relative coordinates and size
        zm = ax.inset_axes([0.16, 0.05, 0.37, 0.32])  # Adjust width and height as needed
        zm.plot(t_extract, y_extract, color="gray", alpha=0.9)
        zm.scatter(t_extract, data_points_extract, s=1)
        ax.indicate_inset_zoom(zm, edgecolor='red')

        plt.xlabel('Time t [days]')
        plt.ylabel('Temperature T [°C]')
        plt.legend()

    def plot_residuals(self):
        params = {'legend.fontsize': 'xx-large',
                  'axes.labelsize': 'xx-large',
                  'axes.titlesize': 'xx-large',
                  'xtick.labelsize': 'xx-large',
                  'ytick.labelsize': 'xx-large'}
        pylab.rcParams.update(params)
        t_eval = np.linspace(0, 365, len(self.df))

        predicted_temperatures = self.model_function(t_eval, *self.parameters)

        residuals = self.df['air_temperature'] - predicted_temperatures

        # Plot residuals
        plt.figure()
        plt.scatter(t_eval, residuals, color="blue", s=1, label="Residuals")
        plt.axhline(0, color='red', linestyle='--', linewidth=1)
        plt.xlabel("Time t [days]")
        plt.ylabel("Residuals [°C]")
        plt.title("Residuals of Temperature Model Fit")
        plt.legend()

    def exterior_temperature(self, t):
        return self.model_function(t, *self.parameters)




