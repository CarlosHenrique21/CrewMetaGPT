# Python Design Patterns and Best Practices Examples

"""
Common design patterns and coding best practices in Python.
"""

# ============================================================================
# 1. SINGLETON PATTERN
# ============================================================================

class Singleton:
    """
    Ensures only one instance of a class exists.
    Useful for: Configuration managers, Database connections, Loggers
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# Modern Python Singleton using metaclass
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = None


# ============================================================================
# 2. FACTORY PATTERN
# ============================================================================

from abc import ABC, abstractmethod
from typing import Protocol


class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"


class AnimalFactory:
    """Factory for creating animals"""

    @staticmethod
    def create_animal(animal_type: str) -> Animal:
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")


# ============================================================================
# 3. BUILDER PATTERN
# ============================================================================

class Pizza:
    def __init__(self):
        self.size = None
        self.cheese = False
        self.pepperoni = False
        self.mushrooms = False

    def __str__(self):
        return f"Pizza(size={self.size}, cheese={self.cheese}, pepperoni={self.pepperoni}, mushrooms={self.mushrooms})"


class PizzaBuilder:
    """Builder for constructing complex Pizza objects"""

    def __init__(self):
        self.pizza = Pizza()

    def set_size(self, size: str):
        self.pizza.size = size
        return self

    def add_cheese(self):
        self.pizza.cheese = True
        return self

    def add_pepperoni(self):
        self.pizza.pepperoni = True
        return self

    def add_mushrooms(self):
        self.pizza.mushrooms = True
        return self

    def build(self) -> Pizza:
        return self.pizza


# Usage: pizza = PizzaBuilder().set_size("large").add_cheese().add_pepperoni().build()


# ============================================================================
# 4. STRATEGY PATTERN
# ============================================================================

class PaymentStrategy(Protocol):
    def pay(self, amount: float) -> str:
        ...


class CreditCardPayment:
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} with Credit Card"


class PayPalPayment:
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} with PayPal"


class ShoppingCart:
    def __init__(self, payment_strategy: PaymentStrategy):
        self.payment_strategy = payment_strategy
        self.total = 0

    def checkout(self):
        return self.payment_strategy.pay(self.total)


# ============================================================================
# 5. OBSERVER PATTERN
# ============================================================================

class Subject:
    """Observable object"""

    def __init__(self):
        self._observers = []
        self._state = None

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self._state)

    def set_state(self, state):
        self._state = state
        self.notify()


class Observer:
    """Observer that watches Subject"""

    def __init__(self, name: str):
        self.name = name

    def update(self, state):
        print(f"{self.name} received update: {state}")


# ============================================================================
# 6. DECORATOR PATTERN
# ============================================================================

import time
import functools
from typing import Callable, Any


def timer(func: Callable) -> Callable:
    """Decorator to measure execution time"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result

    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator to retry function on failure"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                    time.sleep(delay)

        return wrapper

    return decorator


def log_calls(func: Callable) -> Callable:
    """Decorator to log function calls"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result

    return wrapper


# ============================================================================
# 7. CONTEXT MANAGER PATTERN
# ============================================================================

class DatabaseTransaction:
    """Context manager for database transactions"""

    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        self.connection.begin()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        return False


# Modern approach with contextlib
from contextlib import contextmanager


@contextmanager
def temporary_file(filename: str):
    """Context manager for temporary file operations"""
    f = open(filename, 'w')
    try:
        yield f
    finally:
        f.close()
        # os.remove(filename)  # Clean up


# ============================================================================
# 8. DEPENDENCY INJECTION
# ============================================================================

class Logger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass


class ConsoleLogger(Logger):
    def log(self, message: str) -> None:
        print(f"[CONSOLE] {message}")


class FileLogger(Logger):
    def __init__(self, filename: str):
        self.filename = filename

    def log(self, message: str) -> None:
        with open(self.filename, 'a') as f:
            f.write(f"{message}\n")


class UserService:
    """Service with injected logger dependency"""

    def __init__(self, logger: Logger):
        self.logger = logger

    def create_user(self, username: str):
        # Business logic
        self.logger.log(f"Created user: {username}")


# ============================================================================
# 9. REPOSITORY PATTERN
# ============================================================================

from typing import List, Optional


class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = {}
        self._next_id = 1

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def get_all(self) -> List[User]:
        return list(self._users.values())

    def save(self, user: User) -> None:
        if user.id is None:
            user.id = self._next_id
            self._next_id += 1
        self._users[user.id] = user

    def delete(self, user_id: int) -> None:
        if user_id in self._users:
            del self._users[user_id]


# ============================================================================
# 10. ASYNC/AWAIT PATTERNS
# ============================================================================

import asyncio
from typing import List


async def fetch_data(url: str) -> str:
    """Simulate async API call"""
    await asyncio.sleep(1)
    return f"Data from {url}"


async def fetch_multiple(urls: List[str]) -> List[str]:
    """Fetch multiple URLs concurrently"""
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


# ============================================================================
# 11. DATACLASS PATTERN
# ============================================================================

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Product:
    """Modern Python data container"""
    name: str
    price: float
    quantity: int = 0
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def total_value(self) -> float:
        return self.price * self.quantity


# ============================================================================
# 12. ENUM PATTERN
# ============================================================================

from enum import Enum, auto


class Status(Enum):
    """Status enum with auto values"""
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()


class HttpStatus(Enum):
    """HTTP status codes"""
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_ERROR = 500


# ============================================================================
# 13. PROPERTY PATTERN
# ============================================================================

class Temperature:
    """Class with getter/setter properties"""

    def __init__(self, celsius: float):
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float):
        self.celsius = (value - 32) * 5/9


# ============================================================================
# 14. CHAIN OF RESPONSIBILITY
# ============================================================================

class Handler(ABC):
    def __init__(self):
        self._next_handler = None

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


class ValidationHandler(Handler):
    def handle(self, request):
        if not request.get('valid'):
            return "Validation failed"
        return super().handle(request)


class AuthenticationHandler(Handler):
    def handle(self, request):
        if not request.get('authenticated'):
            return "Authentication failed"
        return super().handle(request)


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # Builder pattern
    pizza = PizzaBuilder().set_size("large").add_cheese().add_pepperoni().build()
    print(pizza)

    # Strategy pattern
    cart = ShoppingCart(CreditCardPayment())
    cart.total = 100.0
    print(cart.checkout())

    # Decorator pattern
    @timer
    @log_calls
    def slow_function(n: int) -> int:
        time.sleep(1)
        return n * 2

    result = slow_function(5)

    print("Examples completed successfully!")
