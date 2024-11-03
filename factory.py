import numpy as np

# The factory class contains all properties which are directly related to the factory we consider


class Factory:
    def __init__(self, ground_area, height, heat_transfer_coefficient, t_on, t_off):
        # Basic properties of the factory
        self.ground_area = ground_area
        self.height = height
        self.volume = self.ground_area * self.height
        # Ground is a square
        self.side_length = 35.35
        self.surface_area = self.ground_area + 4 * self.height * self.side_length

        # Insulation, heat energy properties
        self.rho = 1.2041   # density of air at 20°C
        self.c_p = 1012     # specific heat capacity of air at 20°C
        self.proportionality_celsius_joule = self.rho * self.volume * self.c_p + 3.21e8

        # Heat supply rate
        self.t_on = t_on / 24
        self.t_off = t_off / 24

        # Heat loss rate
        self.heat_transfer_coefficient = heat_transfer_coefficient * 3600 * 24
        self.heat_loss_rate = self.surface_area * self.heat_transfer_coefficient

        print(f"Factory properties: \n"
              f"Ground area: {self.ground_area} m^2, height: {self.height} m^2, volume: {self.volume} m^3,\n"
              f"Side length: {self.side_length} m, surface area: {self.surface_area} m^2\n"
              f"C={self.proportionality_celsius_joule},\n"
              f"h={self.heat_transfer_coefficient} \n"
              f"beta={self.heat_loss_rate}")
