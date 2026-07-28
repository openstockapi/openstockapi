import httpx
from typing import List, Dict, Any

class DailyFXCalendarProvider:
    async def get_events(self) -> List[Dict[str, Any]]:
        # DailyFX provides a JSON economic calendar endpoint
        url = "https://www.dailyfx.com/calendar/dailyfx-calendar.json"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    events = []
                    # DailyFX JSON has list of events
                    for item in data[:50]:
                        events.append({
                            "title": item.get("title") or item.get("event"),
                            "currency": item.get("currency"),
                            "date": item.get("date"),
                            "time": item.get("time"),
                            "impact": item.get("importance") or item.get("impact"),
                            "forecast": item.get("forecast"),
                            "previous": item.get("previous")
                        })
                    if events:
                        return events
        except Exception:
            pass
            
        # Return empty list on failure
        return []
