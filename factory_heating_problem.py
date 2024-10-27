import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp, odeint
from statistics import stdev, mean
import temperature_model


class FactoryHeatingProblem:

    def __init__(self, factory):
        self.factory = factory

    def heat_supply(self, t):
        cycle_t = t - self.factory.t_off * np.floor(t/self.factory.t_off)  # time within the 8-hour cycle
        return (self.factory.heat_supply_rate *
                (np.heaviside(cycle_t - self.factory.t_on, 0.0) -
                 np.heaviside(cycle_t - self.factory.t_off, 0.0)))

    @staticmethod
    def exterior_temperature(t):
        temperature_function = temperature_model.TemperatureFunction()
        return temperature_function.exterior_temperature(t)

    def heat_loss(self, t, y):
        return self.factory.heat_loss_rate * (y - self.exterior_temperature(t))

    def dydt(self, t, y):
        return (1/self.factory.proportionality_celsius_joule) * (self.heat_supply(t) - self.heat_loss(t, y))

    def solve(self, t_span, y0, t_eval):
        sol = solve_ivp(self.dydt, t_span, y0, method="RK45", t_eval=t_eval)
        return sol

    def solution_measure(self, sol):
        m = mean(sol.y[0])
        sd = stdev(sol.y[0])
        return m, sd

    def visualize(self, t_span, y0, t_eval):
        sol = self.solve(t_span, y0, t_eval)
        m, sd = self.solution_measure(sol)
        print(f"Mean: {m}, standard deviation: {sd}")

        plt.figure()
        plt.plot(t_eval, self.exterior_temperature(t_eval), color='gray', label='Exterior Temperature')
        plt.xlabel('Time t [days]')
        plt.ylabel('Temperature T(t) [°C]')
        plt.legend()

        plt.figure()
        plt.plot(sol.t, sol.y[0], color='black', label='Ambient Temperature')
        plt.ylim(10, 30)
        plt.axhline(y=y0, color='g', linestyle='--', label='Initial Temperature', alpha=0.3)
        plt.axhline(y=m, color='r', linestyle='--', label='Mean Temperature', alpha=0.3)
        plt.axhline(y=m-sd, color='orange', linestyle='--', label='Standard Deviation', alpha=0.3)
        plt.axhline(y=m+sd, color='orange', linestyle='--', label='Standard Deviation', alpha=0.3)

        t = self.factory.t_on
        while t < 10:
            #plt.axvline(x=t, color='orange', linestyle='--', alpha=0.3)
            t += (self.factory.t_off - self.factory.t_on)
            #plt.axvline(x=t, color='b', linestyle='--', alpha=0.3)
            t += self.factory.t_on

        plt.xlabel('Time t [days]')
        plt.ylabel('Temperature T(t) [°C]')
        plt.legend()
        plt.show()

