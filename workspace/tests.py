import unittest
from converter.parser import MarkdownParser
from converter.sanitizer import sanitize_html
from flask import json
from backend import api

class TestMarkdownParser(unittest.TestCase):
    def setUp(self):
        self.parser = MarkdownParser()

    def test_title_parsing(self):
        html = self.parser.parse('# Title')
        self.assertIn('<h1>Title</h1>', html)

    def test_unordered_list(self):
        md = '- Item 1\n  - Subitem'
        html = self.parser.parse(md)
        self.assertIn('<ul>', html)
        self.assertIn('<li>Item 1</li>', html)
        self.assertIn('<li>Subitem</li>', html)

    def test_ordered_list(self):
        md = '1. First\n2. Second'
        html = self.parser.parse(md)
        self.assertIn('<ol>', html)
        self.assertIn('<li>First</li>', html)
        self.assertIn('<li>Second</li>', html)

    def test_link_parsing(self):
        md = '[Google](https://google.com)'
        html = self.parser.parse(md)
        self.assertIn('<a href="https://google.com">Google</a>', html)

    def test_html_escape(self):
        md = '<test> & " ''
        html = self.parser.parse(md)
        self.assertIn('&lt;test&gt;', html)
        self.assertIn('&amp;', html)
        self.assertIn('&quot;', html)
        self.assertIn('&#39;', html)

class TestSanitizer(unittest.TestCase):
    def test_allowed_tags(self):
        raw = '<h1>Header</h1><ul><li>Item</li></ul><a href="http://example.com">Link</a>'
        clean = sanitize_html(raw)
        self.assertIn('<h1>Header</h1>', clean)

    def test_strip_script(self):
        raw = '<script>alert(1)</script><p>text</p>'
        clean = sanitize_html(raw)
        self.assertNotIn('<script>', clean)
        self.assertIn('<p>text</p>', clean)

    def test_invalid_href_protocol(self):
        raw = '<a href="javascript:alert(1)">bad</a>'
        clean = sanitize_html(raw)
        self.assertNotIn('javascript:alert(1)', clean)
        self.assertIn('<a>bad</a>', clean)

class TestAPI(unittest.TestCase):
    def setUp(self):
        api.app.testing = True
        self.client = api.app.test_client()

    def test_convert_valid(self):
        resp = self.client.post('/convert', json={"markdown": "# Title"})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIn('<h1>Title</h1>', data.get('html', ''))

    def test_convert_invalid_json(self):
        resp = self.client.post('/convert', data='not json', content_type='text/plain')
        self.assertEqual(resp.status_code, 400)

    def test_convert_missing_markdown(self):
        resp = self.client.post('/convert', json={})
        self.assertEqual(resp.status_code, 400)

    def test_convert_non_string_markdown(self):
        resp = self.client.post('/convert', json={"markdown": 123})
        self.assertEqual(resp.status_code, 400)

if __name__ == '__main__':
    unittest.main()