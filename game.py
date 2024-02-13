import pygame
import sys
import math

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Window Parameters
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 1000

# Player Parameters
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 100
PLAYER_COLOR = (255, 0, 0)
PLAYER_SPEED = 5

# Obstacles parameters.
OBSTACLE_WIDTH = 200
OBSTACLE_HEIGHT = 70
OBSTACLE_COLOR = (0, 255, 0)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_HEIGHT
        self.height = PLAYER_WIDTH
        self.speed = PLAYER_SPEED
        self.color = PLAYER_COLOR

    def has_collided(self, obstacle):
        hit_box = pygame.Rect(self.x, self.y, self.width, self.height)
        return hit_box.colliderect(obstacle)


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Drawing a box')

bg = pygame.image.load("./assets/sprites/sliced_bg.png").convert()
bg_height = bg.get_height()
bg_rect = bg.get_rect()
tiles = math.ceil(WINDOW_HEIGHT / bg_height) + 1

scroll = 0
scroll_speed = 5

# WINDOW_WIDTH - box_width calculates the space available to center the box
player = Player((WINDOW_WIDTH - PLAYER_WIDTH) // 2, 50)

obstacles = [
    pygame.Rect(40, 200, OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
    pygame.Rect(300, 400, OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
    pygame.Rect(40, 600, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
]


def check_for_collisions(player, obstacles):
    for obstacle in obstacles:
        if player.has_collided(obstacle):
            return True
    return False


running = True
while running:

    # Clicking the x fires a quit event but we need to capture it
    # and get off the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Gets all the keys that have been pressed in this cycle
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= player.speed
        if check_for_collisions(player, obstacles):
            player.x += player.speed
    if keys[pygame.K_RIGHT]:
        player.x += player.speed
        if check_for_collisions(player, obstacles):
            player.x -= player.speed
    if keys[pygame.K_UP]:
        scroll -= scroll_speed
        player.y -= player.speed
        if check_for_collisions(player, obstacles):
            scroll += scroll_speed
            player.y += player.speed
    if keys[pygame.K_DOWN]:
        player.y += player.speed
        scroll += scroll_speed
        if check_for_collisions(player, obstacles):
            player.y -= player.speed
            scroll -= scroll_speed

    # reset scroll
    if scroll > bg_height:
        scroll = 0
    if scroll < -bg_height:
        scroll = 0

    if player.x < 0:
        player.x = 0
    if player.x + player.width > WINDOW_WIDTH:
        player.x = WINDOW_WIDTH - player.width
    if player.y < 0:
        player.y = 0
    if player.y + player.height > WINDOW_HEIGHT:
        player.y = WINDOW_HEIGHT - player.height

    clock.tick(FPS)
    for i in range(0, tiles):
        window.blit(bg, (0, i * bg_height + scroll))
        bg_rect.y = i * bg_height + scroll

    for obstacle in obstacles:
        pygame.draw.rect(window, OBSTACLE_COLOR, obstacle)

    pygame.draw.rect(window, player.color, (player.x, player.y, player.width, player.height))
    pygame.display.flip()

pygame.quit()
sys.exit()
