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
        self.side_thrust = 0

        self.target_y_acceleration = self.settings.gravitational_acceleration


    def symulate_next_step(self):
        self.acceleration[0] = self.side_thrust / self.settings.rocket_mass
        self.acceleration[1] = self.settings.gravitational_acceleration + self.thrust / self.settings.rocket_mass

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
            self.velocity[0] = 0


    def save_step_to_file(self):
        file = open("logs.elo", "a")
        file.write(f"{self.velocity[0]},{self.velocity[1]};{self.positon[0]},{self.positon[1]}\n")
        file.close()


    def up_engine(self):
        if self.thrust < self.settings.rocket_max_thrust:
            self.thrust = self.thrust + self.settings.rocket_max_thrust / 100

    def down_engine(self):
        if self.thrust > 0:
            self.thrust = self.thrust - self.settings.rocket_max_thrust / 100

    def rotation_right(self):
        self.side_thrust = self.settings.rocket_max_side_thrust

    def rotation_left(self):
        self.side_thrust = self.settings.rocket_max_side_thrust * -1


    def go_to_landing_pad(self):
        # if self.settings.landing_pad_position > self.positon[0]:
        #     self.set_x_speed(10, 2)
        # if self.settings.landing_pad_position < self.positon[0]:
        #     self.set_x_speed(-10, 2)
        speed = (1000 - self.positon[0]) / abs(self.positon[1] * 2 / -self.target_y_acceleration-0.1) ** 0.5
        if self.positon[0] > self.settings.landing_pad_position:
            speed = -speed
        # print(speed)
        self.set_x_speed(int(speed), 2)

    def set_x_speed(self, target, max_acceleration):
        if self.velocity[0] > target:
            self.set_x_acceleration(-max_acceleration)
        if self.velocity[0] < target:
            self.set_x_acceleration(max_acceleration)

    def set_x_acceleration(self, target):
        if self.acceleration[0] > target:
            if self.side_thrust > -self.settings.rocket_max_side_thrust:
                self.side_thrust = self.side_thrust - self.settings.rocket_max_side_thrust / 100
        if self.acceleration[0] < target:
            if self.side_thrust < self.settings.rocket_max_side_thrust:
                self.side_thrust = self.side_thrust + self.settings.rocket_max_side_thrust / 100

    def auto_landing(self):
        if self.positon[1] > 300:
            self.set_y_speed(-50,10)
        elif self.positon[1] > 50:
            self.set_y_speed(-5,8)
        else:
            self.set_y_speed(-2, 1)

    def set_y_speed(self, target, max_acceleration):
        if self.velocity[1] > target:
            self.set_y_acceleration(-max_acceleration)
        if self.velocity[1] < target:
            self.set_y_acceleration(max_acceleration)

    def set_y_acceleration(self, target):
        self.target_y_acceleration = target
        if self.acceleration[1] > target:
            if self.thrust > 0:
                self.thrust = self.thrust - self.settings.rocket_max_thrust / 100
        if self.acceleration[1] < target:
            if self.thrust < self.settings.rocket_max_thrust:
                self.thrust = self.thrust + self.settings.rocket_max_thrust / 100





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
        self.landing = pygame.image.load("images/landing.bmp")


        self.time = 0

        self.run_game()

    def run_game(self):
        landing = False
        go_to_landing_pad = False
        run = True
        while run:
            self.rocket.side_thrust = 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False
            if keys[pygame.K_SPACE]:
                time.sleep(60)
            if keys[pygame.K_w]:
                self.rocket.up_engine()
            if keys[pygame.K_s]:
                self.rocket.down_engine()
            if keys[pygame.K_a]:
                self.rocket.rotation_left()
            if keys[pygame.K_d]:
                self.rocket.rotation_right()
            if keys[pygame.K_f]:
                landing = True
            if keys[pygame.K_g]:
                go_to_landing_pad = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if landing:
                self.rocket.auto_landing()
            if go_to_landing_pad:
                self.rocket.go_to_landing_pad()


            self.rocket.symulate_next_step()
            self.rocket.save_step_to_file()

            self.screen.fill([0,255,255])
            self.screen.blit(self.ground_sprite, [600-self.rocket.positon[0], 450 + self.rocket.positon[1]])
            self.screen.blit(self.ground_sprite, [-9400-self.rocket.positon[0], 450 + self.rocket.positon[1]])
            self.screen.blit(self.landing, (self.settings.landing_pad_position + 600 - 50 - self.rocket.positon[0], 450 + self.rocket.positon[1]))
            x, y = 595, 410
            if self.rocket.thrust > 0:
                rocket = self.rocket_fire_sprite

            else:
                rocket = self.rocket_sprite
            rocket.set_colorkey((0, 0, 255))
            rocket_rect = rocket.get_rect()
            rocket_rect.center = x, y
            self.screen.blit(rocket, rocket_rect)
            self.screen.blit(self.game_font_30.render("Positon: " + (str(round(self.rocket.positon[0],2)) + "m  " + str(round(self.rocket.positon[1],2))) + "m", True, (0,0,0)), [10, 10])
            self.screen.blit(self.game_font_30.render("Velocity: " + (str(round(self.rocket.velocity[0], 2)) + "m/s  " + str(round(self.rocket.velocity[1], 2))) + "m/s", True, (0, 0, 0)), [10, 50])
            self.screen.blit(self.game_font_30.render("Acceleration: " + (str(round(self.rocket.acceleration[0], 2)) + "m/s2  " + str(round(self.rocket.acceleration[1], 2))) + "m/s2", True, (0, 0, 0)), [10, 90])
            self.screen.blit(self.game_font_30.render("Thrust: " + str(int(self.rocket.thrust/1000)) + "KN", True, (0, 0, 0)), [10, 130])
            self.screen.blit(self.game_font_30.render("Fuel: " + str(self.settings.fuel), True, (0, 0, 0)), [10, 170])
            self.screen.blit(self.game_font_30.render("Rotation: " + str(round(self.rocket.rotation, 2)), True, (0, 0, 0)), [10, 210])
            self.screen.blit(self.game_font_30.render(f"Time: {self.time}s", True, (0,0,0)), [10, 250])

            pygame.display.update()
            self.clock.tick(self.settings.game_clock)
            self.time = round(self.time + self.settings.delta_t, 2)









if __name__ == '__main__':
    try:
        os.remove("logs.elo")
    except:
        pass
    display = Display()
    display.run_game
