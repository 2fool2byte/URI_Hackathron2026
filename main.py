import pygame
import sys
from typing import Dict, List

from spells import Spell, SpellType

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

# Animation
ANIMATION_COOLDOWN = 330

# Color Constants
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_DARK_GRAY = (50, 50, 50)

# -----------------------------------

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Pygame Window")

# Image cache for efficient loading
_image_cache: Dict[str, pygame.Surface] = {}

def load_image(path: str, scale: tuple = None) -> pygame.Surface:
    """Load image from cache or disk. Apply scaling if provided."""
    if path in _image_cache and scale is None:
        return _image_cache[path]
    
    img = pygame.image.load(path).convert_alpha()
    if scale:
        img = pygame.transform.scale(img, scale)
    
    if scale is None:
        _image_cache[path] = img
    
    return img

# Load Images for Background
main_menu_bg = load_image('img/Backgrounds/main_menu_bg.png', (SCREEN_WIDTH, SCREEN_HEIGHT))
game_bg = load_image('img/Backgrounds/game_bg.png', (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Panel Image
panel_img = load_image('img/Icons/UI/Scroll.png', (SCREEN_WIDTH/2, SCREEN_HEIGHT/3))

# Load Resource Images (Health and Mana) - scaled to 75% of original size
def scale_resource_image(path: str, scale_factor: float = 0.75) -> pygame.Surface:
    img = load_image(path)
    return pygame.transform.scale(img, (img.get_width() * scale_factor, img.get_height() * scale_factor))

health_img = scale_resource_image('img/Icons/UI/Health.png')
mana_img = scale_resource_image('img/Icons/UI/Mana.png')
health_holder_img = scale_resource_image('img/Icons/UI/HealthHolder.png')
mana_holder_img = scale_resource_image('img/Icons/UI/ManaHolder.png')

# Draw Text
def draw_text(text: str, font: pygame.font.Font, color: tuple, x: float, y: float) -> None:
    """Render and blit text to the screen."""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Draw Background Function
def draw_bg() -> None:
    """Draw the game background."""
    screen.blit(game_bg, (0, 0))

def draw_main_menu() -> None:
    """Draw the main menu screen."""
    screen.blit(main_menu_bg, (0, 0))
    draw_text('Press Any Key to Start', text_font, COLOR_WHITE, SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 20)

def draw_settings_menu() -> None:
    """Draw the settings menu screen."""
    screen.fill(COLOR_DARK_GRAY)
    draw_text('Settings Menu - Press Any Key to Return', text_font, COLOR_WHITE, SCREEN_WIDTH / 2 - 250, SCREEN_HEIGHT / 2 - 20)

# Draw Panel Function
def draw_panel(turn: int) -> None:
    """Draw the panel indicating turn number."""
    screen.blit(panel_img, (SCREEN_WIDTH / 2 - panel_img.get_width() / 2, 0))
    draw_text(f'Turn: {turn}', text_font, COLOR_WHITE, SCREEN_WIDTH / 2 - 225, 20)

# Draw Resources
def draw_resources(health: int, mana: int) -> None:
    """Draw player health and mana on the screen."""
    screen.blit(health_img, (53, SCREEN_HEIGHT - 130))
    screen.blit(health_holder_img, (50, SCREEN_HEIGHT - 60))
    draw_text(f'{health}/100', resource_font, COLOR_RED, 60, SCREEN_HEIGHT - 95)
    screen.blit(mana_img, (203, SCREEN_HEIGHT - 130))
    screen.blit(mana_holder_img, (200, SCREEN_HEIGHT - 60))
    draw_text(f'{mana}/100', resource_font, COLOR_BLUE, 210, SCREEN_HEIGHT - 95)


# Button positioning constants
BUTTON_BASE_X = SCREEN_WIDTH / 2 + SCREEN_WIDTH / 4
BUTTON_BASE_Y = BOTTOM_PANEL + 445

class Button:
    """Clickable button UI element."""
    
    def __init__(self, x: float, y: float, image: pygame.Surface, scale: float = 1.0) -> None:
        self.x = x
        self.y = y
        self.original_image = image
        self.scale = scale
        self.rect = self.original_image.get_rect()
        self.rect.topleft = (x, y)
        self._update_image()
    
    def _update_image(self) -> None:
        """Update the scaled image based on current scale."""
        self.image = pygame.transform.scale(
            self.original_image,
            (int(self.rect.width * self.scale), int(self.rect.height * self.scale))
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the button on the given surface."""
        surface.blit(self.image, self.rect)

    def is_clicked(self, pos: tuple) -> bool:
        """Check if the button was clicked at the given position."""
        return self.rect.collidepoint(pos)



# Load Button Images
items_button_img = load_image('img/Icons/UI/ItemsButton.png')
punch_button_img = load_image('img/Icons/UI/PunchButton.png')
spells_button_img = load_image('img/Icons/UI/SpellsButton.png')

# Calculate button dimensions for positioning
BUTTON_WIDTH = items_button_img.get_width()
BUTTON_HEIGHT = items_button_img.get_height()

# Create Button Instances with optimized positioning
items_button = Button(BUTTON_BASE_X - BUTTON_WIDTH - 20, BUTTON_BASE_Y, items_button_img, scale=1)
punch_button = Button(BUTTON_BASE_X - BUTTON_WIDTH / 2 - 20, BUTTON_BASE_Y - BUTTON_HEIGHT, punch_button_img, scale=1)
spells_button = Button(BUTTON_BASE_X - 10, BUTTON_BASE_Y, spells_button_img, scale=1)


class Skill:
    """Represents a usable skill with damage, mana cost, and cooldown mechanics."""
    
    def __init__(self, name: str, damage: int, mana_cost: int, element: str, 
                 skill_type: int, max_cooldown: int) -> None:
        self.name = name
        self.damage = damage
        self.mana_cost = mana_cost
        self.element = element
        self.type = skill_type  # 0 = basic, 1 = signature
        self.max_cooldown = max_cooldown
        self.cooldown = 0
    
    def get_damage(self) -> int:
        """Return the damage of this skill."""
        return self.damage
    
    def reduce_cooldown(self) -> None:
        """Reduce cooldown by 1 if active."""
        if self.cooldown > 0:
            self.cooldown -= 1
    
    def use_skill(self) -> None:
        """Activate the skill cooldown."""
        self.cooldown = self.max_cooldown


class Character:
    """Character class managing animations, resources, and combat."""
    
    def __init__(self, x: float, y: float, name: str, max_health: int, 
                 max_mana: int, skills: List[Skill] = None) -> None:
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.max_mana = max_mana
        self.mana = max_mana
        self.skills = skills or []

        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: idle, 1: attack
        self.update_time = pygame.time.get_ticks()

        # Load animations
        self._load_animations()
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def _load_animations(self) -> None:
        """Load all character animations from disk."""
        # Load idle animations
        idle_frames = []
        for i in range(4):
            img = load_image(f'img/Characters/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(
                img,
                (int(img.get_width() * CHARACTER_SIZE_MULTIPLIER),
                 int(img.get_height() * CHARACTER_SIZE_MULTIPLIER))
            )
            idle_frames.append(img)
        self.animation_list.append(idle_frames)

        # Load attack animations
        attack_frames = []
        for i in range(4):
            img = load_image(f'img/Characters/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(
                img,
                (int(img.get_width() * CHARACTER_SIZE_MULTIPLIER),
                 int(img.get_height() * CHARACTER_SIZE_MULTIPLIER))
            )
            attack_frames.append(img)
        self.animation_list.append(attack_frames)

    def update_skill(self, skill: Skill, index: int = 1) -> None:
        """Replace a skill at the specified index."""
        if index < len(self.skills):
            self.skills[index] = skill
        else:
            self.skills.append(skill)

    def update_x(self, x: float) -> None:
        """Update character X position."""
        self.rect.x = x

    def take_damage(self, damage: int) -> None:
        """Reduce health by damage amount."""
        self.health = max(0, self.health - damage)

    def restore_mana(self, amount: int) -> None:
        """Increase mana up to max."""
        self.mana = min(self.max_mana, self.mana + amount)

    def use_mana(self, amount: int) -> bool:
        """Use mana if available. Returns True if successful."""
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False

    def is_alive(self) -> bool:
        """Check if character is still alive."""
        return self.health > 0

    def update(self) -> None:
        """Update character animation."""
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def draw(self) -> None:
        """Draw character on screen."""
        screen.blit(self.image, self.rect)


# Create Player Character
player = Character(25, 250, "Player", max_health=100, max_mana=100, skills=[])

# Create Enemy Characters (pre-allocated for efficiency)
enemies = {
    "Slime": Character(900, 250, "Slime", max_health=50, max_mana=0, skills=[]),
    "FireSpirit": Character(900, 250, "FireSpirit", max_health=60, max_mana=0, skills=[]),
    "Golem": Character(900, 250, "Golem", max_health=80, max_mana=0, skills=[]),
    "Witch": Character(900, 250, "Witch", max_health=70, max_mana=0, skills=[])
}

current_enemy = None  # Will be set when a battle starts
turn = 1

# Game Loop
running = True
while running:
    clock.tick(fps)  # Cap frame rate for consistent performance

    # Draw Background and Panel
    draw_bg()
    draw_panel(turn)

    # Draw Buttons
    items_button.draw(screen)
    spells_button.draw(screen)
    punch_button.draw(screen)

    # Update and draw Player
    player.update()
    player.draw()

    # Draw Resources (Health and Mana)
    draw_resources(player.health, player.mana)

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # Get mouse position

            # Check button clicks
            if items_button.is_clicked(mouse_pos):
                print("Items Button Clicked!")
                # Add game logic here

            elif spells_button.is_clicked(mouse_pos):
                print("Spells Button Clicked!")
                # Add game logic here

            elif punch_button.is_clicked(mouse_pos):
                print("Punch Button Clicked!")
                # Add game logic here

    pygame.display.update()  # Update the display once per frame

# Cleanup resources
pygame.quit()
sys.exit()