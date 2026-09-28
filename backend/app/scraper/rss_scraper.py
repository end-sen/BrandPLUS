import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

class RSSScraper:
    def fetch_google_news_rss(self, brand_name: str, limit: int = 10) -> list:
        """Fetches live news articles for brand_name from Google News RSS feed with exact phrase search & relevance check."""
        # Use quotes for exact phrase matching in Google News query
        exact_query = f'"{brand_name.strip()}"'
        encoded_brand = quote_plus(exact_query)
        rss_url = f"https://news.google.com/rss/search?q={encoded_brand}&hl=en-US&gl=US&ceid=US:en"
        
        articles = []
        brand_words = [w.lower() for w in brand_name.split() if len(w) > 2]
        
        try:
            response = requests.get(rss_url, headers=HEADERS, timeout=6)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                for item in root.findall(".//item"):
                    if len(articles) >= limit:
                        break

                    title = item.find("title").text if item.find("title") is not None else ""
                    link = item.find("link").text if item.find("link") is not None else ""
                    description = item.find("description").text if item.find("description") is not None else ""
                    
                    # Clean description text using BeautifulSoup
                    snippet = BeautifulSoup(description, "html.parser").get_text() if description else title
                    
                    # Parse source from title if available (e.g., "Title - SourceName")
                    source = "Google News"
                    if " - " in title:
                        parts = title.rsplit(" - ", 1)
                        title = parts[0]
                        source = parts[1]

                    # Validate relevance: check if exact brand name or key brand words are in title/snippet
                    full_content = f"{title} {snippet}".lower()
                    b_name_lower = brand_name.lower().strip()
                    
                    if b_name_lower in full_content or (len(brand_words) > 1 and all(w in full_content for w in brand_words)):
                        articles.append({
                            "title": title,
                            "text": snippet if len(snippet) > 30 else title,
                            "source": source,
                            "source_type": "News",
                            "url": link,
                            "publication_date": datetime.utcnow()
                        })
        except Exception as e:
            logger.warning(f"Error fetching Google News RSS for {brand_name}: {e}")
            
        return articles

rss_scraper = RSSScraper()
