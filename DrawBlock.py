import pygame

SCREEN_WIDTH = 400

pygame.init()

surface = pygame.display.set_mode((SCREEN_WIDTH, 300))
pygame.display.set_caption('Downwell Clone')
color = (255, 0, 0)

# Initial position of the rectangle
rect_x = 30
rect_y = 30

# Rectangle dimensions
rect_width = 30
rect_height = 30

# Movement speed
speed = 0.1

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Update the position based on key presses
    if keys[pygame.K_LEFT]:
        rect_x -= speed
    if keys[pygame.K_RIGHT]:
        rect_x += speed

    # Boundary checks to keep the rectangle within the screen
    if rect_x < 0:
        rect_x = 0
    if rect_x + rect_width > SCREEN_WIDTH:  # Assuming screen width is 400
        rect_x = SCREEN_WIDTH - rect_width

    # Clear the screen
    surface.fill((0, 0, 0))

    # Draw the rectangle at the updated position
    pygame.draw.rect(surface, color, pygame.Rect(rect_x, rect_y, rect_width, rect_height))
    pygame.display.flip()
