import pytest
from app.nlp.preprocessor import preprocessor
from app.nlp.sentiment_model import sentiment_analyzer
from app.nlp.emotion_model import emotion_classifier
from app.nlp.ner_topic_model import ner_topic_extractor

def test_text_cleaning():
    raw_html = "<p>Check out https://example.com for <b>great</b> updates! @user #awesome</p>"
    cleaned = preprocessor.clean_text(raw_html)
    assert "https" not in cleaned
    assert "<b>" not in cleaned
    assert "great updates" in cleaned

def test_nlp_processing():
    text = "The quick brown foxes are running fast!"
    processed = preprocessor.process_text(text)
    assert "fox" in processed or "running" in processed or "quick" in processed

def test_sentiment_analysis():
    pos_res = sentiment_analyzer.analyze("Outstanding quality, fast delivery, incredible experience!")
    assert pos_res["sentiment"] == "Positive"
    assert pos_res["score"] > 0

    neg_res = sentiment_analyzer.analyze("Terrible service, system broken, complete fraud.")
    assert neg_res["sentiment"] == "Negative"
    assert neg_res["score"] < 0

def test_emotion_detection():
    joy_em = emotion_classifier.classify("Love this amazing update, super excited!", "Positive")
    assert joy_em in ["Joy", "Surprise"]

    fear_em = emotion_classifier.classify("Massive data breach security leak warning threat", "Negative")
    assert fear_em in ["Fear", "Anger"]

def test_topic_and_ner_extraction():
    text = "Tesla announced record Model 3 sales in Silicon Valley while Elon Musk hosted quarterly earnings call."
    topics = ner_topic_extractor.extract_topics(text)
    entities = ner_topic_extractor.extract_entities(text)
    
    assert len(topics) > 0
    entity_names = [e["name"] for e in entities]
    assert "Tesla" in entity_names or "Elon Musk" in entity_names
