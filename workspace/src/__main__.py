"""
Entry point for SimpleCalc CLI.
"""
from cli import SimpleCalcCLI

def main():
    cli = SimpleCalcCLI()
    cli.run()

if __name__ == '__main__':
    main()
