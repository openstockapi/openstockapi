import re
from datetime import datetime
from typing import Any

def clean_symbol(symbol: str) -> str:
    """Standardize ticker symbols to uppercase alphanumeric, preserving common prefixes/suffixes."""
    return re.sub(r"[^A-Za-z0-9\^\-\./]", "", symbol).upper()

def parse_market_symbol(symbol: str, default_market: str = "VN") -> tuple[str, str]:
    """
    Parses symbol and market.
    Supports formats: 'AAPL.US', 'VNM.VN', or 'VNM' with market="VN".
    Returns tuple of (cleaned_symbol, market_code).
    """
    valid_markets = {"VN", "US", "JP", "CN", "HK", "ASX", "AU"}
    if "." in symbol:
        parts = symbol.rsplit(".", 1)
        suffix = parts[1].upper()
        if len(suffix) in (2, 3) and suffix.isalpha() and suffix in valid_markets:
            return clean_symbol(parts[0]), suffix
    return clean_symbol(symbol), default_market.upper()


def parse_date(date_val: Any) -> datetime:
    """Parse common date inputs into datetime objects."""
    if isinstance(date_val, datetime):
        return date_val
    if isinstance(date_val, (int, float)):
        if date_val > 1e11: # milliseconds
            date_val = date_val / 1000.0
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


def get_derivative_maturity_date(suffix: str, reference_date = None) -> datetime:
    import datetime as dt
    if reference_date is None:
        reference_date = datetime.now()
        
    suffix = suffix.upper()
    match_explicit = re.match(r"^F(\d{2})(\d{2})$", suffix)
    if match_explicit:
        year = 2000 + int(match_explicit.group(1))
        month = int(match_explicit.group(2))
    elif suffix == "F1M":
        year = reference_date.year
        month = reference_date.month
        mat_date = _get_third_thursday(year, month)
        if reference_date.date() > mat_date:
            month += 1
            if month > 12:
                month = 1
                year += 1
    elif suffix == "F2M":
        year = reference_date.year
        month = reference_date.month + 1
        if reference_date.date() > _get_third_thursday(reference_date.year, reference_date.month):
            month += 1
        if month > 12:
            month = month - 12
            year += 1
    elif suffix == "F1Q":
        curr_month = reference_date.month
        q_months = [3, 6, 9, 12]
        target_month = None
        year = reference_date.year
        for m in q_months:
            if m > curr_month:
                target_month = m
                break
            elif m == curr_month:
                if reference_date.date() <= _get_third_thursday(year, m):
                    target_month = m
                    break
        if target_month is None:
            target_month = 3
            year += 1
        month = target_month
    elif suffix == "F2Q":
        f1q_date = get_derivative_maturity_date("F1Q", reference_date)
        year = f1q_date.year
        month = f1q_date.month + 3
        if month > 12:
            month = month - 12
            year += 1
    else:
        year = reference_date.year
        month = reference_date.month
        
    return _get_third_thursday(year, month)


def _get_third_thursday(year: int, month: int):
    import datetime as dt
    first_day = dt.date(year, month, 1)
    days_to_thursday = (3 - first_day.weekday() + 7) % 7
    third_thursday = first_day + dt.timedelta(days=days_to_thursday + 14)
    return third_thursday


def convert_derivative_symbol(symbol: str, reference_date = None) -> str:
    symbol = symbol.upper()
    underlying_map = {'VN30': 'I1', 'VN100': 'I2', 'GB05': 'B5', 'GB10': 'BA'}
    underlying_code = None
    suffix = None
    for prefix, code in underlying_map.items():
        if symbol.startswith(prefix):
            underlying_code = code
            suffix = symbol[len(prefix):]
            break
            
    if not underlying_code:
        raise ValueError(f"Unknown underlying asset for symbol {symbol}")
        
    mat_date = get_derivative_maturity_date(suffix, reference_date)
    mat_year = mat_date.year
    mat_month = mat_date.month
    
    year_cycle_index = (mat_year - 2010) % 30
    alphabet = 'ABCDEFGHJKLMNPQRSTVW'
    if 0 <= year_cycle_index <= 9:
        year_code = str(year_cycle_index)
    else:
        year_code = alphabet[year_cycle_index - 10]
        
    if 1 <= mat_month <= 9:
        month_code = str(mat_month)
    else:
        month_codes = {10: 'A', 11: 'B', 12: 'C'}
        month_code = month_codes[mat_month]
        
    return f"41{underlying_code}{year_code}{month_code}000"


def safe_convert_derivative_symbol(symbol: str, reference_date = None) -> str:
    try:
        if len(symbol) == 9 and symbol.startswith('41'):
            return symbol
        return convert_derivative_symbol(symbol, reference_date)
    except Exception:
        return symbol


def get_asset_type(symbol: str) -> str:
    symbol = symbol.upper()
    if symbol in ['VNINDEX', 'HNXINDEX', 'UPCOMINDEX', 'VN30', 'VN100', 'HNX30', 'VNSML', 'VNMID', 'VNALL']:
        return 'index'
    elif len(symbol) == 3:
        return 'stock'
    elif len(symbol) in [7, 9]:
        fm_pattern = re.compile(r'^VN30F\d{1,2}M$')
        ym_pattern = re.compile(r'^VN30F\d{4}$')
        gov_bond_pattern = re.compile(r'^GB\d{2}F\d{4}$')
        comp_bond_pattern = re.compile(r'^(?!VN30F)[A-Z]{3}\d{6}$')
        if gov_bond_pattern.match(symbol) or comp_bond_pattern.match(symbol):
            return 'bond'
        elif fm_pattern.match(symbol) or ym_pattern.match(symbol):
            return 'derivative'
        else:
            raise ValueError('Invalid derivative or bond symbol.')
    elif len(symbol) == 8:
        return 'coveredWarr'
    else:
        raise ValueError('Invalid symbol format.')


