import unittest
from password_manager import PasswordManager, PasswordCriteria

class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        self.password_manager = PasswordManager()

    def test_generate_password(self):
        criteria = PasswordCriteria(length=12, include_uppercase=True, include_lowercase=True, include_numbers=True, include_special_chars=True)
        password = self.password_manager.generate_password(criteria)
        self.assertEqual(len(password), 12)

    def test_generate_password_no_characters(self):
        with self.assertRaises(ValueError):
            criteria = PasswordCriteria(length=12, include_uppercase=False, include_lowercase=False, include_numbers=False, include_special_chars=False)
            self.password_manager.generate_password(criteria)

if __name__ == '__main__':
    unittest.main()