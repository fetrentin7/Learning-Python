import pygame
import random
import sys
from collections import deque
from jogar import batalha
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 40
FONT_SIZE = 24
BACKGROUND_COLOR = (255, 255, 255)
PLAYER_COLOR = (0, 0, 255)
ENEMY_COLOR = (255, 0, 0)
PATH_COLOR = (0, 255, 0)
COLLISION_THRESHOLD = 0.5  # Adjust this value to control collision sensitivity

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Game")

# Create a clock object to control the frame rate
clock = pygame.time.Clock()


# Create the Mapa class
class Mapa:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map_data = [[0] * width for _ in range(height)]

    def generate_map(self):
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < 0.2:
                    self.map_data[y][x] = 1

    def draw_map(self, path=None):
        for y in range(self.height):
            for x in range(self.width):
                cell_color = (0, 0, 0)  # Default color for walls
                if self.map_data[y][x] == 0:
                    if path and (x, y) in path:
                        cell_color = PATH_COLOR  # Color for path cells
                    pygame.draw.rect(screen, cell_color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


# Create the player class
class Player:
    def __init__(self, x, y, weapon, name):
        self.x = x
        self.y = y
        self.weapon = weapon
        self.name = name
        self.health = 100

    def draw(self):
        pygame.draw.rect(screen, PLAYER_COLOR, (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if the new position is within the map boundaries
        if 0 <= new_x < mapa.width and 0 <= new_y < mapa.height:
            # Check if the new position is not blocked by a wall
            if mapa.map_data[new_y][new_x] != 1:
                self.x = new_x
                self.y = new_y

    def attack(self, enemy):
        damage = self.weapon.damage
        enemy.health -= damage

    def died(self):
        if self.health <= 0:
            return True
        return False

    def find_enemy(self, enemies):
        start = (self.x, self.y)
        queue = deque([start])
        visited = set([start])
        path = {}
        found_enemy = False

        while queue:
            current = queue.popleft()

            if current in enemies:
                found_enemy = True
                break

            x, y = current

            # Explore neighboring cells
            neighbors = [
                (x - 1, y),  # Left
                (x + 1, y),  # Right
                (x, y - 1),  # Up
                (x, y + 1)  # Down
            ]

            for nx, ny in neighbors:
                if 0 <= nx < mapa.width and 0 <= ny < mapa.height and (nx, ny) not in visited and mapa.map_data[ny][
                    nx] != 1:
                    queue.append((nx, ny))
                    visited.add((nx, ny))
                    path[(nx, ny)] = current

        if found_enemy:
            # Reconstruct the path from the enemy to the player
            enemy_path = [current]
            while current != start:
                current = path[current]
                enemy_path.append(current)

            # Reverse the path to get the correct order
            enemy_path = enemy_path[::-1]

            return enemy_path

        return None


# Create the enemy class
class Enemy:
    def __init__(self, health, weapon, name):
        valid_position = False
        while not valid_position:
            self.x = random.randint(0, mapa.width - 1)
            self.y = random.randint(0, mapa.height - 1)
            if mapa.map_data[self.y][self.x] != 1:
                valid_position = True
        self.health = health
        self.weapon = weapon
        self.name = name

    def draw(self):
        pygame.draw.rect(screen, ENEMY_COLOR, (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def attack(self, player):
        damage = self.weapon.damage
        player.health -= damage

    def died(self):
        if self.health <= 0:
            return True
        return False

# Create the weapon class
class Arma:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage


mapa = Mapa(SCREEN_WIDTH // BLOCK_SIZE, SCREEN_HEIGHT // BLOCK_SIZE)
mapa.generate_map()

# Declare weapons
Graveto = Arma("Graveto", 1)
EspadaDeMadeira = Arma("Espada de Madeira", 2)
EspadaSimples = Arma("Espada Simples", 4)
MachadoSimples = Arma("Machado Simples", 6)
EspadaLonga = Arma("Espada Longa", 8)
MachadoDuplo = Arma("Machado Duplo", 10)

# Declare enemies
Goblin = Enemy(5, Graveto, "Goblin")
LiderGoblin = Enemy(15, EspadaDeMadeira, "Lider Goblin")
Troll = Enemy(25, EspadaSimples, "Troll")
LiderTroll = Enemy(35, MachadoSimples, "Lider Troll")
Orcc = Enemy(60, EspadaLonga, "Orcc")

# Declare player
Nicolas = Player(1, 1, MachadoDuplo, "Nicolas")

enemies = [Goblin, LiderGoblin, Troll, LiderTroll, Orcc]
remaining_enemies = len(enemies)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Nicolas.move(0, -1)
            elif event.key == pygame.K_DOWN:
                Nicolas.move(0, 1)
            elif event.key == pygame.K_LEFT:
                Nicolas.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                Nicolas.move(1, 0)
            elif event.key == pygame.K_SPACE:
                # Attack the enemy if in range
                for enemy in enemies:
                    distance = math.sqrt((Nicolas.x - enemy.x) ** 2 + (Nicolas.y - enemy.y) ** 2)
                    if distance < COLLISION_THRESHOLD:
                        Nicolas.attack(enemy)

    # Find the enemy closest to the player using BFS
    path = Nicolas.find_enemy([(enemy.x, enemy.y) for enemy in enemies])

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the map
    mapa.draw_map(path)

    # Check for collisions between player and enemies
    for enemy in enemies:
        distance = math.sqrt((Nicolas.x - enemy.x) ** 2 + (Nicolas.y - enemy.y) ** 2)
        if distance < COLLISION_THRESHOLD:
            batalha(Nicolas, enemy)
            if enemy.died():
                enemies.remove(enemy)
                remaining_enemies -= 1

    # Draw the enemies
    for enemy in enemies:
        enemy.draw()

    # Draw the player
    Nicolas.draw()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

    if remaining_enemies == 0:
        running = False

# Quit the game
pygame.quit()
sys.exit()
