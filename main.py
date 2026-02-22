import pygame
import sys


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
items_button_img = pygame.image.load('img/Icons/UI/ItemsButton.png').convert_alpha()
punch_button_img = pygame.image.load('img/Icons/UI/PunchButton.png').convert_alpha()
spells_button_img = pygame.image.load('img/Icons/UI/SpellsButton.png').convert_alpha()

# Create Button Instances (position, scale)
items_button = Button((SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4) - items_button_img.get_width() - 20, BOTTOM_PANEL + 445, items_button_img, scale=1)
punch_button = Button((SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4) - items_button_img.get_width() / 2 - 20, (BOTTOM_PANEL + 440) - items_button_img.get_height(), punch_button_img, scale=1)
spells_button = Button((SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4) - 10, BOTTOM_PANEL + 445, spells_button_img, scale=1)

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
    def __init__(self, x, y, name, max_health, max_mana):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.max_mana = max_mana
        self.mana = max_mana

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

    # Replaces the selected skill with a new skill, the player can only hold up to 2 skills at a time, 
    # the player can only replace index 1 with basic skills and index 2 with signature skills,
    # the player can only replace a skill after a level is cleared
    

    def updateX(self, x):
        self.rect.x = x

    def updateAction(self, new_action):
        self.action = new_action
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def update(self):
        animation_cooldown = 330
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            if self.action == 0:
                self.updateAction(1)
            elif self.action == 1:
                self.updateAction(0)

    def draw(self):
        screen.blit(self.image, self.rect)

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp  
    
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 200, 20))


    # Method to take damage and reduce health, when called; character will flash white for a brief moment to indicate damage taken
    def take_damage(self, damage):
        self.health -= damage
        self.image = pygame.Surface(self.image.get_size()).convert_alpha()
        # Flash white with some transparency
        self.image.fill((255, 255, 255, 128))
        if self.health < 0:
            self.health = 0
    
    def is_alive(self):
        return self.health > 0

# Create Player Character
player = Character(0, 250, "Player", 100, 100)
# Create Enemy Characters
slime = Character(250, 250, "Slime", 50, 0)
fire_spirit = Character(500, 250, "FireSpirit", 60, 0)
golem = Character(740, 250, "Golem", 80, 0)
witch = Character(1000, 250, "Witch", 70, 0)

# Game Loop
running = True
while running:
    clock.tick(fps)

    # Draw Background and Panel
    draw_bg()
    draw_panel(1)

    # Draw Buttons
    items_button.draw(screen)
    spells_button.draw(screen)
    punch_button.draw(screen)

    # Draw Player
    player.draw()
    player.update()
    slime.draw()
    slime.update()
    fire_spirit.draw()
    fire_spirit.update()
    golem.draw()
    golem.update()
    witch.draw()
    witch.update()

    # Draw Resources (Health and Mana)
    draw_resources(player.health, player.mana)

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

            if spells_button.is_clicked(mouse_pos):
                print("Spells Button Clicked!")
                # Add game logic for Spells Button here

            if punch_button.is_clicked(mouse_pos):
                print("Punch Button Clicked!")
                # Add game logic for Punch Button here

    pygame.display.update()  # Update the screen

# Quit Pygame
pygame.quit()
sys.exit()