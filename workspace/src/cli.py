"""
CLI interface for SimpleCalc CLI.
Handles user input, commands and output.
"""
import sys
from parser import parse_expression
from calculator import evaluate_expression
from history import HistoryManager
from errors import ParseError, EvaluationError


class SimpleCalcCLI:
    def __init__(self):
        self.history_manager = HistoryManager()
        self.exit_flag = False

    def print_welcome(self):
        welcome_msg = (
            "Welcome to SimpleCalc CLI!\n"
            "Enter arithmetic expressions to calculate.\n"
            "Commands: history, save <filename>, help, exit\n"
        )
        print(welcome_msg)

    def print_help(self):
        help_msg = ("""
SimpleCalc CLI Help:

- Enter arithmetic expressions using +, -, *, /, and parentheses.
- Commands:
  - history                Show calculation history
  - save <filename>        Save history to the specified file
  - help                   Show this help message
  - exit                   Exit the calculator

Examples:
  2 + 3 * 4
  (5 + 2) / 3
""")
        print(help_msg)

    def process_input(self, user_input):
        user_input = user_input.strip()
        if not user_input:
            return
        if user_input.lower() == 'exit':
            self.exit_flag = True
            print("Goodbye!")
            return
        if user_input.lower() == 'help':
            self.print_help()
            return
        if user_input.lower() == 'history':
            history_text = self.history_manager.format_history()
            if history_text:
                print(history_text)
            else:
                print("No history yet.")
            return
        if user_input.lower().startswith('save '):
            _, _, filename = user_input.partition(' ')
            filename = filename.strip()
            if not filename:
                print("Error: Please specify a filename to save history.")
                return
            try:
                self.history_manager.save_to_file(filename)
                print(f"History saved to {filename}")
            except Exception as e:
                print(f"Error saving history: {e}")
            return
        # Otherwise, treat as expression
        try:
            rpn = parse_expression(user_input)
            result = evaluate_expression(rpn)
            result_str = str(result)
            print(result_str)
            self.history_manager.add(user_input, result_str)
        except ParseError as pe:
            error_msg = f"Parse error: {pe.message}" if hasattr(pe, 'message') else f"Parse error: {pe}"
            print(error_msg)
            self.history_manager.add(user_input, error_msg)
        except EvaluationError as ee:
            error_msg = f"Evaluation error: {ee.message}" if hasattr(ee, 'message') else f"Evaluation error: {ee}"
            print(error_msg)
            self.history_manager.add(user_input, error_msg)
        except Exception as e:
            print(f"Unexpected error: {e}")

    def run(self):
        self.print_welcome()
        while not self.exit_flag:
            try:
                user_input = input("calc> ")
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break
            self.process_input(user_input)
