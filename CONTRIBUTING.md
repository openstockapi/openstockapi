# OpenStock Connector Development Kit (CDK) — Contributor Guide

> **Target Audience:** Developers who want to contribute a new data provider to `openstockapi`.  
> **Requirements:** Python 3.10+, basic understanding of HTTP requests and REST APIs.

---

## Overview

Want to add a new data source (e.g., SSI Securities, Fireant, Barchart...) to OpenStockAPI? The CDK (Connector Development Kit) allows you to do this in **under 30 minutes** without needing to understand the entire core system architecture.

**All you need to do is:**
1. Understand the API of the data source you want to add (URL, query parameters, response format).
2. Run a CLI command to automatically generate the boilerplate code.
3. Fill in your API parser logic at the `# TODO:` placeholders.
4. Run tests to verify the data conforms to quality standards.
5. Open a Pull Request.

---

## Step 1 — Environment Setup

```bash
# Clone the repository
git clone https://github.com/openstockapi/openstockapi.git
cd openstockapi

# Create a new feature branch
git checkout -b feature/add-ssi-provider

# Install dependencies (including dev and cdk tools)
pip install -e ".[cdk,dev]"
```

---

## Step 2 — Generate Code Templates using CDK CLI

```bash
# Replace "ssi" with your provider's name (lowercase, no spaces)
# Replace "VN" with the market code: VN, US, JP, CN, HK, AU, GLOBAL
# Replace "stock" with the asset type: stock, crypto, forex

python -m openstockapi.cdk generate --name ssi --market VN --type stock
```

The CLI will automatically generate 3 files for you:
- `openstockapi/providers/vn_stock/providers/ssi.py` — **Main provider class** (where you implement parsing logic).
- `tests/unit/test_ssi.py` — Unit test template.
- `tests/cdk/test_ssi_cdk.py` — CDK contract validation test (no edits needed here).

---

## Step 3 — Implement Your API Logic

Open the generated file `openstockapi/providers/vn_stock/providers/ssi.py` and locate all the `# TODO:` comments.

### Example — Replacing URL and Field Maps

**Before:**
```python
url = f"https://TODO_SSI_API_ENDPOINT/ohlcv/{symbol}"
# ...
raw_list = data.get("data", [])
# ...
results.append(OHLCVBar(
    timestamp=parse_date(item.get("date")),   # TODO: adjust field name
    open=float(item.get("open", 0)),          # TODO: adjust field name
```

**After (when mapping real SSI API responses):**
```python
url = f"https://api.ssi.com.vn/v2/market/ohlcv/{symbol}"
# ...
raw_list = data.get("Items", [])
# ...
results.append(OHLCVBar(
    timestamp=parse_date(item.get("TradingDate")),
    open=float(item.get("OpenPrice", 0)),
```

### Mandated Guidelines to Follow

| Guideline | Description |
|-----------|-------------|
| **Use `parse_date()`** | Never parse dates manually — use `from openstockapi.core.utils import parse_date` |
| **Use `http_client`** | Do not instantiate custom `requests.Session` — use `from openstockapi.core.http_client import http_client` |
| **Raise correct exceptions** | Catch all errors and re-raise them as `DataParseError` or `ProviderUnavailableError` |
| **No raw dicts** | Always return standard Pydantic models (`OHLCVBar`, `FinancialItem`, etc.) |
| **Sort outputs** | Always sort the output list ascending by timestamp: `results.sort(key=lambda x: x.timestamp)` |

---

## Step 4 — Register the Provider Manually (2 Files)

### 4.1 `openstockapi/providers/__init__.py`

```python
# Add import statement (alphabetically ordered)
from openstockapi.providers.vn_stock.providers.ssi import SSIProvider

# Register in the PROVIDERS dictionary
PROVIDERS = {
    # ... existing providers ...
    "ssi": SSIProvider(),   # ← add this line
}
```

### 4.2 `openstockapi/config/settings.py`

```python
"VN": {
    "ohlcv": ["dnse", "kbs", "ssi", "vci"],  # ← add "ssi" into the priority chain list
    # ...
}
```

---

## Step 5 — Run Verification Tests

```bash
# CDK Contract Tests — validates data quality against standard schemas
python -m pytest tests/cdk/ -v -p no:mpl

# Unit Tests — validates provider parsing logic and mocked behaviors
python -m pytest tests/unit/ -v -p no:mpl
```

**All tests must pass (green)** before opening a Pull Request.

---

## Step 6 — Submit a Pull Request

### Pre-submission Checklist

- [ ] All `# TODO:` placeholders have been implemented with real logic.
- [ ] `tests/cdk/test_<name>_cdk.py` exists and passes.
- [ ] `tests/unit/test_<name>.py` exists and passes.
- [ ] Provider is registered in `openstockapi/providers/__init__.py`.
- [ ] Priority list updated in `openstockapi/config/settings.py`.
- [ ] No hardcoded API keys, session tokens, or sensitive credentials.

### PR Title Convention

```
feat(provider): Add SSIProvider for VN Stock market

- Implements get_ohlcv() and get_financial_statements()
- Supports VN market, FREE tier
- CDK contract tests: ✅ 15/15 passed
```

---

## Frequently Asked Questions

**Q: My provider requires a private API Key. How do I configure it?**  
A: Initialize the API key inside the provider's `__init__` constructor and read it from environment variables. Do not commit keys to source code.

```python
import os

class SSIProvider(BaseStockProvider):
    def __init__(self):
        self._api_key = os.getenv("SSI_API_KEY", "")
```

**Q: The data source does not have Financial Statements. Do I need to implement it?**  
A: No. Simply remove `"get_financial_statements"` from the class's `supported_methods` list. The CDK testing harness will automatically skip it.

**Q: I want to add a completely new market region (e.g. Thailand). What should I do?**  
A: You will need to create a new folder under `openstockapi/providers/th_stock/` and register `TH` in `settings.py`. Open an issue first to coordinate design changes.
