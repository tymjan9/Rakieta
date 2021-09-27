import pygame
import os


class Settings:
    def __init__(self):
        pygame.init()

        self.rocket_mass = 3000000
        self.rocket_max_thrust = 35000000
        self.rocket_start_postition = [0,0]
        self.rocket_start_velocity = [0,0]

        self.gravitational_acceleration = -9.8
        self.delta_t = 0.02

        self.game_clock = 50
        # self.game_font = pygame.font.Font("Fonts/Penisfont.ttf", 50)
        self.game_font_30 = pygame.font.Font(pygame.font.get_default_font(), 30)
        self.game_font_15 = pygame.font.Font(pygame.font.get_default_font(), 15)
