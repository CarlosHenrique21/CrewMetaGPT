"""
CLI entry point and argument parsing for SecurePass CLI Generator.
"""

import argparse
import sys
from src.generator import generate_multiple_passwords
from src.output import output_passwords
from src.entropy import estimate_entropy
from src.utils import validate_length, validate_strength


def parse_arguments():
    parser = argparse.ArgumentParser(description='SecurePass CLI Generator - Generate secure random passwords')

    parser.add_argument('--length', type=int, default=12, help='Password length (8-64, default: 12)')
    parser.add_argument('--strength', choices=['weak', 'medium', 'strong'], default='medium', help='Password strength level (weak, medium, strong, default: medium)')
    parser.add_argument('--special-chars', action='store_true', help='Include special characters')
    parser.add_argument('--count', type=int, default=1, help='Number of passwords to generate (default: 1)')
    parser.add_argument('--copy', action='store_true', help='Copy first generated password to clipboard')
    parser.add_argument('--save', metavar='FILE', type=str, help='Save generated passwords to file')
    parser.add_argument('--entropy', action='store_true', help='Show entropy estimation for generated passwords')

    return parser.parse_args()


def main():
    args = parse_arguments()

    # Validate input arguments
    if not validate_length(args.length):
        print('Error: Password length must be between 8 and 64.')
        sys.exit(1)
    if not validate_strength(args.strength):
        print(f"Error: Invalid strength level '{args.strength}'. Must be one of weak, medium, strong.")
        sys.exit(1)
    if args.count < 1:
        print('Error: Count must be at least 1.')
        sys.exit(1)

    # Generate passwords
    try:
        passwords = generate_multiple_passwords(args.count, args.length, args.strength, args.special_chars)
    except ValueError as ve:
        print(f"Error during password generation: {ve}")
        sys.exit(1)

    # Output passwords
    output_mode = 'console'
    output_path = None
    if args.save:
        output_mode = 'file'
        output_path = args.save

    try:
        output_passwords(passwords, output_mode, output_path, copy_to_clipboard=args.copy)
    except ValueError as ve:
        print(f"Error in output handling: {ve}")
        sys.exit(1)

    # Show entropy if requested
    if args.entropy:
        for idx, pwd in enumerate(passwords, start=1):
            entropy_val = estimate_entropy(pwd)
            print(f"Entropy for Password {idx}: {entropy_val:.2f} bits")


if __name__ == '__main__':
    main()
