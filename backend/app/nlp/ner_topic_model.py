import re
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from .preprocessor import preprocessor

TOPIC_CATEGORIES = {
    "Product Quality & Features": ["feature", "update", "quality", "design", "interface", "app", "software", "version", "build", "usability"],
    "Customer Support & Service": ["support", "service", "help", "ticket", "response", "staff", "representative", "contact", "issue"],
    "Pricing & Billing": ["price", "pricing", "cost", "subscription", "expensive", "cheap", "fee", "bill", "refund", "dollar", "plan"],
    "Performance & Reliability": ["speed", "slow", "fast", "crash", "outage", "downtime", "lag", "bug", "performance", "server", "stable"],
    "Security & Data Privacy": ["security", "privacy", "breach", "hack", "leak", "password", "encryption", "vulnerability", "auth", "trust"],
    "Financial & Market Performance": ["earnings", "stock", "shares", "revenue", "quarter", "investor", "growth", "market", "valuation", "profit"]
}

KNOWN_ENTITIES = {
    "Brand": ["Tesla", "Apple", "Microsoft", "OpenAI", "Google", "Amazon", "Meta", "Netflix", "Uber", "Spotify"],
    "Product": ["iPhone", "Windows", "ChatGPT", "Azure", "AWS", "Model 3", "CyberTruck", "Pixel", "PlayStation", "Xbox"],
    "Organization": ["SEC", "FTC", "Wall Street", "Federal Reserve", "EU Commission", "NASDAQ", "NYSE"],
    "Person": ["Elon Musk", "Tim Cook", "Satya Nadella", "Sam Altman", "Sundar Pichai", "Jeff Bezos", "Mark Zuckerberg"],
    "Location": ["Silicon Valley", "New York", "California", "Texas", "London", "Tokyo", "Berlin", "San Francisco"]
}

class TopicAndNERExtractor:
    def __init__(self):
        pass

    def extract_topics(self, text: str, max_topics: int = 3) -> List[str]:
        """Classifies text into key predefined topic categories based on keyword relevance."""
        cleaned_text = text.lower()
        topic_scores = {}

        for category, keywords in TOPIC_CATEGORIES.items():
            score = 0
            for kw in keywords:
                if re.search(rf'\b{kw}\b', cleaned_text):
                    score += 1
            if score > 0:
                topic_scores[category] = score

        if not topic_scores:
            # Fallback to keyword extraction
            keywords = preprocessor.extract_keywords(text, top_n=2)
            if keywords:
                return [f"General ({', '.join(keywords)})"]
            return ["General Discussions"]

        sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
        return [t[0] for t in sorted_topics[:max_topics]]

    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extracts Named Entities: Brand, Product, Person, Organization, Location.
        Combines pattern matching, capitalized phrase detection, and known dictionaries.
        """
        entities = []
        found_names = set()

        # 1. Match known dictionary entities
        for category, names in KNOWN_ENTITIES.items():
            for name in names:
                pattern = rf'\b{re.escape(name)}\b'
                if re.search(pattern, text, re.IGNORECASE):
                    if name.lower() not in found_names:
                        entities.append({"name": name, "entity_type": category})
                        found_names.add(name.lower())

        # 2. Extract capitalized phrases (heuristic for NER)
        words = text.split()
        for i, word in enumerate(words):
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word and clean_word[0].isupper() and len(clean_word) > 2:
                if clean_word.lower() not in found_names and clean_word.lower() not in preprocessor.stop_words:
                    # Guess entity type
                    if clean_word in ["Inc", "Corp", "Ltd", "Group", "Co"]:
                        category = "Organization"
                    elif clean_word in ["USA", "UK", "Europe", "Asia"]:
                        category = "Location"
                    else:
                        category = "Organization"
                    
                    entities.append({"name": clean_word, "entity_type": category})
                    found_names.add(clean_word.lower())

        return entities[:8]  # Top 8 entities max

ner_topic_extractor = TopicAndNERExtractor()
