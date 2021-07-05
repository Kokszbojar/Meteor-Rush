# Import the pygame module
import pygame, random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Loading an image of background
bckgr = pygame.image.load("galaxy.png")

# Score variables
score_val = 0

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((60,60))
        self.rect = self.surf.get_rect()
        self.surf = pygame.image.load("battleship.png")
        self.surf.set_alpha(None)
        self.surf.set_colorkey((255,255,255))

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -3)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 3)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def collision(self, col):   # If player collides with and enemy he gets destroyed
        if self.rect.colliderect(col):
            self.kill()

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        x = random.randint(1,4)
        if x == 1:          # x variable is created to make different enemies
            self.surf = pygame.Surface((60, 60))
            self.rect = self.surf.get_rect(center=(1250,random.randint(30,(720-30))))
            self.surf = pygame.image.load("met1.png")
            self.speed = (4)
        elif x == 2:
            self.surf = pygame.Surface((70, 70))
            self.rect = self.surf.get_rect(center=(1245,random.randint(35,(720-35))))
            self.surf = pygame.image.load("met2.png")
            self.speed = (4)
        elif x == 3:
            self.surf = pygame.Surface((80, 80))
            self.rect = self.surf.get_rect(center=(1240,random.randint(40,(720-40))))
            self.surf = pygame.image.load("met3.png")
            self.speed = (3)
        elif x == 4:
            self.surf = pygame.Surface((90, 90))
            self.rect = self.surf.get_rect(center=(1235,random.randint(45,(720-45))))
            self.surf = pygame.image.load("met4.png")
            self.speed = (3)
        self.surf.set_alpha(None)
        self.surf.set_colorkey((255,255,255))   # white color of image is transparent
        
    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            global score_val, player, all_sprites
            if player in all_sprites:       # adding 1 to score per one enemy dodged
                score_val += 1

# Initialize pygame
pygame.init()

# Setting the name of game window and the font
font = pygame.font.Font("QuirkyRobot.ttf", 32)
logo = pygame.image.load("asteroid.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Meteor Rush")

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 800)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

        # Add a new enemy?
        elif event.type == ADDENEMY and len(enemies) < 15:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Check if player got hit by an enemy
    for enemy in enemies:
        player.collision(enemy)
            
    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Update enemy position
    enemies.update()
    
    # Fill the screen with black
    screen.blit(bckgr,(0,0))

    # Show score
    score = font.render("Score: " + str(score_val), True, (40,210,0))
    screen.blit(score, (15,15))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Update the display
    pygame.display.flip()
    
