import random
from src.constants import GRID_WIDTH, GRID_HEIGHT, STATE_RUNNING, STATE_GAMEOVER

class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        # Initialize snake in middle of grid
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # List of (x,y) tuples
        self.direction = (1, 0)  # Default right
        self.score = 0
        self.spawn_food()
        self.state = STATE_RUNNING

    def spawn_food(self):
        # Spawn food in random position not occupied by snake
        while True:
            self.food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if self.food not in self.snake:
                break

    def update(self, direction):
        if self.state != STATE_RUNNING:
            return

        # Update the direction with the given one
        # Prevent reversing direction directly
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check collisions with walls
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            self.state = STATE_GAMEOVER
            return

        # Check collision with self
        if new_head in self.snake:
            self.state = STATE_GAMEOVER
            return

        # Insert new head
        self.snake.insert(0, new_head)

        # Check if food eaten
        if new_head == self.food:
            self.score += 1
            self.spawn_food()
            # Snake grows (do not remove tail)
        else:
            # Remove tail segment (snake moves)
            self.snake.pop()

    def get_state(self):
        return {
            'snake': self.snake,
            'food': self.food,
            'score': self.score,
            'state': self.state
        }
