import numpy as np
import matplotlib.pyplot as plt
import factory_heating_problem as fhp
import factory

# ToDo:
# Plot exterior temperature in comparison to data set
# Plot residuals
# Git repo
# Put equations and constants in latex
# Research -> other articles about the topic

# Initialisation of ODE solver
t_0 = 10
T = 20
t_span = (t_0, T)
y0 = [20]
t_eval = np.linspace(t_0, T, (T-t_0)*24)
# Factory properties
ground_area_factory = 1250
height_factory = 10

factory = factory.Factory(1250, 10, 0.18,
                          9000, 4, 8)
factory_heating_problem = fhp.FactoryHeatingProblem(factory)
factory_heating_problem.visualize(t_span, y0, t_eval)



