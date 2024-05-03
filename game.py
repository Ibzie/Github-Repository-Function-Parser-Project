import streamlit as st
import pygame
import random

pygame.init()

# Set up the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player
player_width, player_height = 50, 50
player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - player_height - 10
player_speed = 3

# Enemy
enemy_width, enemy_height = 50, 50
enemy_x, enemy_y = random.randint(0, SCREEN_WIDTH - enemy_width), random.randint(50, 150)
enemy_speed = 2

# Game state
game_started = False
game_over = False
score = 0

# Fonts
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_over:
                    game_over = False
                    game_started = True
                    player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - player_height - 10
                    enemy_x, enemy_y = random.randint(0, SCREEN_WIDTH - enemy_width), random.randint(50, 150)
                    score = 0
                else:
                    game_started = True

    if not game_started:
        continue

    if game_over:
        continue

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed

    # Move enemy
    enemy_y += enemy_speed
    if enemy_y > SCREEN_HEIGHT:
        enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
        enemy_y = random.randint(-SCREEN_HEIGHT, -enemy_height)
        score += 1

    # Check for collision
    if (player_x < enemy_x + enemy_width and player_x + player_width > enemy_x and
            player_y < enemy_y + enemy_height and player_y + player_height > enemy_y):
        st.write("You died! Press Enter to play again.")
        game_over = True

    # Clear the screen
    screen.fill(BLACK)

    # Draw player and enemy
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, WHITE, (enemy_x, enemy_y, enemy_width, enemy_height))

    # Draw score
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
