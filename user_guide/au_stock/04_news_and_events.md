# AU Stock News & Events

## Use Case 10.8 — Get Dividend History (ASX Dividends)

**Required Tier:** `Free`  
**API:** `asx_dividends(symbol, provider=None)`

Retrieves corporate dividend announcement history.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

divs = osapi.asx_dividends(symbol="BHP", provider="asx")
print(divs)
```

**Sample Output:**
```json
{
  "symbol": "BHP",
  "dividends": [
    {
      "ex_date": "2025-09-04",
      "pay_date": "2025-10-02",
      "amount": 1.09,
      "type": "Dividend",
      "franking": 1.0
    }
  ],
  "provider": "asx"
}
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | — | Stock ticker symbol (e.g. `BHP`) |
| `provider` | `str` | No | — | Optional. Explicitly select provider: `asx`, `marketindex`, `yahoo` |

---

## Use Case 10.9 — Get Company Announcements (ASX Announcements)

**Required Tier:** `Free`  
**API:** `asx_announcements(symbol, provider=None)`

Retrieves listed company announcements feed.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

announcements = osapi.asx_announcements(symbol="BHP", provider="asx")
print(announcements)
```

**Sample Output:**
```json
{
  "symbol": "BHP",
  "announcements": [
    {
      "date": "2026-07-20",
      "title": "BHP Operational Review for the year ended 30 June 2026",
      "url": "https://www.asx.com.au/asxpdf/20260720/pdf/example.pdf"
    }
  ],
  "provider": "asx"
}
```

#### Parameters
| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `symbol` | `str` | Yes | — | Stock ticker symbol (e.g. `BHP`) |
| `provider` | `str` | No | — | Optional. Explicitly select provider: `asx`, `marketindex` |

---

## Use Case 10.10 — Get Corporate News (ASX News)

**Required Tier:** `Free`  
**API:** `asx_news(symbol, provider=None)`

Retrieves recent news articles pertaining to the company.

```python
import openstockapi as osapi
osapi.init("your_free_api_key")

news_data = osapi.asx_news(symbol="BHP", provider="yahoo")
print(news_data)
```

**Sample Output:**
```json
{
  "symbol": "BHP",
  "news": [
    {
      "title": "BHP Group Limited Q4 Production Report Analysis",
      "publisher": "Core News",
      "link": "https://finance.yahoo.com/news/bhp-report-example"
    }
  ],
  "provider": "yahoo"
}
```

#### Parameters
| `symbol` | `str` | Yes | — | Stock ticker symbol (e.g. `BHP`) |
| `provider` | `str` | No | — | Optional. Explicitly select provider: `yahoo` |

---

