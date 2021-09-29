import pygame, os, sys, json, socket, math, time
from settings import Settings



class Rocket:
    def __init__(self):
        self.settings = Settings()

        self.acceleration = [0, 0]
        self.velocity = self.settings.rocket_start_velocity
        self.positon = self.settings.rocket_start_postition
        self.thrust = 0

        self.rotational_acceleration = 0
        self.rotational_speed = 0
        self.rotation = 0
        self.torque = 0


    def symulate_next_step(self):
        self.rotational_acceleration = self.torque / self.settings.rocket_mass

        self.rotational_speed = self.rotational_speed + self.rotational_acceleration * self.settings.delta_t

        self.rotation = self.rotation + self.rotational_speed * self.settings.delta_t + self.rotational_acceleration * self.settings.delta_t**2 / 2

        if self.rotation > 360:
            self.rotation = self.rotation - 360
        if self.rotation < -0:
            self.rotation = 360 - self.rotation


        self.acceleration[0] = math.sin(self.rotation) * self.thrust / self.settings.rocket_mass

        self.acceleration[1] = math.cos(self.rotation) * self.thrust / self.settings.rocket_mass + self.settings.gravitational_acceleration
        # self.acceleration[1] = self.thrust / self.settings.rocket_mass + self.settings.gravitational_acceleration

        # self.acceleration[0] = 0
        # self.acceleration[1] = self.settings.gravitational_acceleration + self.thrust / self.settings.rocket_mass

        self.velocity[0] = self.velocity[0] + self.acceleration[0] * self.settings.delta_t
        self.velocity[1] = self.velocity[1] + self.acceleration[1] * self.settings.delta_t

        self.positon[0] = self.positon[0] + self.velocity[0] * self.settings.delta_t + self.acceleration[0] * self.settings.delta_t**2 / 2
        self.positon[1] = self.positon[1] + self.velocity[1] * self.settings.delta_t + self.acceleration[1] * self.settings.delta_t ** 2 / 2

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
        pygame.display.set_caption("Rocket_landing_simulation")
        self.screen = pygame.display.set_mode((1200, 800))
        self.screen_rect = self.screen.get_rect()

#        self.game_font = pygame.font.Font("Fonts/Penisfont.ttf", 50)
        self.game_font_15 = pygame.font.Font(pygame.font.get_default_font(), 15)
        self.game_font_30 = pygame.font.Font(pygame.font.get_default_font(), 30)

        self.ground_sprite = pygame.transform.scale(pygame.image.load("images/Ground.bmp"), (10000,600))
        self.rocket_sprite = pygame.transform.scale(pygame.image.load("images/Rocket.bmp"), (10, 120))
        self.rocket_fire_sprite = pygame.transform.scale(pygame.image.load("images/Rocket_fire.bmp"), (10, 120))


        self.time = 0

        self.run_game()

    def run_game(self):

        run = True
        while run:
            self.rocket.torque = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False
            if keys[pygame.K_SPACE]:
                time.sleep(60)
            if keys[pygame.K_w]:
                self.up_engine()
            if keys[pygame.K_s]:
                self.down_engine()
            if keys[pygame.K_a]:
                self.rotation_left()
            if keys[pygame.K_d]:
                self.rotation_right()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


            self.rocket.symulate_next_step()
            self.rocket.save_step_to_file()
            print(self.rocket.acceleration)

            self.screen.fill([0,255,255])
            self.screen.blit(self.ground_sprite, [600-self.rocket.positon[0], 450 + self.rocket.positon[1]])
            self.screen.blit(self.ground_sprite, [-9400-self.rocket.positon[0], 450 + self.rocket.positon[1]])
            x, y = 595, 410
            if self.rocket.thrust > 0:
                rocket = pygame.transform.rotate(self.rocket_fire_sprite, -self.rocket.rotation)

            else:
                rocket = pygame.transform.rotate(self.rocket_sprite, -self.rocket.rotation)
            rocket.set_colorkey((0, 0, 255))
            rocket_rect = rocket.get_rect()
            rocket_rect.center = x, y
            self.screen.blit(rocket, rocket_rect)
            self.screen.blit(self.game_font_30.render("Positon: " + (str(round(self.rocket.positon[0],2)) + "m  " + str(round(self.rocket.positon[1],2))) + "m", True, (0,0,0)), [10, 10])
            self.screen.blit(self.game_font_30.render("Velocity: " + (str(round(self.rocket.velocity[0], 2)) + "m/s  " + str(round(self.rocket.velocity[1], 2))) + "m/s", True, (0, 0, 0)), [10, 50])
            self.screen.blit(self.game_font_30.render("Thrust: " + str(int(self.rocket.thrust/1000)) + "KN", True, (0, 0, 0)), [10, 90])
            self.screen.blit(self.game_font_30.render("Rotation: " + str(round(self.rocket.rotation, 2)), True, (0, 0, 0)), [10, 130])
            self.screen.blit(self.game_font_30.render(f"Time: {self.time}s", True, (0,0,0)), [10, 170])

            pygame.display.update()
            self.clock.tick(self.settings.game_clock)
            self.time = round(self.time + self.settings.delta_t, 2)



    def up_engine(self):
        if self.rocket.thrust < self.settings.rocket_max_thrust:
            self.rocket.thrust = self.rocket.thrust + self.settings.rocket_max_thrust / 100
        
    def down_engine(self):
        if self.rocket.thrust > 0:
            self.rocket.thrust = self.rocket.thrust - self.settings.rocket_max_thrust / 100

    def rotation_right(self):
        self.rocket.torque = self.settings.rocket_max_torque

    def rotation_left(self):
        self.rocket.torque = self.settings.rocket_max_torque * -1






if __name__ == '__main__':
    try:
        os.remove("logs.elo")
    except:
        pass
    display = Display()
    display.run_game
