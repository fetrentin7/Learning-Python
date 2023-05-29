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

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height) #add colision and move player around
        self.x_vel = 0
        self.y_vel = 0


def get_background(name):
    image = pygame.image.load(join('assets', 'Background', name))
    x, y, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            position = (i * width, j * height)
            tiles.append(position)

    return tiles, image


def draw(window, background, bg_image):
    for tile in background:
        window.blit(bg_image, tile)

    pygame.display.update()


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    runner = True
    while runner:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runner = False
                break

        draw(window, background, bg_image)

    pygame.quit()


if __name__ == "__main__":
    main(main_window)
