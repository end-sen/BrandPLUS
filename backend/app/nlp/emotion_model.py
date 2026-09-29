import re
from typing import Dict

EMOTION_LEXICON = {
    "Joy": [
        "happy", "delighted", "love", "awesome", "fantastic", "great", "excellent",
        "best", "wonderful", "satisfied", "success", "innovative", "brilliant", "smooth", "excited",
        "outperforming", "victory", "award", "achievement", "placed", "accolades"
    ],
    "Anger": [
        "angry", "furious", "outrageous", "terrible", "worst", "hate", "greedy",
        "rip-off", "scam", "unacceptable", "frustrated", "annoyed", "garbage", "trash",
        "arson", "loot", "vandalism", "violence", "riot", "clash", "protest", "strike",
        "brawl", "outrage", "destroy", "destroyed", "vandalized"
    ],
    "Sadness": [
        "disappointed", "sad", "disappointing", "sorry", "loss", "regret", "depressing",
        "unfortunate", "hopeless", "heartbroken", "down", "pity", "scars", "littered",
        "tragedy", "injured", "injury", "casualty", "victim", "damaged"
    ],
    "Fear": [
        "afraid", "scared", "breach", "leak", "security", "threat", "vulnerability",
        "hack", "risk", "warning", "danger", "concerning", "unstable", "crash",
        "fire", "tore", "masks", "rod", "rods", "rumour", "rumor", "outsider", "outsiders",
        "police", "investigation", "unrest", "panic", "terror"
    ],
    "Surprise": [
        "shocking", "surprising", "unexpected", "unbelievable", "wow", "amazing",
        "unprecedented", "breakthrough", "sudden", "curious", "questions", "controversy"
    ],
    "Disgust": [
        "gross", "disgusting", "revolting", "nasty", "horrible", "awful",
        "unethical", "shameful", "dirty", "corrupt", "scandal", "fraud"
    ]
}

class EmotionClassifier:
    def classify(self, text: str, sentiment: str = "Neutral") -> str:
        """
        Classifies input text into one of 6 core emotions:
        Joy, Anger, Sadness, Fear, Surprise, Disgust
        """
        if not text:
            return "Joy" if sentiment == "Positive" else ("Anger" if sentiment == "Negative" else "Surprise")

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
            # Default negative emotion heuristics
            if any(w in words for w in ["fire", "hack", "leak", "breach", "security", "danger", "threat", "rod", "police", "rumour"]):
                return "Fear"
            elif any(w in words for w in ["arson", "loot", "vandalism", "violence", "riot", "clash", "protest", "angry"]):
                return "Anger"
            elif any(w in words for w in ["scars", "tragedy", "loss", "injury", "broken", "fail", "slow", "poor"]):
                return "Sadness"
            else:
                return "Anger"
        else:
            return "Surprise" if "?" in text or "!" in text else "Surprise"

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
