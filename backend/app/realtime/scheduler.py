import asyncio
import json
import random
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Brand, Article, Alert, ReputationScore, Topic, Entity
from ..nlp.sentiment_model import sentiment_analyzer
from ..nlp.emotion_model import emotion_classifier
from ..nlp.ner_topic_model import ner_topic_extractor
from ..scraper.web_scraper import MENTION_TEMPLATES, SOURCE_TEMPLATES
from ..analytics.reputation_engine import reputation_engine
from .websocket_manager import ws_manager

logger = logging.getLogger(__name__)

class BackgroundMonitorScheduler:
    def __init__(self, interval_seconds: int = 25):
        self.interval_seconds = interval_seconds
        self.is_running = False
        self._task = None

    def start(self):
        if not self.is_running:
            self.is_running = True
            self._task = asyncio.create_task(self._monitoring_loop())
            logger.info("Background Brand Monitoring Scheduler started.")

    def stop(self):
        if self.is_running:
            self.is_running = False
            if self._task:
                self._task.cancel()
            logger.info("Background Brand Monitoring Scheduler stopped.")

    async def _monitoring_loop(self):
        while self.is_running:
            try:
                await asyncio.sleep(self.interval_seconds)
                await self._run_monitoring_cycle()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in background monitoring cycle: {e}")

    async def _run_monitoring_cycle(self):
        db = SessionLocal()
        try:
            brands = db.query(Brand).all()
            for brand in brands:
                # Simulate receiving 1 new mention periodically for actively monitored brands
                tmpl = random.choice(MENTION_TEMPLATES)
                stype = tmpl["source_type"]
                sources = SOURCE_TEMPLATES.get(stype, SOURCE_TEMPLATES["News"])
                source_info = random.choice(sources)
                
                title = tmpl["title"].format(brand=brand.name)
                text = tmpl["text"].format(brand=brand.name)
                
                # Analyze NLP
                sent_res = sentiment_analyzer.analyze(text)
                emotion = emotion_classifier.classify(text, sent_res["sentiment"])
                topics = ner_topic_extractor.extract_topics(text)
                entities = ner_topic_extractor.extract_entities(text)
                reliability = reputation_engine.calculate_reliability_score(stype)

                # Save new Article
                new_art = Article(
                    brand_id=brand.id,
                    title=title,
                    text=text,
                    source=source_info[0],
                    source_type=stype,
                    url=f"{source_info[1]}/article/{random.randint(1000, 9999)}",
                    publication_date=datetime.utcnow(),
                    sentiment=sent_res["sentiment"],
                    sentiment_score=sent_res["score"],
                    emotion=emotion,
                    topics_json=json.dumps(topics),
                    entities_json=json.dumps(entities),
                    reliability_score=reliability
                )
                db.add(new_art)
                db.commit()
                db.refresh(new_art)

                # Re-calculate brand score
                all_arts = db.query(Article).filter(Article.brand_id == brand.id).all()
                score_res = reputation_engine.calculate_reputation_score(all_arts)
                
                new_score = ReputationScore(
                    brand_id=brand.id,
                    score=score_res["score"],
                    positive_pct=score_res["positive_pct"],
                    neutral_pct=score_res["neutral_pct"],
                    negative_pct=score_res["negative_pct"],
                    health_status=score_res["health_status"]
                )
                db.add(new_score)
                db.commit()

                # Check anomalies and trigger alert if necessary
                anomalies = reputation_engine.detect_anomalies([new_art], db.query(ReputationScore).filter(ReputationScore.brand_id == brand.id).all())
                triggered_alert = None
                if anomalies:
                    ano = anomalies[0]
                    triggered_alert = Alert(
                        brand_id=brand.id,
                        alert_type=ano["type"],
                        severity=ano["severity"],
                        title=ano["title"],
                        message=ano["message"]
                    )
                    db.add(triggered_alert)
                    db.commit()
                    db.refresh(triggered_alert)

                # Broadcast via WebSocket
                mention_data = {
                    "id": new_art.id,
                    "title": new_art.title,
                    "text": new_art.text,
                    "source": new_art.source,
                    "source_type": new_art.source_type,
                    "url": new_art.url,
                    "publication_date": new_art.publication_date.isoformat(),
                    "sentiment": new_art.sentiment,
                    "sentiment_score": new_art.sentiment_score,
                    "emotion": new_art.emotion,
                    "topics": topics,
                    "entities": entities,
                    "reliability_score": reliability
                }

                await ws_manager.broadcast_to_brand(brand.id, "new_mention", mention_data)
                await ws_manager.broadcast_to_brand(brand.id, "score_updated", score_res)
                
                if triggered_alert:
                    alert_payload = {
                        "id": triggered_alert.id,
                        "brand_id": brand.id,
                        "alert_type": triggered_alert.alert_type,
                        "severity": triggered_alert.severity,
                        "title": triggered_alert.title,
                        "message": triggered_alert.message,
                        "is_read": triggered_alert.is_read,
                        "timestamp": triggered_alert.timestamp.isoformat()
                    }
                    await ws_manager.broadcast_to_brand(brand.id, "alert_triggered", alert_payload)

        finally:
            db.close()

background_scheduler = BackgroundMonitorScheduler()
