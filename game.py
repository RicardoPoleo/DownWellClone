import pygame
import sys

pygame.init()

# Window Parameters
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 1000

# Player Paremeters
PLAYER_HEIGHT = 30
PLAYER_WIDTH = 30
PLAYER_COLOR = (255, 0, 0)
PLAYER_SPEED = 5

# Obtacles parameters.
OBSTACLE_WIDTH = 200
OBSTACLE_HEIGHT = 70
OBSTACLE_COLOR = (0, 255, 0)

class GameObject:
    """ Generic game object class
    """
    __slots__ = ("x", "y", "width", "height", "speed", "color")

    def __init__(self, x, y, height, width, speed, color):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.speed: int = speed
        self.color = color

    def check_collision(self, other: GameObject) -> bool:
        """ Check that two game objects are colliding with one another
        """
        pass        

class Player(GameObject):
    """ Player game object class
    """
    __slots__ = ("x", "y", "width", "height", "speed", "color", "fall_frames")

    def __init__(self, x, y, height, width, speed, color):
        super().__init__(x, y, height, width, speed, color)
        self.fall_frames: int = 0

    def has_collided(self, obstacle: pygame.Rect) -> bool:
        """ Check collision between player and an individual gameobject
        """
        hit_box = pygame.Rect(self.x, self.y, self.width, self.height)
        return hit_box.colliderect(obstacle)

    def update_fall_frames(self, obstacles: list[pygame.Rect]) -> None:
        """ Determine if the player is falling and how long it's been falling for
        Params:
           obstacles: all obstacles currently colliding with the player 
        """
        for obstacle in obstacles:
            if obstacle.y <= player.y:
                self.fall_frames = 0
        self.fall_frames += 1

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Drawing a box')

# WINDOW_WIDTH - box_width calculates the space available to center the box
player = Player((WINDOW_WIDTH - PLAYER_WIDTH) // 2, 50)

obstacles = [
    pygame.Rect(0, 200, OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
    pygame.Rect(300, 400, OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
    pygame.Rect(0, 600, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
]

def detect_collisions(player: Player, obstacles: list[pygame.Rect]) -> list[pygame.Rect]:
    """ Check which gameobjects the player currently collides with.
    
    Params:
        player: movable gameobject.
        obstacles: other gameobjects with collisions.
    Return:
        A list with all gameobjects the player currently collides with

    """
    
    collision_list = []

    for obstacle in obstacles:
        if player.has_collided(obstacle):
           collision_list.append(obstacle) 

    return collision_list

running = True
while running:
    # Clicking the x fires a quit event but we need to capture it
    # and get off the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    colliding_objects = detect_collisions(player, obstacles)
    player.update_fall_frames(obstacles) 
    player.y += int(player.fall_frames * 0.1)

    # Gets all the keys that have been pressed in this cycle
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= player.speed
        if detect_collisions(player, obstacles):
            player.x += player.speed
    if keys[pygame.K_RIGHT]:
        player.x += player.speed
        if detect_collisions(player, obstacles):
            player.x -= player.speed
    if keys[pygame.K_UP]:
        player.y -= player.speed
        if detect_collisions(player, obstacles):
            player.y += player.speed
    
    #if keys[pygame.K_DOWN]:
    #    player.y += player.speed
    #    if detect_collisions(player, obstacles):
    #        player.y -= player.speed

    # Boundary check
    if player.x < 0:
        player.x = 0
    if player.x + player.width > WINDOW_WIDTH:
        player.x = WINDOW_WIDTH - player.width
    if player.y < 0:
        player.y = 0
    if player.y + player.height > WINDOW_HEIGHT:
        player.y = WINDOW_HEIGHT - player.height

    # This needs to happen before drawing all the other objects
    window.fill((255, 255, 255))

    for obstacle in obstacles:
        pygame.draw.rect(window, OBSTACLE_COLOR, obstacle)

    pygame.draw.rect(window, player.color, (player.x, player.y, player.width, player.height))
    pygame.display.flip()

pygame.quit()
sys.exit()


