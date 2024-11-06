import numpy as np
import factory_heating_problem as fhp
import factory
import visualiser
import pandas as pd

# This script runs several instances of the factory heating problem with different heat settings

# Initialisation of ODE solver
t_0 = 0
T = 7
t_span = (t_0, T)
y0 = [20]
t_eval = np.linspace(t_0, T, (T-t_0)*24)
# Factory properties
ground_area_factory = 1250
height_factory = 10

# save output to csv
save_output_to_csv = True

# heater settings
heater_watts_settings = [6500, 5500, 7500]
#heater_watts_settings = np.linspace(12000, 16000, 20)
t_on = 1
t_off = 12

additional_info = True

solution_functions = []

for i in range(len(heater_watts_settings)):
    factory_i = factory.Factory(1225, 10, 0.18, t_on, t_off)
    factory_heating_problem = fhp.FactoryHeatingProblem(factory_i, heater_watts_settings[i])
    solution_functions.append(factory_heating_problem.solve(t_span, y0, t_eval, save_output_to_csv))

factory_heating_problem.visualise_temperature_info(t_eval)

temp_spring = pd.read_csv('ideal_setting_temps/amb_temp_func_vals_spring.csv').values.flatten()
temp_summer = pd.read_csv('ideal_setting_temps/amb_temp_func_vals_summer.csv').values.flatten()
temp_autumn = pd.read_csv('ideal_setting_temps/amb_temp_func_vals_autumn.csv').values.flatten()
temp_winter = pd.read_csv('ideal_setting_temps/amb_temp_func_vals_winter.csv').values.flatten()

amb_temp = [temp_spring, temp_summer, temp_autumn, temp_winter]

visualiser = visualiser.Visualiser(solution_functions, heater_watts_settings)
visualiser.visualise(amb_temp, True, True)


