import pygame, os, sys, json, socket
from settings import Settings

class Rocket:
    def __init__(self):
        self.settings = Settings()

        self.positon = self.settings.rocket_start_postition
        self.velocity = self.settings.rocket_start_velocity
        self.thrust = 10000


    def symulate_next_step(self):

        self.velocity[0] = self.velocity[0] + 0 * self.settings.delta_t
        self.velocity[1] = self.velocity[1] + (self.settings.gravitational_acceleration + self.thrust / self.settings.rocket_mass) * self.settings.delta_t

        print(self.velocity)

    def _check_events(self):
         for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
         #       if event.key == pygame.K_d:
           #         self.right_engine()
          #      elif event.key == pygame.K_a:
          #          self.left_engine()
                if event.key == pygame.K_w:
                    self.up_engine()
                elif event.key == pygame.K_s:
                    self.down_engine()
                    
   # def right_engine(self):
        
        
   # def left_engine(self):
        
        
    def up_engine(self):
        
        
    def down_engine(self):
                    




if __name__ == '__main__':
    rocket = Rocket()
    for i in range(100):
        rocket.symulate_next_step()
