import re
import html
import nltk
from typing import List

# Ensure necessary NLTK data is available
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Fallback stopwords if nltk fails
FALLBACK_STOPWORDS = set([
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers",
    "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does",
    "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
    "while", "of", "at", "by", "for", "with", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then", "once"
])

class TextPreprocessor:
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except Exception:
            self.stop_words = FALLBACK_STOPWORDS
            
        try:
            self.lemmatizer = WordNetLemmatizer()
        except Exception:
            self.lemmatizer = None

    def clean_text(self, text: str) -> str:
        """Removes HTML tags, URLs, special characters, and normalizes spaces."""
        if not text:
            return ""
        
        # 1. Unescape HTML entities & strip tags
        text = html.unescape(text)
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # 2. Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # 3. Remove user mentions and hashtag symbols
        text = re.sub(r'@\w+|#', '', text)
        
        # 4. Remove special characters and numbers (keep letters and basic punctuation for sentence context)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # 5. Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def process_text(self, text: str) -> str:
        """Complete NLP pipeline: Clean -> Tokenize -> Lowercase -> Remove Stopwords -> Lemmatize."""
        cleaned = self.clean_text(text)
        if not cleaned:
            return ""
        
        tokens = cleaned.lower().split()
        processed_tokens = []
        
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                if self.lemmatizer:
                    try:
                        lemma = self.lemmatizer.lemmatize(token)
                    except Exception:
                        lemma = token
                else:
                    lemma = token
                processed_tokens.append(lemma)
                
        return " ".join(processed_tokens)

    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """Utility for quick keyword extraction from text."""
        processed = self.process_text(text)
        words = processed.split()
        freq = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:top_n]]

preprocessor = TextPreprocessor()
