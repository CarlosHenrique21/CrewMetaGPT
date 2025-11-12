# CLI Snake Game with Pygame

## Project Description

CLI Snake Game with Pygame is a classic snake game playable entirely from the command line interface, implemented using Python and the Pygame library. Control the snake using arrow keys or WASD to eat food and grow the snake, while avoiding collisions with the walls or the snake's own body. The game offers an engaging arcadestyle experience with smooth controls and real-time score tracking.

## Features

- Classic snake gameplay with smooth, responsive controls (arrow keys or WASD).
- Food spawns randomly for the snake to eat and grow.
- Game over on collision with walls or self.
- Real-time score display.
- Restart or exit option after game over.
- High score tracking with persistent storage.
- Simple and portable, runs on Windows, macOS, and Linux.

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install Pygame library via pip:

```
pip install pygame
```

3. Clone or download the CLI Snake Game source code.

4. Navigate to the project directory.

## Usage

Run the game using the following command in your terminal or command prompt:

```
python src/main.py
```

### Controls

- Arrow keys or WASD to control the snake direction.
- `Esc` key to quit anytime.
- After Game Over:
  - Press `R` to restart the game.
  - Press `Q` or `Esc` to quit.

## Project Structure

```
cli-snake-game/
├── src/                  # Source code modules
│   ├── __init__.py
│   ├── main.py           # Main entry point and game loop
│   ├── game.py           # Game logic and state management
│   ├── snake.py          # Snake entity and movement
│   ├── food.py           # Food spawning and position
│   ├── input_handler.py  # Keyboard input management
│   ├── renderer.py       # Rendering game elements with Pygame
│   ├── score.py          # Score tracking and persistence
│   └── config.py         # Game configuration constants
├── assets/               # Placeholder for assets
├── tests/                # Unit and integration tests
│   ├── test_game.py
│   ├── test_snake.py
│   └── test_food.py
├── requirements.txt      # Python dependencies
├── highscore.json        # Persistent high score storage
├── README.md             # Project overview and instructions
└── user_guide.md         # Detailed user manual
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit your changes with clear messages.
4. Push the branch to your fork.
5. Open a pull request describing your changes.

Please ensure your code follows existing style and includes tests if applicable.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy playing the CLI Snake Game!