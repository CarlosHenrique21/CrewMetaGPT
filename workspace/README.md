# CLI Simple Calculator

A command-line interface calculator application that provides basic arithmetic operations: addition, subtraction, multiplication, and division. The application aims to deliver quick and efficient calculations for users who prefer using CLI tools.

## Features
- Perform addition, subtraction, multiplication, and division
- Handle division by zero with proper error messaging
- Display results in a user-friendly format
- Maintain a history of calculations (optional)

## Installation Instructions
1. Ensure you have Python 3.11 or higher installed on your system.
2. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
3. Navigate to the project directory:
   ```bash
   cd cli_simple_calculator
   ```
4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage Examples
- To add two numbers:
  ```bash
  python cli.py add 3 5
  ```
  Expected output: `Result: 8`

- To subtract two numbers:
  ```bash
  python cli.py subtract 10 4
  ```
  Expected output: `Result: 6`

- To multiply numbers:
  ```bash
  python cli.py multiply 2 3 4
  ```
  Expected output: `Result: 24`

- To divide two numbers:
  ```bash
  python cli.py divide 20 5
  ```
  Expected output: `Result: 4.0`

## Project Structure Overview
```
cli_simple_calculator/
├── cli.py                # User interface and command handling
├── calculator.py         # Business logic for arithmetic operations
├── history.py            # Management of calculation history
├── storage.py            # Data persistence layer
├── tests/
│   ├── test_calculator.py # Unit tests for calculator logic
│   ├── test_history.py    # Unit tests for history management
│   └── test_cli.py        # Unit tests for CLI interaction
├── history.json          # Data file for storing calculation history
└── README.md             # Project documentation and usage instructions
```

## Testing Instructions
To run the tests, navigate to the project directory and execute:
```bash
python -m unittest discover -s tests
```

## Contributing Guidelines
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add your message"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Create a pull request.

## License
This project is licensed under the MIT License.