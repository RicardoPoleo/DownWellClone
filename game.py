import pygame
import sys
from game_objects import *
import math

PLAYER_SPRITE_FOLDER = './assets/sprites/'
INITIAL_SCROLL_POSITION = 0

            

def main():

    #Start Game
    pygame.init() 
    #Create game instance to keep track of game state
    game = GameInstance() 
    #Draw window
    game.start_window()
    pygame.display.set_caption('Drawing a box')

    #Create Player
    PLAYER_HEIGHT = 48
    PLAYER_WIDTH = 48
    player = game.create_player(width = PLAYER_WIDTH, height= PLAYER_HEIGHT)

    #Create Controller attached to player
    player_controller: Controller = Controller(player)

    # Obtacles parameters.
    obstacle_width = 200
    obstacle_height = 70
    obstacle_color = (0, 255, 0)
    
    # Each animation sequence has 8 frames
    player_animation_frame = [pygame.Rect(PLAYER_WIDTH * i, 0, PLAYER_WIDTH, PLAYER_HEIGHT) for i in range(9)]

    # Instantiate obstacles
    game.create_game_object(0  , 200, obstacle_height, obstacle_width, obstacle_color)
    game.create_game_object(300, 400, obstacle_height, obstacle_width, obstacle_color)
    game.create_game_object(0  , 600, obstacle_height, obstacle_width, obstacle_color)

    window = game.window 
    if window is None:
        raise RuntimeError("Cannot run without a window")

    bg = pygame.image.load("%ssliced_bg.png" % PLAYER_SPRITE_FOLDER).convert()
    bg_height = bg.get_height()
    bg_rect = bg.get_rect()
    window_height:int = window.get_height()
    tiles = math.ceil(window_height / bg_height) + 1

    # Load the sprite sheet
    standing_sheet = pygame.image.load('%sStanding.png' % PLAYER_SPRITE_FOLDER)
    walking_right_sheet = pygame.image.load('%sWalking_right.png' % PLAYER_SPRITE_FOLDER)
    walking_left_sheet = pygame.image.load('%sWalking_left.png' % PLAYER_SPRITE_FOLDER)

    # Initialize player animation variables
    current_frame = 0
    last_frame_time = pygame.time.get_ticks()
    
    FPS = 60
    clock = pygame.time.Clock()
    running = True

    while running:

        # Reset the flags for the player's animation
        player.facing_dir = None

        # Lock FPS
        clock.tick(FPS)

        # Clicking the x fires a quit event but we need to capture it
        # and get off the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        game.update_collisions()
        player_controller.listen()
        game.update_scroll(bg_height)

        # This needs to happen before drawing all the other objects
        window.fill((255, 255, 255))


        # Calculate current frame based on animation speed
        current_time = pygame.time.get_ticks()

        # By updating the frames every 200 milliseconds, the animation looks smooth 
        # (smaller values make it faster)
        if current_time - last_frame_time >= 200:
            current_frame = (current_frame + 1) % 4
            last_frame_time = current_time

        # Getting the current frame to draw based on the direction (Note that the frames
        # change so fast that, even if the current frame is not as accurate as it could be,
        # the animation looks smooth)
        frame_ = player_animation_frame[current_frame]
        if player.facing_dir == "left":
            window.blit(walking_right_sheet, (player.rect.x, player.rect.y), frame_)
        elif player.facing_dir == "right":
            window.blit(walking_left_sheet, (player.rect.x, player.rect.y), frame_)
        else:
            window.blit(standing_sheet, (player.rect.x, player.rect.y), frame_)

        scroll = game.update_scroll(bg_height)
            
        for i in range(0, tiles):
            window.blit(bg, (0, i * bg_height + scroll))
            bg_rect.y = i * bg_height + scroll

        # Draw non-moving tiles 
        for game_object in game.game_objects:
            pygame.draw.rect(window, game_object.color, game_object.rect)


        pygame.display.update()

    pygame.quit()
    sys.exit()

main()
