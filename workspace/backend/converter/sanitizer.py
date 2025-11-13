"""
Sanitizer module for purifying HTML output to prevent XSS attacks.
Uses bleach library for sanitization.
"""

import bleach

# Allowed tags and attributes based on expected output (h1-h3, ul, ol, li, a)
ALLOWED_TAGS = [
    'h1', 'h2', 'h3',
    'ul', 'ol', 'li',
    'a', 'p'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel']
}

# Allowed protocols for href attributes
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


def sanitize_html(html: str) -> str:
    """
    Sanitize HTML output to remove potentially malicious content.

    Args:
        html (str): Raw HTML string.

    Returns:
        str: Sanitized HTML string.
    """
    cleaned = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True
    )
    return cleaned


# Manual test
if __name__ == '__main__':
    unsafe_html = '<h1>Test</h1><script>alert(1)</script><a href="javascript:alert(2)">link</a>'
    safe_html = sanitize_html(unsafe_html)
    print(safe_html)
