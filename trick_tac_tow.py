import pygame as pg
from random import randint
import os
import time


WIDTH = 480
HEIGHT = 600
FPS = 15

RED = (255, 50, 50)
BLUE = (0, 0, 255)
GREEN = (175, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

TOP_Y = 180
BOTOM_Y = HEIGHT-35
MIDLE_Y = 335

JUMP = 155

X_MIDLE = 70
TOP_LEFT = (X_MIDLE, TOP_Y)
TOP_MID = (WIDTH/2, TOP_Y)
TOP_RIGHT = (WIDTH-X_MIDLE, TOP_Y)
MID_LEFT = (X_MIDLE, MIDLE_Y)
MID = (WIDTH/2, MIDLE_Y)
MID_RIGHT = (WIDTH-X_MIDLE, MIDLE_Y)
BOT_LEFT = (X_MIDLE, BOTOM_Y-X_MIDLE)
BOT_MID = (WIDTH/2, BOTOM_Y-X_MIDLE)
BOT_RIGHT = (WIDTH-X_MIDLE, BOTOM_Y-X_MIDLE)


# set up assets folders
game_folder = os.path.dirname(__file__)
player_img_folder = os.path.join(game_folder, "tictac assets")


enemy_in_state = False
SCALE = 5
Score = 0


class Board(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(player_img_folder, "board2.png")).convert()
        self.image.set_colorkey((246, 246, 246))
        self.rect = self.image.get_rect()
        self.rect.centerx = (WIDTH/2)
        self.rect.bottom = HEIGHT
        self.score = 0

    def update(self):
        self.score += 1
        if self.score % 15 == 0:
            pass


class PlayerX(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join(player_img_folder, "x.png")).convert()
        self.image.set_colorkey((254, 254, 254))

        self.size = self.image.get_size()
        self.image = pg.transform.scale(self.image, (140, 140))

        self.rect = self.image.get_rect()
        self.rect.center = MID

   # def update(self):

    def move(self):
        key = pg.key.get_pressed()
        if key[pg.K_UP] and self.rect.centery > TOP_Y:
            self.rect.centery -= JUMP
        elif key[pg.K_DOWN] and self.rect.bottom < BOTOM_Y-X_MIDLE:
            self.rect.centery += JUMP
        elif key[pg.K_RIGHT] and self.rect.right < WIDTH-X_MIDLE:
            self.rect.centerx += JUMP
        elif key[pg.K_LEFT] and self.rect.left > X_MIDLE:
            self.rect.centerx -= JUMP


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 10))
        self.image.fill(RED)
        self.scale = 1
        self.position = False
        self.colide = False
        self.rect = self.image.get_rect()

    def update(self):
        if not self.position:
            p = randint(1, 9)
            switcher = {
                1: BOT_LEFT,
                2: BOT_MID,
                3: BOT_RIGHT,
                4: MID_LEFT,
                5: MID,
                6: MID_RIGHT,
                7: TOP_LEFT,
                8: TOP_MID,
                9: TOP_RIGHT
            }
            self.rect.center = switcher[p]
            self.position = True

        elif self.scale < 120:
            self.image = pg.transform.scale(self.image, (self.scale, self.scale))
            self.rect.center = (self.rect.centerx-(SCALE/2), self.rect.centery-(SCALE/2))
            self.scale += SCALE
        else:
            self.position = False
            self.scale = 1
            self.image = pg.transform.scale(self.image, (self.scale, self.scale))


class TrackingEnemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 10))
        self.image.fill(RED)
        self.scale = 1
        self.position = False
        self.colide = False
        self.rect = self.image.get_rect()
        self.rect.center = MID

    def move(self, x_posx, x_posy, screen, score):
        if self.scale < 120:
            self.image = pg.transform.scale(self.image, (self.scale, self.scale))
            self.rect.center = (self.rect.centerx-(SCALE/2), self.rect.centery-(SCALE/2))
            self.scale += SCALE
            return score
        else:
            self.rect.center = (x_posx, x_posy)
            self.scale = 1
            self.image = pg.transform.scale(self.image, (self.scale, self.scale))
            show_score(score, screen)
            return score + 1


def menu(screen):
    pg.display.set_caption("shmup game")
    run = True
    while run:
        screen.fill(WHITE)
         
        text = pg.font.Font("freesansbold.ttf", 50).render("shmup game", True, BLACK)
        text2 = pg.font.Font("freesansbold.ttf", 30).render("press enter to start", True, BLACK)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH/2, HEIGHT/2 - 100)
        
        text_rect2 = text2.get_rect()
        text_rect2.center = (WIDTH/2, HEIGHT/2)
         
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)
          
        for event in pg.event.get():
            if event.type == pg.QUIT:  # check close window
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    run = False
        
        pg.display.update()


def show_score(score, screen):
    scoreFont = pg.font.Font("freesansbold.ttf", 30).render("score: " + str(score), True, BLACK)
    scoreRect = scoreFont.get_rect()
    
    scoreRect.center = (75, 50)
    screen.blit(scoreFont, scoreRect)



# initialize pygame
pg.init()  # start pygame
pg.mixer.init()  # start sound player
screen = pg.display.set_mode((WIDTH, HEIGHT))  # start screen
pg.display.set_caption("new game")
clock = pg.time.Clock()


all_sprites = pg.sprite.Group()  # sprites
mob = pg.sprite.Group()  # enemy group

board = Board()
x = PlayerX()
tracker = TrackingEnemy()
all_sprites.add(board)

for i in range(4):
    e = Enemy()
    mob.add(e)
    all_sprites.add(e)

mob.add(tracker)
all_sprites.add(tracker, x)
all_sprites.update()
time.sleep(0.5)




menu(screen)
screen.fill(BLACK)
pg.display.update()
time.sleep(0.5)

scoree = 0
# game loop
running = True
while running:
    # run at the right speed:
    clock.tick(FPS)

    # process input:
        # get the events that happen while at update and draw
    for event in pg.event.get():
        if event.type == pg.QUIT:  # check close window
            running = False
        if event.type == pg.KEYDOWN:
            x.move()

    # update:
    tracker.move(x.rect.centerx, x.rect.centery, screen, Score)
    all_sprites.update()
        # check for collision
    hits = pg.sprite.spritecollide(x, mob, False)
    if hits:
        for h in hits:
            if h.image.get_size()[0] > 100:
                running = False

    
    Score += 1
    if Score % 15 == 0:
        scoree += 1

    if (Score / 15) % 3 == 0 and Score/15 < 8:
        SCALE += 1

    elif (Score / 15) % 4 == 0 and Score/15 < 15:
        SCALE += 1
    # draw:
    
    screen.fill(WHITE)
    all_sprites.draw(screen) 
    show_score(scoree, screen)
    pg.display.flip()  # after drawing flip the display


