import pygame
import os


class Settings:
    def __init__(self):
        self.fuel = 2550000/2
        self.rocket_mass = 450000 + self.fuel
        self.rocket_max_thrust = 35000000
        self.rocket_max_side_thrust = 5000000
        self.rcket_max_side_speed = 10
        self.rocket_start_postition = [0,0]
        self.rocket_start_velocity = [0,0]

        self.gravitational_acceleration = -9.8
        self.delta_t = 0.02

        self.game_clock = 50

        self.landing_pad_position = 200