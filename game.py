import pygame
import sys
import math

PLAYER_SPRITE_FOLDER = './assets/sprites/'
DEFAULT_SCROLL_SPEED = 5
INITIAL_SCROLL_POSITION = 0

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Window Parameters
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 1000

# Player Parameters
PLAYER_HEIGHT = 48
PLAYER_WIDTH = 48
PLAYER_COLOR = (255, 0, 0)
PLAYER_SPEED = 5

# Obstacles parameters.
OBSTACLE_WIDTH = 200
OBSTACLE_HEIGHT = 70
OBSTACLE_COLOR = (0, 255, 0)

# Each animation sequence has 8 frames
player_animation_frame = [pygame.Rect(PLAYER_WIDTH * i, 0, PLAYER_WIDTH, PLAYER_HEIGHT) for i in range(9)]


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

bg = pygame.image.load("%ssliced_bg.png" % PLAYER_SPRITE_FOLDER).convert()
bg_height = bg.get_height()
bg_rect = bg.get_rect()
tiles = math.ceil(WINDOW_HEIGHT / bg_height) + 1

# Load the sprite sheet
standing_sheet = pygame.image.load('%sStanding.png' % PLAYER_SPRITE_FOLDER)
walking_right_sheet = pygame.image.load('%sWalking_right.png' % PLAYER_SPRITE_FOLDER)
walking_left_sheet = pygame.image.load('%sWalking_left.png' % PLAYER_SPRITE_FOLDER)

scroll = INITIAL_SCROLL_POSITION
scroll_speed = DEFAULT_SCROLL_SPEED

# WINDOW_WIDTH - box_width calculates the space available to center the box
player = Player((WINDOW_WIDTH - PLAYER_WIDTH) // 2, 50)

# Initialize player animation variables
current_frame = 0
last_frame_time = pygame.time.get_ticks()

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
    # Reset the flags for the player's animation
    is_facing_right = False
    is_facing_left = False
    is_standing = False

    # Clicking the x fires a quit event but we need to capture it
    # and get off the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Gets all the keys that have been pressed in this cycle
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= player.speed
        is_facing_left = True
        if check_for_collisions(player, obstacles):
            player.x += player.speed
    if keys[pygame.K_RIGHT]:
        player.x += player.speed
        is_facing_right = True
        if check_for_collisions(player, obstacles):
            player.x -= player.speed
    if keys[pygame.K_UP]:
        scroll -= scroll_speed
        player.y -= player.speed
        is_standing = True
        if check_for_collisions(player, obstacles):
            scroll += scroll_speed
            player.y += player.speed
    if keys[pygame.K_DOWN]:
        player.y += player.speed
        scroll += scroll_speed
        is_standing = True
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

    # Update the background
    clock.tick(FPS)
    for i in range(0, tiles):
        window.blit(bg, (0, i * bg_height + scroll))
        bg_rect.y = i * bg_height + scroll

    for obstacle in obstacles:
        pygame.draw.rect(window, OBSTACLE_COLOR, obstacle)

    # Calculate current frame based on animation speed
    current_time = pygame.time.get_ticks()
    # By updating the frames every 200 milliseconds, the animation looks smooth (smaller values make it faster)
    if current_time - last_frame_time >= 200:
        current_frame = (current_frame + 1) % 4
        last_frame_time = current_time

    # Getting the current frame to draw based on the direction (Note that the frames change so fast that, even if
    # the current frame is not as accurate as it could be, the animation looks smooth)
    frame_ = player_animation_frame[current_frame]
    if is_facing_right:
        window.blit(walking_right_sheet, (player.x, player.y), frame_)
    elif is_facing_left:
        window.blit(walking_left_sheet, (player.x, player.y), frame_)
    else:
        window.blit(standing_sheet, (player.x, player.y), frame_)

    pygame.display.update()

pygame.quit()
sys.exit()
