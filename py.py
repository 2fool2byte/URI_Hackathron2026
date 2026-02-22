import pygame
import sys

from spells import spells

pygame.init()

clock = pygame.time.Clock()
fps = 60

# ------------ Constants ------------
BOTTOM_PANEL = 200
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 520 + BOTTOM_PANEL

# -----------------------------------

def open_spells():
    global active_buttons, current_menu
    current_menu = "spells"
    active_buttons = [back_button, fire_button, aqua_button, punch_button]

def back_to_main():
    global active_buttons, current_menu
    current_menu = "main"
    active_buttons = [items_button, spells_button, punch_button]

def fire_spell():
    print("Fire spell cast!")
    back_to_main()

def aqua_spell():
    print("Aqua spell cast!")
    back_to_main()



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Pygame Window")

# Load Images for Background
main_menu_bg = pygame.image.load('img/Backgrounds/main_menu_bg.png').convert_alpha()
main_menu_bg = pygame.transform.scale(main_menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

game_bg = pygame.image.load('img/Backgrounds/game_bg.png').convert_alpha()
game_bg = pygame.transform.scale(game_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Panel Image (optional, but you can use it later)
# panel_img = pygame.image.load('img/panel.png').convert_alpha()

# ---------------------------
# Button Class for Creating Buttons
class Button:
    def __init__(self, x, y, image, scale, action=None):
        self.x = x
        self.y = y
        self.original_image = image
        self.scale = scale
        self.action = action

        # Scale the image first
        width = int(image.get_width() * scale)
        height = int(image.get_height() * scale)
        self.image = pygame.transform.scale(image, (width, height))

        # Then create rect from scaled image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                return True
        return False
# ---------------------------

current_menu = "main" 


# Load Button Images (make sure these exist in the img folder)
items_button_img = pygame.image.load('img/Icons/UI/ItemsButton.png').convert_alpha()
punch_button_img = pygame.image.load('img/Icons/UI/PunchButton.png').convert_alpha()
spells_button_img = pygame.image.load('img/Icons/UI/SpellsButton.png').convert_alpha()

# Create Button Instances (position, scale)
items_button = Button((SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4) - items_button_img.get_width() - 20, BOTTOM_PANEL + 445, items_button_img, 1)
punch_button = Button((SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4) - items_button_img.get_width() / 2 - 20, (BOTTOM_PANEL + 440) - items_button_img.get_height(), punch_button_img, 1)
spells_button = Button((SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4) - 10, BOTTOM_PANEL + 445, spells_button_img, 1, open_spells)

#Spell UI Button Instances
aqua_button_img = pygame.image.load('img/Icons/Spells/AquaBoltButton.png').convert_alpha()
fire_button_img = pygame.image.load('img/Icons/Spells/FireBallButton.png').convert_alpha()
back_button_img = pygame.image.load('img/Icons/UI/Escape.png').convert_alpha()

aqua_button = Button((SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4) - items_button_img.get_width() - 20, BOTTOM_PANEL + 445, aqua_button_img, 1, aqua_spell)
fire_button = Button((SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4) - 10, BOTTOM_PANEL + 445, fire_button_img, 1, fire_spell)
back_button = Button((SCREEN_WIDTH / 2 + SCREEN_WIDTH/2) - 100, (BOTTOM_PANEL + 440) - items_button_img.get_height(), back_button_img, 0.08, back_to_main)
# ---------------------------
# Skill and Character Classes (as in your code)

active_buttons = [items_button, spells_button, punch_button]  # starts with main menu

# Drawing
for button in active_buttons:
    button.draw(screen)

# Event handling
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    for button in active_buttons:
        button.is_clicked(event)

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
        self.action = 1  # 0: idle, 1: attack, 2: hurt, 3: death
        self.update_time = pygame.time.get_ticks()

        # Load idle images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/Characters/{self.name}/Idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load attack images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/Characters/{self.name}/Attack/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
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

    # -----------------------------
    # Draw background
    screen.blit(game_bg, (0, 0))

    # Optional panel
    # screen.blit(panel_img, (0, SCREEN_HEIGHT - BOTTOM_PANEL))

    # Draw buttons depending on current menu
    if current_menu == "main":
        items_button.draw(screen)
        spells_button.draw(screen)
        punch_button.draw(screen)
    elif current_menu == "spells":
        back_button.draw(screen)
        fire_button.draw(screen)
        aqua_button.draw(screen)
        punch_button.draw(screen)

    # Update and draw player
    player.update()
    player.draw()

    # -----------------------------
    # Handle input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pass the event to the buttons for click handling
        if current_menu == "main":
            items_button.is_clicked(event)
            spells_button.is_clicked(event)
            punch_button.is_clicked(event)
        elif current_menu == "spells":
            back_button.is_clicked(event)
            fire_button.is_clicked(event)
            aqua_button.is_clicked(event)

    # Update the display
    pygame.display.update()  # Update the screen



# Quit Pygame
pygame.quit()
sys.exit()