# Clipboard handling using pyperclip

try:
    import pyperclip
except ImportError:
    pyperclip = None


def copy_to_clipboard(text: str):
    if pyperclip is None:
        raise ImportError("pyperclip module is not installed.")
    pyperclip.copy(text)
