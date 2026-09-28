import re
from typing import Dict

EMOTION_LEXICON = {
    "Joy": [
        "happy", "delighted", "love", "awesome", "fantastic", "great", "excellent",
        "best", "wonderful", "satisfied", "success", "innovative", "brilliant", "smooth", "excited"
    ],
    "Anger": [
        "angry", "furious", "outrageous", "terrible", "worst", "hate", "greedy",
        "rip-off", "scam", "unacceptable", "frustrated", "annoyed", "garbage", "trash"
    ],
    "Sadness": [
        "disappointed", "sad", "disappointing", "sorry", "loss", "regret", "depressing",
        "unfortunate", "hopeless", "heartbroken", "down", "pity"
    ],
    "Fear": [
        "afraid", "scared", "breach", "leak", "security", "threat", "vulnerability",
        "hack", "risk", "warning", "danger", "concerning", "unstable", "crash"
    ],
    "Surprise": [
        "shocking", "surprising", "unexpected", "unbelievable", "wow", "amazing",
        "unprecedented", "breakthrough", "sudden", "curious"
    ],
    "Disgust": [
        "gross", "disgusting", "revolting", "nasty", "horrible", "awful",
        "unethical", "shameful", "dirty", "corrupt"
    ]
}

class EmotionClassifier:
    def classify(self, text: str, sentiment: str = "Neutral") -> str:
        """
        Classifies input text into one of 6 core emotions:
        Joy, Anger, Sadness, Fear, Surprise, Disgust
        """
        words = set(re.sub(r'[^a-zA-Z\s]', '', text.lower()).split())
        
        scores: Dict[str, int] = {emotion: 0 for emotion in EMOTION_LEXICON}
        
        for emotion, keywords in EMOTION_LEXICON.items():
            for kw in keywords:
                if kw in words:
                    scores[emotion] += 1
                    
        # Find maximum scored emotion
        best_emotion = max(scores, key=scores.get)
        if scores[best_emotion] > 0:
            return best_emotion
            
        # Fallback heuristic aligned with predicted sentiment
        if sentiment == "Positive":
            return "Joy"
        elif sentiment == "Negative":
            # Default negative emotion heuristic
            if any(w in words for w in ["hack", "leak", "breach", "security", "down"]):
                return "Fear"
            elif any(w in words for w in ["broken", "fail", "slow", "poor"]):
                return "Sadness"
            else:
                return "Anger"
        else:
            return "Surprise" if "?" in text or "!" in text else "Joy"

    def get_emotion_scores(self, text: str) -> Dict[str, float]:
        """Returns relative distribution across all 6 emotions."""
        words = set(re.sub(r'[^a-zA-Z\s]', '', text.lower()).split())
        scores = {emotion: 1.0 for emotion in EMOTION_LEXICON}  # base smoothing
        
        for emotion, keywords in EMOTION_LEXICON.items():
            for kw in keywords:
                if kw in words:
                    scores[emotion] += 2.0
                    
        total = sum(scores.values())
        return {e: round(v / total, 3) for e, v in scores.items()}

emotion_classifier = EmotionClassifier()
