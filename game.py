import pygame
from config import *
import os
import random

# Init
pygame.init()

i = 0
cloud_alpha = 150

#DISPLAY BG AND THEN SCALE IT TO FIT WINDOW
bg_img = pygame.image.load(LEVELS_PATH + "spritesheet/background.png")
bg = pygame.transform.scale(bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT) )

bg_img3 = pygame.image.load(LEVELS_PATH + "spritesheet/1.png")
bg_img3.set_alpha(cloud_alpha)

bg3 = pygame.transform.scale(bg_img3, (WINDOW_WIDTH, WINDOW_HEIGHT) )

bg_img2 = pygame.image.load(LEVELS_PATH + "spritesheet/backgroundii.png")
bg2 = pygame.transform.scale(bg_img2, (WINDOW_WIDTH, WINDOW_HEIGHT) )

rose_img = pygame.image.load(LEVELS_PATH + "spritesheet/Rose.png")
rose = pygame.transform.scale(rose_img, (32, 32) )

# Scene B asserts

scene_img = pygame.image.load(LEVELS_PATH + "spritesheet/4.png")
scene_bg = pygame.transform.scale(scene_img, (WINDOW_WIDTH, WINDOW_HEIGHT) )

# OPEN WINDOW
displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#title the Window
pygame.display.set_caption("Eco system")

idle = pygame.image.load(os.path.join("Eco/spritesheet/hero", "standing.png"))

right = [None] * 10
for picIndex in range(1, 10):
    right[picIndex - 1] = pygame.image.load(os.path.join("Eco/spritesheet/hero", "R" + str(picIndex) + ".png"))
    picIndex +=1

left = [None] * 10
for picIndex in range(1, 10):
    left[picIndex - 1] = pygame.image.load(os.path.join("Eco/spritesheet/hero", "L" + str(picIndex) + ".png"))
    picIndex +=1
water = [None] * 50
for picIndex in range(1, 50):
    water[picIndex - 1] = pygame.transform.scale(pygame.image.load(os.path.join("Eco/spritesheet/water", "w" + str(picIndex) + ".png")), (100,100))
    picIndex +=1

x = 0
y = 290
vel_x = 5
vel_y = 5
stepIndex = 0
flow = 0
jump = False
movL = False
movR = False
well = False
smoke = True
planted = False
hitbox = (x, y, 64, 64)
plantation = []
cool_down_count = 0
desertHealth = 60
green = (0,255,0)
yellow = (255,255,0)
red = (255, 0, 0)

state_A = "Desert"
state_B = "Forested"

state = state_A


#text
text_font = pygame.font.SysFont("Arial", 15)

MY_TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MY_TIMER_EVENT, 2000)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    displaySurface.blit(img, (x,y))

def cooldown():
    global cool_down_count

    if cool_down_count >= 20:
        cool_down_count = 0
    elif cool_down_count > 0:
        cool_down_count += 1

def plant(player):
    cooldown()
    global well
    global plantation
    global rose
    global planted
    global cool_down_count
    global desertHealth
    global smoke

    plantee = None

    xx = 0
    yy = 0
    xx, yy = random.randint(0, 755), random.randint(270, 300)

    if well and pygame.key.get_pressed()[pygame.K_p] and cool_down_count == 0:
        planted = True
        plantee = Rose(xx, yy, rose)
        plantation.append(plantee)
        cool_down_count = 1
        if smoke:
            desertHealth -= 2

def moving(userInput):
    global movL
    global movR
    global x
    global y
    global vel_x
    global vel_y
    global stepIndex
    global jump

    if userInput[pygame.K_LEFT] and x > 0:
            x -= vel_x
            movL = True
            movR = False
    elif userInput[pygame.K_RIGHT] and x < 755:
        x += vel_x
        movL = not True
        movR = not False
    elif userInput[pygame.K_UP] and y > 270:
        y -= vel_y
        movL = not True
        movR = not False
    elif userInput[pygame.K_DOWN] and y < 300:
        y += vel_y
        movL = not True
        movR = not False
    else:
        movL = False
        movR = False
        stepIndex = 0
    
    # jumping code 
    if jump is False and userInput[pygame.K_SPACE]:
        jump = True

    if jump:
        y -= vel_y
        vel_y -= 1
        if vel_y < -10:
            jump = False
            vel_y = 10

def collision(player, obj):
    global well
    if player.x == obj.x and pygame.key.get_pressed()[pygame.K_h]:
        well = True

