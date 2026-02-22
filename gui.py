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

# Load Images

# Background Images
main_menu_bg = pygame.image.load('img/Backgrounds/main_menu_bg.png').convert_alpha()
main_menu_bg = pygame.transform.scale(main_menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

game_bg = pygame.image.load('img/Backgrounds/game_bg.png').convert_alpha()
game_bg = pygame.transform.scale(game_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Panel Images
# panel_img = pygame.image.load('panel.png').convert_alpha

# Button Images
# start_img = pygame.image.load('start_btn.png').convert_alpha
# exit_img = pygame.image.load('exit_button.png').convert_alpha

def draw_bg():
    screen.blit(game_bg, (0, 0))

def draw_panel(img):
    screen.blit(img, (0, SCREEN_HEIGHT - BOTTOM_PANEL))

class Character():
    def __init__(self, x, y, name, max_health):
        self.name = name
        self.max_health = max_health
        self.health = max_health

        self.animation_list = []
        self.frame_index = 0
        # 0: idle, 1: attack, 2: hurt, 3: death
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # Load idle images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # Load attack images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def attack(self, target, skill):
        

    def update(self):
        animation_cooldown = 330
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start        
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self):
        screen.blit(self.image, self.rect)

player = Character(150, 250, "Player", 100)


running = True
while running:

    clock.tick(fps)

    draw_bg()
    # draw_panel()

    # Draw Player
    player.draw()
    player.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()






# Quit Pygame
pygame.quit()
sys.exit()