import pygame
import random

# Initialize Pygame
pygame.init()


# General variables
points = 0
no_enemies = 6
hitbox_b = 32
hitbox_p = 64
speed = 0.4  # Speed of ship
enemy_speed = 0.4  # Initial speed of enemies

# Create a screen
x = 1000
y = 600
screen = pygame.display.set_mode((x, y))

# Title and Icon
pygame.display.set_caption("Space Invaders")
game_icon = pygame.image.load("ship.png")
pygame.display.set_icon(game_icon)

# Player images
player_icon = pygame.image.load("ship.png")
move_up = pygame.image.load("move_up.png")
move_down = pygame.image.load("move_down.png")
left = pygame.image.load("left.png")
right = pygame.image.load("right.png")
pos_x = 500
pos_y = 500

# Enemy class
class Enemy:
    def __init__(self, x, y, icon_image, speed):
        self.x = x
        self.y = y
        self.icon = pygame.image.load(icon_image)
        self.speed = speed

    def draw(self, screen):
        screen.blit(self.icon, (self.x, self.y))

    def update_position(self):
        self.x += self.speed
        if self.x >= x-64:
            self.y += 32

    def check_bullet_collision(self, bullet_x, bullet_y):
        distance = ((self.x - bullet_x) ** 2 + (self.y - bullet_y) ** 2) ** 0.5
        return distance < hitbox_b

    def check_player_collision(self, player_x, player_y):
        distance = ((self.x - player_x) ** 2 + (self.y - player_y) ** 2) ** 0.5
        return distance < hitbox_p

# Initialize enemies
enemies = []
for i in range(no_enemies):
    enemy = Enemy(random.randint(0, 800), random.randint(40, 120), "enemy.png", enemy_speed)
    enemies.append(enemy)

# Bullet variables
bullet_icon = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = pos_y
bullet_speed = 1.4
bullet_state = 'ready'  # Initialize bullet state

# Function to draw player
def player(pos_x, pos_y, current_icon):
    screen.blit(current_icon, (pos_x, pos_y))

# Function to draw enemies
def draw_enemies():
    for enemy in enemies:
        enemy.draw(screen)

# Function to update enemy positions and speed
def update_enemies():
    global enemy_speed
    for enemy in enemies:
        enemy.update_position()
        if enemy.x < 0 or enemy.x > x - 64:
            enemy.speed = -enemy.speed  # Reverse direction
    enemy_speed += 0.01  # Increase enemy speed gradually

# Function to fire bullet
def fire_bullet(bullet_x, bullet_y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_icon, (bullet_x + 16, bullet_y + 10))

# Function to check bullet collision with enemies
def check_bullet_collisions():
    global bullet_state, bullet_x, bullet_y, points
    for enemy in enemies:
        if bullet_state == 'fire' and enemy.check_bullet_collision(bullet_x, bullet_y):
            bullet_state = 'ready'
            bullet_y = pos_y
            enemy.x = random.randint(0, 800)
            enemy.y = random.randint(40, 120)
            points += 10

# Function to check player collision with enemies
def check_player_collisions():
    global running
    for enemy in enemies:
        if enemy.check_player_collision(pos_x, pos_y):
            print('GAME OVER')
            print(f'Total Points: {points}')
            running = False

# Main game loop
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
running = True

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_x = pos_x
                    fire_bullet(bullet_x, bullet_y)

    keys = pygame.key.get_pressed()

    current_icon = player_icon
    if keys[pygame.K_d]:
        pos_x += speed
        current_icon = right
    elif keys[pygame.K_a]:
        pos_x -= speed
        current_icon = left
    if keys[pygame.K_w]:
        pos_y -= speed
        current_icon = move_up
    elif keys[pygame.K_s]:
        pos_y += speed
        current_icon = move_down

    if pos_x < 0:
        pos_x = 0
    elif pos_x > x - 64:
        pos_x = x - 64

    if pos_y < 0:
        pos_y = 0
    elif pos_y > y - 64:
        pos_y = y - 64

    draw_enemies()

    # Update bullet position
    if bullet_state == 'fire':
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed
    if bullet_y <= 0:
        bullet_y = pos_y
        bullet_state = 'ready'

    # Update enemies
    update_enemies()

    # Check collisions
    check_bullet_collisions()
    check_player_collisions()

    # Draw player
    player(pos_x, pos_y, current_icon)

    # Display FPS and points
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {int(fps)}", True, (0, 0, 0))
    screen.blit(fps_text, (15, 15))
    points_text = font.render(f'POINTS: {points}', True, (0, 0, 0))
    screen.blit(points_text, (15, 55))

    pygame.display.update()
    clock.tick(9999)

pygame.quit()
