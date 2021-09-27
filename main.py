import pygame, os, sys, json, socket
from settings import Settings



class Rocket:
    def __init__(self):
        self.settings = Settings()

        self.acceleration = [0, 0]
        self.velocity = self.settings.rocket_start_velocity
        self.positon = self.settings.rocket_start_postition
        self.rotation = 0

        self.thrust = 0


    def symulate_next_step(self):
        self.acceleration[0] = 0
        self.acceleration[1] = self.settings.gravitational_acceleration + self.thrust / self.settings.rocket_mass


        self.velocity[0] = self.velocity[0] + self.acceleration[0] * self.settings.delta_t
        self.velocity[1] = self.velocity[1] + self.acceleration[1] * self.settings.delta_t

        self.positon[0] = self.positon[0] + self.velocity[0] * self.settings.delta_t + self.acceleration[0] * self.settings.delta_t**2 / 2
        self.positon[1] = self.positon[1] + self.velocity[1] * self.settings.delta_t + self.acceleration[1] * self.settings.delta_t ** 2 / 2
        # print(self.velocity, "   ", self.positon)

        if self.positon[1] < 0:
            if self.acceleration[1] < 0:
                self.acceleration[1] = 0
            if self.velocity[1] < 0:
                self.velocity[1] = 0
            if self.positon[1] < 0:
                self.positon[1] = 0

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
        self.ground_sprite = pygame.transform.scale(pygame.image.load("images/Ground.png"), (10000,600))
        self.rocket_sprite = pygame.transform.scale(pygame.image.load("images/Rocket.png"), (10, 100))
        self.rocket_sprite.set_colorkey((0,255,255))
        self.fire_sprite = pygame.transform.scale(pygame.image.load("images/fire.png"), (10, 20))
        self.fire_sprite.set_colorkey((255,255,255))


        self.time = 0

        self.run_game()

    def run_game(self):

        run = True
        while run:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False
            if keys[pygame.K_w]:
                self.up_engine()
            if keys[pygame.K_s]:
                self.down_engine()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False



            self.rocket.symulate_next_step()
            self.rocket.save_step_to_file()
            # print(self.rocket.positon)

            self.screen.fill([0,255,255])
            self.screen.blit(self.ground_sprite, [600, 450 + self.rocket.positon[1]])
            self.screen.blit(self.ground_sprite, [-9400, 450 + self.rocket.positon[1]])
            self.screen.blit(self.rocket_sprite, [595, 350])
            if self.rocket.thrust > 0:
                self.screen.blit(self.fire_sprite, [595, 450])
            self.screen.blit(self.settings.game_font_30.render("Positon: " + (str(round(self.rocket.positon[0],2)) + "m  " + str(round(self.rocket.positon[1],2))) + "m", True, (0,0,0)), [10, 10])
            self.screen.blit(self.settings.game_font_30.render("Velocity: " + (str(round(self.rocket.velocity[0], 2)) + "m/s  " + str(round(self.rocket.velocity[1], 2))) + "m/s", True, (0, 0, 0)), [10, 50])
            self.screen.blit(self.settings.game_font_30.render("Thrust: " + str(int(self.rocket.thrust/1000)) + "KN", True, (0, 0, 0)), [10, 90])
            self.screen.blit(self.settings.game_font_30.render(f"Time: {self.time}s", True, (0,0,0)), [10, 130])

            pygame.display.update()
            self.clock.tick(self.settings.game_clock)
            self.time = round(self.time + self.settings.delta_t, 2)



    def up_engine(self):
        if self.rocket.thrust < self.settings.rocket_max_thrust:
            self.rocket.thrust = self.rocket.thrust + self.settings.rocket_max_thrust / 100
        
    def down_engine(self):
        if self.rocket.thrust > 0:
            self.rocket.thrust = self.rocket.thrust - self.settings.rocket_max_thrust / 100




if __name__ == '__main__':
    try:
        os.remove("logs.elo")
    except:
        pass
    display = Display()
    display.run_game
