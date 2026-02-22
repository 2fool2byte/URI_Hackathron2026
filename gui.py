import pygame
import sys

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Pygame Window")

start_img = pygame.image.load('start_btn.png').convert_alpha
exit_img = pygame.image.load('exit_button.png').convert_alpha

def Button()

running = True
while running:
    # 1. Handle events (user input, window close, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle other events here (e.g., keyboard presses, mouse clicks)
        # if event.type == pygame.KEYDOWN: ...

    # 2. Game logic and drawing
    # Fill the screen with a color (e.g., white using RGB values)
    screen.fill((255, 255, 255))
    
    # Draw elements onto the screen (e.g., shapes, images)
    # pygame.draw.circle(screen, (0, 0, 0), (100, 100), 50)

    # 3. Update the display
    # This makes everything we've drawn visible
    pygame.display.flip()
    # To control the frame rate
    # clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()