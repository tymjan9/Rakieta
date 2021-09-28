import pygame
import os


class Settings:
    def __init__(self):

        self.rocket_mass = 3000000
        self.rocket_max_thrust = 35000000
        self.rocket_max_torque = 100000
        self.rocket_start_postition = [0,0]
        self.rocket_start_velocity = [0,0]

        self.gravitational_acceleration = -9.8
        self.delta_t = 0.02

        self.game_clock = 50