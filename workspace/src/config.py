# Configuration constants for CLI Snake Game

# Game window settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20  # Size of each grid cell

# Derived grid size
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Colors (R, G, B)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_DARK_GREEN = (0, 155, 0)
COLOR_DARK_GREY = (40, 40, 40)

# Game settings
FPS = 15

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Controls mapping
KEY_DIRECTION_MAP = {
    'up': UP,
    'down': DOWN,
    'left': LEFT,
    'right': RIGHT
}

# Highscore file
HIGHSCORE_FILE = 'highscore.json'
