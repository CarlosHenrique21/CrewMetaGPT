import argparse
import pyperclip # For clipboard functionality
from storage import Storage
from password_manager import PasswordManager


def main():
    parser = argparse.ArgumentParser(description='CLI Secure Password Generator')
    parser.add_argument('--length', type=int, help='Length of the password (8-128)', required=True)
    parser.add_argument('--uppercase', action='store_true', help='Include uppercase letters')
    parser.add_argument('--lowercase', action='store_true', help='Include lowercase letters')
    parser.add_argument('--numbers', action='store_true', help='Include numbers')
    parser.add_argument('--special', action='store_true', help='Include special characters')
    args = parser.parse_args()

    # Creating password criteria
    criteria = {
        'length': args.length,
        'include_uppercase': args.uppercase,
        'include_lowercase': args.lowercase,
        'include_numbers': args.numbers,
        'include_special_chars': args.special
    }

    password_manager = PasswordManager()
    password = password_manager.generate_password(criteria)

    # Outputting the password
    print(f'Generated Password: {password}')
    pyperclip.copy(password)  # Copy password to clipboard
    print('Password copied to clipboard!')

if __name__ == '__main__':
    main()