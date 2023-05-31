import os
import pygame
import math
from os import listdir
from os.path import isfile, join

from pygame.transform import flip

pygame.init()
pygame.display.set_caption("Game")

WIDTH, HEIGHT = 1280, 720
FPS = 60
PLAYER_SPEED = 5

main_window = pygame.display.set_mode((WIDTH, HEIGHT))


def flip_image(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]  # load files from `assets` and split them images
    # into individual

    all_sprites = {}

    for img in images:
        sprite_sheet = pygame.image.load(join(path, img)).convert_alpha()  # load image and append path

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

            if direction:
                all_sprites[img.replace(".png", "") + "_right"] = sprites
                all_sprites[img.replace(".png", "") + "_left"] = flip_image(sprites)
            else:
                all_sprites[img.replace(".png", "")] = sprites

    return all_sprites


class Player(pygame.sprite.Sprite):
    PLAYER_COLOR = (255, 0, 0)
    GRAVITY_ACC = 1
    SPRITES = load_sprite_sheets("MainCharacters", "VirtualGuy", 32, 32, True)
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__()

        self.sprite = None
        self.rect = pygame.Rect(x, y, width, height)  # add colision and move player around
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.move_check = "left"
        self.animation_counter = 0
        self.fall_counter = 0

    def player_move(self, dis_x, dis_y):
        self.rect.x += dis_x
        self.rect.y += dis_y

    def player_move_right(self, velocity):
        self.x_vel = +velocity
        if self.move_check != "right":
            self.move_check = "right"
            self.animation_counter = 0

    def player_move_left(self, velocity):
        self.x_vel = -velocity
        if self.move_check != "left":
            self.move_check = "left"
            self.animation_counter = 0

    def move_lef_right(self, fps):  # fps variable will increase the y.vel by gravity
        #self.y_vel += min(1, (self.fall_counter / fps) * self.GRAVITY_ACC)
        self.player_move(self.x_vel, self.y_vel)

        self.fall_counter = self.fall_counter + 1

    def draw(self, win):
        self.sprite = self.SPRITES["idle_" + self.move_check][0]
        win.blit(self.sprite, (self.rect.x, self.rect.y))


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    x, y, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            position = (i * width, j * height)
            tiles.append(position)

    return tiles, image


def sprite
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
