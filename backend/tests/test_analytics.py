from app.analytics.reputation_engine import reputation_engine
from app.analytics.summary_generator import summary_generator

class DummyArticle:
    def __init__(self, sentiment, sentiment_score, source="News", source_type="News", title="Test Title"):
        self.sentiment = sentiment
        self.sentiment_score = sentiment_score
        self.source = source
        self.source_type = source_type
        self.reliability_score = 0.9
        self.title = title

def test_reputation_score_calculation():
    articles = [
        DummyArticle("Positive", 0.8),
        DummyArticle("Positive", 0.9),
        DummyArticle("Neutral", 0.0),
        DummyArticle("Negative", -0.7)
    ]
    res = reputation_engine.calculate_reputation_score(articles)
    assert 0 <= res["score"] <= 100
    assert res["positive_pct"] == 50.0
    assert res["negative_pct"] == 25.0

def test_anomaly_detection():
    # Test high negative spike anomaly
    neg_articles = [DummyArticle("Negative", -0.8) for _ in range(6)] + [DummyArticle("Positive", 0.8) for _ in range(4)]
    anomalies = reputation_engine.detect_anomalies(neg_articles, [])
    assert len(anomalies) > 0
    assert anomalies[0]["type"] == "negative_spike"

def test_ai_summary_generation():
    articles = [DummyArticle("Positive", 0.8, title="Tesla beats earnings record")]
    score_data = {"score": 85.0, "positive_pct": 80.0, "negative_pct": 10.0, "health_status": "Excellent"}
    summary = summary_generator.generate_summary("Tesla", articles, score_data, [], [])
    assert "one_sentence_digest" in summary
    assert "Tesla" in summary["one_sentence_digest"]
    assert len(summary["action_items"]) > 0
