#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initializing
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

#Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE = (10, 0, 200)
RED = (200, 0, 10)
GREEN = (0, 200, 10)
BLACK = (10, 10, 10)
WHITE = (240, 240, 240)

#Other Variable for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
LIVE = 4
HIT = False

#setting up fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, GREEN)

background = pygame.image.load("road.png")

#Create a white screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png")
        self.surf = pygame.Surface((42, 70))
        self.rect = self.surf.get_rect(center = (random.randint(40, SCREEN_WIDTH - 40), 0))

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center = (160, 520))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        #if self.rect.top > 0
            #if pressed_keys[K_UP]:
                #self.rect.move_ip(0, -5)
        #if self.rect.bottom < SCREEN_HEIGHT
            #if pressed_keys[K_DOWN]:
                #self.rect.move_ip(0, 5)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)   

#Setting up Sprites
P1 = Player()
E1 = Enemy()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#Adding increasing speed with time
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 2000)

#Adding increasing enemies with time
INC_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(INC_ENEMY, 10000)

#Game Loop
while True:
    
    #Cycles through all events occurring
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += .5

        if event.type == INC_ENEMY:
            E1 = Enemy()
            enemies.add(E1)
            all_sprites.add(E1)
            
    
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    lives = font_small.render(str(LIVE), True, GREEN)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(lives, (SCREEN_WIDTH - 20, 10))

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    
    #To be run if collision occurs between Player and Enemy
    HIT = False
    if pygame.sprite.spritecollideany(P1, enemies):
        HIT = True
        LIVE -= 1
        if LIVE == 0:
            pygame.mixer.Sound('crash.wav').play()
            time.sleep(.5)
            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(game_over, (30, 250))
            pygame.display.update()
            for entity in all_sprites:
                entity.kill()
            time.sleep(2)
            pygame.quit()
            sys.exit()
        else:
            pygame.mixer.Sound('fuc.wav').play()
            DISPLAYSURF.fill(RED)
            time.sleep(.01666)
    pygame.display.update()
    FramePerSec.tick(FPS)
