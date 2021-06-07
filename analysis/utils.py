from math import pi, log10
from scipy import constants


def get_reynolds_number_regime(reynolds_number):
    if reynolds_number < 2300:
        return "laminar"
    elif reynolds_number > 2600:
        return "turbulent"
    else:
        return "transitional"


def calculate_cross_sectional_area(pipe_diameter):
    return (pipe_diameter ** 2) * (pi / 4)


def calculate_fluid_velocity(pipe_diameter, volumetric_flow_rate):
    area = calculate_cross_sectional_area(pipe_diameter)
    return volumetric_flow_rate / area


def calculate_reynolds_number(pipe_diameter, kinematic_viscosity, volumetric_flow_rate):
    fluid_velocity = calculate_fluid_velocity(pipe_diameter, volumetric_flow_rate)
    return (pipe_diameter * fluid_velocity) / (kinematic_viscosity * 0.0001)
