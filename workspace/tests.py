import unittest
from unittest.mock import patch, mock_open
import builtins
import sys
import io

from src import utils, generator, entropy, output

class TestUtils(unittest.TestCase):
    def test_validate_length(self):
        self.assertFalse(utils.validate_length(7))
        self.assertTrue(utils.validate_length(8))
        self.assertTrue(utils.validate_length(64))
        self.assertFalse(utils.validate_length(65))

    def test_validate_strength(self):
        self.assertTrue(utils.validate_strength('weak'))
        self.assertTrue(utils.validate_strength('medium'))
        self.assertTrue(utils.validate_strength('strong'))
        self.assertFalse(utils.validate_strength('invalid'))

class TestGenerator(unittest.TestCase):
    def test_generate_password_valid(self):
        pwd = generator.generate_password(12, 'medium', include_special=False)
        self.assertEqual(len(pwd), 12)
        # medium includes lower, upper and digits
        self.assertTrue(any(c.islower() for c in pwd))
        self.assertTrue(any(c.isupper() for c in pwd))
        self.assertTrue(any(c.isdigit() for c in pwd))

    def test_generate_password_special_chars(self):
        pwd = generator.generate_password(10, 'weak', include_special=True)
        self.assertEqual(len(pwd), 10)
        # weak is only lowercase + special chars
        self.assertTrue(all(c.islower() or c in generator.SPECIAL_CHARACTERS for c in pwd))

    def test_generate_password_length_too_short(self):
        with self.assertRaises(ValueError):
            generator.generate_password(7, 'medium', False)

    def test_generate_password_length_too_long(self):
        with self.assertRaises(ValueError):
            generator.generate_password(65, 'medium', False)

    def test_generate_password_invalid_strength(self):
        with self.assertRaises(ValueError):
            generator.generate_password(12, 'invalid', False)

    def test_generate_multiple_passwords(self):
        pwds = generator.generate_multiple_passwords(3, 8, 'weak', False)
        self.assertEqual(len(pwds), 3)
        for pwd in pwds:
            self.assertEqual(len(pwd), 8)

    def test_generate_multiple_passwords_invalid_count(self):
        with self.assertRaises(ValueError):
            generator.generate_multiple_passwords(0, 12, 'medium', False)

class TestEntropy(unittest.TestCase):
    def test_entropy_empty(self):
        self.assertEqual(entropy.estimate_entropy(''), 0.0)

    def test_entropy_various(self):
        low = 'a' * 10
        med = 'aA1' * 4
        high = 'aA1!' * 4
        self.assertTrue(entropy.estimate_entropy(low) < entropy.estimate_entropy(med))
        self.assertTrue(entropy.estimate_entropy(med) < entropy.estimate_entropy(high))

class TestOutput(unittest.TestCase):
    def test_output_console(self):
        passwords = ['password1', 'password2']
        captured = io.StringIO()
        sys.stdout = captured
        output.output_passwords(passwords, output_mode='console')
        sys.stdout = sys.__stdout__
        output_text = captured.getvalue()
        self.assertIn('Password 1: password1', output_text)
        self.assertIn('Password 2: password2', output_text)

    def test_output_file(self):
        passwords = ['pass1', 'pass2']
        m = mock_open()
        with patch('builtins.open', m):
            output.output_passwords(passwords, output_mode='file', output_path='dummy.txt')
        m.assert_called_once_with('dummy.txt', 'w', encoding='utf-8')
        handle = m()
        handle.write.assert_any_call('pass1' + '\n')
        handle.write.assert_any_call('pass2' + '\n')

    def test_output_invalid_mode(self):
        with self.assertRaises(ValueError):
            output.output_passwords(['pwd'], output_mode='invalid')

    def test_output_file_no_path(self):
        with self.assertRaises(ValueError):
            output.output_passwords(['pwd'], output_mode='file')

    @patch('src.output.PYPERCLIP_AVAILABLE', True)
    @patch('src.output.pyperclip.copy')
    def test_output_clipboard_success(self, mock_copy):
        output.output_passwords(['pwd1'], copy_to_clipboard=True)
        mock_copy.assert_called_once_with('pwd1')

    @patch('src.output.PYPERCLIP_AVAILABLE', False)
    def test_output_clipboard_unavailable(self):
        captured = io.StringIO()
        sys.stdout = captured
        output.output_passwords(['pwd1'], copy_to_clipboard=True)
        sys.stdout = sys.__stdout__
        output_text = captured.getvalue()
        self.assertIn('Clipboard copy requested but pyperclip is not installed.', output_text)

if __name__ == '__main__':
    unittest.main()
