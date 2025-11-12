# Tic-Tac-Toe Game

## Project Description

Tic-Tac-Toe is a classic two-player game where players take turns marking spaces in a 3x3 grid. The objective is to place three of your marks in a horizontal, vertical, or diagonal row to win the game. This digital version offers an intuitive, smooth, and engaging experience playable on both desktop and mobile browsers.

## Features

- Standard 3x3 grid for gameplay
- Two-player mode on the same device
- Automatic win and draw detection
- Clear visual indicators of game status (win, draw, next player's turn)
- Restart game button
- Scoreboard to track wins, losses, and draws
- Responsive design for desktop and mobile
- Undo last move feature (if enabled in future releases)
- Optional single-player mode with AI opponent (planned for future updates)

## Installation

1. Clone or download the project files from the repository.
2. Ensure you have a modern web browser (Chrome, Firefox, Safari, Edge).
3. Open the `src/index.html` file in your browser to start playing.

_No additional installations or dependencies are required since this is a fully client-side web application._

## Usage

- Open the game in your web browser.
- The game board consists of a 3x3 grid.
- Players take turns clicking on empty cells to place their marks ('X' or 'O').
- The game automatically detects wins or draws and updates the status message.
- Use the "Restart Game" button to start a new game anytime.
- The scoreboard tracks the total wins for each player and the number of draws.

## Project Structure

```
/tic-tac-toe/
│
├── /src/
│   ├── index.html            # Main HTML file
│   ├── styles.css            # Core CSS styles
│   ├── /js/
│   │   ├── app.js            # Application entry and UI logic
│   │   ├── gameEngine.js     # Game rules and state management
│   │   ├── storage.js        # Local Storage handling
│   │   ├── utils.js          # Utility functions
│   │   └── ai.js             # AI module (optional)
│   └── /assets/
│       ├── images/           # Icons and graphics
│       ├── sounds/           # Audio files
│
├── /tests/                  # Unit and integration tests
│   ├── gameEngine.test.js
│   ├── ai.test.js
│
├── README.md                # Project overview and setup (this file)
├── package.json             # Optional build/configurations
└── .gitignore               # Ignored files
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes with clear, concise commit messages.
4. Ensure your code follows the existing style and includes relevant tests.
5. Submit a pull request describing your changes.

Please report any bugs or feature requests via the repository's issue tracker.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Enjoy playing and improving your Tic-Tac-Toe skills!