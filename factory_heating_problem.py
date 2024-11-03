import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from scipy.integrate import solve_ivp
import temperature_model
import pandas as pd

# This class sets up our model equation and solves the ode numerically
# Additionally, the external temperature function can be visualised


class FactoryHeatingProblem:

    def __init__(self, factory, heater_watts):
        self.factory = factory
        self.temperature_function = temperature_model.TemperatureFunction()
        self.heater_watts = heater_watts
        self.heat_supply_rate = self.heater_watts * 3600 * 24

    def heat_supply(self, t):
        cycle_t = t - np.floor(t)
        return (self.heat_supply_rate *
                (np.heaviside(cycle_t - self.factory.t_on, 0.0) -
                 np.heaviside(cycle_t - self.factory.t_off, 0.0)))

    def exterior_temperature(self, t):
        return self.temperature_function.exterior_temperature(t)

    def heat_loss(self, t, y):
        return self.factory.heat_loss_rate * (y - self.exterior_temperature(t))

    def dydt(self, t, y):
        return (1/self.factory.proportionality_celsius_joule) * (self.heat_supply(t) - self.heat_loss(t, y))

    def solve(self, t_span, y0, t_eval, save_output_to_csv=False):
        sol = solve_ivp(self.dydt, t_span, y0, method="RK45", atol=1e-6, rtol=1e-6, t_eval=t_eval)
        if save_output_to_csv:
            df = pd.DataFrame(sol.y[0])
            df.to_csv('amb_temp_func_vals.csv', index=False)
        return sol

    def visualise_temperature_info(self, t_eval):
        params = {'legend.fontsize': 'x-large',
                  'axes.labelsize': 'x-large',
                  'axes.titlesize': 'x-large',
                  'xtick.labelsize': 'large',
                  'ytick.labelsize': 'large'}
        pylab.rcParams.update(params)
        # Exterior temperature plot for the given time interval
        plt.figure()
        plt.plot(t_eval, self.exterior_temperature(t_eval), color='gray', label='Exterior Temperature')
        plt.xlabel('Time t [days]')
        plt.ylabel('Temperature T [°C]')
        plt.legend()

        # Residuals
        self.temperature_function.plot_residuals()

        # Data points and exterior temperature plot
        self.temperature_function.plot_datapoints_and_function()



