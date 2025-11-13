import re


def is_valid_url(url: str) -> bool:
    # Simple URL validation regex
    regex = re.compile(
        r'^(https?://)?'  # http:// or https:// optional
        r'(([\da-zA-Z.-]+)\.([a-zA-Z.]{2,6}))'  # domain
        r'([/\w .-]*)*/?$'  # path
    )
    return re.match(regex, url) is not None
