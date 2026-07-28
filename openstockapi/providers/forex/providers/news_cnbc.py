import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from email.utils import parsedate_to_datetime

class CNBCForexNewsProvider:
    def __init__(self, feed_name: str = "CNBC", feed_url: str = "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664"):
        self.feed_name = feed_name
        self.feed_url = feed_url

    async def get_news(self, limit: int = 20) -> List[Dict[str, Any]]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(self.feed_url, headers=headers)
                if res.status_code == 200:
                    root = ET.fromstring(res.content)
                    items = root.findall(".//item")
                    news_list = []
                    for item in items[:limit]:
                        title = item.find("title")
                        link = item.find("link")
                        pub_date = item.find("pubDate")
                        desc = item.find("description")
                        
                        title_str = title.text if title is not None else ""
                        link_str = link.text if link is not None else ""
                        desc_str = desc.text if desc is not None else ""
                        
                        ts = 0
                        if pub_date is not None and pub_date.text:
                            try:
                                dt = parsedate_to_datetime(pub_date.text)
                                ts = int(dt.timestamp() * 1000)
                            except Exception:
                                pass
                                
                        news_list.append({
                            "id": link_str,
                            "title": title_str,
                            "url": link_str,
                            "published_at": ts,
                            "source": self.feed_name,
                            "summary": desc_str
                        })
                    return news_list
        except Exception:
            pass
        return []
