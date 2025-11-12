"""
Parser module to convert Markdown text to HTML.
Supports titles (#, ##, ###), unordered lists, ordered lists, links, and nested lists.
"""
import re

class MarkdownParser:
    def __init__(self):
        # Regular expressions for matching markdown patterns
        self.title_pattern = re.compile(r'^(#{1,3})\s+(.*)')
        self.ulist_pattern = re.compile(r'^([ \t]*)([-+*])\s+(.*)')
        self.olist_pattern = re.compile(r'^([ \t]*)(\d+)\.\s+(.*)')
        self.link_pattern = re.compile(r'\[(.*?)\]\((.*?)\)')

    def parse(self, markdown: str) -> str:
        """
        Convert markdown string to HTML string.

        Args:
            markdown (str): The input markdown text.

        Returns:
            str: Converted HTML string.
        """
        lines = markdown.splitlines()
        html_lines = []
        list_stack = []  # Stack to hold current list context tuples (list_type, indent_level)

        def close_open_lists(curr_indent):
            """Helper to close lists until current indent"""
            while list_stack and list_stack[-1][1] >= curr_indent:
                list_type, _ = list_stack.pop()
                if list_type == 'ul':
                    html_lines.append('</ul>')
                elif list_type == 'ol':
                    html_lines.append('</ol>')

        for line in lines:
            if not line.strip():
                # Empty line closes all open lists
                close_open_lists(0)
                html_lines.append('')
                continue

            # Check for title
            title_match = self.title_pattern.match(line)
            if title_match:
                close_open_lists(0)
                level = len(title_match.group(1))
                content = self._parse_inline(title_match.group(2).strip())
                html_lines.append(f'<h{level}>{content}</h{level}>')
                continue

            # Check for unordered list item
            ulist_match = self.ulist_pattern.match(line)
            if ulist_match:
                indent = len(ulist_match.group(1).expandtabs(4))
                content = self._parse_inline(ulist_match.group(3).strip())

                # Manage list stack
                if not list_stack or indent > list_stack[-1][1]:
                    # Open new ul
                    list_stack.append(('ul', indent))
                    html_lines.append('<ul>')
                else:
                    # Close lists if indent lesser or equal
                    close_open_lists(indent)
                    if not list_stack or list_stack[-1][0] != 'ul':
                        list_stack.append(('ul', indent))
                        html_lines.append('<ul>')

                html_lines.append(f'<li>{content}</li>')
                continue

            # Check for ordered list item
            olist_match = self.olist_pattern.match(line)
            if olist_match:
                indent = len(olist_match.group(1).expandtabs(4))
                content = self._parse_inline(olist_match.group(3).strip())

                # Manage list stack
                if not list_stack or indent > list_stack[-1][1]:
                    # Open new ol
                    list_stack.append(('ol', indent))
                    html_lines.append('<ol>')
                else:
                    # Close lists if indent lesser or equal
                    close_open_lists(indent)
                    if not list_stack or list_stack[-1][0] != 'ol':
                        list_stack.append(('ol', indent))
                        html_lines.append('<ol>')

                html_lines.append(f'<li>{content}</li>')
                continue

            # If reaches here, line is normal text or paragraph
            close_open_lists(0)
            escaped = self._escape_html(line)
            parsed_line = self._parse_inline(escaped)
            html_lines.append(f'<p>{parsed_line}</p>')

        # Close any open lists at end of document
        close_open_lists(0)

        return '\n'.join(html_lines)

    def _parse_inline(self, text: str) -> str:
        """
        Parse inline Markdown elements like links.

        Args:
            text (str): Text with potential inline markdown

        Returns:
            str: Text with HTML inline elements
        """
        def replace_link(match):
            label = self._escape_html(match.group(1))
            url = self._escape_html(match.group(2))
            return f'<a href="{url}">{label}</a>'

        # Replace links
        processed = self.link_pattern.sub(replace_link, text)
        return processed

    def _escape_html(self, text: str) -> str:
        """
        Escape HTML special characters.

        Args:
            text (str): Raw text

        Returns:
            str: Escaped text
        """
        return (text.replace('&', '&amp;')
                    .replace('<', '&lt;')
                    .replace('>', '&gt;')
                    .replace('"', '&quot;')
                    .replace("'", '&#39;'))


# For manual testing
if __name__ == '__main__':
    sample_md = '''
# Título 1
## Título 2
### Título 3

Texto com um [link](https://example.com).

- Item 1
  - Subitem 1.1
  - Subitem 1.2
- Item 2

1. Primeiro
2. Segundo
3. Terceiro

Parágrafo simples.
'''
    parser = MarkdownParser()
    html = parser.parse(sample_md)
    print(html)
