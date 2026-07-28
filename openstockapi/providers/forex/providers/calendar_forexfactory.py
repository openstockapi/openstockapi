import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict, Any

class ForexFactoryCalendarProvider:
    async def get_events(self) -> List[Dict[str, Any]]:
        url = "https://www.forexfactory.com/ff_calendar_thisweek.xml"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=headers)
                if res.status_code == 200:
                    root = ET.fromstring(res.content)
                    events = []
                    for ev in root.findall("event"):
                        title = ev.find("title")
                        country = ev.find("country")
                        date = ev.find("date")
                        time = ev.find("time")
                        impact = ev.find("impact")
                        forecast = ev.find("forecast")
                        previous = ev.find("previous")
                        
                        events.append({
                            "title": title.text if title is not None else "",
                            "currency": country.text if country is not None else "",
                            "date": date.text if date is not None else "",
                            "time": time.text if time is not None else "",
                            "impact": impact.text if impact is not None else "",
                            "forecast": forecast.text if forecast is not None else "",
                            "previous": previous.text if previous is not None else ""
                        })
                    return events
        except Exception:
            pass
        return []
