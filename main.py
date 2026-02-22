import pygame
import sys

from spells import spells

pygame.init()

clock = pygame.time.Clock()
fps = 60

# ------------ Constants ------------
# Game Window
BOTTOM_PANEL = 200
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 520 + BOTTOM_PANEL

# Font
text_font = pygame.font.SysFont('copperplate', 30)
resource_font = pygame.font.SysFont('copperplate', 22)

# Character Size
CHARACTER_SIZE_MULTIPLIER = 2.5

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

# Load Settings Menu 

# Load Panel Image
panel_img = pygame.image.load('img/Icons/UI/Scroll.png').convert_alpha()
panel_img = pygame.transform.scale(panel_img, (SCREEN_WIDTH/2, SCREEN_HEIGHT/3))

# Load Resource Images (Health and Mana)
health_img = pygame.image.load('img/Icons/UI/Health.png').convert_alpha()
mana_img = pygame.image.load('img/Icons/UI/Mana.png').convert_alpha()
health_holder_img = pygame.image.load('img/Icons/UI/HealthHolder.png').convert_alpha()
mana_holder_img = pygame.image.load('img/Icons/UI/ManaHolder.png').convert_alpha()
health_holder_img = pygame.transform.scale(health_holder_img, (health_holder_img.get_width() * 0.75, health_holder_img.get_height() * 0.75))
mana_holder_img = pygame.transform.scale(mana_holder_img, (mana_holder_img.get_width() * 0.75, mana_holder_img.get_height() * 0.75))
health_img = pygame.transform.scale(health_img, (health_img.get_width() * 0.75, health_img.get_height() * 0.75))
mana_img = pygame.transform.scale(mana_img, (mana_img.get_width() * 0.75, mana_img.get_height() * 0.75))

# Draw Text
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Draw Background Function
def draw_bg():
    screen.blit(game_bg, (0, 0))

def draw_main_menu():
    screen.blit(main_menu_bg, (0, 0))
    draw_text('Press Any Key to Start', text_font, (255, 255, 255), SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 20)

def draw_settings_menu():
    screen.fill((50, 50, 50))
    draw_text('Settings Menu - Press Any Key to Return', text_font, (255, 255, 255), SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 20)

# Draw Panel Function, indicates Turn Number and Player's Turn, Shows how much damage the player does and the enemy does.
def draw_panel(turn):
    screen.blit(panel_img, (SCREEN_WIDTH / 2 - panel_img.get_width() / 2, 0))
    draw_text(f'Turn: {turn}', text_font, (255, 255, 255), SCREEN_WIDTH / 2 - 225, 20)

# Draw Health and Mana on the bottom left corner of the screen side by side with the icons and the text on top of the icons
def draw_resources(health, mana):
    screen.blit(health_img, (53, SCREEN_HEIGHT - 130))
    screen.blit(health_holder_img, (50, SCREEN_HEIGHT - 60))
    draw_text(f'{health}/{player.max_health}', resource_font, (200, 0, 0), 60, SCREEN_HEIGHT - 95)
    screen.blit(mana_img, (203, SCREEN_HEIGHT - 130))
    screen.blit(mana_holder_img, (200, SCREEN_HEIGHT - 60))
    draw_text(f'{mana}/{player.max_mana}', resource_font, (0, 0, 255), 210, SCREEN_HEIGHT - 95)


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
    def __init__(self, x, y, name, max_health, max_mana, skills):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.max_mana = max_mana
        self.mana = max_mana
        self.skills = skills

        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: idle, 1: attack
        self.update_time = pygame.time.get_ticks()

        # Load idle images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/Characters/{self.name}/Idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * CHARACTER_SIZE_MULTIPLIER, img.get_height() * CHARACTER_SIZE_MULTIPLIER))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load attack images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/Characters/{self.name}/Attack/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * CHARACTER_SIZE_MULTIPLIER, img.get_height() * CHARACTER_SIZE_MULTIPLIER))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def attack(self, target):
        

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

    # Optional Panel: Uncomment if you want to draw the panel image
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