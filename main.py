#To restructure the code according to Object-Oriented Programming (OOP) principles, we need to encapsulate related functionality into classes and ensure that responsibilities are assigned clearly to each class. For example:

# 1. Create a `Game` class to manage the overall game flow.
# 2. Introduce a `Player` class to handle the player's movement and interaction with the environment.
# 3. Use a `Rose` class (already exists) for handling plant entities.
# 4. Introduce a `Background` class for handling the background assets and rendering.
# 5. Implement a `WaterSource` class to represent wells and water sources.
# 6. Modularize functions like `collision` and `plant` inside appropriate classes.
import pygame
import os
import random

# Init
pygame.init()

# Configurations (add your config module or constants here)
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
LEVELS_PATH = "./levels/"

# Constants
MY_TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MY_TIMER_EVENT, 2000)

class Game:
    def __init__(self):
        # Init window
        self.displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Eco system")
        
        # Font for displaying text
        self.text_font = pygame.font.SysFont("Arial", 15)
        
        # Load game assets
        self.background = Background()
        self.player = Player()
        self.water_source = WaterSource()
        self.roses = []
        self.state_A = "Desert"
        self.state_B = "Forested"
        self.state = self.state_A
        self.desertHealth = 60
        self.smoke = True
        self.cool_down_count = 0
        self.isGameRunning = True
        self.cloud_alpha = 150

    def run(self):
        while self.isGameRunning:
            self.handle_events()
            self.update_game_state()
            self.render()
            pygame.time.delay(10)
            pygame.display.update()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isGameRunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.isGameRunning = False
            elif event.type == MY_TIMER_EVENT:
                if len(self.roses) > random.randint(5, 20):
                    pygame.time.set_timer(MY_TIMER_EVENT, 0)
                    self.smoke = not self.smoke
                    self.state = self.state_B

    def update_game_state(self):
        if self.state == self.state_A:
            self.player.moving(pygame.key.get_pressed())
            if pygame.key.get_pressed()[pygame.K_p]:
                self.player.plant(self.roses, self.water_source, self.cool_down_count, self.smoke, self.desertHealth)

    def render(self):
        if self.state == self.state_A:
            self.background.draw_desert(self.displaySurface, self.smoke)
            self.draw_ui()
            self.player.draw(self.displaySurface)
            self.water_source.draw(self.displaySurface, self.smoke, self.desertHealth)
        elif self.state == self.state_B:
            self.background.draw_forested(self.displaySurface)
            self.draw_ui()
            self.player.draw(self.displaySurface)
        
        for rose in self.roses:
            rose.draw(self.displaySurface)
    
    def draw_ui(self):
        pygame.draw.rect(self.displaySurface, (0, 255, 0), (10, 10, 60, 10))
        pygame.draw.rect(self.displaySurface, (255, 0, 0), (10, 10, self.desertHealth, 10))
        pygame.draw.rect(self.displaySurface, (255, 255, 0), (10, 25, WINDOW_WIDTH / 2, 100), 1)
        self.draw_text("# ReForeste the Desert", (0, 0, 0), 15, 30)
        self.draw_text("## Find H2O Press h to dig", (255, 0, 0), 20, 45)
        self.draw_text("## press P to Plant Seeds rem what plants need", (255, 0, 0), 20, 60)
        self.draw_text("## Plants will reduce CO2 in the atmosphere", (255, 0, 0), 20, 75)
    
    def draw_text(self, text, color, x, y):
        img = self.text_font.render(text, True, color)
        self.displaySurface.blit(img, (x, y))