def draw_game():
    global stepIndex
    global flow
    global hitbox
    global desertHealth
    player = None
    Obj = None


    if flow >= 49:
        flow = 0

    #fountain
    if well:
        displaySurface.blit(water[flow//4], (540,230))
        flow += 1
        if desertHealth > 40:
            desertHealth = 39

    #animation mechanic
    if stepIndex >= 36:
        stepIndex = 0
    if movL:
        displaySurface.blit(left[stepIndex//4], (x,y))
        stepIndex += 1
    elif movR:
        displaySurface.blit(right[stepIndex//4], (x,y))
        stepIndex += 1
    else :
        displaySurface.blit(idle, (x,y))
    
    hitbox = (x + 15,y + 15, 30,40)
    player = pygame.draw.rect(displaySurface, (0,0,0), hitbox, 1)
    obj = pygame.draw.rect(displaySurface, (0,0,0), (580,180, 50, 150), 1)

    collision(player, obj)
    plant(player)
    
class Rose:
    def __init__(self, x, y, png):
        self.x = x
        self.y = y
        self.png = png
    
    def draw(self, screen):
        displaySurface.blit(self.png, ( self.x, self.y))
        # pygame.draw.rect(screen, (0,0,0), (self.x, self.y, 32, 32), 1)

isGameRunning = True
while isGameRunning:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isGameRunning = False

    if state == state_A:
        displaySurface.blit(bg, (i,0))
        if smoke:
            displaySurface.blit(bg3, (i,0))


        displaySurface.blit(bg, (WINDOW_HEIGHT + i, 0))
        if smoke:
            displaySurface.blit(bg3, (WINDOW_HEIGHT + i, 0))

        if i == -WINDOW_HEIGHT:
            displaySurface.blit(bg, (WINDOW_HEIGHT + 1, 0))
            if smoke:
                displaySurface.blit(bg3, (WINDOW_HEIGHT + 1, 0))
            i = 0
        i -= 1
        displaySurface.blit(bg2, (0,0))

        pygame.draw.rect(displaySurface, green, (10, 10, 60, 10))
        pygame.draw.rect(displaySurface, red, (10, 10, desertHealth, 10))
        pygame.draw.rect(displaySurface, (255, 255, 0), (10, 25, WINDOW_WIDTH / 2, 100), 1)

        draw_text("# ReForeste the Desert", text_font, (0, 0, 0), 15, 30)
        draw_text("## Find H2O Press h to dig", text_font, red, 20, 45)
        draw_text("## press P to Plant Seeds rem what plants need", text_font, red, 20, 60)
        draw_text("## Plants will reduce CO2 in the atmosphere", text_font, red, 20, 75)

        draw_game()

        userInput = pygame.key.get_pressed()

        if userInput[pygame.K_LEFT] and x > 0:
            x -= vel_x
            movL = True
            movR = False
        elif userInput[pygame.K_RIGHT] and x < 755:
            x += vel_x
            movL = not True
            movR = not False

        elif userInput[pygame.K_UP] and y > 270:
            y -= vel_y
            movL = not True
            movR = not False

        elif userInput[pygame.K_DOWN] and y < 300:
            y += vel_y
            movL = not True
            movR = not False
        else:
            movL = False
            movR = False
            stepIndex = 0

        if jump is False and userInput[pygame.K_SPACE]:
            jump = True

        if jump:
            y -= vel_y
            vel_y -= 1
            if vel_y < -10:
                jump = False
                vel_y = 10

        if planted:
            for plantee in plantation:
                plantee.draw(displaySurface)
                if event.type == MY_TIMER_EVENT and len(plantation) > random.randint(5, 20):
                    pygame.time.set_timer(MY_TIMER_EVENT, 0)
                    smoke = not smoke
                    state = state_B

    elif state == state_B:
        # SKY
        displaySurface.blit(bg, (i,0))
        
        displaySurface.blit(bg, (WINDOW_HEIGHT + i, 0)) # SKY 2

        # carsal
        if i == -WINDOW_HEIGHT:
            displaySurface.blit(bg, (WINDOW_HEIGHT + 1, 0))
            i = 0
        
        i -= 1

        # draw mountain bg and grass bg
        displaySurface.blit(bg2, (0,0))
        displaySurface.blit(scene_bg, (0,0))

        # rect boxes on character and ...
        pygame.draw.rect(displaySurface, green, (10, 10, 60, 10))
        pygame.draw.rect(displaySurface, red, (10, 10, desertHealth, 10))
        pygame.draw.rect(displaySurface, (255, 255, 0), (10, 25, WINDOW_WIDTH / 2, 100), 1)

        # Text on screen to show env state
        draw_text("# ReForeste the Desert", text_font, (0, 0, 0), 15, 30)
        draw_text("## Find H2O Press h to dig", text_font, green, 20, 45)
        draw_text("## press P to Plant Seeds rem what plants need", text_font, green, 20, 60)
        draw_text("## Plants will reduce CO2 in the atmosphere", text_font, green, 20, 75)

        # draw character 
        draw_game()
        
        # character movement
        moving(pygame.key.get_pressed())

    pygame.time.delay(10)
    pygame.display.update()

# Close pygame
pygame.quit()