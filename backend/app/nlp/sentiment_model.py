import os
import re
import joblib
import numpy as np
import nltk
from typing import Dict, Any, List

# Try importing Hugging Face Transformers pipeline for DistilBERT
try:
    from transformers import pipeline
    transformer_sentiment = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        truncation=True,
        max_length=512
    )
except Exception:
    transformer_sentiment = None

# Ensure VADER lexicon is available
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    try:
        nltk.download('vader_lexicon', quiet=True)
    except Exception:
        pass

try:
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    vader_analyzer = SentimentIntensityAnalyzer()
except Exception:
    vader_analyzer = None

from .preprocessor import preprocessor

MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")

# 1. High-Precision Domain Override Lexicons
STRONG_NEGATIVE_KEYWORDS = {
    "vulnerability", "breach", "outage", "disruption", "violence", "arson", "loot", "vandalism",
    "backlash", "criticism", "failure", "exploit", "scars", "scandal", "fire", "tore", "riot",
    "brawl", "hike", "protest", "strike", "dispute", "crashes", "leaks", "investigation", "police",
    "court", "fined", "penalty", "damage", "damaged", "scam", "fraud", "hacked", "stolen", "unrest",
    "horrible", "terrible", "disastrous", "overpriced", "threat", "rods", "masks", "rumour", "rumor",
    "outsider", "outsiders", "interruption", "interrupted"
}

STRONG_POSITIVE_KEYWORDS = {
    "outperforming", "accreditation", "placement", "placements", "award", "excellence", "breakthrough",
    "milestone", "praise", "accolades", "unmatched", "transformed", "grant", "record", "rallies",
    "unveiled", "revolutionary", "top tier", "highest", "seamless", "outstanding"
}

NEGATION_WORDS = {"no", "not", "never", "without", "failed to", "prevented", "zero", "denied", "false"}

class ContextAwareSentimentAnalyzer:
    def __init__(self):
        self.vader = vader_analyzer
        self.transformer = transformer_sentiment

    def _has_negation(self, text: str, target_word: str) -> bool:
        """Checks if a keyword in text is preceded by a negation word within a 3-word context window."""
        words = text.lower().split()
        for i, w in enumerate(words):
            if target_word in w:
                window = words[max(0, i - 3):i]
                if any(neg in window for neg in NEGATION_WORDS):
                    return True
        return False

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Multi-Layer Context-Aware Sentiment Analysis Engine:
        Layer 1: Domain-Specific Override Rules
        Layer 2: Negation & Context Handling
        Layer 3: DistilBERT Transformer Model / VADER Ensemble
        Layer 4: Confidence Score Calculation
        """
        if not text or not text.strip():
            return {
                "sentiment": "Neutral",
                "score": 0.0,
                "confidence": 0.50,
                "probabilities": {"Positive": 0.33, "Neutral": 0.34, "Negative": 0.33}
            }

        text_lower = text.lower()
        cleaned_words = set(re.sub(r'[^a-zA-Z\s]', ' ', text_lower).split())

        # Layer 1: Domain Override Rule Engine
        neg_matches = [w for w in STRONG_NEGATIVE_KEYWORDS if w in cleaned_words or w in text_lower]
        pos_matches = [w for w in STRONG_POSITIVE_KEYWORDS if w in cleaned_words or w in text_lower]

        active_neg = [w for w in neg_matches if not self._has_negation(text, w)]
        active_pos = [w for w in pos_matches if not self._has_negation(text, w)]

        if active_neg and len(active_neg) >= len(active_pos):
            conf = min(0.98, 0.85 + 0.04 * len(active_neg))
            return {
                "sentiment": "Negative",
                "score": -round(conf, 3),
                "confidence": round(conf, 3),
                "probabilities": {
                    "Positive": round((1.0 - conf) / 2, 3),
                    "Neutral": round((1.0 - conf) / 2, 3),
                    "Negative": round(conf, 3)
                }
            }
        elif active_pos and len(active_pos) > len(active_neg):
            conf = min(0.98, 0.85 + 0.04 * len(active_pos))
            return {
                "sentiment": "Positive",
                "score": round(conf, 3),
                "confidence": round(conf, 3),
                "probabilities": {
                    "Positive": round(conf, 3),
                    "Neutral": round((1.0 - conf) / 2, 3),
                    "Negative": round((1.0 - conf) / 2, 3)
                }
            }

        # Layer 2: Transformer Pipeline (DistilBERT)
        if self.transformer:
            try:
                t_res = self.transformer(text[:512])[0]
                label = t_res["label"].upper()
                score_val = t_res["score"]
                
                if label == "NEGATIVE" and score_val > 0.60:
                    return {
                        "sentiment": "Negative",
                        "score": -round(score_val, 3),
                        "confidence": round(score_val, 3),
                        "probabilities": {"Positive": round(1 - score_val, 3), "Neutral": 0.05, "Negative": round(score_val, 3)}
                    }
                elif label == "POSITIVE" and score_val > 0.60:
                    return {
                        "sentiment": "Positive",
                        "score": round(score_val, 3),
                        "confidence": round(score_val, 3),
                        "probabilities": {"Positive": round(score_val, 3), "Neutral": 0.05, "Negative": round(1 - score_val, 3)}
                    }
            except Exception:
                pass

        # Layer 3: VADER Polarity Fallback
        vader_comp = 0.0
        if self.vader:
            try:
                vs = self.vader.polarity_scores(text)
                vader_comp = vs["compound"]
            except Exception:
                pass

        if vader_comp <= -0.05:
            conf = min(0.95, 0.60 + abs(vader_comp) * 0.35)
            return {
                "sentiment": "Negative",
                "score": round(vader_comp, 3),
                "confidence": round(conf, 3),
                "probabilities": {"Positive": round((1 - conf) / 2, 3), "Neutral": round((1 - conf) / 2, 3), "Negative": round(conf, 3)}
            }
        elif vader_comp >= 0.05:
            conf = min(0.95, 0.60 + vader_comp * 0.35)
            return {
                "sentiment": "Positive",
                "score": round(vader_comp, 3),
                "confidence": round(conf, 3),
                "probabilities": {"Positive": round(conf, 3), "Neutral": round((1 - conf) / 2, 3), "Negative": round((1 - conf) / 2, 3)}
            }

        return {
            "sentiment": "Neutral",
            "score": 0.0,
            "confidence": 0.70,
            "probabilities": {"Positive": 0.25, "Neutral": 0.50, "Negative": 0.25}
        }

sentiment_analyzer = ContextAwareSentimentAnalyzer()
