import json
from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..models import Brand, Article, Topic, Entity, Alert, ReputationScore
from ..schemas import (
    BrandCreate, BrandResponse, ArticleSchema, ReputationScoreSchema,
    AlertSchema, TopicSchema, EntitySchema, DashboardOverview, ExecutiveSummary
)
from ..scraper.web_scraper import web_scraper_manager
from ..nlp.sentiment_model import sentiment_analyzer
from ..nlp.emotion_model import emotion_classifier
from ..nlp.ner_topic_model import ner_topic_extractor
from ..analytics.reputation_engine import reputation_engine
from ..analytics.summary_generator import summary_generator
from ..realtime.websocket_manager import ws_manager

router = APIRouter()

@router.post("/brand/search", response_model=BrandResponse)
def search_and_monitor_brand(payload: BrandCreate, db: Session = Depends(get_db)):
    """
    POST /api/brand/search
    Starts or retrieves monitoring for a brand name.
    Triggers web scraping, NLP processing, sentiment classification, emotion detection, and reputation scoring.
    """
    brand_name = payload.name.strip()
    if not brand_name:
        raise HTTPException(status_code=400, detail="Brand name cannot be empty")

    brand = db.query(Brand).filter(Brand.name.ilike(brand_name)).first()
    
    if not brand:
        brand = Brand(name=brand_name, description=payload.description or f"Monitoring feedback and news for {brand_name}")
        db.add(brand)
        db.commit()
        db.refresh(brand)

        # Scrape initial article batch
        raw_articles = web_scraper_manager.collect_brand_articles(brand_name, max_articles=18)
        
        for art in raw_articles:
            full_content = f"{art['title']}. {art['text']}"
            sent_res = sentiment_analyzer.analyze(full_content)
            emotion = emotion_classifier.classify(full_content, sent_res["sentiment"])
            topics = ner_topic_extractor.extract_topics(art["text"])
            entities = ner_topic_extractor.extract_entities(art["text"])
            reliability = reputation_engine.calculate_reliability_score(art.get("source_type", "News"))

            db_article = Article(
                brand_id=brand.id,
                title=art["title"],
                text=art["text"],
                source=art["source"],
                source_type=art.get("source_type", "News"),
                url=art.get("url"),
                publication_date=art.get("publication_date", datetime.utcnow()),
                sentiment=sent_res["sentiment"],
                sentiment_score=sent_res["score"],
                emotion=emotion,
                topics_json=json.dumps(topics),
                entities_json=json.dumps(entities),
                reliability_score=reliability
            )
            db.add(db_article)
        db.commit()

        # Build initial Topics and Entities tables
        all_articles = db.query(Article).filter(Article.brand_id == brand.id).all()
        topic_counts = {}
        entity_counts = {}

        for a in all_articles:
            t_list = json.loads(a.topics_json) if a.topics_json else []
            for t in t_list:
                if t not in topic_counts:
                    topic_counts[t] = {"count": 0, "scores": []}
                topic_counts[t]["count"] += 1
                topic_counts[t]["scores"].append(a.sentiment_score)

            e_list = json.loads(a.entities_json) if a.entities_json else []
            for e in e_list:
                key = (e["name"], e["entity_type"])
                entity_counts[key] = entity_counts.get(key, 0) + 1

        for t_name, t_data in topic_counts.items():
            avg_score = sum(t_data["scores"]) / len(t_data["scores"]) if t_data["scores"] else 0.0
            db.add(Topic(
                brand_id=brand.id,
                name=t_name,
                mention_count=t_data["count"],
                avg_sentiment_score=avg_score,
                keywords_json=json.dumps([t_name])
            ))

        for (e_name, e_type), count in entity_counts.items():
            db.add(Entity(
                brand_id=brand.id,
                name=e_name,
                entity_type=e_type,
                count=count
            ))

        # Initial Reputation Score
        score_res = reputation_engine.calculate_reputation_score(all_articles)
        db.add(ReputationScore(
            brand_id=brand.id,
            score=score_res["score"],
            positive_pct=score_res["positive_pct"],
            neutral_pct=score_res["neutral_pct"],
            negative_pct=score_res["negative_pct"],
            health_status=score_res["health_status"]
        ))

        # Initial Anomaly check
        anomalies = reputation_engine.detect_anomalies(all_articles, [])
        for ano in anomalies:
            db.add(Alert(
                brand_id=brand.id,
                alert_type=ano["type"],
                severity=ano["severity"],
                title=ano["title"],
                message=ano["message"]
            ))

        db.commit()

    return brand


