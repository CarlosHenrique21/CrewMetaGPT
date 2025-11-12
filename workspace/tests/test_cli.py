import subprocess
import sys

def test_help_command():
    result = subprocess.run([sys.executable, 'src/cli.py', 'help'], capture_output=True, text=True)
    assert 'CLI Weather Forecast Tool' in result.stdout

# Additional CLI tests would require test doubles or mocks for the API client
# and could be implemented similarly to ensure CLI argument parsing and output
