import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Define the snake class
class Snake:
    def __init__(self):
        self.size = 1
        self.positions = [(window_width // 2, window_height // 2)]
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        self.direction = random.choice(directions)

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + (x * gridsize)) % window_width, (cur[1] + (y * gridsize)) % window_height)
        if len(self.positions) > 2 and new in self.positions[2:] or new == self.get_head_position():
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.size:
                self.positions.pop()
        return True

    def reset(self):
        self.size = 1
        self.positions = [(window_width // 2, window_height // 2)]
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        self.direction = random.choice(directions)

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, GREEN, (p[0], p[1], gridsize, gridsize))

# Define the food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, window_width - gridsize) // gridsize * gridsize,
                         random.randint(0, window_height - gridsize) // gridsize * gridsize)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], gridsize, gridsize))

# Define game constants
gridsize = 20
clock = pygame.time.Clock()
score = 0

# Define game states
STATE_PLAYING = 0
STATE_GAME_OVER = 1

# Initialize the snake and food
snake = Snake()
food = Food()

# Initialize the game state
game_state = STATE_PLAYING

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == STATE_PLAYING:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)
            elif game_state == STATE_GAME_OVER:
                if event.key == pygame.K_r:  # Restart the game
                    snake.reset()
                    food.randomize_position()
                    score = 0
                    game_state = STATE_PLAYING
                elif event.key == pygame.K_q:  # Quit the game
                    running = False

    # Game logic
    if game_state == STATE_PLAYING:
        # Move the snake
        game_over = not snake.move()

        # Check for collisions with the food
        if snake.get_head_position() == food.position:
            snake.size += 1
            food.randomize_position()
            score += 1

        # Check for collisions with the walls
        if (
            snake.get_head_position()[0] < 0
            or snake.get_head_position()[0] >= window_width
            or snake.get_head_position()[1] < 0
            or snake.get_head_position()[1] >= window_height
        ):
            game_over = True

        if game_over:
            game_state = STATE_GAME_OVER

    # Render
    window.fill(BLACK)

    if game_state == STATE_PLAYING:
        snake.draw(window)
        food.draw(window)

        # Display the score on the window
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, GREEN)
        window.blit(score_text, (10, 10))
    elif game_state == STATE_GAME_OVER:
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over", True, WHITE)
        restart_text = font.render("Press 'R' to restart or 'Q' to quit", True, WHITE)
        window.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, 200))
        window.blit(restart_text, (window_width // 2 - restart_text.get_width() // 2, 300))

    pygame.display.flip()

    # Set the frame rate
    clock.tick(10)  # Adjust the value to change the game speed

# Quit the game
pygame.quit()





