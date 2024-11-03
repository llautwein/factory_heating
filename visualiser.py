import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from statistics import stdev, mean
import pandas as pd
import numpy as np

# The Visualiser class manages the result plots


class Visualiser:
    def __init__(self, solution_functions, heater_settings):
        self.solution_functions = solution_functions
        self.heater_settings = heater_settings

    def visualise(self, amb_temp, means_bool=False, stdev_bool=False):
        params = {'legend.fontsize': 'xx-large',
                  'axes.labelsize': 'xx-large',
                  'axes.titlesize': 'xx-large',
                  'xtick.labelsize': 'xx-large',
                  'ytick.labelsize': 'xx-large'}
        pylab.rcParams.update(params)
        n = len(self.solution_functions)
        means = [mean(self.solution_functions[i].y[0]) for i in range(n)]
        st_devs = [stdev(self.solution_functions[i].y[0]) for i in range(n)]
        print(f"Means: {means}, St. Dev. {st_devs}")
        final_data = pd.DataFrame({
            "heater_watts": self.heater_settings,
            "means": means,
            "stdevs": st_devs
        })

        plt.figure()
        for i in range(n):
            plt.plot(self.solution_functions[i].t, self.solution_functions[i].y[0],
                     label=f'{self.heater_settings[i]} W heater')
        plt.grid(True)
        plt.axhline(y=20, color='black', linewidth=3, label='Initial Temperature', alpha=0.7)
        plt.xlabel('Time t [days]')
        plt.ylabel('Temperature T [°C]')
        plt.ylim(15, 25)
        plt.legend(loc="upper left")

        plt.figure()
        plt.plot(np.linspace(0, 91, 2184), amb_temp[0], linewidth=0.5, label="Ambient Temperature", color="b")
        plt.plot(np.linspace(91, 183, 2184), amb_temp[1], linewidth=0.5, color="b")
        plt.plot(np.linspace(183, 275, 2184), amb_temp[2], linewidth=0.5, color="b")
        plt.plot(np.linspace(275, 365,  2160), amb_temp[3], linewidth=0.5, color="b")
        plt.xlabel('Time t [days]')
        plt.ylabel('Temperature T [°C]')
        plt.legend(loc="upper left")
        plt.grid(True)
        plt.axvline(x=91, color="gray", linestyle="--", alpha=0.8)
        plt.axvline(x=183, color="gray", linestyle="--", alpha=0.8)
        plt.axvline(x=275, color="gray", linestyle="--", alpha=0.8)

        if means_bool:
            plt.figure()
            plt.plot(self.heater_settings, means, label="Mean Temperature")
            plt.fill_between(final_data["heater_watts"],
                             final_data["means"] - final_data["stdevs"],  # Lower bound (mean - stdev)
                             final_data["means"] + final_data["stdevs"],  # Upper bound (mean + stdev)
                             color='b', alpha=0.2, label='Mean ± Std Dev')
            plt.axhline(y=20, color='black', linewidth=3, label='Initial Temperature', alpha=0.7)
            plt.grid(True)
            plt.ylim(15, 25)
            plt.legend(loc="upper left")
            plt.xlabel("Heater Power [W]")
            plt.ylabel("Temperature T [°C]")
            """
            plt.figure()
            plt.errorbar(self.heater_settings, means, yerr=st_devs, fmt='o', capsize=5, label='Mean ± Std Dev')
            plt.xlabel("Heater Power [W]")
            plt.ylabel("Mean Temperature")
            plt.legend()
            """
        if stdev_bool:
            plt.figure()
            plt.plot(self.heater_settings, st_devs, label="Standard Deviations")
            plt.grid(True)
            plt.ylim(0.5, 3)
            plt.xlabel("Heater Power [W]")
            plt.ylabel("Temperature T [°C]")
            plt.legend(loc="upper left")

        plt.show()

