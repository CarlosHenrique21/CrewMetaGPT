# Sample Unit Tests for Markdown to HTML Converter

import unittest
from src.services.ConverterService import ConverterService

class TestConverterService(unittest.TestCase):
    
    def setUp(self):
        self.converter = ConverterService()
    
    def test_convert_header(self):
        result = self.converter.convert("# Header")
        self.assertEqual(result, "<h1>Header</h1>")
    
    def test_convert_list(self):
        result = self.converter.convert("* Item 1\n* Item 2")
        self.assertEqual(result, "<ul><li>Item 1</li><li>Item 2</li></ul>")
    
    def test_empty_input(self):
        with self.assertRaises(Exception) as context:
            self.converter.convert("")
        self.assertEqual(str(context.exception), "Input cannot be empty")

if __name__ == '__main__':
    unittest.main()