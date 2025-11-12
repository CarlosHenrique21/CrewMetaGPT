from datetime import datetime

def parse_date(date_str: str) -> datetime:
    """Parse a string into a datetime object using YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD.")
