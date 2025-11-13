# Constants used throughout the CLI Snake Game

# Screen size (width x height in pixels)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Grid size (we will use blocks to represent snake segments and food)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors (R, G, B)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_GRAY = (128, 128, 128)

# Frames Per Second (game speed)
FPS = 10

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game states
STATE_RUNNING = 'running'
STATE_GAMEOVER = 'gameover'
STATE_PAUSED = 'paused'
