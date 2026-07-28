# US Stock News & Events

## Use Case 11.8 — US Stock News

**Required Tier:** `Free`

**API:** `us_news(symbol: str, provider: Optional[str] = None)`

Retrieve stock-specific corporate financial news articles.

### Code Snippet

```python
news = osapi.us_news("AAPL", provider="google_news")
print(news["news"][0]["title"])
```

### Sample Output

```json
{
  "symbol": "AAPL",
  "news": [
    {
      "id": "12345",
      "title": "Apple Reports Third Quarter Results",
      "url": "https://news.google.com/...",
      "published_at": "2026-07-23T20:19:30Z",
      "publisher": "Google News",
      "summary": "Apple today announced financial results for its fiscal 2026 third quarter..."
    }
  ],
  "provider": "google_news",
  "market": "us",
  "asset_class": "stock"
}
```

### Parameters

| `symbol` | `str` | Yes | - | US stock ticker symbol (e.g., `AAPL`, `MSFT`). |
| `provider` | `str` | No | `None` | Restrict query to a specific provider. Valid choices: `"yahoo"`, `"google_news"`. |

---

