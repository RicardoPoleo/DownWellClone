import random

import pygame
import time

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 400
# Initial position of the rectangle
rect_x = 30
rect_y = 30
rect_width = 30
rect_height = 30

# Player speed in pixels per millisecond (integer-based)
speed = 1

# List of Obstacles
obstacles = []
obstacle_width = 30
obstacle_height = 10
obstacle_speed = 1  # Integer-based speed
obstacle_color = (0, 255, 0)
max_obstacles = 3

pygame.init()

surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Down Well Clone')
player_color = (255, 0, 0)

# Track time for frame rate independence
clock = pygame.time.Clock()
last_time = pygame.time.get_ticks()

# Initialize hit count and max hits
hit_count = 0
max_hits = 3

is_paused = False
is_running = True
is_game_over = False


def update_screen():
    surface.fill((0, 0, 0))
    repaint_player()
    repaint_obstacles()
    pygame.display.flip()


def repaint_obstacles():
    for obstacle_object in obstacles:
        pygame.draw.rect(surface, obstacle_color, obstacle_object)


def repaint_player():
    pygame.draw.rect(surface, player_color, pygame.Rect(rect_x, rect_y, rect_width, rect_height))


def generate_obstacles():
    if len(obstacles) < max_obstacles:
        obstacles_to_generate = max_obstacles - len(obstacles)
        for i in range(obstacles_to_generate):
            obstacle_x = random.randint(0, SCREEN_WIDTH - obstacle_width)
            obstacles.append(pygame.Rect(obstacle_x, SCREEN_HEIGHT, obstacle_width, obstacle_height))


def display_game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", 1, (255, 255, 255))
    surface.blit(text, (110, 250))
    pygame.display.flip()
    time.sleep(5)


def update_player_position():
    global rect_x
    if keys[pygame.K_LEFT]:
        rect_x -= speed * elapsed_time
    if keys[pygame.K_RIGHT]:
        rect_x += speed * elapsed_time
    if rect_x < 0:
        rect_x = 0
    if rect_x + rect_width > SCREEN_WIDTH:
        rect_x = SCREEN_WIDTH - rect_width


generate_obstacles()


def update_obstacles_positions():
    for obstacle_object in obstacles:
        obstacle_object.y -= obstacle_speed * elapsed_time
        if obstacle_object.y <= 0:
            obstacles.remove(obstacle_object)


# Game loop
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_paused = not is_paused
            last_time = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()

    if not is_paused:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - last_time
        last_time = current_time

        # Update the position based on key presses and elapsed time
        update_player_position()

        # Evaluate collisions with obstacles
        for obstacle in obstacles:
            if obstacle.colliderect(pygame.Rect(rect_x, rect_y, rect_width, rect_height)):
                hit_count += 1  # Increment hit count
                if hit_count >= max_hits:
                    is_game_over = True  # Set game over state
                    print("Game Over")
                    display_game_over()
                    break
                obstacles.remove(obstacle)  # Remove obstacle from list

        # Update the position of the obstacles based on elapsed time
        update_obstacles_positions()

        # Generate new obstacles if there are less than the maximum allowed
        generate_obstacles()

        update_screen()
        clock.tick(60)

pygame.quit()
