"""
Output handling for SecurePass CLI Generator.
Handles console output, file saving, and clipboard copy.
"""

import os
from typing import List, Optional

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False


def output_passwords(passwords: List[str], output_mode: str = 'console', output_path: Optional[str] = None, copy_to_clipboard: bool = False) -> None:
    """
    Output generated passwords according to user options.

    Args:
        passwords (List[str]): List of generated passwords.
        output_mode (str): 'console' | 'file'
        output_path (Optional[str]): Path to save file if output_mode == 'file'
        copy_to_clipboard (bool): If true, copy first password to clipboard if available

    Raises:
        ValueError: If invalid output_mode or missing output_path when mode is file.
    """
    if output_mode not in ('console', 'file'):
        raise ValueError("Invalid output_mode, choose 'console' or 'file'.")

    if output_mode == 'file' and not output_path:
        raise ValueError("Output path must be specified when output_mode is 'file'.")

    if output_mode == 'console':
        for idx, pwd in enumerate(passwords, start=1):
            print(f"Password {idx}: {pwd}")
    elif output_mode == 'file':
        # Write passwords to file, one per line
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for pwd in passwords:
                    f.write(pwd + os.linesep)
            print(f"Passwords saved to file: {output_path}")
        except Exception as e:
            print(f"Error writing to file {output_path}: {e}")

    if copy_to_clipboard:
        if not PYPERCLIP_AVAILABLE:
            print("Clipboard copy requested but pyperclip is not installed.")
        elif len(passwords) < 1:
            print("No passwords to copy to clipboard.")
        else:
            try:
                pyperclip.copy(passwords[0])
                print("First password copied to clipboard.")
            except pyperclip.PyperclipException as e:
                print(f"Failed to copy to clipboard: {e}")
