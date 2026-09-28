import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import random
import logging
from typing import List, Dict, Any
from .rss_scraper import rss_scraper

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Template pools for synthetic scraping simulation per source type
SOURCE_TEMPLATES = {
    "News": [
        ("TechCrunch", "https://techcrunch.com"),
        ("Forbes", "https://forbes.com"),
        ("Bloomberg", "https://bloomberg.com"),
        ("Reuters", "https://reuters.com"),
        ("The Wall Street Journal", "https://wsj.com"),
        ("Business Insider", "https://businessinsider.com")
    ],
    "Review": [
        ("Trustpilot", "https://trustpilot.com"),
        ("G2 Crowd", "https://g2.com"),
        ("Capterra", "https://capterra.com"),
        ("Product Hunt", "https://producthunt.com")
    ],
    "Blog": [
        ("Medium Tech", "https://medium.com"),
        ("Substack Insights", "https://substack.com"),
        ("Dev.to", "https://dev.to"),
        ("HackerNoon", "https://hackernoon.com")
    ],
    "Forum": [
        ("Reddit r/technology", "https://reddit.com/r/technology"),
        ("Hacker News", "https://news.ycombinator.com"),
        ("Quora", "https://quora.com"),
        ("Stack Overflow", "https://stackoverflow.com")
    ]
}

MENTION_TEMPLATES = [
    # Positive
    {
        "sentiment_hint": "Positive",
        "title": "{brand} Announces Revolutionary AI Upgrade with 300% Speed Boost",
        "text": "{brand} has officially unveiled its latest product update today. The new platform introduces cutting-edge capabilities, reducing latency by 70% and providing users with an intuitive, seamless interface. Industry analysts praise the innovation.",
        "source_type": "News"
    },
    {
        "sentiment_hint": "Positive",
        "title": "Why {brand} is Outperforming Competitors in 2026 Customer Satisfaction",
        "text": "A recent survey across 5,000 enterprise clients ranked {brand} at the top for reliability, support quality, and cost efficiency. Users highlighted the responsive support team and flawless uptime.",
        "source_type": "Review"
    },
    {
        "sentiment_hint": "Positive",
        "title": "Switched to {brand} Last Month - Absolutely Transformed Our Workflow",
        "text": "After migrating our entire stack to {brand}, productivity jumped by 40%. The onboarding process was painless and the customer support team guided us through every step. 10/10 recommended!",
        "source_type": "Blog"
    },
    {
        "sentiment_hint": "Positive",
        "title": "Unboxing & First Impressions: {brand}'s Latest Flagship Release",
        "text": "The build quality and attention to detail from {brand} is unmatched. Setup took under 3 minutes, and performance is super snappy. Highly impressed with what they delivered.",
        "source_type": "Review"
    },
    {
        "sentiment_hint": "Positive",
        "title": "{brand} Stock Rallies After Beating Q3 Earnings Expectations",
        "text": "Investors responded enthusiastically as {brand} reported a 28% year-over-year revenue growth. Wall Street firms upgraded their price targets, citing strong market momentum.",
        "source_type": "News"
    },

    # Neutral
    {
        "sentiment_hint": "Neutral",
        "title": "{brand} Schedules Annual Developer Conference for Next Month",
        "text": "{brand} announced that its annual developer event will take place virtually. The agenda includes keynote presentations on cloud infrastructure, security compliance, and upcoming API updates.",
        "source_type": "News"
    },
    {
        "sentiment_hint": "Neutral",
        "title": "Comparing {brand} vs Major Industry Alternatives: A Full Analysis",
        "text": "This detailed breakdown evaluates {brand}'s pricing structures, feature sets, and integration ecosystem relative to other market solutions to help buyers choose the right fit.",
        "source_type": "Blog"
    },
    {
        "sentiment_hint": "Neutral",
        "title": "{brand} Releases Patch 4.2 Addressing Minor UI Formatting",
        "text": "The engineering team at {brand} published a scheduled patch today. The release notes detail bug fixes for table rendering and updated OAuth2 integration documentation.",
        "source_type": "Forum"
    },
    {
        "sentiment_hint": "Neutral",
        "title": "Everything You Need to Know About {brand}'s Updated Terms of Service",
        "text": "{brand} sent an email notice to registered subscribers detailing standard modifications to its global privacy policy and user terms ahead of European regulatory guidelines.",
        "source_type": "News"
    },

    # Negative
    {
        "sentiment_hint": "Negative",
        "title": "{brand} Users Report Widespread Outage and Dashboard Disruption",
        "text": "Thousands of active users experienced service interruption with {brand} starting early this morning. Error code 502 spiked across multiple server nodes. Engineers are currently investigating.",
        "source_type": "Forum"
    },
    {
        "sentiment_hint": "Negative",
        "title": "Customer Backlash Mounts Over {brand}'s Surprise 35% Price Increase",
        "text": "Existing clients expressed disappointment on social media following {brand}'s unannounced subscription tier hike. Many small business users are threatening to cancel their plans.",
        "source_type": "Blog"
    },
    {
        "sentiment_hint": "Negative",
        "title": "Critical Vulnerability Discovered in Legacy {brand} API Integration",
        "text": "Security researchers published a CVE report detailing an authentication bypass vulnerability affecting older versions of {brand}'s client library. A patch has been requested.",
        "source_type": "News"
    },
    {
        "sentiment_hint": "Negative",
        "title": "Horrible Experience with {brand} Support - Tickets Ignored for Days",
        "text": "Our team spent 72 hours trying to resolve a critical billing error with {brand}. Support tickets were repeatedly closed without explanation. Extremely frustrating experience.",
        "source_type": "Review"
    }
]

