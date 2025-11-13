import unittest
import subprocess

class TestCLI(unittest.TestCase):
    def test_generate_password(self):
        result = subprocess.run(['python', 'cli.py', '--length', '12', '--uppercase', '--lowercase', '--numbers', '--special'],
                                capture_output=True, text=True)
        self.assertIn('Generated Password:', result.stdout)
        self.assertEqual(result.returncode, 0)

    def test_invalid_length(self):
        result = subprocess.run(['python', 'cli.py', '--length', '200'],
                                capture_output=True, text=True)
        self.assertIn('usage:', result.stderr)
        self.assertNotEqual(result.returncode, 0)

if __name__ == '__main__':
    unittest.main()