class Player:
    def __init__(self):
        self.x = 0
        self.y = 290
        self.vel_x = 5
        self.vel_y = 5
        self.stepIndex = 0
        self.jump = False
        self.movL = False
        self.movR = False
        self.idle_img = pygame.image.load(os.path.join("Eco/spritesheet/hero", "standing.png"))
        self.right_imgs = [pygame.image.load(os.path.join("Eco/spritesheet/hero", "R" + str(i) + ".png")) for i in range(1, 10)]
        self.left_imgs = [pygame.image.load(os.path.join("Eco/spritesheet/hero", "L" + str(i) + ".png")) for i in range(1, 10)]
        self.hitbox = (self.x, self.y, 64, 64)

    def moving(self, userInput):
        if userInput[pygame.K_LEFT] and self.x > 0:
            self.x -= self.vel_x
            self.movL = True
            self.movR = False
        elif userInput[pygame.K_RIGHT] and self.x < 755:
            self.x += self.vel_x
            self.movL = False
            self.movR = True
        elif userInput[pygame.K_UP] and self.y > 270:
            self.y -= self.vel_y
        elif userInput[pygame.K_DOWN] and self.y < 300:
            self.y += self.vel_y
        else:
            self.movL = False
            self.movR = False
            self.stepIndex = 0

        # Jumping mechanic
        if not self.jump and userInput[pygame.K_SPACE]:
            self.jump = True

        if self.jump:
            self.y -= self.vel_y
            self.vel_y -= 1
            if self.vel_y < -10:
                self.jump = False
                self.vel_y = 10

    def plant(self, plantation, water_source, cooldown_count, smoke, desertHealth):
        if water_source.well and pygame.key.get_pressed()[pygame.K_p] and cooldown_count == 0:
            plantation.append(Rose(random.randint(0, 755), random.randint(270, 300), pygame.image.load(LEVELS_PATH + "spritesheet/Rose.png")))
            cooldown_count = 1
            if smoke:
                desertHealth -= 2

    def draw(self, screen):
        if self.movL:
            screen.blit(self.left_imgs[self.stepIndex // 4], (self.x, self.y))
            self.stepIndex += 1
        elif self.movR:
            screen.blit(self.right_imgs[self.stepIndex // 4], (self.x, self.y))
            self.stepIndex += 1
        else:
            screen.blit(self.idle_img, (self.x, self.y))
        self.hitbox = (self.x + 15, self.y + 15, 30, 40)


class Rose:
    def __init__(self, x, y, png):
        self.x = x
        self.y = y
        self.png = png

    def draw(self, screen):
        screen.blit(self.png, (self.x, self.y))


class Background:
    def __init__(self):
        self.bg_img = pygame.transform.scale(pygame.image.load(LEVELS_PATH + "spritesheet/background.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_img2 = pygame.transform.scale(pygame.image.load(LEVELS_PATH + "spritesheet/backgroundii.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_img3 = pygame.transform.scale(pygame.image.load(LEVELS_PATH + "spritesheet/1.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_img3.set_alpha(150)
        self.scene_bg = pygame.transform.scale(pygame.image.load(LEVELS_PATH + "spritesheet/4.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.i = 0

    def draw_desert(self, screen, smoke):
        screen.blit(self.bg_img, (self.i, 0))
        if smoke:
            screen.blit(self.bg_img3, (self.i, 0))
        screen.blit(self.bg_img2, (0, 0))
        self.i -= 1

    def draw_forested(self, screen):
        screen.blit(self.bg_img, (self.i, 0))
        screen.blit(self.bg_img2, (0, 0))
        screen.blit(self.scene_bg, (0, 0))
        self.i -= 1


class WaterSource:
    def __init__(self):
        self.well = False
        self.water_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("Eco/spritesheet/water", "w" + str(i) + ".png")), (100, 100)) for i in range(1, 50)]
        self.flow = 0

    def draw(self, screen, smoke, desertHealth):
        if self.flow >= 49:
            self.flow = 0
       

 if pygame.key.get_pressed()[pygame.K_h]:
            self.well = True
            screen.blit(self.water_imgs[self.flow // 4], (500, 250))
            if desertHealth >= 60:
                desertHealth += 1
