import re
from datetime import datetime
from typing import Any

def clean_symbol(symbol: str) -> str:
    """Standardize ticker symbols to uppercase alphanumeric."""
    return re.sub(r"[^A-Za-z0-9]", "", symbol).upper()

def parse_market_symbol(symbol: str, default_market: str = "VN") -> tuple[str, str]:
    """
    Parses symbol and market.
    Supports formats: 'AAPL.US', 'VNM.VN', or 'VNM' with market="VN".
    Returns tuple of (cleaned_symbol, market_code).
    """
    if "." in symbol:
        parts = symbol.rsplit(".", 1)
        if len(parts[1]) in (2, 3) and parts[1].isalpha():
            return clean_symbol(parts[0]), parts[1].upper()
    return clean_symbol(symbol), default_market.upper()


def parse_date(date_val: Any) -> datetime:
    """Parse common date inputs into datetime objects."""
    if isinstance(date_val, datetime):
        return date_val
    if isinstance(date_val, (int, float)):
        return datetime.fromtimestamp(date_val)
    if isinstance(date_val, str):
        if date_val.isdigit():
            val = int(date_val)
            if val > 1e11: # milliseconds
                val = val / 1000.0
            return datetime.fromtimestamp(val)
        
        # Handle KBS format 'YYYY-MM-DD HH:MM:SS:MS' where milliseconds has colon instead of dot/space
        if date_val.count(':') == 3:
            # Replace last colon with a dot
            parts = date_val.rsplit(':', 1)
            date_val = f"{parts[0]}.{parts[1]}"
            
        cleaned = date_val.split('.')[0].rstrip('Z')

        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y%m%d"):
            try:
                return datetime.strptime(cleaned, fmt)
            except ValueError:
                continue

    raise ValueError(f"Could not parse date: {date_val}")



import html

def clean_html_text(text: Any) -> Any:
    """Strips HTML tags, decodes HTML entities, and removes excess whitespace."""
    if not text or not isinstance(text, str):
        return text
    decoded = html.unescape(text)
    stripped = re.sub(r"<[^>]+>", " ", decoded)
    cleaned = re.sub(r"\s+", " ", stripped).strip()
    return cleaned if cleaned else None

