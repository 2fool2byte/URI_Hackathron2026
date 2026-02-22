import pygame
import sys

pygame.init()

clock = pygame.time.Clock()
fps = 60

# ------------ Constants ------------
BOTTOM_PANEL = 200
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 520 + BOTTOM_PANEL

# -----------------------------------

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Pygame Window")

# Load Images for Background
main_menu_bg = pygame.image.load('img/Backgrounds/main_menu_bg.png').convert_alpha()
main_menu_bg = pygame.transform.scale(main_menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

game_bg = pygame.image.load('img/Backgrounds/game_bg.png').convert_alpha()
game_bg = pygame.transform.scale(game_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Panel Image (optional, but you can use it later)
#panel_img = pygame.image.load('img/panel.png').convert_alpha()

# ---------------------------
# Button Class for Creating Buttons
class Button():
    def __init__(self, x, y, image, scale=1):
        self.x = x
        self.y = y
        self.image = image
        self.original_image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.scale = scale
        self.image = pygame.transform.scale(self.image, (self.rect.width * scale, self.rect.height * scale))

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# ---------------------------

# Load Button Images (make sure these exist in the img folder)
items_button_img = pygame.image.load('img/Icons\\Spells/ItemsButton.png').convert_alpha()
leafstorm_button_img = pygame.image.load('img/Icons\\Spells/LeafStormButton.png').convert_alpha()
punch_button_img = pygame.image.load('img/Icons\\Spells/PunchButton.png').convert_alpha()
aquabolt_button_img = pygame.image.load('img/Icons\\Spells/AquaBoltButton.png').convert_alpha()

# Create Button Instances (position, scale)
items_button = Button(SCREEN_WIDTH/2 + SCREEN_WIDTH/3, 400, items_button_img, scale=0.5)
leafstorm_button = Button(SCREEN_WIDTH/3, 400, leafstorm_button_img, scale=0.5)
punch_button = Button(500, 400, punch_button_img, scale=0.5)
aquabolt_button = Button(700, 400, aquabolt_button_img, scale=0.5)

# ---------------------------
# Skill and Character Classes (as in your code)

class Skill():
    def __init__(self, name, damage, mana_cost, element, type, max_cooldown):
        self.name = name
        self.damage = damage
        self.mana_cost = mana_cost
        self.element = element
        self.type = type  # 0 = basic, 1 = signature
        self.max_cooldown = max_cooldown
        self.cooldown = 0
    
    def getDamage(self):
        return self.damage

class Character():
    def __init__(self, x, y, name, max_health):
        self.name = name
        self.max_health = max_health
        self.health = max_health

        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: idle, 1: attack, 2: hurt, 3: death
        self.update_time = pygame.time.get_ticks()

        # Load idle images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load attack images (currently not in use, as no attack animations)
        temp_list = []
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        animation_cooldown = 330
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def draw(self):
        screen.blit(self.image, self.rect)

player = Character(150, 250, "Player", 100)

# Game Loop
running = True
while running:
    clock.tick(fps)

    # Draw Background and Panel
    screen.blit(game_bg, (0, 0))
    #screen.blit(panel_img, (0, SCREEN_HEIGHT - BOTTOM_PANEL))

    # Draw Buttons
    items_button.draw(screen)
    leafstorm_button.draw(screen)
    punch_button.draw(screen)
    aquabolt_button.draw(screen)

    # Draw Player
    player.draw()
    player.update()

    # Handle Mouse Clicks
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # Get mouse position

            # Check if any button was clicked and perform actions
            if items_button.is_clicked(mouse_pos):
                print("Items Button Clicked!")
                # Add game logic for Items Button here

            if leafstorm_button.is_clicked(mouse_pos):
                print("LeafStorm Button Clicked!")
                # Add game logic for LeafStorm Button here

            if punch_button.is_clicked(mouse_pos):
                print("Punch Button Clicked!")
                # Add game logic for Punch Button here

            if aquabolt_button.is_clicked(mouse_pos):
                print("AquaBolt Button Clicked!")
                # Add game logic for AquaBolt Button here

    pygame.display.update()  # Update the screen

# Quit Pygame
pygame.quit()
sys.exit()