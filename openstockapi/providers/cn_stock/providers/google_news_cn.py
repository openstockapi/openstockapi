import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict, Any

class GoogleNewsCNProvider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    async def get_news(self, symbol: str) -> List[Dict[str, Any]]:
        sym_norm = symbol.upper().strip()
        sym_search = sym_norm.split(".")[0]
        
        url = "https://news.google.com/rss/search"
        params = {
            "q": f"{sym_search} 股票",
            "hl": "zh-CN",
            "gl": "CN",
            "ceid": "CN:zh-Hans"
        }
            
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params, headers=self.headers)
                if res.status_code == 200:
                    root = ET.fromstring(res.text)
                    items = root.findall(".//item")
                    
                    news_items = []
                    for item in items[:15]:
                        title = item.find("title").text if item.find("title") is not None else ""
                        link = item.find("link").text if item.find("link") is not None else ""
                        pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
                        
                        source_elem = item.find("source")
                        publisher = source_elem.text if source_elem is not None else "Google News"
                        
                        description_elem = item.find("description")
                        summary = description_elem.text if description_elem is not None else ""
                        
                        import re
                        summary_clean = re.sub('<[^<]+?>', '', summary).strip()

                        news_items.append({
                            "id": link,
                            "title": title,
                            "url": link,
                            "published_at": pub_date,
                            "publisher": publisher,
                            "summary": summary_clean
                        })
                    return news_items
        except Exception:
            pass
        return []
