from typing import Optional, Tuple, List
from src.utils import get_random_position

class GameEngine:
    DIRECTIONS = {
        'UP': (0, -1),
        'DOWN': (0, 1),
        'LEFT': (-1, 0),
        'RIGHT': (1, 0),
    }

    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.reset_game()

    def reset_game(self):
        # Initialize snake in middle
        mid_x = self.width // 2
        mid_y = self.height // 2
        self.snake: List[Tuple[int, int]] = [(mid_x, mid_y), (mid_x-1, mid_y), (mid_x-2, mid_y)]
        self.direction = 'RIGHT'
        self.food = self.spawn_food()
        self.score = 0
        self.running = False
        self.paused = False
        self.game_over = False

    def spawn_food(self):
        exclude = set(self.snake)
        return get_random_position(self.width, self.height, exclude)

    def start(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.game_over = False

    def pause(self):
        if self.running:
            self.paused = not self.paused

    def restart(self):
        self.reset_game()
        self.start()

    def update(self, input_key: Optional[str]) -> None:
        if input_key == 'QUIT':
            self.running = False
            return

        if not self.running or self.game_over or self.paused:
            # Only allow pause toggle or restart
            if input_key == 'PAUSE':
                self.pause()
            elif input_key == 'RESTART':
                self.restart()
            return

        # Change direction if valid and not opposite
        if input_key in self.DIRECTIONS:
            opposite = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
            if input_key != opposite[self.direction]:
                self.direction = input_key

        # Move snake
        self.move_snake()

    def move_snake(self):
        head_x, head_y = self.snake[0]
        dx, dy = self.DIRECTIONS[self.direction]
        new_head = (head_x + dx, head_y + dy)

        # Check collisions
        if (
            new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height or
            new_head in self.snake
        ):
            self.game_over = True
            self.running = False
            return

        # Add new head
        self.snake.insert(0, new_head)

        # Check if food eaten
        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            # Remove tail
            self.snake.pop()
