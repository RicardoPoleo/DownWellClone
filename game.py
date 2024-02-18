import pygame
import sys
from game_objects import *

            

def main():

    #Start Game
    pygame.init() 
    #Create game instance to keep track of game state
    game = GameInstance() 
    #Draw window
    game.start_window()
    pygame.display.set_caption('Drawing a box')
    #Create Player
    player = game.create_player()
    #Create Controller attached to player
    player_controller: Controller = Controller(player)

    # Obtacles parameters.
    obstacle_width = 200
    obstacle_height = 70
    obstacle_color = (0, 255, 0)
    
    # Instantiate obstacles
    game.create_game_object(0  , 200, obstacle_height, obstacle_width, obstacle_color)
    game.create_game_object(300, 400, obstacle_height, obstacle_width, obstacle_color)
    game.create_game_object(0  , 600, obstacle_height, obstacle_width, obstacle_color)

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        # Clicking the x fires a quit event but we need to capture it
        # and get off the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        game.update_collisions()
        player_controller.listen()
        
        #if keys[pygame.K_DOWN]:
        #    player.y += player.speed
        #    if detect_collisions(player, obstacles):
        #        player.y -= player.speed

        # Boundary check
        #if player.x < 0:
        #    player.x = 0
        #if player.x + player.width > WINDOW_WIDTH:
        #    player.x = WINDOW_WIDTH - player.width
        #if player.y < 0:
        #    player.y = 0
        #if player.y + player.height > WINDOW_HEIGHT:
        #    player.y = WINDOW_HEIGHT - player.height

        # This needs to happen before drawing all the other objects
        game.window.fill((255, 255, 255))

        for game_object in game.game_objects:
            pygame.draw.rect(game.window, game_object.color, game_object.rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

main()