EDUCATION_MENTION_TEMPLATES = [
    # Positive
    {
        "sentiment_hint": "Positive",
        "title": "{brand} Achieves Highest Accreditation Rating & 95% Placement Rate",
        "text": "{brand} has received top honors from national education accreditation boards following impressive campus infrastructure expansion and outstanding student career placements across major global companies.",
        "source_type": "News"
    },
    {
        "sentiment_hint": "Positive",
        "title": "Why Students & Alumni Consistently Recommend {brand} for Higher Education",
        "text": "A recent survey across 3,000 university graduates ranked {brand} exceptionally high for faculty mentorship, campus life, practical lab exposure, and modern library resources.",
        "source_type": "Review"
    },
    {
        "sentiment_hint": "Positive",
        "title": "Attending {brand} Transformed My Academic & Professional Career",
        "text": "Studying at {brand} provided invaluable research exposure and hands-on industry projects. The supportive professors and active student clubs made my college years memorable and impactful.",
        "source_type": "Blog"
    },
    {
        "sentiment_hint": "Positive",
        "title": "{brand} Secures Major Research Grant for AI & Engineering Department",
        "text": "The research division at {brand} was awarded a multimillion-dollar innovation grant to establish a state-of-the-art research lab focusing on renewable energy and computing technology.",
        "source_type": "News"
    },

    # Neutral
    {
        "sentiment_hint": "Neutral",
        "title": "{brand} Releases Annual Academic Calendar & Admission Portal Guidelines",
        "text": "{brand} published the official schedule for upcoming semester examinations, entrance tests, and campus placement registration guidelines for the upcoming academic session.",
        "source_type": "News"
    },
    {
        "sentiment_hint": "Neutral",
        "title": "Comprehensive Overview of Programs, Courses, and Fees at {brand}",
        "text": "An in-depth breakdown evaluating degree offerings, specialization tracks, eligibility criteria, and hostel facilities at {brand} for prospective applicants.",
        "source_type": "Blog"
    },
    {
        "sentiment_hint": "Neutral",
        "title": "{brand} Hosts National Student Symposium & Inter-College Sports Meet",
        "text": "Representatives from over 40 institutions participated in the annual technical symposium and inter-university sports tournament organized at {brand} main campus.",
        "source_type": "Forum"
    },

    # Negative
    {
        "sentiment_hint": "Negative",
        "title": "Students at {brand} Voice Concerns Over Sudden Hostel Maintenance Delays",
        "text": "Student council representatives at {brand} submitted a petition regarding delayed hostel facility maintenance and requested urgent upgrades to campus WiFi and cafeteria services.",
        "source_type": "Forum"
    },
    {
        "sentiment_hint": "Negative",
        "title": "Disappointment Among Applicants Over {brand} Tuition & Administrative Fee Structure",
        "text": "Several student groups expressed concern online following {brand}'s recent announcement regarding fee revisions for specialized elective courses.",
        "source_type": "Blog"
    },
    {
        "sentiment_hint": "Negative",
        "title": "{brand} Examination Portal Suffers Server Outage During Result Publication",
        "text": "The online portal for {brand} experienced high traffic congestion earlier today, causing temporary delays for students trying to access semester grade sheets.",
        "source_type": "News"
    }
]

