# Coding Standards and Best Practices

## General Principles

### Code Readability
- Code is read more often than it's written
- Write for humans first, computers second
- Use meaningful names
- Keep functions small and focused

### DRY (Don't Repeat Yourself)
- Avoid code duplication
- Extract common logic into reusable functions
- Use inheritance and composition appropriately

### YAGNI (You Aren't Gonna Need It)
- Don't add functionality until it's needed
- Avoid over-engineering
- Start simple, refactor when necessary

## Naming Conventions

### Variables
```python
# Good
user_count = 10
is_active = True
MAX_RETRIES = 3

# Bad
x = 10
flag = True
val = 3
```

### Functions
```python
# Good - Verbs that describe actions
def calculate_total_price(items):
    pass

def fetch_user_by_id(user_id):
    pass

# Bad
def data(items):
    pass

def get(id):
    pass
```

### Classes
```python
# Good - Nouns
class UserManager:
    pass

class DatabaseConnection:
    pass

# Bad
class DoStuff:
    pass

class Manager:  # Too generic
    pass
```

## Python Best Practices

### PEP 8 Compliance
- Use 4 spaces for indentation
- Maximum line length: 79 characters
- Use snake_case for functions and variables
- Use PascalCase for classes
- Use UPPER_CASE for constants

### Type Hints
```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def calculate_average(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)
```

### Docstrings
```python
def complex_function(param1: str, param2: int) -> dict:
    """
    Brief description of what the function does.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param2 is negative
    """
    pass
```

### List Comprehensions
```python
# Good - Simple and readable
squares = [x**2 for x in range(10)]

# Bad - Too complex
result = [x**2 for x in range(10) if x % 2 == 0 if x > 5]

# Better - Break it down
numbers = [x for x in range(10) if x % 2 == 0 and x > 5]
squares = [x**2 for x in numbers]
```

### Context Managers
```python
# Good
with open('file.txt', 'r') as f:
    content = f.read()

# Bad - Doesn't guarantee file closure
f = open('file.txt', 'r')
content = f.read()
f.close()
```

## JavaScript/TypeScript Best Practices

### Use const and let, not var
```javascript
// Good
const MAX_SIZE = 100;
let counter = 0;

// Bad
var MAX_SIZE = 100;
var counter = 0;
```

### Arrow Functions
```javascript
// Good - Concise for simple operations
const double = (x) => x * 2;

// Good - Use regular functions for methods
class Calculator {
    add(a, b) {
        return a + b;
    }
}
```

### Destructuring
```javascript
// Good
const { name, age } = user;
const [first, second] = array;

// Bad
const name = user.name;
const age = user.age;
```

### Template Literals
```javascript
// Good
const greeting = `Hello, ${name}!`;

// Bad
const greeting = 'Hello, ' + name + '!';
```

## Error Handling

### Python
```python
# Good - Specific exceptions
try:
    result = risky_operation()
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
    raise
except PermissionError as e:
    logger.error(f"Permission denied: {e}")
    return None

# Bad - Bare except
try:
    result = risky_operation()
except:
    pass
```

### JavaScript
```javascript
// Good - Proper error handling
async function fetchData() {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch data:', error);
        throw error;
    }
}
```

## Comments

### When to Comment
```python
# Good - Explain WHY, not WHAT
# Using binary search because dataset is sorted and large (1M+ items)
result = binary_search(data, target)

# Bad - States the obvious
# Increment counter by 1
counter += 1
```

### TODO Comments
```python
# TODO(username): Optimize this query for large datasets
# FIXME: This breaks when user has no email
# HACK: Temporary workaround for API bug, remove after v2.0
```

## Function Design

### Single Responsibility
```python
# Good - Each function does one thing
def validate_email(email: str) -> bool:
    return '@' in email and '.' in email.split('@')[1]

def send_welcome_email(email: str) -> None:
    if validate_email(email):
        send_email(email, "Welcome!")

# Bad - Does too much
def process_user(email: str) -> None:
    if '@' in email and '.' in email.split('@')[1]:
        save_to_db(email)
        send_email(email, "Welcome!")
        log_event("user_registered")
```

### Parameter Limits
- Maximum 3-4 parameters
- Use objects/dicts for multiple related parameters
- Use keyword arguments in Python

```python
# Good
def create_user(username: str, email: str, config: UserConfig):
    pass

# Bad
def create_user(username, email, age, country, language, timezone, theme):
    pass
```

## Testing Best Practices

### Test Naming
```python
# Good - Describes what's being tested
def test_calculate_discount_returns_zero_for_negative_price():
    pass

def test_user_creation_raises_error_when_email_is_invalid():
    pass

# Bad
def test_discount():
    pass

def test_user():
    pass
```

### AAA Pattern (Arrange, Act, Assert)
```python
def test_add_item_to_cart():
    # Arrange
    cart = ShoppingCart()
    item = Item("Book", 19.99)

    # Act
    cart.add_item(item)

    # Assert
    assert len(cart.items) == 1
    assert cart.total == 19.99
```

## Code Organization

### Project Structure (Python)
```
project/
├── src/
│   ├── __init__.py
│   ├── models/
│   ├── services/
│   ├── utils/
│   └── config.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_services.py
├── docs/
├── requirements.txt
└── README.md
```

### Import Organization
```python
# Standard library imports
import os
import sys
from pathlib import Path

# Third-party imports
import numpy as np
import pandas as pd
from flask import Flask

# Local imports
from src.models import User
from src.utils import logger
```

## Performance Best Practices

### Avoid Premature Optimization
1. Write clear, correct code first
2. Profile to find bottlenecks
3. Optimize the slowest parts

### Common Optimizations
```python
# Good - Generator for large datasets
def read_large_file(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

# Bad - Loads entire file into memory
def read_large_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f]
```

### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(n):
    # Complex calculation
    return result
```

## Security Best Practices

### Input Validation
```python
# Good - Validate and sanitize
def process_username(username: str) -> str:
    if not username or len(username) < 3:
        raise ValueError("Username must be at least 3 characters")
    return username.strip().lower()

# Bad - No validation
def process_username(username):
    return username
```

### SQL Injection Prevention
```python
# Good - Parameterized queries
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# Bad - String concatenation
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

## Git Commit Messages

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

### Example
```
feat(auth): add JWT authentication

Implement JWT-based authentication system with refresh tokens.
Includes middleware for protected routes.

Closes #123
```

## Code Review Guidelines

### What to Look For
1. Correctness - Does it work?
2. Design - Is it well-structured?
3. Readability - Is it clear?
4. Tests - Is it tested?
5. Documentation - Is it documented?
6. Security - Is it secure?

### Giving Feedback
- Be kind and constructive
- Explain the "why"
- Suggest alternatives
- Ask questions
- Praise good work

## Continuous Improvement

### Refactoring
- Small, incremental changes
- Always have tests
- One refactoring at a time
- Commit frequently

### Learning
- Read code from others
- Stay updated with language features
- Learn design patterns
- Practice regularly

Remember: Clean code is not about following rules blindly, but about making code that is easy to understand, maintain, and modify.
