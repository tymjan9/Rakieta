import pygame, os, sys, json, socket
from settings import Settings



class Rocket:
    def __init__(self):
        self.settings = Settings()

        self.positon = self.settings.rocket_start_postition
        self.velocity = self.settings.rocket_start_velocity
        self.thrust = 35000000


    def symulate_next_step(self):
        self.velocity[0] = self.velocity[0] + 0 * self.settings.delta_t
        self.velocity[1] = self.velocity[1] + (self.settings.gravitational_acceleration + self.thrust / self.settings.rocket_mass) * self.settings.delta_t

        self.positon[0] = self.positon[0] + self.velocity[0] * self.settings.delta_t + 0 * self.settings.delta_t**2 / 2
        self.positon[1] = self.positon[1] + self.velocity[1] * self.settings.delta_t + (self.settings.gravitational_acceleration + self.thrust / self.settings.rocket_mass) * self.settings.delta_t ** 2 / 2
        # print(self.velocity, "   ", self.positon)

    def save_step_to_file(self):
        file = open("logs.elo", "a")
        file.write(f"{self.velocity[0]},{self.velocity[1]};{self.positon[0]},{self.positon[1]}\n")
        file.close()



class Display:
    def __init__(self):
        self.settings = Settings()
        self.rocket = Rocket()

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1200, 800))
        self.screen_rect = self.screen.get_rect()
        self.rocket_sprites = [ pygame.image.load('images/Rocket.bmp') ]

        



        self.run_game()



    def run_game(self):

        run = True
        while run:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.up_engine()
                    elif event.key == pygame.K_s:
                        self.down_engine()


            self.rocket.symulate_next_step()
            self.rocket.save_step_to_file()
            print(self.rocket.positon)

            self.screen.fill([0,255,255])
            self.screen.blit(self.rocket_sprites[0], [595, 350])
            self.screen.blit(self.settings.game_font.render((str(round(self.rocket.positon[0],2)) + " " + str(round(self.rocket.positon[1],2))), True, (0,0,0)), [900, 10])


            pygame.display.update()
            self.clock.tick(self.settings.game_clock)

        
        
    def up_engine(self):
        pass
        
    def down_engine(self):
        pass




if __name__ == '__main__':
    try:
        os.remove("logs.elo")
    except:
        pass
    display = Display()
    display.run_game
