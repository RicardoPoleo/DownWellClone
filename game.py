import pygame
import sys
from game_objects import *
            

def main():

    pygame.init()
    game_instance = GameInstance()
    window = pygame.display.set_mode((game_instance.window_width, game_instance.window_height))
    pygame.display.set_caption('Drawing a box')
    player_controller = game_instance.create_player()
    player: Pawn = player_controller[0]
    controller: Controller = player_controller[1]

    # Obtacles parameters.
    obstacle_width = 200
    obstacle_height = 70
    obstacle_color = (0, 255, 0)
    
    # Instantiate obstacles
    game_instance.create_game_object(0, 200, obstacle_width, obstacle_height, obstacle_color)
    game_instance.create_game_object(300, 400, obstacle_width, obstacle_height, obstacle_color)
    game_instance.create_game_object(0, 600, obstacle_width, obstacle_height, obstacle_color)

    running = True
    while running:
        # Clicking the x fires a quit event but we need to capture it
        # and get off the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        controller.listen()
        
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

main()