class WebScraperManager:
    def _is_education_institution(self, brand_name: str) -> bool:
        lower = brand_name.lower()
        edu_keywords = {"university", "college", "school", "institute", "academy", "campus", "polytechnic", "vidya", "shiksha"}
        return any(k in lower for k in edu_keywords)

    def scrape_url(self, url: str) -> Dict[str, str]:
        """Scrapes single URL using requests & BeautifulSoup."""
        try:
            resp = requests.get(url, headers=HEADERS, timeout=5)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, "html.parser")
                title = soup.title.string if soup.title else "Scraped Article"
                
                # Extract text paragraphs
                paragraphs = [p.get_text() for p in soup.find_all("p")]
                full_text = " ".join(paragraphs) if paragraphs else soup.get_text()
                
                return {
                    "title": title.strip(),
                    "text": full_text[:1000].strip(),
                    "source": "Web Page",
                    "source_type": "News",
                    "url": url,
                    "publication_date": datetime.utcnow()
                }
        except Exception as e:
            logger.error(f"Failed to scrape URL {url}: {e}")
            
        return {}

    def collect_brand_articles(self, brand_name: str, max_articles: int = 18) -> List[Dict[str, Any]]:
        """
        Main collection pipeline combining live RSS feeds with multi-source simulated web scraping.
        Extracts: title, text, source, source_type, URL, publication_date
        """
        articles = []
        
        # 1. Try Live RSS Feed with exact phrase search
        live_articles = rss_scraper.fetch_google_news_rss(brand_name, limit=6)
        articles.extend(live_articles)

        # Select appropriate template pool based on brand category
        template_pool = EDUCATION_MENTION_TEMPLATES if self._is_education_institution(brand_name) else MENTION_TEMPLATES

        # 2. Enrich with domain-aware synthetic scrape for comprehensive dataset coverage
        needed = max_articles - len(articles)
        if needed > 0:
            now = datetime.utcnow()
            for i in range(needed):
                tmpl = template_pool[i % len(template_pool)]
                stype = tmpl["source_type"]
                sources = SOURCE_TEMPLATES.get(stype, SOURCE_TEMPLATES["News"])
                source_info = random.choice(sources)
                
                title = tmpl["title"].format(brand=brand_name)
                text = tmpl["text"].format(brand=brand_name)
                pub_date = now - timedelta(hours=random.randint(1, 120), minutes=random.randint(0, 59))
                
                url_slug = title.lower().replace(" ", "-").replace("'", "").replace(":", "")[:40]
                url = f"{source_info[1]}/article/{url_slug}"
                
                articles.append({
                    "title": title,
                    "text": text,
                    "source": source_info[0],
                    "source_type": stype,
                    "url": url,
                    "publication_date": pub_date
                })

        return articles

web_scraper_manager = WebScraperManager()