@router.get("/brands", response_model=List[BrandResponse])
def get_all_brands(db: Session = Depends(get_db)):
    """GET /api/brands"""
    return db.query(Brand).order_by(Brand.created_at.desc()).all()


@router.get("/brand/{brand_id}/dashboard", response_model=DashboardOverview)
def get_brand_dashboard(brand_id: int, db: Session = Depends(get_db)):
    """GET /api/brand/{id}/dashboard - Returns combined dashboard overview payload."""
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    articles = db.query(Article).filter(Article.brand_id == brand_id).order_by(Article.publication_date.desc()).all()
    latest_score = db.query(ReputationScore).filter(ReputationScore.brand_id == brand_id).order_by(ReputationScore.timestamp.desc()).first()

    # Automatically sync existing DB articles with upgraded ContextAwareSentimentAnalyzer
    updated_any = False
    for a in articles:
        full_content = f"{a.title}. {a.text}"
        res = sentiment_analyzer.analyze(full_content)
        new_sent = res["sentiment"]
        new_emo = emotion_classifier.classify(full_content, new_sent)
        if a.sentiment != new_sent or a.emotion != new_emo:
            a.sentiment = new_sent
            a.emotion = new_emo
            updated_any = True

    if updated_any:
        s_res = reputation_engine.calculate_reputation_score(articles)
        if latest_score:
            latest_score.score = s_res["score"]
            latest_score.positive_pct = s_res["positive_pct"]
            latest_score.neutral_pct = s_res["neutral_pct"]
            latest_score.negative_pct = s_res["negative_pct"]
            latest_score.health_status = s_res["health_status"]
        db.commit()

    if not latest_score:
        s_res = reputation_engine.calculate_reputation_score(articles)
        latest_score = ReputationScore(
            score=s_res["score"],
            positive_pct=s_res["positive_pct"],
            neutral_pct=s_res["neutral_pct"],
            negative_pct=s_res["negative_pct"],
            trend_direction="stable",
            health_status=s_res["health_status"],
            timestamp=datetime.utcnow()
        )

    # Sentiment distribution
    pos_c = sum(1 for a in articles if a.sentiment == "Positive")
    neu_c = sum(1 for a in articles if a.sentiment == "Neutral")
    neg_c = sum(1 for a in articles if a.sentiment == "Negative")
    tot_c = len(articles) or 1

    sent_dist = {
        "positive": pos_c,
        "neutral": neu_c,
        "negative": neg_c,
        "total": len(articles),
        "positive_pct": round((pos_c / tot_c) * 100, 1),
        "neutral_pct": round((neu_c / tot_c) * 100, 1),
        "negative_pct": round((neg_c / tot_c) * 100, 1)
    }

    # Emotion distribution
    emotions = {"joy": 0, "anger": 0, "sadness": 0, "fear": 0, "surprise": 0, "disgust": 0}
    for a in articles:
        em_lower = (a.emotion or "joy").lower()
        if em_lower in emotions:
            emotions[em_lower] += 1

    # Topics and Entities
    topics = db.query(Topic).filter(Topic.brand_id == brand_id).order_by(Topic.mention_count.desc()).all()
    entities = db.query(Entity).filter(Entity.brand_id == brand_id).order_by(Entity.count.desc()).all()
    alerts = db.query(Alert).filter(Alert.brand_id == brand_id).order_by(Alert.timestamp.desc()).all()

    # AI Summary
    summary_data = summary_generator.generate_summary(
        brand.name,
        articles,
        {
            "score": latest_score.score,
            "positive_pct": latest_score.positive_pct,
            "negative_pct": latest_score.negative_pct,
            "health_status": latest_score.health_status
        },
        topics,
        alerts
    )

    # Format articles for schema response
    formatted_articles = []
    for a in articles[:15]:
        formatted_articles.append(ArticleSchema(
            id=a.id,
            title=a.title,
            text=a.text,
            source=a.source,
            source_type=a.source_type,
            url=a.url,
            publication_date=a.publication_date,
            sentiment=a.sentiment,
            sentiment_score=a.sentiment_score,
            emotion=a.emotion,
            topics=json.loads(a.topics_json) if a.topics_json else [],
            entities=json.loads(a.entities_json) if a.entities_json else [],
            reliability_score=a.reliability_score
        ))

    return {
        "brand": brand,
        "current_score": latest_score,
        "sentiment_distribution": sent_dist,
        "emotion_distribution": emotions,
        "recent_mentions": formatted_articles,
        "top_topics": topics[:6],
        "top_entities": entities[:8],
        "active_alerts": alerts,
        "summary": summary_data
    }


