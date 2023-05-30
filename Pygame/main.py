import os
import pygame
import math
from os import listdir
from os.path import isfile, join

pygame.init()
pygame.display.set_caption("Game")

WIDTH, HEIGHT = 1280, 720
FPS = 60
PLAYER_SPEED = 5

main_window = pygame.display.set_mode((WIDTH, HEIGHT))


class Player(pygame.sprite.Sprite):
    PLAYER_COLOR = (255, 0, 0)
    GRAVITY_ACC = 1

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)  # add colision and move player around
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.move_check = 'Left'
        self.animation_counter = 0
        self.fall_counter = 0
    def player_move(self, dis_x, dis_y):
        self.rect.x += dis_x
        self.rect.y += dis_y

    def player_move_right(self, velocity):
        self.x_vel = +velocity
        if self.move_check != 'Right':
            self.move_check = 'Right'
            self.animation_counter = 0

    def player_move_left(self, velocity):
        self.x_vel = -velocity
        if self.move_check != 'Left':
            self.move_check = 'Left'
            self.animation_counter = 0

    def move_lef_right(self, fps):  # fps variable will increase the y.vel by gravity
        self.y_vel += min(1, (self.fall_counter/fps) * self.GRAVITY_ACC)
        self.player_move(self.x_vel, self.y_vel)

        self.fall_counter = self.fall_counter + 1
    def draw(self, win):
        pygame.draw.rect(win, self.PLAYER_COLOR, self.rect)


def get_background(name):
    image = pygame.image.load(join('assets', 'Background', name))
    x, y, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            position = (i * width, j * height)
            tiles.append(position)

    return tiles, image


def draw(window, background, bg_image, player):
    for tile in background:
        window.blit(bg_image, tile)

    player.draw(window)
    pygame.display.update()


def movement(player):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.player_move_left(PLAYER_SPEED)

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.player_move_right(PLAYER_SPEED)


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    player = Player(100, 100, 50, 50)

    runner = True
    while runner:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runner = False
                break

        player.move_lef_right(FPS)
        movement(player)
        draw(window, background, bg_image, player)
    pygame.quit()


if __name__ == "__main__":
    main(main_window)
