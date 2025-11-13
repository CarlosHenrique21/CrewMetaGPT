# CLI Simple Calculator

## Overview
The CLI Simple Calculator is a command-line interface application that performs basic arithmetic operations: addition, subtraction, multiplication, and division. It aims to provide quick calculations in a user-friendly CLI environment.

## Features
- Perform basic arithmetic operations: add, subtract, multiply, divide
- Clear display of results in the command line
- Error messages for invalid inputs (e.g., division by zero)
- Support for multiple calculations in one session

## Installation
1. Clone the repository.
2. Navigate to the project directory.
3. Install the required dependencies (if any).

## Usage
To use the calculator, run the following command in the terminal:

```bash
python cli.py <operation> <operand1> <operand2> ...
```

### Operations
- `add`: Adds the operands
- `subtract`: Subtracts the second operand from the first
- `multiply`: Multiplies the operands
- `divide`: Divides the first operand by the subsequent operands

### Example
```bash
python cli.py add 2 3
# Output: Result: 5
```

## Testing
To run the tests, use the following command:

```bash
pytest
```

## License
This project is licensed under the MIT License.
