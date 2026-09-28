import os
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from .preprocessor import preprocessor

MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")
MODEL_PATH = os.path.join(MODEL_DIR, "sentiment_model.joblib")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib")

# Seed Dataset for Logistic Regression Training
SEED_DATASET = [
    # Positive (🟢)
    ("Outstanding product quality, fantastic customer service and fast delivery!", "Positive"),
    ("I absolutely love this brand! Best purchase I've made all year.", "Positive"),
    ("Great innovation, excellent support team and robust security features.", "Positive"),
    ("Their stock reached record highs today due to overwhelming positive sales reports.", "Positive"),
    ("Seamless user experience, intuitive interface, highly recommended.", "Positive"),
    ("Customer support resolved my issue in 5 minutes. Amazing service!", "Positive"),
    ("Game changer in the industry. Super reliable and cost-effective.", "Positive"),
    ("Clean UI, fast speed, and wonderful performance overall.", "Positive"),
    ("Top tier company with impressive leadership and employee satisfaction.", "Positive"),
    ("Solid earnings report. Wall Street analysts upgrade ratings to strong buy.", "Positive"),
    ("Love the new features in the latest update. Super smooth!", "Positive"),
    ("Exceeded all expectations! Truly impressive performance.", "Positive"),
    ("University achieves top NIRF ranking and record campus placements this year.", "Positive"),
    ("Faculty research paper published in prestigious international journal with high accolades.", "Positive"),
    ("State of the art campus laboratory facilities and vibrant student community.", "Positive"),
    
    # Neutral (🟡)
    ("The company announced its Q3 financial results earlier today.", "Neutral"),
    ("They released a new software patch version 2.4 today.", "Neutral"),
    ("The executive team will host a press conference tomorrow at 10 AM.", "Neutral"),
    ("Product specifications include 16GB RAM and 512GB SSD storage.", "Neutral"),
    ("The brand opened a new office location in Chicago last week.", "Neutral"),
    ("User manual and API documentation have been updated on the website.", "Neutral"),
    ("Market share remains stable compared to the previous quarter.", "Neutral"),
    ("The meeting discussed upcoming roadmap milestones for next year.", "Neutral"),
    ("Pricing plans start at $19 per month for basic subscription.", "Neutral"),
    ("System maintenance is scheduled for Sunday midnight UTC.", "Neutral"),
    ("The university announced semester examination dates and timetable on portal.", "Neutral"),
    ("Annual sports meet and cultural festival scheduled for next month.", "Neutral"),
    
    # Negative (🔴)
    ("Terrible experience! The product broke within 2 days of usage.", "Negative"),
    ("Massive data breach leaks user passwords! Complete security failure.", "Negative"),
    ("System outage causes millions in losses. Customers are furious.", "Negative"),
    ("Horrible customer support, nobody answers emails or calls.", "Negative"),
    ("Overpriced, buggy software with frequent crashes and lag.", "Negative"),
    ("Customer complaints surge after surprise price hike and feature removal.", "Negative"),
    ("Disastrous product launch. Full of bugs and missing promised features.", "Negative"),
    ("Regulatory agency fines company $50M for anti-competitive behavior.", "Negative"),
    ("Poor quality, flimsy build, waste of money. Returning immediately!", "Negative"),
    ("Shares drop 15% after missing revenue targets and guidance downgrade.", "Negative"),
    ("Unreliable service, constant downtime, and zero transparency.", "Negative"),
    ("Worst purchase ever. Fraudulent advertising and poor service.", "Negative"),
    ("Students protest unexpected tuition fee hike and hostel maintenance delays.", "Negative"),
    ("Severe backlash over delayed exam results and poor campus administrative response.", "Negative")
]

class SentimentAnalyzer:
    def __init__(self):
        self.vectorizer = None
        self.model = None
        self._initialize_or_load_model()

    def _initialize_or_load_model(self):
        os.makedirs(MODEL_DIR, exist_ok=True)
        # Always retrain seed model to ensure updated vocabulary is active
        self.train_seed_model()

    def train_seed_model(self):
        texts = [preprocessor.process_text(item[0]) for item in SEED_DATASET]
        labels = [item[1] for item in SEED_DATASET]
        
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        X = self.vectorizer.fit_transform(texts)
        
        self.model = LogisticRegression(C=1.0, max_iter=200, random_state=42)
        self.model.fit(X, labels)
        
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.vectorizer, VECTORIZER_PATH)

    def analyze(self, text: str) -> dict:
        """
        Analyzes sentiment of given text.
        Returns: {
            'sentiment': 'Positive' | 'Neutral' | 'Negative',
            'score': float (-1.0 to 1.0),
            'probabilities': {'Positive': float, 'Neutral': float, 'Negative': float}
        }
        """
        cleaned_text = preprocessor.process_text(text)
        if not cleaned_text:
            return {"sentiment": "Neutral", "score": 0.0, "probabilities": {"Positive": 0.33, "Neutral": 0.34, "Negative": 0.33}}

        # Lexicon keywords for additional polarity boost
        pos_words = {
            "love", "amazing", "great", "excellent", "best", "fantastic", "smooth", "high", "upgrade", 
            "clean", "impressive", "outstanding", "solid", "top", "rank", "ranking", "placed", "placement", 
            "accredited", "praise", "accolades", "vibrant", "success"
        }
        neg_words = {
            "terrible", "worst", "buggy", "broke", "crash", "breach", "outage", "furious", "disaster", 
            "fine", "fraud", "lag", "horrible", "overpriced", "drop", "backlash", "complaint", "protest", 
            "delay", "fail", "failure", "concern", "criticism", "poor", "bad", "hike", "scam", "upset", 
            "cancel", "disappointment", "backlash"
        }
        
        raw_words = set(preprocessor.clean_text(text).lower().split())
        pos_hits = len(raw_words.intersection(pos_words))
        neg_hits = len(raw_words.intersection(neg_words))
        
        X = self.vectorizer.transform([cleaned_text])
        probs = self.model.predict_proba(X)[0]
        classes = self.model.classes_
        
        prob_dict = {cls: float(prob) for cls, prob in zip(classes, probs)}
        for k in ["Positive", "Neutral", "Negative"]:
            if k not in prob_dict:
                prob_dict[k] = 0.0

        # Adjust with lexicon hits
        if pos_hits > neg_hits:
            prob_dict["Positive"] += 0.25 * pos_hits
        elif neg_hits > pos_hits:
            prob_dict["Negative"] += 0.25 * neg_hits

        # Normalize probabilities
        total_p = sum(prob_dict.values())
        prob_dict = {k: v / total_p for k, v in prob_dict.items()}

        predicted_sentiment = max(prob_dict, key=prob_dict.get)
        
        # Calculate continuous sentiment score between -1.0 and +1.0
        score = prob_dict.get("Positive", 0.0) - prob_dict.get("Negative", 0.0)

        return {
            "sentiment": predicted_sentiment,
            "score": round(score, 3),
            "probabilities": {k: round(v, 3) for k, v in prob_dict.items()}
        }

sentiment_analyzer = SentimentAnalyzer()
