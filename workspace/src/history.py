"""
History manager for SimpleCalc CLI.
Maintains in-memory history and supports saving to file.
"""

class HistoryManager:
    def __init__(self):
        self.history = []  # list of tuples (expression, result)

    def add(self, expression, result):
        """Add a calculation entry to history."""
        self.history.append((expression, result))

    def get_all(self):
        """Return list of all history entries."""
        return self.history

    def clear(self):
        """Clear the history."""
        self.history.clear()

    def format_history(self):
        """Return formatted string of history entries."""
        lines = [f"{idx + 1}: {expr} = {res}" for idx, (expr, res) in enumerate(self.history)]
        return "\n".join(lines)

    def save_to_file(self, file_path):
        """Save history entries to a text file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            for expr, res in self.history:
                f.write(f"{expr} = {res}\n")
