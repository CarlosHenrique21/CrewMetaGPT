import argparse
import sys
from enum import Enum
from typing import List

from .generator import PasswordGenerator
from .config import StrengthLevel, DEFAULT_PASSWORD_LENGTH


def parse_strength_level(value: str) -> StrengthLevel:
    value_lower = value.lower()
    if value_lower not in [level.value for level in StrengthLevel]:
        raise argparse.ArgumentTypeError(f"Invalid strength level: {value}. Choose from weak, moderate, strong.")
    return StrengthLevel(value_lower)


def positive_int(value: str) -> int:
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"Invalid positive int value: {value}")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid int value: {value}")


def parse_args(args: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SecurePass CLI: Generate secure passwords based on parameters.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        '-l', '--length', type=positive_int, default=DEFAULT_PASSWORD_LENGTH,
        help='Specify password length'
    )
    parser.add_argument(
        '-s', '--strength', type=parse_strength_level, default=StrengthLevel.MODERATE,
        help='Password strength level: weak, moderate, strong'
    )
    parser.add_argument(
        '--include-special', action='store_true',
        help='Include special characters in the password'
    )
    parser.add_argument(
        '-n', '--number', type=positive_int, default=1,
        help='Number of passwords to generate'
    )
    parser.add_argument(
        '--copy', action='store_true',
        help='Copy the last generated password to the clipboard (requires pyperclip)'
    )
    parser.add_argument(
        '--save', action='store_true',
        help='Save generated passwords to an encrypted local file (optional feature, not implemented)'
    )
    parser.add_argument(
        '--seed', type=int, default=None,
        help='Seed for repeatable password generation (not implemented for security reasons)'
    )

    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])

    generator = PasswordGenerator()

    try:
        passwords = []
        for _ in range(args.number):
            pwd = generator.generate_password(
                length=args.length,
                include_special_chars=args.include_special,
                strength=args.strength,
                seed=args.seed
            )
            passwords.append(pwd)

        # Display generated passwords
        for i, pwd in enumerate(passwords, start=1):
            if args.number == 1:
                print(pwd)
            else:
                print(f"Password {i}: {pwd}")

        # Optional clipboard copy
        if args.copy:
            try:
                from .clipboard import copy_to_clipboard
                copy_to_clipboard(passwords[-1])
                print("Password copied to clipboard.")
            except ImportError:
                print("pyperclip module not found. Clipboard copy not available.")

        # Placeholder for save option
        if args.save:
            print("Save option is not implemented yet.")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
