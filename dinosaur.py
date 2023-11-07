import sys
import os
import random
import pygame.mixer
import time

import pygame as pg


SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [
    pg.image.load(os.path.join("ex05/Assets/Dino", "DinoRun1.png")),
    pg.image.load(os.path.join("ex05/Assets/Dino", "DinoRun2.png")),
]
JUMPING = pg.image.load(os.path.join("ex05/Assets/Dino", "DinoJump.png"))
DUCKING = [
    pg.image.load(os.path.join("ex05/Assets/Dino", "DinoDuck1.png")),
    pg.image.load(os.path.join("ex05/Assets/Dino", "DinoDuck2.png")),
]


BG = pg.image.load(os.path.join("ex05/Assets/Other", "Track.png"))



"""
サウンドの追加

"""
#bgmの追加
def bgm():
    pg.mixer.init() #初期化
    bgm = pygame.mixer.Sound("ex05/Assets/music/maou_bgm_8bit14.ogg")
    bgm.play()

#効果音の追加
def sound_jump():
    pg.mixer.init() #初期化
    bgm_jump = pygame.mixer.Sound("ex05/Assets/music/8bitジャンプ.mp3")
    bgm_jump.play()

def sound_duck():
    pg.mixer.init() #初期化
    bgm_duck = pygame.mixer.Sound("ex05/Assets/music/8bitかわす.mp3")
    bgm_duck.play()



class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pg.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pg.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pg.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1
        sound_duck()

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
        sound_jump()

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))




def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pg.time.Clock()
    player = Dinosaur()
    # 雲
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pg.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    pg.display.set_caption("恐竜ゲーム")

    def score():
        """
        スコアを表示する関数
        """
        global points, game_speed
        points += 0.1  # スコアを0.1ずつ加算する
        if points % 100 == 0:
            game_speed += 1  # スコアを100ごとにゲームスピードを速くする

        text = font.render(f"ScorePoint:{points:.0f}", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                sys.exit()

        SCREEN.fill((255, 255, 255))
        userInput = pg.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        # 鳥　呼び出し
        if len(obstacles) == 0:
            if random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pg.time.delay(2000)

        background()
        # 雲の発生
        cloud.draw(SCREEN)
        cloud.update()
        score()
        clock.tick(30)
        pg.display.update()


if __name__ == "__main__":
    bgm()
    pg.init()
    main()
    pg.quit()
    sys.exit()
