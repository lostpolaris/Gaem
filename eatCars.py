#Imports
from typing import Sized
import pygame
from pygame.locals import *
import sys
import random
import time

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
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SPEED = 5
SIZE = 1
HEALTH = 50
ENEMYX = 50
ENEMYY = 80
PLAYERX = 50
PLAYERY = 100


enemySprites = ['enemy.png', 'enemy1.png', 'enemy2.png', 'enemy3.png', 'enemy4.png']

#setting up fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, GREEN)

background = pygame.image.load("carena.png")

#Create a white screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Eat or Get Eaten")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(enemySprites[random.randint(0, 4)])
        self.surf = pygame.Surface(((.9 * ENEMYX), (.9 * ENEMYY)))
        self.rect = self.surf.get_rect(center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(50, SCREEN_HEIGHT - 50)))

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center = (500, 500))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)
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
pygame.time.set_timer(INC_ENEMY, 250)

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

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    
    #To be run if collision occurs between Player and Enemy
    for enemy in pygame.sprite.spritecollide(P1, enemies, 1):
        pygame.mixer.Sound('crash.wav').play()
    if pygame.sprite.spritecollideany(P1, enemies):
        #if vulnerable:
        #    LIVE -= 1
        #    P1.invulnerability
        if HEALTH == 0:
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
    pygame.display.update()
    FramePerSec.tick(FPS)
