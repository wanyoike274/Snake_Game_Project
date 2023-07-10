import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 640, 480
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the clock
clock = pygame.time.Clock()

# Set up the font
font = pygame.font.Font(None, 36)

# Snake initial position and size
snake_pos = [(320, 240)]
snake_size = 1

# Food initial position
food_pos = (random.randint(0, WIDTH // 20 - 1) * 20, random.randint(0, HEIGHT // 20 - 1) * 20)

# Snake initial movement direction
direction = "RIGHT"

# Game state variables
game_over = False
game_restart = False

# Game loop
while not game_restart:
    while not game_over:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_restart = False

            # Change direction based on arrow key press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # Game logic
        # Move the snake
        if direction == "UP":
            new_head = (snake_pos[0][0], snake_pos[0][1] - 20)
        elif direction == "DOWN":
            new_head = (snake_pos[0][0], snake_pos[0][1] + 20)
        elif direction == "LEFT":
            new_head = (snake_pos[0][0] - 20, snake_pos[0][1])
        elif direction == "RIGHT":
            new_head = (snake_pos[0][0] + 20, snake_pos[0][1])

        snake_pos.insert(0, new_head)

        # Check if the snake eats the food
        if snake_pos[0] == food_pos:
            snake_size += 1
            food_pos = (random.randint(0, WIDTH // 20 - 1) * 20, random.randint(0, HEIGHT // 20 - 1) * 20)

        if len(snake_pos) > snake_size:
            snake_pos.pop()

        # Check if the snake hits the boundary
        if snake_pos[0][0] < 0:
            snake_pos[0] = (WIDTH - 20, snake_pos[0][1])
        elif snake_pos[0][0] >= WIDTH:
            snake_pos[0] = (0, snake_pos[0][1])
        elif snake_pos[0][1] < 0:
            snake_pos[0] = (snake_pos[0][0], HEIGHT - 20)
        elif snake_pos[0][1] >= HEIGHT:
            snake_pos[0] = (snake_pos[0][0], 0)

        # Check if the snake hits itself
        for segment in snake_pos[1:]:
            if snake_pos[0] ==segment:
                game_over = True

        # Drawing on the screen
        window.fill(BLACK)
        pygame.draw.rect(window, RED, (food_pos[0], food_pos[1], 20, 20))

        for pos in snake_pos:
            pygame.draw.rect(window, WHITE, (pos[0], pos[1], 20, 20))

        # Display score
        score_text = font.render("Score: {}".format(snake_size - 1), True, GREEN)
        window.blit(score_text, (10, 10))

        # Update the display
        pygame.display.update()

        # Control the game speed
        clock.tick(10)

    # Game over logic
    window.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    window.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + restart_text.get_height() // 2))
    pygame.display.update()

    # Restart or quit handling
    restart = False
    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart = True
                    game_over = False
                    snake_pos = [(320, 240)]
                    snake_size = 1
                    direction = "RIGHT"
                    food_pos = (random.randint(0, WIDTH // 20 - 1) * 20, random.randint(0, HEIGHT // 20 - 1) * 20)
                elif event.key == pygame.K_q:
                    restart = True
                    game_over = False
                    game_restart = True
                    break

# Quit the game
pygame.quit()