@router.get("/brand/{brand_id}/sentiment")
def get_brand_sentiment(brand_id: int, db: Session = Depends(get_db)):
    """GET /api/brand/{id}/sentiment"""
    articles = db.query(Article).filter(Article.brand_id == brand_id).all()
    pos = sum(1 for a in articles if a.sentiment == "Positive")
    neu = sum(1 for a in articles if a.sentiment == "Neutral")
    neg = sum(1 for a in articles if a.sentiment == "Negative")
    tot = len(articles) or 1

    return {
        "distribution": {
            "Positive": pos,
            "Neutral": neu,
            "Negative": neg,
            "Total": len(articles)
        },
        "percentages": {
            "Positive": round((pos / tot) * 100, 1),
            "Neutral": round((neu / tot) * 100, 1),
            "Negative": round((neg / tot) * 100, 1)
        }
    }


@router.get("/brand/{brand_id}/trends")
def get_brand_trends(brand_id: int, db: Session = Depends(get_db)):
    """GET /api/brand/{id}/trends"""
    articles = db.query(Article).filter(Article.brand_id == brand_id).all()
    points = reputation_engine.generate_trend_history(articles)
    return {"trends": points}


@router.get("/brand/{brand_id}/topics")
def get_brand_topics(brand_id: int, db: Session = Depends(get_db)):
    """GET /api/brand/{id}/topics"""
    topics = db.query(Topic).filter(Topic.brand_id == brand_id).order_by(Topic.mention_count.desc()).all()
    entities = db.query(Entity).filter(Entity.brand_id == brand_id).order_by(Entity.count.desc()).all()
    return {"topics": topics, "entities": entities}


@router.get("/brand/{brand_id}/alerts")
def get_brand_alerts(brand_id: int, db: Session = Depends(get_db)):
    """GET /api/brand/{id}/alerts"""
    return db.query(Alert).filter(Alert.brand_id == brand_id).order_by(Alert.timestamp.desc()).all()


@router.put("/alert/{alert_id}/read")
def mark_alert_read(alert_id: int, db: Session = Depends(get_db)):
    """PUT /api/alert/{alert_id}/read"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if alert:
        alert.is_read = True
        db.commit()
    return {"status": "success"}


@router.post("/brand/{brand_id}/scrape-now")
def trigger_live_scrape(brand_id: int, db: Session = Depends(get_db)):
    """POST /api/brand/{id}/scrape-now - Triggers an immediate scrape pass."""
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    new_arts = web_scraper_manager.collect_brand_articles(brand.name, max_articles=5)
    added_count = 0

    for art in new_arts:
        full_content = f"{art['title']}. {art['text']}"
        sent_res = sentiment_analyzer.analyze(full_content)
        emotion = emotion_classifier.classify(full_content, sent_res["sentiment"])
        topics = ner_topic_extractor.extract_topics(art["text"])
        entities = ner_topic_extractor.extract_entities(art["text"])
        reliability = reputation_engine.calculate_reliability_score(art.get("source_type", "News"))

        db_article = Article(
            brand_id=brand.id,
            title=art["title"],
            text=art["text"],
            source=art["source"],
            source_type=art.get("source_type", "News"),
            url=art.get("url"),
            publication_date=art.get("publication_date", datetime.utcnow()),
            sentiment=sent_res["sentiment"],
            sentiment_score=sent_res["score"],
            emotion=emotion,
            topics_json=json.dumps(topics),
            entities_json=json.dumps(entities),
            reliability_score=reliability
        )
        db.add(db_article)
        added_count += 1

    db.commit()

    # Recalculate score
    all_arts = db.query(Article).filter(Article.brand_id == brand.id).all()
    s_res = reputation_engine.calculate_reputation_score(all_arts)
    db.add(ReputationScore(
        brand_id=brand.id,
        score=s_res["score"],
        positive_pct=s_res["positive_pct"],
        neutral_pct=s_res["neutral_pct"],
        negative_pct=s_res["negative_pct"],
        health_status=s_res["health_status"]
    ))
    db.commit()

    return {"message": f"Successfully scraped and indexed {added_count} new articles for {brand.name}."}
